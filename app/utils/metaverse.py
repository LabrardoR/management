import json
import logging

from sqlalchemy.sql.functions import current_timestamp

import requests
import hashlib
import time
import json

from app import config


def md5(s):
    s = s.encode("utf8")
    m = hashlib.md5()
    m.update(s)
    return m.hexdigest()
# 获取 token
str(md5(config.AccessKey + str(current_timestamp) + config.Secretkey))


# 获取 access_token 的函数
async def get_access_token():
    # 构造请求参数
    param = {
        "appId": "69wCg6iKHMGlcULLGahXIQT3",
        "grant_type": "sign",
        "timestamp": str(current_timestamp),
        "sign": str(md5(config.AccessKey + str(current_timestamp) + config.Secretkey))
    }
    # 发起请求
    request = requests.get("https://meta.guiji.ai/openapi/oauth/token", params=param)
    # 获取响应内容并解析
    response_content = request.content
    # 将字节数据转换为字符串
    response_str = response_content.decode('utf-8')
    # 解析 JSON 数据
    response_json = json.loads(response_str)
    # 提取 access_token
    if response_json.get('code') == "0" and response_json.get('data'):
        access_token = response_json['data']['access_token']
        return access_token
    else:
        # 如果没有返回成功或没有 access_token，处理错误
        raise Exception("获取token出现异常")

async def get_training_id(VIDEO_URL : str, name : str, token : str):
    """
    制作数字人
    """
    data = {
        "name" : name,
        "videoUrl" : VIDEO_URL,
        "level" : 1
    }
    # 查询 trainingId
    url = f"https://meta.guiji.ai/openapi/video/v2/create/training?access_token={token}"
    request_get_training_id = requests.post(url=url, json=data)
    # 检查响应是否成功
    if request_get_training_id.status_code == 200:
        # 解析 JSON 数据
        response_data = request_get_training_id.json()
        print("get_training_id:" + json.dumps(response_data, ensure_ascii=False))
        # 获取 trainingId
        if 'data' in response_data and 'trainingId' in response_data['data']:
            training_id = response_data['data']['trainingId']
            return training_id
        else:
            return -1
    else:
        logging.info(f"请求失败，状态码: {request_get_training_id.status_code}")

async def get_scene_id(trainingId : int, token : str):
    url = f"https://meta.guiji.ai/openapi/video/v2/training/get/{trainingId}?access_token={token}"
    request_get_scene_id = requests.get(url=url)
    if request_get_scene_id.status_code == 200:
        response_data = request_get_scene_id.json()
        if 'data' in response_data:
            id = response_data['data']['id']
            scene_id = response_data['data']['sceneId']
            createTime = response_data['data']['createTime']
            updateTime = response_data['data']['updateTime']
            coverUrl = response_data['data']['coverUrl']
            return { "trainingId" : id,
                     "sceneId" : scene_id,
                     "createTime" : createTime,
                     "updateTime" : updateTime,
                     "coverUrl" : coverUrl,
                     "token" : token
            }
        else:
            return -1
    else:
        logging.info(f"请求失败，状态码: {request_get_scene_id.status_code}")

async def get_video_id(AUDIO_URL : str, scene_id : int, token : str):
    params = {
        "access_token" : token
    }
    data = {
        "sceneId" : scene_id,
        "audioUrl" : AUDIO_URL
    }
    url = "https://meta.guiji.ai/openapi/video/v2/simpleCreate"
    request_get_video_id = requests.post(url=url, params=params, json=data)
    if request_get_video_id.status_code == 200:
        response_data = request_get_video_id.json()
        if 'data' in response_data and 'videoId' in response_data['data']:
            video_id = response_data['data']['videoId']
            return video_id
        else:
            return -1
    else:
        logging.info(f"请求失败，状态码: {request_get_video_id.status_code}")

async def get_download_url(videoId: int, token: str):
    """
    生成视频
    :param videoId:
    :param token:
    :return:
    """
    params = {
        "access_token": token
    }
    data = {
        "page": 1,
        "size": 100
    }
    # 发送 POST 请求
    url = "https://meta.guiji.ai/openapi/video/v2/pageList"
    request_get_download_url = requests.post(url=url, params=params, json=data)

    time.sleep(15)
    # 检查响应状态码
    if request_get_download_url.status_code == 200:
        response_data = request_get_download_url.json()

        # 响应数据中包含 `data` 和 `records` 字段
        if 'data' in response_data and 'records' in response_data['data']:
            records = response_data['data']['records']

            # 遍历 records 查找匹配的 videoId
            for record in records:
                if record.get('id') == int(videoId):  # 判断 id 是否匹配
                    video_url = record.get('videoUrl')  # 获取 videoUrl
                    if videoId:
                        return {
                            "videoId" : videoId,
                            "videoUrl" : video_url,
                            "createTime" : record.get('createTime'),
                            "updateTime" : record.get('updateTime')
                        }
                    else:
                        logging.info(f"videoId 为 {videoId} 的视频还在生成中或不存在，请稍后再试")
                        return -1
            logging.info(f"videoId 为 {videoId} 的视频还在生成中或不存在，请稍后再试")
            return None
        else:
            return None
    else:
        logging.error(f"请求失败，状态码: {request_get_download_url.status_code}")
        return None