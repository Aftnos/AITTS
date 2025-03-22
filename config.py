# config.py
import os
import json

CONFIG_FILE = 'config.json'

default_config = {
    "MODEL_API_URL": "http://localhost:11434/api/generate",
    "__comment_MODEL_API_URL": "模型 API 的 URL",
    "MODEL_LIST_URL": "http://localhost:11434/api/tags",
    "__comment_MODEL_LIST_URL": "LLM 模型列表的 URL",
    "TTS_URL": "http://127.0.0.1:5000/tts",
    "__comment_TTS_URL": "TTS 服务的基础 URL，不包含参数",
    "TTS_LIST_URL": "http://127.0.0.1:5000/character_list",
    "__comment_TTS_LIST_URL": "TTS 模型列表的 URL",
    "TTS_PARAMS": {
        "stream": "true",
        "character": "花火",
        "emotion": "平常",
        "speed": "1.0",
        "batch_size": "100"
    },
    "__comment_TTS_PARAMS": "TTS 服务的默认参数，可在此处设置默认角色、情感、语速等",
    "DEFAULT_LLM_MODEL": "qwen2.5:7b",
    "__comment_DEFAULT_LLM_MODEL": "默认的 LLM 模型名称",
    "ASR_MODEL_PATH": r"E:\ai\FunAsr_Faster_Whisper_Multi_Subs\faster-whisper-large-v3-turbo-ct2",
    "__comment_ASR_MODEL_PATH": "faster_whisper ASR 模型的本地路径",
    "ASR_MODEL_SIZE": "large-v3-turbo-ct2",
    "__comment_ASR_MODEL_SIZE": "ASR 模型的大小，如 tiny, base, small, medium, large",
    "API_PORT": 20005,
    "__comment_API_PORT": "Flask 服务器的端口号",
    "OTHER_CONFIG": "value",
    "__comment_OTHER_CONFIG": "其他配置参数的说明"
}

def create_default_config():
    """生成默认配置文件。"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
    print("已生成默认的 config.json 文件，请根据需要修改配置。")

def load_config():
    """加载配置文件，忽略以 '__comment' 开头的键。"""
    if not os.path.isfile(CONFIG_FILE):
        create_default_config()
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)
    filtered_config = {k: v for k, v in config.items() if not k.startswith("__comment")}
    return filtered_config

if __name__ == '__main__':
    # 仅用于测试配置加载
    config = load_config()
    print("配置加载成功：", config)
