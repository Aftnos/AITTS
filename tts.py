# tts.py
import json
import base64
import requests

class TTSClient:
    def __init__(self, base_url, default_params):
        self.base_url = base_url
        self.default_params = default_params

    def get_audio(self, text, extra_params=None):
        """
        调用 TTS 服务接口，返回音频数据的字节串，若失败返回 None。
        """
        params = self.default_params.copy()
        if extra_params:
            params.update(extra_params)
        params['text'] = text
        try:
            print("即将发送的 TTS 请求参数:")
            print(f"URL: {self.base_url}")
            print(f"参数: {params}")
            response = requests.get(self.base_url, params=params, stream=True)
            response.raise_for_status()
            audio_data = b''.join(response.iter_content(chunk_size=4096))
            return audio_data
        except requests.exceptions.RequestException as e:
            print(f"TTS 服务请求失败：{e}")
            return None

    def get_audio_base64(self, text, extra_params=None):
        """
        返回经过 Base64 编码后的音频数据字符串。
        """
        audio_data = self.get_audio(text, extra_params)
        if audio_data:
            return base64.b64encode(audio_data).decode('ascii')
        return ""
