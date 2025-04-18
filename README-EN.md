# AITTS

![AITTS](https://socialify.git.ci/Aftnos/AITTS/image?description=1&font=Jost&forks=1&issues=1&language=1&logo=https%3A%2F%2Favatars.githubusercontent.com%2Fu%2F128480098&name=1&owner=1&pattern=Circuit%20Board&pulls=1&stargazers=1&theme=Dark)

## 📦 Project Overview

**AITTS** is an experimental project designed for low-latency, end-to-end speech interaction with localized large models. It integrates speech recognition (ASR), large language model (LLM) interactions, and text-to-speech synthesis (TTS) into a single system that supports fully local deployment. The core of the project is written in Python and relies on [whisper](https://github.com/openai/whisper) for speech recognition, uses [GSVI TTS](#) for speech synthesis, and wraps around the Ollama model to deliver a low-latency, intelligent speech interaction experience. All the code in this project is generated by AI. Currently in its initial stage, the project is gradually evolving into a fully intelligent interactive companion that will incorporate VLM and other multimodal capabilities. Stay tuned!

## 🔧 Main Features

- **LLM Interaction**
- **Speech Recognition (ASR)**
- **TTS Speech Synthesis**
- **Full Local Deployment**

## 🚀 Environment Dependencies

This project is developed based on Python 3.8 or later, and primarily depends on the following open source projects and libraries:

- **[whisper](https://github.com/openai/whisper)**  
  Used for speech recognition, providing high-quality ASR capabilities.

- **Ollama**  
  Provides an interface encapsulation for large language models, supporting various LLM models (such as qwen2.5:7b).

- **GSVI TTS**  
  Converts text to speech synthesis, supporting customizable roles, emotions, and speech rates.

- **Other Dependencies**  
  - Flask: for building API services  
  - requests: for HTTP request handling  
  - opencc: for conversion between Simplified and Traditional Chinese  
  - torch: PyTorch backend support  
  - faster_whisper: accelerated version for calling the whisper model

> **Note:** Please ensure that all services (Ollama, GSVI TTS, and the whisper model) are properly configured and running, and that the API endpoints are accessible.

## 💻 Usage Instructions

1. **Preparation Before Starting**  
   - Ensure that your local environment has Python 3.8 or later installed.  
   - Install the project dependencies with:  
     ```bash
     pip install -r requirements.txt
     ```  
   - Configure the access addresses for each service by modifying the parameters in the `config.json` file (including the ports for Ollama, GSVI TTS, etc.).

2. **Starting the Service**  
   - Start the Ollama and GSVI TTS services and confirm that their respective API endpoints are available.  
   - > **Note:** Please test whether the Ollama API endpoint is accessible. If not, add the PATH environment variable to expose the Ollama API.  
   - Start the project's API service by running the startup script:  
     ```bash
     python app.py
     ```  
     The service will listen on the port specified in the configuration.

3. **Usage Considerations**  
   - > For webpage recording, please enable HTTPS; otherwise, recording will not be possible. When using HTTPS, configure Flask with an SSL certificate (if the certificate is not trusted, please access via the IP to trust the certificate before using the API).  
   - > Each user's conversation history is managed via an 8-character hexadecimal string ID.

## 🔮 Project Roadmap

- **Multi-Platform Integration**  
  Support cloud-based models and ensure compatibility with the OpenAI standard API.

- **Tool Invocation Support**  
  Add built-in tools (such as current time queries, calculators, web searches, etc.).

- **Long-Term Memory Feature**  
  Develop a mechanism for storing and managing long-term memory based on conversation content, enhancing the continuity of interactions.

- **Hardware Integration**  
  Enable integration with microcontrollers like STM32 and ESP32 for combining physical hardware.

- **Smart Home Control**  
  Leverage open interfaces such as Mi Home to achieve automated voice-controlled smart home devices.

- **Intelligent Companion**  
  Integrate VLM, LLM, long-term memory, and tool control to create an intelligent companion.

## 📸 Screenshots

![Project Screenshot](https://github.com/user-attachments/assets/f1c85337-e3a6-4073-8663-64bd7806d984)  
![Project GIF](https://github.com/user-attachments/assets/53f82963-aa42-4ee2-b58f-3c2fbc86d785)  
![Project Screenshot 2](https://github.com/user-attachments/assets/48065544-fb11-4904-9ab7-3b28fc0914cb)

Demo webpage: [https://aitts.fkdk.ink](https://aitts.fkdk.ink)

## 📬 Contribution and Feedback

Contributions via Issues or Pull Requests are welcome to improve the code and add new features. If you have any questions or feature requests, please open an issue on [GitHub Issues](https://github.com/Aftnos/AITTS/issues).

## 📝 License

This project is open-sourced under the [GPL-3.0 License](https://github.com/Aftnos/AITTS/blob/main/LICENSE). Feel free to study and share.

## 📞 Contact

If you have any questions or suggestions, please contact [Aftnos](https://github.com/Aftnos) or email alyfk@qq.com.

---
