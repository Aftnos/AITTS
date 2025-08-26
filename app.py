# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import re
import json

from config import load_config
from asr import ASRProcessor
from tts import TTSClient
from chat import process_chat_request

# 加载配置
config = load_config()
MODEL_API_URL = config.get("MODEL_API_URL")
MODEL_LIST_URL = config.get("MODEL_LIST_URL")
TTS_URL_BASE = config.get("TTS_URL")
TTS_LIST_URL = config.get("TTS_LIST_URL")
TTS_DEFAULT_PARAMS = config.get("TTS_PARAMS")
DEFAULT_LLM_MODEL = config.get("DEFAULT_LLM_MODEL")
ASR_MODEL_PATH = config.get("ASR_MODEL_PATH")
ASR_MODEL_SIZE = config.get("ASR_MODEL_SIZE")
API_PORT = config.get("API_PORT")

# 初始化 Flask
app = Flask(__name__)
CORS(app)

# 初始化 ASR 模型
print("正在加载 ASR 模型，请稍候...")
asr_processor = ASRProcessor(ASR_MODEL_PATH, ASR_MODEL_SIZE)

# 初始化 TTS 客户端
tts_client = TTSClient(TTS_URL_BASE, TTS_DEFAULT_PARAMS)

@app.route('/api/chat', methods=['POST'])
def chat():
    req_data = request.json
    user_input = req_data.get('question')
    llm_model = req_data.get('llm_model')
    enable_memory = req_data.get('enable_memory', True)
    extra_tts_params = req_data.get('tts_params', {})
    convert_to_16k = req_data.get('convert_to_16k', False)
    yhid = req_data.get('yhid')

    if not user_input:
        return jsonify({"error": "未提供问题文本"}), 400
    if not yhid:
        return jsonify({"error": "未提供 yhid"}), 400
    if not isinstance(yhid, str) or not re.fullmatch(r'[0-9a-fA-F]{8}', yhid):
        return jsonify({"error": "yhid 格式错误，应为8位16进制字符串"}), 400

    return process_chat_request(user_input, yhid, MODEL_API_URL, DEFAULT_LLM_MODEL,
                                enable_memory, tts_client, extra_tts_params, convert_to_16k)

@app.route('/api/asr', methods=['POST'])
def asr():
    if 'audio' not in request.files:
        return jsonify({"error": "未提供音频文件"}), 400
    audio_file = request.files['audio']
    language = request.form.get('language')
    beam_size = int(request.form.get('beam_size', 5))
    task = request.form.get('task', 'transcribe')
    yhid = request.form.get('yhid')
    llm_model = request.form.get('llm_model')
    enable_memory = request.form.get('enable_memory', 'true').lower() == 'true'
    tts_params_str = request.form.get('tts_params', '{}')
    convert_to_16k = request.form.get('convert_to_16k', 'false').lower() == 'true'
    try:
        extra_tts_params = json.loads(tts_params_str)
    except json.JSONDecodeError:
        extra_tts_params = {}

    if not yhid:
        return jsonify({"error": "未提供 yhid"}), 400
    if not isinstance(yhid, str) or not re.fullmatch(r'[0-9a-fA-F]{8}', yhid):
        return jsonify({"error": "yhid 格式错误，应为8位16进制字符串"}), 400

    if asr_processor.model is None:
        return jsonify({"error": "ASR 模型未初始化"}), 500

    try:
        transcription, info = asr_processor.transcribe(audio_file, language, beam_size, task)
        return process_chat_request(transcription, yhid, MODEL_API_URL, DEFAULT_LLM_MODEL,
                                    enable_memory, tts_client, extra_tts_params, convert_to_16k)
    except Exception as e:
        return jsonify({"error": f"ASR 转写失败：{e}"}), 500

@app.route('/api/tts_models', methods=['GET'])
def get_tts_models():
    try:
        import requests
        response = requests.get(TTS_LIST_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": f"获取 TTS 模型列表失败：{e}"}), 500

@app.route('/api/llm_models', methods=['GET'])
def get_llm_models():
    try:
        import requests
        response = requests.get(MODEL_LIST_URL)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": f"获取 LLM 模型列表失败：{e}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=API_PORT, threaded=True, ssl_context=('cert.pem', 'key.pem'))
