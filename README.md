# AITTS

![AITTS](https://socialify.git.ci/Aftnos/AITTS/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F128480098&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark)  

## 📦 项目简介

**AITTS** 是一个专为本地化大模型语音端到语音端低延时交互而设计的实验性项目。它将语音识别（ASR）、大语言模型（LLM）交互以及语音合成（TTS）功能整合在一起，支持全本地部署。项目核心依赖于 Python 语言，基于 [whisper](https://github.com/openai/whisper) 进行语音识别，利用 [GSVI TTS](#) 实现语音合成，并对 Ollama 模型进行封装聚合，打造低延时、智能化的语音交互体验。本项目全部代码由AI完成，本项目目前处于初始阶段，会逐步转型为全智能交互场景的智能陪护，接入VLM等多模态，请拭目以待！

## 🔧 主要功能

- **LLM 交互**  
- **语音识别（ASR）**  
- **TTS 语音合成**  
- **全本地部署**  

## 🚀 环境依赖

本项目基于 Python 3.8 及以上版本开发，主要依赖以下开源项目和库：

- **[whisper](https://github.com/openai/whisper)**  
  用于语音识别，提供高质量的 ASR 能力。

- **Ollama**  
  用于大语言模型接口封装，支持多种 LLM 模型（如 qwen2.5:7b）。

- **GSVI TTS**  
  实现文本到语音的合成转换，支持自定义角色、情感和语速等参数。

- **其他依赖**  
  - Flask：构建 API 服务  
  - requests：HTTP 请求处理  
  - opencc：简繁体中文转换  
  - torch：PyTorch 后端支持  
  - faster_whisper：加速版 whisper 模型调用

> 注意：请确保各项服务（Ollama、GSVI TTS 及 whisper 模型）已正确配置并启动，确保 API 接口可正常访问。

## 💻 使用说明

1. **启动前准备**  
   - 确保本地环境安装了 Python 3.8 以上版本。  
   - 安装项目依赖：`pip install -r requirements.txt`。  
   - 配置各个服务的访问地址，开放端口、Ollama、GSVI TTS地址，修改 `config.json` 文件中的参数。

2. **启动服务**  
   - 启动 Ollama 和 GSVI TTS 服务，并确认各自 API 接口可用。  
   - >注意：请测试ollama API接口是否可用，不可用请添加PATH环境变量开放ollama API。
   - 启动本项目的 API 服务，运行启动脚本`python app.py`，服务将监听配置中指定的端口。

3. **使用注意**  
   - >网页使用录音请打开HTTPS，否则无法录音，使用HTTPS时Flask请配置SSL证书（证书不对的时候请先直接访问IP信任证书再使用API）。
   - >每个用户的对话记录由ID方式记录（8位 16 进制字符串）进行管理。

## 🔮 项目规划

- **多端融合**  
  实现云端模型支持，兼容 OpenAI 标准接口兼容。

- **工具调用支持**  
  添加内置工具（如当前时间查询、计算器、联网搜索等）。

- **长记忆功能**  
  开发基于对话内容的长期记忆存储与管理机制，提升连续对话体验。

- **硬件接入**  
  实现 STM32、ESP32 等单片机的接入，实现物理硬件结合。

- **智能家居控制**  
  利用米家等开源接口，实现智能家居设备的语音控制自动化。

- **智能陪护**  
  打通 VLM、LLM、长记忆与工具控制，实现智能化陪护。

## 📸 截图

![项目截图](https://github.com/user-attachments/assets/f1c85337-e3a6-4073-8663-64bd7806d984)
![项目GIF](https://github.com/user-attachments/assets/53f82963-aa42-4ee2-b58f-3c2fbc86d785)
![项目截图2](https://github.com/user-attachments/assets/48065544-fb11-4904-9ab7-3b28fc0914cb)

Demo 网页地址：[https://aitts.fkdk.ink](https://aitts.fkdk.ink)

## 📬 贡献与反馈

欢迎提交 Issue 或 Pull Request 来贡献代码和改进建议。如有问题或功能需求，请在 [GitHub Issues](https://github.com/Aftnos/AITTS/issues) 中提出。

## 📝 许可证

本项目基于 [GPL-3.0 许可证](https://github.com/Aftnos/AITTS/blob/main/LICENSE) 开源，欢迎学习与交流。

## 📞 联系方式

如有任何问题或建议，请联系 [Aftnos](https://github.com/Aftnos) 或发送邮件至 alyfk@qq.com。

---
