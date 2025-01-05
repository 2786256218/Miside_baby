#coding=utf-8
import base64
import json
import uuid
import requests
from pydub import AudioSegment
import pyaudio
import wave
import keyboard
import whisper
import os
import tempfile
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2


# 填写平台申请的appid, access_token以及cluster
appid = "XXX"
access_token = "XXX"
cluster = "XXX"

voice_type = "XXX"
host = "openspeech.bytedance.com"
api_url = f"https://{host}/api/v1/tts"

header = {"Authorization": f"Bearer;{access_token}"}

conversation_history = []  # 用于存储聊天历史记录


def ollama_chat(input_text):
    """
    向指定API发送请求，使用gemma2模型与ollama进行聊天交互并返回回复内容

    :param input_text: 聊天输入的文本内容
    :return: ollama回复的文本内容，若请求或解析出现问题则返回空字符串
    """
    print(f"进入ollama_chat函数，输入内容为: {input_text}")
    base_url = "http://localhost:11434/api/chat"
    model_name = "gemma2"
    prompt_template = "你的名字叫米塔，英文名Miside，性别女，米塔是用户的女朋友，你的任务就是扮演米塔的角色来和用户聊天，以及陪伴用户。"

    # 将历史聊天记录和新输入一起构建请求消息
    messages = [
        {"role": "system", "content": prompt_template}
    ]
    messages.extend(conversation_history)
    messages.append({"role": "user", "content": input_text})

    data = {
        "model": model_name,
        "messages": messages,
        "stream": False
    }

    print("请求的URL:", base_url)
    print("发送的请求参数:", data)
    try:
        response = requests.post(
            base_url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        print("响应状态码:", response.status_code)
        response.raise_for_status()  # 检查请求是否成功，若不成功则抛出异常
        response_json = response.json()
        reply = response_json.get('message', {}).get('content', '').strip()
        print("退出ollama_chat函数")
        return reply
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"出现错误: {e}")
        return ""


def play_audio(file_path):
    """
    使用pydub和pyaudio播放指定路径的音频文件

    :param file_path: 音频文件的路径
    """
    audio = AudioSegment.from_file(file_path)
    audio_data = audio.raw_data
    sample_width = audio.sample_width
    channels = audio.channels
    frame_rate = audio.frame_rate

    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(sample_width),
                    channels=channels,
                    rate=frame_rate,
                    output=True)
    stream.write(audio_data)
    stream.stop_stream()
    stream.close()
    p.terminate()
    time.sleep(1)  # 添加延迟，等待资源释放，可根据实际情况调整时间长短


def TTS_read(text):
    """
    使用字节跳动语音合成服务将输入的文本合成为音频并保存为临时文件，
    然后播放音频文件，播放完毕后删除该文件。

    :param text: 要转换为语音的文本内容
    """
    print(f"进入TTS_read函数，输入文本为: {text}")
    request_json = {
        "app": {
            "appid": appid,
            "token": "access_token",
            "cluster": cluster
        },
        "user": {
            "uid": "388808087185088"
        },
        "audio": {
            "voice_type": voice_type,
            "encoding": "mp3",
            "speed_ratio": 1.0,
            "volume_ratio": 1.0,
            "pitch_ratio": 1.0,
        },
        "request": {
            "reqid": str(uuid.uuid4()),
            "text": text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"
        }
    }
    try:
        resp = requests.post(api_url, json=request_json, headers=header)
        if resp.status_code == 200:
            print(f"resp body: \n{resp.json()}")
            if "data" in resp.json():
                data = resp.json()["data"]
                # 创建临时文件并获取文件对象和文件_path
                with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                    file_path = temp_file.name
                    temp_file.write(base64.b64decode(data))
                # 使用pydub和pyaudio播放音频文件
                play_audio(file_path)
                # 删除临时文件
                os.remove(file_path)
            else:
                print("服务器返回数据中不包含音频数据")
        else:
            print(f"请求失败，状态码: {resp.status_code}，错误信息: {resp.text}")
    except Exception as e:
        print(f"出现异常: {e}")
    print("退出TTS_read函数")


def record_audio(file_path):
    """
    这个函数用于从麦克风录制音频，并将其保存到指定的文件路径

    参数：
    file_path (str): 音频文件的保存路径

    """
    # 创建 PyAudio 对象
    p = pyaudio.PyAudio()
    # 打开音频流，设置格式、声道数、采样率等参数
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    # 创建一个空列表用于存储录制的音频数据
    frames = []
    # 打印提示信息，表示开始录制
    print("Press 's' to start recording...")
    # 等待用户按下 's' 键开始录制
    keyboard.wait('s')
    # 打印提示信息，表示开始录制
    print("Recording...")
    # 开始录制
    while True:
        # 从音频流中读取 1024 个数据样本
        data = stream.read(1024)
        # 将数据添加到 frames 列表中
        frames.append(data)
        # 检查是否按下 'q' 键结束录制
        if keyboard.is_pressed('q'):
            break
    # 打印提示信息，表示录制已停止
    print("Recording stopped.")
    # 停止音频流
    stream.stop_stream()
    # 关闭音频流
    stream.close()
    # 终止 PyAudio 对象
    p.terminate()
    # 打开文件，以写入模式打开
    wf = wave.open(file_path, 'wb')
    # 设置音频的声道数、采样_width和采样率
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    # 将 frames 列表中的所有数据连接成一个字节串，并写入文件
    wf.writeframes(b''.join(frames))
    # 关闭文件
    wf.close()
    print("Done")


def send_message():
    """
    发送消息的函数，获取文本框内容，发送给ollama并处理回复和语音合成等后续逻辑
    """
    user_input = input_text.get("1.0", tk.END).strip()
    if user_input:
        # 获取ollama的回复内容
        ollama_reply = ollama_chat(user_input)
        print(f"米塔回复：{ollama_reply}")

        # 将聊天记录添加到历史记录列表
        conversation_history.append({"role": "user", "content": user_input})
        if ollama_reply:
            conversation_history.append({"role": "assistant", "content": ollama_reply})

        # 只对ollama返回的内容进行语音合成
        if ollama_reply:
            TTS_read(ollama_reply)

        # 清空输入框内容
        input_text.delete("1.0", tk.END)


def voice_input():
    """
    语音输入的函数，调用record_audio录制语音后进行语音识别等操作
    """
    file_path = "temp_audio.wav"
    record_audio(file_path)
    # 加载Whisper语音识别模型
    model = whisper.load_model("turbo")
    # 使用Whisper模型进行语音识别
    result = model.transcribe(file_path)
    user_input = result["text"]
    print("识别出的语音内容:", user_input)
    # 删除录制的音频文件
    if os.path.exists(file_path):
        os.remove(file_path)
    # 将识别的内容显示在文本框
    input_text.insert(tk.END, user_input)
    root.update()  # 强制更新界面，确保后续操作能正常进行
    ollama_reply = ollama_chat(user_input)
    root.update()  # 再次更新界面，防止后续操作出现阻塞界面无响应的情况
    print(f"米塔回复：{ollama_reply}")
    # 将聊天记录添加到历史记录列表
    conversation_history.append({"role": "user", "content": user_input})
    if ollama_reply:
        conversation_history.append({"role": "assistant", "content": ollama_reply})

    # 只对ollama返回的内容进行语音合成
    if ollama_reply:
        TTS_read(ollama_reply)


def play_video():
    """
    用于在界面上方的视频播放区域自动播放指定的视频文件（mita.mp4）并进行缩放和循环播放，以原视频的默认速度播放
    """
    cap = cv2.VideoCapture('./Scripts/Mita/mita.mp4')
    if not cap.isOpened():
        messagebox.showerror("错误", "无法打开视频文件")
        return
    video_frame = root.nametowidget('.!frame')
    canvas = tk.Canvas(video_frame, width=854, height=480)
    canvas.pack()

    # 获取视频的帧率信息
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        # 如果获取的帧率为0（可能出现异常情况），设置一个默认帧率，比如25帧每秒
        fps = 25
    frame_delay = 1 / fps

    prev_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            # 当视频播放到末尾，将视频读取位置重置到开头，实现循环播放
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
        frame = cv2.resize(frame, (854, 480))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        photo = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=photo, anchor=tk.NW)

        # 根据视频帧率控制帧显示间隔，精准控制视频播放速度
        current_time = time.time()
        if current_time - prev_time >= frame_delay:
            root.update()
            prev_time = current_time
            time.sleep(frame_delay)  # 增加这一行，让每一帧按照帧率间隔显示


if __name__ == '__main__':
    root = tk.Tk()
    root.title("与米塔聊天")

    # 使用grid布局管理器进行上下布局划分
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=1)
    root.columnconfigure(0, weight=1)

    # 上方单元格用于播放视频
    video_frame = tk.Frame(root, width=854, height=480, bg="black")
    video_frame.grid(row=0, column=0, sticky="nsew")

    # 下方单元格用于功能按钮和文本框等
    bottom_frame = tk.Frame(root, width=854, height=350, bg="gray")
    bottom_frame.grid(row=1, column=0, sticky="nsew")

    # 在下方单元格中创建文本输入框
    input_text = tk.Text(bottom_frame, height=5, width=50)
    input_text.pack(pady=10)

    # 创建发送按钮
    send_button = tk.Button(bottom_frame, text="发送", command=send_message)
    send_button.pack(pady=5)

    # 创建语音输入按钮
    voice_button = tk.Button(bottom_frame, text="语音输入", command=voice_input)
    voice_button.pack(pady=5)

    # 创建退出按钮
    exit_button = tk.Button(bottom_frame, text="退出", command=root.quit)
    exit_button.pack(pady=5)

    # 程序启动时自动播放视频
    play_video()

    root.mainloop()