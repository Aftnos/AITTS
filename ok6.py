import os
import json
import re
import base64
import ssl
import requests
from flask import Flask, request, Response, stream_with_context, jsonify
from flask_cors import CORS
from faster_whisper import WhisperModel
import tempfile
import torch
import opencc
import wave

# 配置文件的路径
CONFIG_FILE = 'config.json'

# 默认配置参数（包含中文注释）
default_config = {
    "MODEL_API_URL": "http://localhost:11434/api/generate",  # 模型 API 的 URL
    "__comment_MODEL_API_URL": "模型 API 的 URL",

    "MODEL_LIST_URL": "http://localhost:11434/api/tags",  # LLM 模型列表的 URL
    "__comment_MODEL_LIST_URL": "LLM 模型列表的 URL",

    "TTS_URL": "http://127.0.0.1:5000/tts",  # TTS 服务的基础 URL
    "__comment_TTS_URL": "TTS 服务的基础 URL，不包含参数",

    "TTS_LIST_URL": "http://127.0.0.1:5000/character_list",  # TTS 模型列表的 URL
    "__comment_TTS_LIST_URL": "TTS 模型列表的 URL",

    "TTS_PARAMS": {
        "stream": "true",
        "character": "花火",
        "emotion": "平常",
        "speed": "1.0",
        "batch_size": "100"
    },
    "__comment_TTS_PARAMS": "TTS 服务的默认参数，可在此处设置默认角色、情感、语速等",

    "DEFAULT_LLM_MODEL": "qwen2.5:7b",  # 默认的 LLM 模型名称
    "__comment_DEFAULT_LLM_MODEL": "默认的 LLM 模型名称",

    "ASR_MODEL_PATH": r"E:\ai\FunAsr_Faster_Whisper_Multi_Subs\faster-whisper-large-v3-turbo-ct2",
    # faster_whisper ASR 模型的本地路径
    "__comment_ASR_MODEL_PATH": "faster_whisper ASR 模型的本地路径，如 E:\\ai\\FunAsr_Faster_Whisper_Multi_Subs\\faster-whisper-large-v3-turbo-ct2",

    "ASR_MODEL_SIZE": "large-v3-turbo-ct2",  # ASR 模型大小，用于日志输出
    "__comment_ASR_MODEL_SIZE": "ASR 模型的大小，如 tiny, base, small, medium, large",

    "API_PORT": 20005,  # Flask 服务器的端口
    "__comment_API_PORT": "Flask 服务器的端口号",

    "OTHER_CONFIG": "value",  # 其他配置参数
    "__comment_OTHER_CONFIG": "其他配置参数的说明"
}


def create_default_config():
    """
    创建默认的config.json文件，并写入默认配置参数。
    """
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
    print("已生成默认的 config.json 文件，请根据需要修改配置。")


def load_config():
    """
    加载config.json配置文件，忽略以'__comment'开头的键。
    如果配置文件不存在，则创建默认配置文件。
    """
    if not os.path.isfile(CONFIG_FILE):
        create_default_config()

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    # 过滤掉以 '__comment' 开头的键
    filtered_config = {k: v for k, v in config.items() if not k.startswith("__comment")}

    return filtered_config


# 读取配置文件
config = load_config()

# 提取配置参数
MODEL_API_URL = config.get("MODEL_API_URL", "http://localhost:11434/api/generate")
MODEL_LIST_URL = config.get("MODEL_LIST_URL", "http://localhost:11434/api/tags")
TTS_URL_BASE = config.get("TTS_URL", "http://127.0.0.1:5000/tts")
TTS_LIST_URL = config.get("TTS_LIST_URL", "http://127.0.0.1:5000/character_list")
TTS_DEFAULT_PARAMS = config.get("TTS_PARAMS", {})
DEFAULT_LLM_MODEL = config.get("DEFAULT_LLM_MODEL", "qwen2.5:7b")
ASR_MODEL_PATH = config.get("ASR_MODEL_PATH", "faster-whisper-base")
ASR_MODEL_SIZE = config.get("ASR_MODEL_SIZE", "base")
API_PORT = config.get("API_PORT", 20005)

# 打印配置信息
print("成功加载配置参数：")
print(f"模型 API URL: {MODEL_API_URL}")
print(f"模型列表 URL: {MODEL_LIST_URL}")
print(f"TTS 服务 URL: {TTS_URL_BASE}")
print(f"TTS 模型列表 URL: {TTS_LIST_URL}")
print(f"TTS 默认参数: {TTS_DEFAULT_PARAMS}")
print(f"默认 LLM 模型: {DEFAULT_LLM_MODEL}")
print(f"ASR 模型路径: {ASR_MODEL_PATH}")
print(f"ASR 模型大小: {ASR_MODEL_SIZE}")
print(f"Flask 服务器端口: {API_PORT}")

app = Flask(__name__)
CORS(app)  # 初始化 CORS，允许所有域名访问

# 初始化 ASR 模型
print("正在加载 ASR 模型，请稍候...")
asr_device = "cuda" if torch.cuda.is_available() else "cpu"
try:
    asr_model = WhisperModel(
        model_size_or_path=ASR_MODEL_PATH,
        device=asr_device,
        compute_type="float16",
        local_files_only=True  # 如果模型已经下载到本地
    )
    print("ASR 模型加载完成。")
except Exception as e:
    print(f"ASR 模型加载失败：{e}")
    asr_model = None

# 初始化 OpenCC，用于简繁体转换
t2s = opencc.OpenCC('t2s.json')  # 转换为简体

# 定义会话上下文存储，每个用户一个上下文
conversation_contexts = {}  # 使用字典来存储不同用户的会话上下文


def process_chat_request(user_input, yhid, llm_model=None, enable_memory=True, tts_params={}):
    """
    处理聊天请求的核心逻辑。

    :param user_input: 用户输入的文本
    :param yhid: 用户ID
    :param llm_model: 使用的LLM模型
    :param enable_memory: 是否启用会话记忆
    :param tts_params: TTS参数字典
    :return: Flask的Response对象
    """
    # 如果客户端未指定 LLM 模型，使用配置文件中的默认模型
    if not llm_model:
        llm_model = DEFAULT_LLM_MODEL

    # 构建请求数据
    data = {
        "model": llm_model,
        "prompt": user_input,
        "stream": True
    }

    # 获取当前用户的会话上下文
    conversation_context = conversation_contexts.get(yhid)

    # 如果启用了会话记忆，且有上下文，添加到请求中
    if enable_memory and conversation_context is not None:
        data['context'] = conversation_context

    # 输出请求体以便诊断
    print(f"用户 {yhid} 即将发送的 POST 请求内容:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    # 准备发送请求到模型 API
    try:
        response = requests.post(MODEL_API_URL, json=data, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Model API request failed: {e}"}), 500

    def generate():
        nonlocal conversation_context  # 引用局部变量
        generated_text = ""
        sentence_buffer = ""

        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    response_json = json.loads(line)
                    message_content = response_json.get('response', '')
                    generated_text += message_content
                    sentence_buffer += message_content

                    # 使用正则表达式检测句子结束符
                    sentences = re.split(r'([。！？])', sentence_buffer)
                    for i in range(0, len(sentences) - 1, 2):
                        sentence = sentences[i] + sentences[i + 1]
                        # 获取 TTS 音频数据
                        audio_data = get_tts_audio(sentence, tts_params)
                        if audio_data is None:
                            audio_data_str = ''
                        else:
                            audio_data_str = base64.b64encode(audio_data).decode('ascii')  # 使用 Base64 编码

                        # 将文本和音频一起返回
                        yield json.dumps({
                            "text": sentence,
                            "audio": audio_data_str
                        }, ensure_ascii=False) + '\n'

                    sentence_buffer = sentences[-1]

                    # 如果响应已完成，获取新的上下文
                    if response_json.get('done', False):
                        # 如果启用了会话记忆，更新上下文
                        if enable_memory:
                            conversation_context = response_json.get('context', None)
                            # 更新全局的会话上下文
                            conversation_contexts[yhid] = conversation_context
                        else:
                            conversation_context = None  # 禁用记忆时，清空上下文
                            conversation_contexts[yhid] = None

                        # 处理剩余的句子
                        if sentence_buffer:
                            audio_data = get_tts_audio(sentence_buffer, tts_params)
                            if audio_data is None:
                                audio_data_str = ''
                            else:
                                audio_data_str = base64.b64encode(audio_data).decode('ascii')  # 使用 Base64 编码
                            yield json.dumps({
                                "text": sentence_buffer,
                                "audio": audio_data_str
                            }, ensure_ascii=False) + '\n'
                        break
                except json.JSONDecodeError:
                    print(f"无法解析的响应行: {line}")

    return Response(stream_with_context(generate()), mimetype='application/json; charset=utf-8')


def get_tts_audio(text, tts_params):
    """
    调用 TTS 服务获取音频数据。

    :param text: 需要转换为语音的文本
    :param tts_params: TTS参数字典
    :return: 音频数据的字节串，或者 None（如果请求失败）
    """
    try:
        # 合并默认参数和文本参数
        params = TTS_DEFAULT_PARAMS.copy()
        params.update(tts_params)  # 更新参数
        params['text'] = text  # 添加文本参数

        # 调试输出请求的参数
        print("即将发送的 TTS 请求参数:")
        print(f"URL: {TTS_URL_BASE}")
        print(f"参数: {params}")

        # 构建完整的 TTS 请求 URL
        response = requests.get(TTS_URL_BASE, params=params, stream=True)
        response.raise_for_status()
        audio_data = b''.join(response.iter_content(chunk_size=4096))
        return audio_data
    except requests.exceptions.RequestException as e:
        print(f"TTS 服务请求失败：{e}")
        return None


# 新增获取 TTS 模型列表的接口
@app.route('/api/tts_models', methods=['GET'])
def get_tts_models():
    try:
        response = requests.get(TTS_LIST_URL)
        response.raise_for_status()
        tts_models = response.json()
        return jsonify(tts_models)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch TTS models: {e}"}), 500


# 新增获取 LLM 模型列表的接口
@app.route('/api/llm_models', methods=['GET'])
def get_llm_models():
    try:
        response = requests.get(MODEL_LIST_URL)
        response.raise_for_status()
        llm_models = response.json()
        return jsonify(llm_models)
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch LLM models: {e}"}), 500


# 修改 /api/chat 路由，调用 process_chat_request
@app.route('/api/chat', methods=['POST'])
def chat():
    # 获取请求中的参数
    user_input = request.json.get('question')
    llm_model = request.json.get('llm_model')
    enable_memory = request.json.get('enable_memory', True)
    tts_params = request.json.get('tts_params', {})
    yhid = request.json.get('yhid')  # 获取用户ID

    if not user_input:
        return jsonify({"error": "No question provided."}), 400

    if not yhid:
        return jsonify({"error": "No yhid provided."}), 400

    # 验证 yhid 是否为 8 位 16 进制字符串
    if not isinstance(yhid, str) or not re.fullmatch(r'[0-9a-fA-F]{8}', yhid):
        return jsonify({"error": "Invalid yhid format. It should be an 8-character hexadecimal string."}), 400

    return process_chat_request(user_input, yhid, llm_model, enable_memory, tts_params)


# 修改 /api/asr 路由，调用 process_chat_request
@app.route('/api/asr', methods=['POST'])
def asr():
    """
    语音识别接口，接受音频文件，识别文本后调用 process_chat_request，并返回响应结果。
    """
    # 获取音频文件
    if 'audio' not in request.files:
        return jsonify({"error": "No audio file provided."}), 400

    audio_file = request.files['audio']

    # 可选参数
    language = request.form.get('language')  # 指定语言（可选）
    beam_size = int(request.form.get('beam_size', 5))  # beam size（可选）
    task = request.form.get('task', 'transcribe')  # 任务类型（transcribe 或 translate）
    yhid = request.form.get('yhid')  # 用户ID
    llm_model = request.form.get('llm_model')
    enable_memory = request.form.get('enable_memory', 'true').lower() == 'true'
    tts_params_str = request.form.get('tts_params', '{}')
    try:
        tts_params = json.loads(tts_params_str)
    except json.JSONDecodeError:
        tts_params = {}

    if not yhid:
        return jsonify({"error": "No yhid provided."}), 400

    # 验证 yhid 是否为 8 位 16 进制字符串
    if not isinstance(yhid, str) or not re.fullmatch(r'[0-9a-fA-F]{8}', yhid):
        return jsonify({"error": "Invalid yhid format. It should be an 8-character hexadecimal string."}), 400

    if asr_model is None:
        return jsonify({"error": "ASR model is not initialized."}), 500

    # 将音频文件保存到临时文件
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
        audio_file.save(tmp.name)
        audio_path = tmp.name

    # 进行语音转录
    try:
        segments, info = asr_model.transcribe(
            audio_path,
            language=language,
            beam_size=beam_size,
            task=task
        )

        # 构建转录结果
        transcription = " ".join(seg.text for seg in segments)

        # 如果需要进行简体转换
        if info.language == 'zh':
            transcription = t2s.convert(transcription)

        # 调用 process_chat_request 函数
        return process_chat_request(transcription, yhid, llm_model, enable_memory, tts_params)

    except Exception as e:
        return jsonify({"error": f"ASR failed: {e}"}), 500
    finally:
        # 删除临时文件
        os.remove(audio_path)


if __name__ == '__main__':
    # 启动 Flask 服务器，使用配置的端口号
    app.run(host='0.0.0.0', port=API_PORT, threaded=True, ssl_context=('cert.pem', 'key.pem'))
