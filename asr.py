# asr.py
import os
import tempfile
import json
import re
import opencc
import torch
import wave
from faster_whisper import WhisperModel
from logger import log

# 初始化 OpenCC，用于繁简体转换
t2s = opencc.OpenCC('t2s.json')

class ASRProcessor:
    def __init__(self, model_path, model_size):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        log("ASR", "INFO", f"使用设备: {self.device}")
        try:
            self.model = WhisperModel(
                model_size_or_path=model_path,
                device=self.device,
                compute_type="float16",
                local_files_only=True
            )
            log("ASR", "INFO", "模型加载完成。")
        except Exception as e:
            log("ASR", "ERROR", f"模型加载失败：{e}")
            self.model = None

    def transcribe(self, audio_file, language=None, beam_size=5, task='transcribe'):
        """
        接受音频文件（file-like对象），保存为临时文件后进行转写。
        """
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            audio_file.save(tmp.name)
            audio_path = tmp.name
        log("ASR", "DEBUG", f"临时音频文件: {audio_path}")

        # 检查并输出输入音频的参数
        try:
            with wave.open(audio_path, 'rb') as wf:
                sample_rate = wf.getframerate()
                channels = wf.getnchannels()
                sample_width = wf.getsampwidth() * 8
                comptype = wf.getcomptype()
                compname = wf.getcompname()
                log(
                    "ASR",
                    "INFO",
                    f"输入音频信息: channels={channels}, sample_rate={sample_rate}, "
                    f"sample_width={sample_width}bit, comptype={comptype} ({compname})",
                )
        except wave.Error as e:
            log("ASR", "ERROR", f"无法读取音频参数: {e}")

        try:
            log("ASR", "DEBUG", f"开始转写，language={language}, beam_size={beam_size}, task={task}")
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
            log("ASR", "INFO", f"转写结果: {transcription}")
            return transcription, info
        except Exception as e:
            raise RuntimeError(f"ASR 转写失败：{e}")
        finally:
            os.remove(audio_path)
            log("ASR", "DEBUG", f"已删除临时文件: {audio_path}")
