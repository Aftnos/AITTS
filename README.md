# AITTS

![AITTS](https://socialify.git.ci/Aftnos/AITTS/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F128480098&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark) <!-- 请确保在仓库的 `assets` 文件夹中放置 `logo.png` 或替换为实际图标路径 -->

## 📦项目简介

AITTS是一个专为本地化大模型语音端到语音端低延时交互实现的简单探索。使用Python对ollama和GSVI TTS和whisper进行封装聚合成API，实现了可全本地部署的语音智能交互。本项目全部代码由AI完成，这是一个实验项目。本项目目前处于初始阶段，会逐步转型为全智能交互场景的智能陪护，接入VLM等多模态，请拭目以待！

## 功能概述

- **LLM交互**：支持单独LLM文字流式/非流式交互，支持Ollama List模型列表。
- **语音识别**：支持直接ASR识别语音。
- **TTS语音**：支持从LLM转TTS，支持自定义TTS List模型列表。

## 截图
![image](https://github.com/user-attachments/assets/f1c85337-e3a6-4073-8663-64bd7806d984)

Demo网页地址 https://aitts.fkdk.ink

## 环境依赖

本工具基于 Python 3.8以上 开发，使用了以下依赖库：
whisper python库
ollama库（非必选，没有实际运用）

后续补充

### 安装依赖

注意：
1.PATH开放ollama连接端口。
2.安装whisper python库。
3.安装GSVI TTS
    
##🚀使用说明

注意，启用HTTPS请配置好证书文件！

### 1. 启动工具

启动你的ollama和GSVI TTS
先测试这俩的API是否开放（本地开放即可除非服务端不同）
以下我自己使用的启动cmd（根据自己项目位置来，我加Frp的）
```bash
@echo off
rem 启动 run.bat
start "" cmd /c "cd /d E:\ai\GPT-SoVITS-Inference && run.bat"

rem 切换到 E:\ai\api 路径并启动 ok6.py 脚本
start "" cmd /c "cd /d E:\ai\api\api_run && E:\ai\api\api_run\.venv\Scripts\python.exe E:\ai\api\api_run\ok6.py"

start "" cmd /c ollama run qwen2.5:7b

start "" cmd /c "cd /d C:\Users\alyfk\Desktop\frp && run.cmd"
```

启动OK.py，然后就可以看到端口和ip，然后运行demo即可（用户ID用于保存个人聊天记录）

## 计划

计划多端融合
1.支持对OpenAI的标准接口实现云端模型支持

2.实现工具的调用（当前时间、计算器、联网搜索等）

3.实现长记忆（使用模型对对话内容进行处理存储为长期记忆）

4.多端接入，逐步开发STM32、ESP32等单片接入接口实现物理硬件

5.实现物联控制，通过米家开源接口，使智能家居能完全接入智能控制（这真智能 雷军star!）

6.实现拟人化陪伴功能，完整打通VLM-LLM-长记忆-长思维-智能工具控制，实现最终效果：智能化陪护，智能化控制！

## 贡献

欢迎通过提交 Issue 或 Pull Request 来贡献代码和改进建议。如果您在使用过程中遇到问题或有功能需求，请在 [GitHub Issues](https://github.com/Aftnos/AITTS/issues) 中提出。

## 许可证

本项目基于 GPL-3.0 许可证开源，详情见 [LICENSE](https://github.com/Aftnos/AITTS/blob/main/LICENSE)。

## 联系方式

如果您有任何问题或建议，请联系 [Aftnos](https://github.com/Aftnos)。邮箱：alyfk@qq.com
