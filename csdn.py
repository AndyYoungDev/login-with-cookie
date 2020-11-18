import json
import os
import re
import time

import qrcode
import requests

if __name__ == '__main__':
    print("开始运行")

    session = requests.session()

    qrcodeUrl = "https://passport.csdn.net/v1/api/app/scan/createAppScan"
    commonHeader = {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/86.0.4240.183 Safari/537.36 "
    }
    # 先访问首页获取cookie，获取二维码要用到
    session.get("https://passport.csdn.net/login?code=public", headers=commonHeader)
    # 获取二维码登录
    response = session.post("https://passport.csdn.net/v1/api/app/scan/createAppScan", headers=commonHeader)
    # 二维码地址 token
    loginDic = json.loads(response.text)
    qrcodeScanUrl = loginDic['data']['url']
    qrcodeScanToken = loginDic['data']['token']
    # 生成二维码
    img = qrcode.make(qrcodeScanUrl)
    img.save("./tmp/csdn.png")
    # 打开二维码扫码
    os.startfile(os.path.dirname(os.path.abspath(__file__)) + "/tmp/csdn.png")
    # 构造请求json
    tmpFilePath = "./tmp"
    fileHandle = open(tmpFilePath + "/csdn.txt", "r")
    webJson = fileHandle.read()
    webJson = json.loads(webJson)
    webJson['token'] = qrcodeScanToken
    webJson = json.dumps(webJson)

    requestHeader = {
        "content-type": "application/json;charset=UTF-8",
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/86.0.4240.183 Safari/537.36 "
    }
    while True:
        response = session.post(url="https://passport.csdn.net/v1/api/app/scan/webRefreshToken", data=webJson,
                                headers=requestHeader)
        print(response.text)
        time.sleep(2)
        # 1已扫码 2已登录
        resJson = json.loads(response.text)
        if resJson['data']['code'] == 2:
            print("登录成功，退出循环")
            break
