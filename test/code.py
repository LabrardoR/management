
"""
榛子云验证码平台
"""
import requests


apiUrl = "http://sms_developer.zhenzikj.com/sms/send.do" # apiUrl
appId = "113981" # 应用id
appSecret = "fc81cd45-08a3-4086-bf38-3103207ab9c6" # 应用secret
templateId = "13031" # 模板id
invalidTimer = "2" # 失效时间


def send_code(telephone_number, code):
    data = {'appId' : appId, 'appSecret': appSecret, 'templateId': templateId, 'number': telephone_number, 'templateParams': [code, invalidTimer]}
    request = requests.post(apiUrl, data=data)
    print(request.text)
if __name__ == '__main__':
    send_code("19254707730", "241242")
