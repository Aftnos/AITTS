# chat.py
import json
import re
import requests
from flask import Response, stream_with_context, jsonify

# 全局会话上下文（可考虑使用更复杂的存储方案）
conversation_contexts = {}

def process_chat_request(user_input, yhid, MODEL_API_URL, DEFAULT_LLM_MODEL,
                         enable_memory=True, tts_client=None, extra_tts_params={},
                         convert_to_16k=False):
    """
    处理聊天请求：调用 LLM 模型 API，按句分割后调用 TTS 生成语音数据，返回流式响应。
    """
    llm_model = DEFAULT_LLM_MODEL
    data = {
        "model": llm_model,
        "prompt": user_input,
        "stream": True
    }

    # 添加会话上下文
    conversation_context = conversation_contexts.get(yhid)
    if enable_memory and conversation_context is not None:
        data['context'] = conversation_context

    print(f"用户 {yhid} 请求数据:")
    print(json.dumps(data, indent=4, ensure_ascii=False))

    try:
        response = requests.post(MODEL_API_URL, json=data, stream=True)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"模型 API 请求失败：{e}"}), 500

    def generate():
        nonlocal conversation_context
        sentence_buffer = ""
        generated_text = ""
        for line in response.iter_lines(decode_unicode=True):
            if line:
                try:
                    response_json = json.loads(line)
                    message_content = response_json.get('response', '')
                    generated_text += message_content
                    sentence_buffer += message_content

                    # 检测句子结束符
                    sentences = re.split(r'([。！？])', sentence_buffer)
                    for i in range(0, len(sentences) - 1, 2):
                        sentence = sentences[i] + sentences[i + 1]
                        audio_str = tts_client.get_audio_base64(
                            sentence, extra_tts_params, convert_to_16k
                        ) if tts_client else ""
                        yield json.dumps({
                            "text": sentence,
                            "audio": audio_str
                        }, ensure_ascii=False) + '\n'

                    sentence_buffer = sentences[-1]
                    if response_json.get('done', False):
                        if enable_memory:
                            conversation_context = response_json.get('context', None)
                            conversation_contexts[yhid] = conversation_context
                        else:
                            conversation_context = None
                            conversation_contexts[yhid] = None
                        if sentence_buffer:
                            audio_str = tts_client.get_audio_base64(
                                sentence_buffer, extra_tts_params, convert_to_16k
                            ) if tts_client else ""
                            yield json.dumps({
                                "text": sentence_buffer,
                                "audio": audio_str
                            }, ensure_ascii=False) + '\n'
                        break
                except json.JSONDecodeError:
                    print(f"无法解析的响应行: {line}")

    return Response(stream_with_context(generate()), mimetype='application/json; charset=utf-8')
