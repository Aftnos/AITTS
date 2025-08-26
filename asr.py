# asr.py
import os
import tempfile
import json
import re
import logging
import opencc
import torch
import wave
from faster_whisper import WhisperModel

# 初始化 OpenCC，用于繁简体转换
t2s = opencc.OpenCC('t2s.json')

class ASRProcessor:
    def __init__(self, model_path, model_size):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.logger = logging.getLogger(__name__)
        try:
            self.model = WhisperModel(
                model_size_or_path=model_path,
                device=self.device,
                compute_type="float16",
                local_files_only=True
            )
            self.logger.info("ASR 模型加载完成。")
        except Exception as e:
            self.logger.error("ASR 模型加载失败：%s", e)
            self.model = None

    def transcribe(self, audio_file, language=None, beam_size=5, task='transcribe'):
        """
        接受音频文件（file-like对象），保存为临时文件后进行转写。
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            audio_path = tmp.name

        try:
            segments, info = self.model.transcribe(
                audio_path,
                language=language,
                beam_size=beam_size,
                task=task
            )
            transcription = " ".join(seg.text for seg in segments)
            # 如果语言为中文，则进行简体转换
            if info.language == 'zh':
                transcription = t2s.convert(transcription)
            return transcription, info
        except Exception as e:
            raise RuntimeError(f"ASR 转写失败：{e}")
        finally:
            os.remove(audio_path)
