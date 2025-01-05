#coding=utf-8
'''
requires Python 3.6 or later
pip install requests
pip install pydub
pip install pyaudio
pip install tempfile
'''
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

    try:
        response = requests.post(
            base_url,
            json=data,
            headers={'Content-Type': 'application/json'}
        )
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
                # 创建临时文件并获取文件对象和文件路径
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
    file_path (str)：音频文件的保存路径

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
    # 设置音频的声道数、采样宽度和采样率
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    # 将 frames 列表中的所有数据连接成一个字节串，并写入文件
    wf.writeframes(b''.join(frames))
    # 关闭文件
    wf.close()
    print("Done")


if __name__ == '__main__':
    while True:
        input_type = input("请选择输入方式（1.打字 2.麦克风）：")
        if input_type == "1":
            user_input = input("请输入你想和米塔聊的内容（输入 'exit' 可退出聊天）：")
        elif input_type == "2":
            file_path = "temp_audio.wav"
            record_audio(file_path)
            # 加载Whisper语音识别模型
            model = whisper.load_model("turbo")
            # 使用Whisper模型进行语音识别
            result = model.transcribe(file_path)
            user_input = result["text"]
            # 删除录制的音频文件
            if os.path.exists(file_path):
                os.remove(file_path)
        else:
            print("输入方式选择错误，请重新输入。")
            continue

        if user_input.lower() == "exit":
            print("已退出聊天，感谢使用！")
            break

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

        # 每轮循环结束后等待2秒，避免请求过于频繁，可根据实际情况调整时间长短
        time.sleep(2)