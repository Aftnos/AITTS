# tts.py
import json
import base64
import requests
import io
import logging
import soundfile as sf
import resampy

class TTSClient:
    def __init__(self, base_url, default_params):
        self.base_url = base_url
        self.default_params = default_params

    def _ensure_16k(self, audio_bytes: bytes) -> bytes:
        """Resample audio to 16 kHz if necessary."""
        logger = logging.getLogger(__name__)
        try:
            with io.BytesIO(audio_bytes) as input_buffer:
                data, sr = sf.read(input_buffer)
            if sr != 16000 and getattr(data, "size", 0) > 0:
                data_16k = resampy.resample(data, sr, 16000)
                output_buffer = io.BytesIO()
                sf.write(output_buffer, data_16k, 16000, format="WAV")
                audio_bytes = output_buffer.getvalue()
        except Exception as e:
            logger.error("音频重采样失败：%s", e)
        return audio_bytes

    def _verify_16k(self, audio_bytes: bytes) -> bool:
        """Verify that audio data has a 16 kHz sample rate."""
        logger = logging.getLogger(__name__)
        try:
            with io.BytesIO(audio_bytes) as buf:
                _, sr = sf.read(buf)
            return sr == 16000
        except Exception as e:
            logger.error("采样率检查失败：%s", e)
            return False

    def get_audio(self, text, extra_params=None, convert_to_16k=False):
        """
        调用 TTS 服务接口，返回音频数据的字节串，若失败返回 None。
        """
        params = self.default_params.copy()
        if extra_params:
            params.update(extra_params)
        params['text'] = text
        logger = logging.getLogger(__name__)
        try:
            logger.info("TTS 请求: url=%s, params=%s", self.base_url, params)
            response = requests.get(self.base_url, params=params, stream=True)
            response.raise_for_status()
            audio_data = b"".join(response.iter_content(chunk_size=4096))

            if convert_to_16k:
                audio_data = self._ensure_16k(audio_data)
                if not self._verify_16k(audio_data):
                    logger.warning("重采样后采样率仍非16kHz")
            else:
                if not self._verify_16k(audio_data):
                    logger.debug("返回音频采样率非16kHz")
            return audio_data
        except requests.exceptions.RequestException as e:
            logger.error("TTS 服务请求失败：%s", e)
            return None

    def get_audio_base64(self, text, extra_params=None, convert_to_16k=False):
        """
        返回经过 Base64 编码后的音频数据字符串。
        """
        audio_data = self.get_audio(text, extra_params, convert_to_16k)
        if audio_data:
            b64 = base64.b64encode(audio_data).decode("ascii")
            if convert_to_16k:
                try:
                    decoded = base64.b64decode(b64)
                    if not self._verify_16k(decoded):
                        logging.getLogger(__name__).warning(
                            "Base64 解码后采样率非16kHz"
                        )
                except Exception as e:
                    logging.getLogger(__name__).error(
                        "Base64 检查失败：%s", e
                    )
            return b64
        return ""
