"""

"""

from fastapi import APIRouter, HTTPException, Depends, Request, Response
from app.config import SERVER_ADDRESS, SERVER_PORT
from app.utils.metaverse import get_access_token, get_training_id, get_scene_id, get_video_id, get_download_url

api_work = APIRouter()

@api_work.post("/make/{token}/{video_name}", description="制作数字人")
async def make_digital(file_name : str, token : str = Depends(get_access_token)):
    print("token:" + token)
    # todo 获取视频链接
    VIDEO_URL = "http://" + SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/video/" + file_name
    print("VIDEO_URL" + VIDEO_URL)
    trainingId = await get_training_id(VIDEO_URL, file_name, token)
    print("trainingId:" + str(trainingId))
    data = await get_scene_id(trainingId, token)
    return data

@api_work.get("/get_scene_id", description='如果调用"制作数字人"接口能正常返回trainingId，但sceneId==null，则是还在生成，可以等一分钟后传入trainingId调用该接口重新查询')
async def get_scene_id_again(trainingId, token : str = Depends(get_access_token)):
    data = await get_scene_id(trainingId, token)
    return data

@api_work.post("/make_video", description="AI生成视频")
async def make_video(audio_name : str, scene_id : int, token : str = Depends(get_access_token)):
    # 换成AUDIO_URL
    AUDIO_URL = "http://" + SERVER_ADDRESS + ":" + str(SERVER_PORT) + "/audio/" + audio_name
    print("AUDIO_URL" + AUDIO_URL)
    videoId = await get_video_id(AUDIO_URL, scene_id, token)
    print("videoId" + str(videoId))
    data = await get_download_url(videoId, token)
    return data

@api_work.get("/get_video_id", description='如果"AI生成视频"接口返回的downloadUrl==null，则可以等待一分钟后传入 videoId 调用该接口重新查询')
async def get_video_id_again(videoId : int, token : str = Depends(get_access_token)):
    data = await get_download_url(videoId, token)
    return data

