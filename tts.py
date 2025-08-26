# tts.py
import json
import base64
import requests
import io
import wave
import audioop

class TTSClient:
    def __init__(self, base_url, default_params):
        self.base_url = base_url
        self.default_params = default_params

    def get_audio(self, text, extra_params=None, convert_to_16k=False):
        """
        调用 TTS 服务接口，返回音频数据的字节串，若失败返回 None。
        当 convert_to_16k 为 True 时，将返回的音频从 32k 采样率转换为 16k。
        """
        params = self.default_params.copy()
        if extra_params:
            params.update(extra_params)
        params['text'] = text

        # 如果在 extra_params 中包含转换参数，则取出并使用
        convert_flag = params.pop('convert_to_16k', convert_to_16k)
        try:
            print("即将发送的 TTS 请求参数:")
            print(f"URL: {self.base_url}")
            print(f"参数: {params}")
            response = requests.get(self.base_url, params=params, stream=True)
            response.raise_for_status()
            audio_data = b''.join(response.iter_content(chunk_size=4096))

            if convert_flag:
                audio_data = self._convert_to_16k(audio_data)

            return audio_data
        except requests.exceptions.RequestException as e:
            print(f"TTS 服务请求失败：{e}")
            return None

    def get_audio_base64(self, text, extra_params=None, convert_to_16k=False):
        """
        返回经过 Base64 编码后的音频数据字符串。
        """
        audio_data = self.get_audio(text, extra_params, convert_to_16k)
        if audio_data:
            return base64.b64encode(audio_data).decode('ascii')
        return ""

    def _convert_to_16k(self, audio_bytes):
        """
        将 WAV 音频字节流从 32k 采样率转换为 16k。
        若输入音频采样率已为 16k，则直接返回。

        如果输入数据不是 WAV 或转换失败，则返回原始音频数据，避免输出损坏的音频。
        """
        # 确认是 WAV 文件
        if not (audio_bytes.startswith(b"RIFF") and audio_bytes[8:12] == b"WAVE"):
            return audio_bytes

        try:
            with wave.open(io.BytesIO(audio_bytes), 'rb') as wf:
                nchannels = wf.getnchannels()
                sampwidth = wf.getsampwidth()
                framerate = wf.getframerate()
                frames = wf.readframes(wf.getnframes())

            if framerate == 16000:
                return audio_bytes

            converted_frames, _ = audioop.ratecv(frames, sampwidth, nchannels, framerate, 16000, None)
            out_buf = io.BytesIO()
            with wave.open(out_buf, 'wb') as wf_out:
                wf_out.setnchannels(nchannels)
                wf_out.setsampwidth(sampwidth)
                wf_out.setframerate(16000)
                wf_out.writeframes(converted_frames)

            return out_buf.getvalue()
        except (wave.Error, audioop.error) as e:
            print(f"音频转换失败: {e}")
            return audio_bytes
