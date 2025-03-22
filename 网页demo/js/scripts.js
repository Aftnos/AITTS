// scripts.js

async function callApi() {
	const apiUrl = document.getElementById("apiUrl").value || 'http://127.0.0.1:20005/api/chat';
	const question = document.getElementById("question").value;
	const yhid = document.getElementById("yhid").value;
	const model = document.getElementById("model").value;
	const character = document.getElementById("character").value;
	const emotion = document.getElementById("emotion").value;
	const speed = document.getElementById("speed").value;
	const enableMemory = document.getElementById("enableMemory").checked;
	const mergeAudio = document.getElementById("mergeAudio").checked;

	if (!question || !yhid) {
		alert("请填写问题和用户ID");
		return;
	}

	if (!model) {
		alert("请选择LLM模型");
		return;
	}

	if (!character) {
		alert("请选择TTS角色");
		return;
	}

	if (!emotion) {
		alert("请选择TTS情感");
		return;
	}

	const requestBody = {
		question: question,
		yhid: yhid
	};

	if (model) requestBody.llm_model = model;
	if (enableMemory) requestBody.enable_memory = enableMemory;
	if (character || emotion || speed) {
		requestBody.tts_params = {};
		if (character) {
			requestBody.tts_params.character = character;
		}
		if (emotion) {
			requestBody.tts_params.emotion = emotion;
		}
		if (speed) {
			requestBody.tts_params.speed = speed;
		}
	}

	const chatSectionContent = document.getElementById("chatSectionContent");
	chatSectionContent.innerHTML +=
		`<div class="message user"><div class="message-bubble user">${question}</div><img src="./png/1.jpeg" alt="用户头像" class="avatar"></div>`;
	document.getElementById("question").value = "";
	chatSectionContent.scrollTop = chatSectionContent.scrollHeight;

	try {
		const response = await fetch(apiUrl, {
			method: "POST",
			headers: {
				"Content-Type": "application/json"
			},
			body: JSON.stringify(requestBody)
		});

		if (!response.ok) {
			const errorText = await response.text();
			alert("错误: " + errorText);
			return;
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder("utf-8");
		let responseData = "";
		let audioChunks = [];

		while (true) {
			const {
				done,
				value
			} = await reader.read();
			if (done) break;
			responseData += decoder.decode(value, {
				stream: true
			});

			const lines = responseData.split("\n");
			responseData = lines.pop();

			for (const line of lines) {
				if (line.trim()) {
					try {
						const data = JSON.parse(line);
						if (data.text) {
							chatSectionContent.innerHTML +=
								`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="message-bubble bot">${data.text}</div></div>`;
						}
						if (data.audio) {
							const byteCharacters = atob(data.audio);
							const byteNumbers = new Array(byteCharacters.length);
							for (let i = 0; i < byteCharacters.length; i++) {
								byteNumbers[i] = byteCharacters.charCodeAt(i);
							}
							const byteArray = new Uint8Array(byteNumbers);
							if (mergeAudio) {
								audioChunks = audioChunks.concat(Array.from(byteArray));
							} else {
								const audioBlob = new Blob([byteArray], {
									type: 'audio/wav'
								});
								const audioDuration = await getAudioDuration(audioBlob);
								if (audioDuration && isFinite(audioDuration)) {
									chatSectionContent.innerHTML +=
										`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="audio-section" onclick="playAudio('${URL.createObjectURL(audioBlob)}')"><svg t="1728236591800" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1483" width="20" height="20"><path d="M138.24 512A71.68 71.68 0 1 0 281.6 512 71.68 71.68 0 0 0 138.24 512z m296.96 314.88a38.784 38.784 0 0 1-27.648-11.776 38.144 38.144 0 0 1 1.024-54.272A342.72 342.72 0 0 0 514.56 512a344.704 344.704 0 0 0-105.984-248.832 38.144 38.144 0 0 1-1.024-54.272 38.144 38.144 0 0 1 54.272-1.024A419.776 419.776 0 0 1 591.36 512c0 115.2-46.08 223.232-129.536 304.128a37.568 37.568 0 0 1-26.624 10.752z m225.28 179.2a37.12 37.12 0 0 1-27.136-11.264 38.656 38.656 0 0 1 0-54.272A600.576 600.576 0 0 0 811.52 512a600.576 600.576 0 0 0-178.176-428.544 38.144 38.144 0 0 1 0-54.272 38.144 38.144 0 0 1 54.272 0A675.2 675.2 0 0 1 888.32 512a675.2 675.2 0 0 1-200.704 482.816 37.952 37.952 0 0 1-27.136 11.264z" fill="#000000" p-id="1484"></path></svg><span>${audioDuration}"</span><div class="red-dot"></div></div></div>`;
								}
							}
						}
					} catch (parseError) {
						console.log("JSON 解析失败:", parseError);
					}
				}
			}
		}
		if (mergeAudio && audioChunks.length > 0) {
			const combinedBlob = new Blob([new Uint8Array(audioChunks)], {
				type: 'audio/wav'
			});
			const audioUrl = URL.createObjectURL(combinedBlob);
			const audioDuration = await getAudioDuration(combinedBlob);
			if (audioDuration && isFinite(audioDuration)) {
				chatSectionContent.innerHTML +=
					`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="audio-section" onclick="playAudio('${audioUrl}')"><svg t="1728236591800" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1483" width="20" height="20"><path d="M138.24 512A71.68 71.68 0 1 0 281.6 512 71.68 71.68 0 0 0 138.24 512z m296.96 314.88a38.784 38.784 0 0 1-27.648-11.776 38.144 38.144 0 0 1 1.024-54.272A342.72 342.72 0 0 0 514.56 512a344.704 344.704 0 0 0-105.984-248.832 38.144 38.144 0 0 1-1.024-54.272 38.144 38.144 0 0 1 54.272-1.024A419.776 419.776 0 0 1 591.36 512c0 115.2-46.08 223.232-129.536 304.128a37.568 37.568 0 0 1-26.624 10.752z m225.28 179.2a37.12 37.12 0 0 1-27.136-11.264 38.656 38.656 0 0 1 0-54.272A600.576 600.576 0 0 0 811.52 512a600.576 600.576 0 0 0-178.176-428.544 38.144 38.144 0 0 1 0-54.272 38.144 38.144 0 0 1 54.272 0A675.2 675.2 0 0 1 888.32 512a675.2 675.2 0 0 1-200.704 482.816 37.952 37.952 0 0 1-27.136 11.264z" fill="#000000" p-id="1484"></path></svg><span>${audioDuration}"</span><div class="red-dot"></div></div></div>`;
			}
		}
		chatSectionContent.scrollTop = chatSectionContent.scrollHeight;
		if (character) {
			document.querySelector('.chat-header').innerText = character;
		}
	} catch (error) {
		alert("请求失败: " + error);
	}
}

function playAudio(audioUrl) {
	const audio = new Audio(audioUrl);
	audio.play();
}

async function getAudioDuration(blob) {
	return new Promise((resolve) => {
		const audio = document.createElement('audio');
		audio.src = URL.createObjectURL(blob);
		audio.addEventListener('loadedmetadata', () => {
			resolve(Math.round(audio.duration));
		});
		audio.addEventListener('error', () => {
			resolve(0);
		});
	});
}

async function fetchModels() {
	const apiUrl = document.getElementById("apiUrl").value;
	if (!apiUrl) {
		alert("请填写 API 地址");
		return;
	}

	const loading = document.getElementById("loading");
	loading.style.display = "block";

	try {
		const ttsResponse = await fetch(`${apiUrl.replace(/\/api\/chat$/, '')}/api/tts_models`);
		if (ttsResponse.ok) {
			const ttsModels = await ttsResponse.json();
			const characterSelect = document.getElementById("character");
			const emotionSelect = document.getElementById("emotion");
			characterSelect.innerHTML = "<option value=''>请选择角色</option>";
			emotionSelect.innerHTML = "<option value=''>请先选择角色</option>";
			Object.keys(ttsModels).forEach(model => {
				const option = document.createElement("option");
				option.value = model;
				option.textContent = model;
				characterSelect.appendChild(option);
			});
			characterSelect.addEventListener('change', function() {
				const selectedCharacter = this.value;
				const emotions = ttsModels[selectedCharacter];
				emotionSelect.innerHTML = "<option value=''>请选择</option>";
				emotionSelect.disabled = !emotions;
				if (emotions) {
					emotions.forEach(emotion => {
						const emotionOption = document.createElement("option");
						emotionOption.value = emotion;
						emotionOption.textContent = emotion;
						emotionSelect.appendChild(emotionOption);
					});
				}
			});
			emotionSelect.disabled = true;
		}

		const llmResponse = await fetch(`${apiUrl.replace(/\/api\/chat$/, '')}/api/llm_models`);
		if (llmResponse.ok) {
			const llmModels = await llmResponse.json();
			const modelInput = document.getElementById("model");
			modelInput.innerHTML = "<option value=''>请选择模型</option>";
			llmModels.models.forEach(m => {
				const option = document.createElement("option");
				option.value = m.model;
				option.textContent = m.name;
				modelInput.appendChild(option);
			});
		}

	} catch (error) {
		alert("获取模型列表失败: " + error);
	} finally {
		loading.style.display = "none";
	}
}

async function callAsrApi(audioFile) {
	const apiUrlInput = document.getElementById("apiUrl").value || 'http://127.0.0.1:20005/api/chat';
	const baseUrl = apiUrlInput.replace(/\/api\/chat$/, '');
	const asrUrl = `${baseUrl}/api/asr`;

	const yhid = document.getElementById("yhid").value;
	const model = document.getElementById("model").value;
	const character = document.getElementById("character").value;
	const emotion = document.getElementById("emotion").value;
	const speed = document.getElementById("speed").value;
	const enableMemory = document.getElementById("enableMemory").checked;
	const mergeAudio = document.getElementById("mergeAudio").checked;
	const language = document.getElementById("language") ? document.getElementById("language").value : '';

	if (!audioFile || !yhid) {
		alert("请上传音频文件并填写用户ID");
		return;
	}

	const formData = new FormData();
	formData.append('audio', audioFile);
	formData.append('yhid', yhid);
	if (language) formData.append('language', language);
	formData.append('beam_size', '5');
	formData.append('task', 'transcribe');
	if (model) formData.append('llm_model', model);
	formData.append('enable_memory', enableMemory.toString());
	const ttsParams = {};
	if (character) ttsParams.character = character;
	if (emotion) ttsParams.emotion = emotion;
	if (speed) ttsParams.speed = speed;
	formData.append('tts_params', JSON.stringify(ttsParams));

	const chatSectionContent = document.getElementById("chatSectionContent");
	chatSectionContent.innerHTML +=
		`<div class="message user"><div class="message-bubble user">[语音输入]</div><img src="./png/1.jpeg" alt="用户头像" class="avatar"></div>`;
	chatSectionContent.scrollTop = chatSectionContent.scrollHeight;

	try {
		const response = await fetch(asrUrl, {
			method: "POST",
			body: formData
		});

		if (!response.ok) {
			const errorText = await response.text();
			alert("错误: " + errorText);
			return;
		}

		const reader = response.body.getReader();
		const decoder = new TextDecoder("utf-8");
		let responseData = "";
		let audioChunks = [];

		while (true) {
			const {
				done,
				value
			} = await reader.read();
			if (done) break;
			responseData += decoder.decode(value, {
				stream: true
			});

			const lines = responseData.split("\n");
			responseData = lines.pop();

			for (const line of lines) {
				if (line.trim()) {
					try {
						const data = JSON.parse(line);
						if (data.text) {
							chatSectionContent.innerHTML +=
								`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="message-bubble bot">${data.text}</div></div>`;
						}
						if (data.audio) {
							const byteCharacters = atob(data.audio);
							const byteNumbers = new Array(byteCharacters.length);
							for (let i = 0; i < byteCharacters.length; i++) {
								byteNumbers[i] = byteCharacters.charCodeAt(i);
							}
							const byteArray = new Uint8Array(byteNumbers);
							if (mergeAudio) {
								audioChunks = audioChunks.concat(Array.from(byteArray));
							} else {
								const audioBlob = new Blob([byteArray], {
									type: 'audio/wav'
								});
								const audioDuration = await getAudioDuration(audioBlob);
								if (audioDuration && isFinite(audioDuration)) {
									chatSectionContent.innerHTML +=
										`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="audio-section" onclick="playAudio('${URL.createObjectURL(audioBlob)}')"><svg t="1728236591800" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1483" width="20" height="20"><path d="M138.24 512A71.68 71.68 0 1 0 281.6 512 71.68 71.68 0 0 0 138.24 512z m296.96 314.88a38.784 38.784 0 0 1-27.648-11.776 38.144 38.144 0 0 1 1.024-54.272A342.72 342.72 0 0 0 514.56 512a344.704 344.704 0 0 0-105.984-248.832 38.144 38.144 0 0 1-1.024-54.272 38.144 38.144 0 0 1 54.272-1.024A419.776 419.776 0 0 1 591.36 512c0 115.2-46.08 223.232-129.536 304.128a37.568 37.568 0 0 1-26.624 10.752z m225.28 179.2a37.12 37.12 0 0 1-27.136-11.264 38.656 38.656 0 0 1 0-54.272A600.576 600.576 0 0 0 811.52 512a600.576 600.576 0 0 0-178.176-428.544 38.144 38.144 0 0 1 0-54.272 38.144 38.144 0 0 1 54.272 0A675.2 675.2 0 0 1 888.32 512a675.2 675.2 0 0 1-200.704 482.816 37.952 37.952 0 0 1-27.136 11.264z" fill="#000000" p-id="1484"></path></svg><span>${audioDuration}"</span><div class="red-dot"></div></div></div>`;
								}
							}
						}
					} catch (parseError) {
						console.log("JSON 解析失败:", parseError);
					}
				}
			}
		}
		if (mergeAudio && audioChunks.length > 0) {
			const combinedBlob = new Blob([new Uint8Array(audioChunks)], {
				type: 'audio/wav'
			});
			const audioUrl = URL.createObjectURL(combinedBlob);
			const audioDuration = await getAudioDuration(combinedBlob);
			if (audioDuration && isFinite(audioDuration)) {
				chatSectionContent.innerHTML +=
					`<div class="message bot"><img src="./png/${character}.jpeg" alt="${character}头像" class="avatar"><div class="audio-section" onclick="playAudio('${audioUrl}')"><svg t="1728236591800" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1483" width="20" height="20"><path d="M138.24 512A71.68 71.68 0 1 0 281.6 512 71.68 71.68 0 0 0 138.24 512z m296.96 314.88a38.784 38.784 0 0 1-27.648-11.776 38.144 38.144 0 0 1 1.024-54.272A342.72 342.72 0 0 0 514.56 512a344.704 344.704 0 0 0-105.984-248.832 38.144 38.144 0 0 1-1.024-54.272 38.144 38.144 0 0 1 54.272-1.024A419.776 419.776 0 0 1 591.36 512c0 115.2-46.08 223.232-129.536 304.128a37.568 37.568 0 0 1-26.624 10.752z m225.28 179.2a37.12 37.12 0 0 1-27.136-11.264 38.656 38.656 0 0 1 0-54.272A600.576 600.576 0 0 0 811.52 512a600.576 600.576 0 0 0-178.176-428.544 38.144 38.144 0 0 1 0-54.272 38.144 38.144 0 0 1 54.272 0A675.2 675.2 0 0 1 888.32 512a675.2 675.2 0 0 1-200.704 482.816 37.952 37.952 0 0 1-27.136 11.264z" fill="#000000" p-id="1484"></path></svg><span>${audioDuration}"</span><div class="red-dot"></div></div></div>`;
			}
		}
		chatSectionContent.scrollTop = chatSectionContent.scrollHeight;
		if (character) {
			document.querySelector('.chat-header').innerText = character;
		}
	} catch (error) {
		alert("请求失败: " + error);
	}
}

async function handleAsrUpload(event) {
	const file = event.target.files[0];
	if (!file) {
		return;
	}
	await callAsrApi(file);
	event.target.value = "";
}

let mediaRecorder;
let recordedChunks = [];
let isRecording = false;

async function initRecording() {
	try {
		const stream = await navigator.mediaDevices.getUserMedia({
			audio: true
		});
		mediaRecorder = new MediaRecorder(stream);

		mediaRecorder.ondataavailable = (event) => {
			if (event.data.size > 0) {
				recordedChunks.push(event.data);
			}
		};

		mediaRecorder.onstop = async () => {
			const blob = new Blob(recordedChunks, {
				type: 'audio/wav'
			});
			recordedChunks = [];
			const file = new File([blob], 'recorded_audio.wav', {
				type: 'audio/wav'
			});
			await callAsrApi(file);
		};
	} catch (err) {
		alert('无法访问麦克风: ' + err.message);
	}
}

async function toggleRecording(button) {
	if (!mediaRecorder) {
		await initRecording();
		if (!mediaRecorder) return;
	}

	if (isRecording) {
		mediaRecorder.stop();
		isRecording = false;
		button.classList.remove('recording');
		button.innerHTML = `<svg t="1728840625403" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1728" width="200" height="200"><path d="M514.048 128q79.872 0 149.504 30.208t121.856 82.432 82.432 122.368 30.208 150.016q0 78.848-30.208 148.48t-82.432 121.856-121.856 82.432-149.504 30.208-149.504-30.208-121.856-82.432-82.432-121.856-30.208-148.48q0-79.872 30.208-150.016t82.432-122.368 121.856-82.432 149.504-30.208z" p-id="1729" fill="#ffffff"></path></svg> 录音`;
	} else {
		mediaRecorder.start();
		isRecording = true;
		button.classList.add('recording');
		button.innerHTML = `<svg t="1728840779874" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2782" width="200" height="200"><path d="M624 358l-224 0c-23.198 0-42 18.8-42 42l0 224c0 23.2 18.802 42 42 42l224 0c23.198 0 42-18.8 42-42l0-224C666 376.8 647.198 358 624 358zM512 64c-247.422 0-448 200.578-448 448s200.578 448 448 448 448-200.578 448-448S759.422 64 512 64zM512 888c-207.652 0-376-168.332-376-376 0-207.652 168.348-376 376-376 207.654 0 376.002 168.332 376.002 376S719.652 888 512 888z" fill="#ffffff" p-id="2783"></path></svg> 停止`;
	}
}

window.onload = () => {
	const recordButton = document.getElementById('recordButton');
	recordButton.innerHTML = `<svg t="1728840625403" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="1728" width="200" height="200"><path d="M514.048 128q79.872 0 149.504 30.208t121.856 82.432 82.432 122.368 30.208 150.016q0 78.848-30.208 148.48t-82.432 121.856-121.856 82.432-149.504 30.208-149.504-30.208-121.856-82.432-82.432-121.856-30.208-148.48q0-79.872 30.208-150.016t82.432-122.368 121.856-82.432 149.504-30.208z" p-id="1729" fill="#ffffff"></path></svg> 录音`;
};