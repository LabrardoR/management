import json

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
def get_access_token():

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

