import re

import requests

if __name__ == '__main__':
    print("开始运行")

    session = requests.session()

    url = "http://127.0.0.1"
    indexUrl = "http://127.0.0.1"
    response = session.get(url)

    # 正则提取csrf
    matchObj = re.match('.*?_csrf" value="(.*?)">', response.text, re.S)

    _csrf = None
    if matchObj:
        print("_csrf", matchObj.group(1))
        _csrf = matchObj.group(1)
    else:
        print("No match!!")
        exit(0)

    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " \
                "Chrome/86.0.4240.183 Safari/537.36 "

    header = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
    }

    postData = {
        "_csrf": _csrf,
        "username": "admin",
        "password": "",
    }

    response = session.post(url, postData, headers=header)
    print(response.text)

    response = session.get(indexUrl)
    print(response.text)
