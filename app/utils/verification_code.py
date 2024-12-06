"""
榛子云验证码平台
"""
import requests
import zhenzismsclient as smsclient


apiUrl = "https://sms_developer.zhenzikj.com" # apiUrl
appId = "113981" # 应用id
appSecret = "fc81cd45-08a3-4086-bf38-3103207ab9c6" # 应用secret
templateId = "13097" # 模板id
invalidTimer = "2" # 失效时间


async def send_code(telephone_number, code):
    client = smsclient.ZhenziSmsClient(apiUrl, appId, appSecret)
    params = {'number': '15104927730', 'templateId': '1', 'templateParams': ['9988', '15分钟']}
    print(client.send(params))
