
import base64
import os
import requests
import json
import uuid

host = "https://openspeech.bytedance.com"


def train(appid, token, audio_path, spk_id):
    url = host + "/api/v1/mega_tts/audio/upload"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer;" + token,
        "Resource-Id": "volc.megatts.voiceclone",
    }
    encoded_data, audio_format = encode_audio_file(audio_path)
    print("encoded_data = ", encoded_data)
    print("audio_format = ", audio_format)

    audios = [{"audio_bytes": encoded_data, "audio_format": audio_format}]
    data = {
        "appid": appid, 
        "speaker_id": spk_id, 
        "audios": audios, 
        "source": 2,
        "language": 0, 
        "model_type": 1
    }
    response = requests.post(url, json=data, headers=headers)
    print("status code = ", response.status_code)
    if response.status_code != 200:
        raise Exception("train请求错误:" + response.text)
    print("headers = ", response.headers)
    print(response.json())


def get_status(appid, token, spk_id):
    url = host + "/api/v1/mega_tts/status"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer;" + token,
        "Resource-Id": "volc.megatts.voiceclone",
    }
    body = {"appid": appid, "speaker_id": spk_id}
    response = requests.post(url, headers=headers, json=body)
    print(response.json())


def encode_audio_file(file_path):
    with open(file_path, mode='rb') as audio_file:
        audio_data = audio_file.read()
        encoded_data = str(base64.b64encode(audio_data), "utf-8")
        audio_format = os.path.splitext(file_path)[1][1:]  # 获取文件扩展名作为音频格式
        return encoded_data, audio_format
    


async def get_train_vocie_result(new_name, audio_path, generate_text):
    appid = "3386087976"
    token = "qLmw6MKMRQdDHnKi5vbz3ovzpFxLnfet"
    spk_id = "S_FoLCsYid1"
    cluster = "volcano_icl"
    voice_type = "S_FoLCsYid1"
    host = "openspeech.bytedance.com"
    api_url = f"https://{host}/api/v1/tts"
    header = {"Authorization": f"Bearer;{token}"}
    
    tts_request_json = {
        "app": {
            "appid": appid,
            "token": token,
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
            "text": generate_text,
            "text_type": "plain",
            "operation": "query",
            "with_frontend": 1,
            "frontend_type": "unitTson"

        }
    }
    # 训练
    print(audio_path)
    train(appid=appid, token=token, audio_path=audio_path, spk_id=spk_id)
    get_status(appid=appid, token=token, spk_id=spk_id)
    # 生成声音
    try:
        resp = requests.post(api_url, json.dumps(tts_request_json), headers=header)
        if not os.path.exists("generate_video"):
            os.makedirs("generate_video")
        if "data" in resp.json():
            data = resp.json()["data"]
            file_to_save = open(f"./generate_audio/{new_name}.mp3", "wb")
            file_to_save.write(base64.b64decode(data))
        return 1
    except Exception as e:
        e.with_traceback()



    