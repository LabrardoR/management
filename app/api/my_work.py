# """
# 我的作品接口接口
# """
# import datetime
# import os
# import logging
# from asyncio import sleep
#
# from fastapi import APIRouter, HTTPException, Depends, Request, Response, UploadFile, File
# from tortoise.exceptions import IntegrityError
#
# from app.api.api_test import upload_video
# from app.config import SERVER_ADDRESS
# from app.models.user import User
# from app.schemas.my_work import CreateCharacterRequest
# from app.schemas.user import UserRegister, UserCodeLogin, UserPasswordLogin, UserReset, UserResponse, UserUpdate
#
# import hashlib
# import random
# import re
# import requests
# from app.utils.metaverse import get_access_token, get_training_id, get_scene_id, get_video_id, get_download_url
#
# api_work = APIRouter()
#
# @api_work.post("/create_character", description="选择video和audio，输入名字后，开始制作")
# async def create_character(create_character_request : CreateCharacterRequest, token : str = Depends(get_access_token)):
#     print("token:" + token)
#
#     # 3.30数字人训练
#     audio_name = create_character_request.audio_name
#     video_name = create_character_request.video_name
#     name = create_character_request.name
#     VIDEO_URL = SERVER_ADDRESS + "/video/" +video_name
#     AUDIO_URL = SERVER_ADDRESS + "/audio/" +audio_name
#
#     VIDEO_URL_TEST = "https://fyztagi.com/assets/video-eg2-DQhBVWBb.mp4"
#     AUDIO_URL_TEST = "https://uy.wzznft.com/i/2024/12/17/ncbsoi.mp3"
#
#     # 3.30数字人训练接口 -> 获取 trainingId
#     trainingId = await get_training_id(VIDEO_URL_TEST, name, token)
#     print("trainingId: " + str(trainingId))
#
#     # 3.15训练任务信息查询 -> 获取 sceneId
#     sceneId = await get_scene_id(trainingId, token)
#     print("sceneId: " + sceneId)
#
#     # 3.31极速克隆视频合成 -> 获取 videoId
#     videoId = await get_video_id(AUDIO_URL_TEST, sceneId, token)
#     print("videoId: " + videoId)
#
#     # 3.9 查询合成视频作品列表 -> 获取合成的视频下载链接
#     download_url = await get_download_url(videoId, token)
#     print("download_url: " + download_url)
#
#
# @api_work.post("/create_video", description="用数字人ID(场景ID)+声音生成视频")
# async def create_video(scene_id : int, audio_name : str, token = Depends(get_access_token)):
#     AUDIO_URL = SERVER_ADDRESS + "/audio/" + audio_name
#     AUDIO_URL_TEST = "https://uy.wzznft.com/i/2024/12/17/ncbsoi.mp3"
#     video_id = await get_video_id(AUDIO_URL_TEST, scene_id, token)
#     await get_download_url(video_id, token)
