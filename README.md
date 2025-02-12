# AITTS

![AITTS](https://socialify.git.ci/Aftnos/AITTS/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F128480098&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark) <!-- 请确保在仓库的 `assets` 文件夹中放置 `logo.png` 或替换为实际图标路径 -->

## 📦项目简介

AITTS是一个专为本地化大模型语音端到语音端交互实现探索。使用Python对ollama和GSVI TTS和whisper进行封装聚合成API，实现了可全本地部署的语音智能交互。

## 功能概述

- **LLM交互**：支持单独LLM文字流式/非流式交互，支持Ollama List模型列表。
- **语音识别**：支持直接ASR识别语音。
- **TTS语音**：支持从LLM转TTS，支持自定义TTS List模型列表。

## 截图

懒，自己上https://aitts.fkdk.ink/看

## 环境依赖

本工具基于 Python 3 开发，使用了以下依赖库：

忘了，后续补充

### 安装依赖

PATH开放ollama连接端口，安装whisper python库，安装GSVI TTS
    
##🚀使用说明

### 1. 启动工具

启动ollama和GSVI TTS
以下我自己使用的启动cmd（根据自己项目位置来，我加Frp的）
```bash
@echo off
rem 启动 run.bat
start "" cmd /c "cd /d E:\ai\GPT-SoVITS-Inference && run.bat"

rem 切换到 E:\ai\api 路径并启动 ok5.py 脚本
start "" cmd /c "cd /d E:\ai\api\api_run && E:\ai\api\api_run\.venv\Scripts\python.exe E:\ai\api\api_run\ok6.py"

start "" cmd /c ollama run qwen2.5:7b

start "" cmd /c "cd /d C:\Users\alyfk\Desktop\frp && run.cmd"
```

启动OK.py，然后就可以看到端口和ip，然后运行demo即可

## 计划

后续看喜欢就给个star，有需求给个issue，看心情写

## 贡献

欢迎通过提交 Issue 或 Pull Request 来贡献代码和改进建议。如果您在使用过程中遇到问题或有功能需求，请在 [GitHub Issues](https://github.com/Aftnos/AITTS/issues) 中提出。

## 许可证

本项目基于 GPL-3.0 许可证开源，详情见 [LICENSE](https://github.com/Aftnos/AITTS/blob/main/LICENSE)。

## 联系方式

如果您有任何问题或建议，请联系 [Aftnos](https://github.com/Aftnos)。

## 其他信息
![Star history chart](https://api.star-history.com/svg?repos=Aftnos/AITTSn&type=Date)
---
