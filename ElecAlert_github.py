#!/user/bin/env python3
# -*- coding: utf-8 -*-
import os

import requests
from bs4 import BeautifulSoup
import re

power_Get: float = 0.0
sysID = os.environ.get("SYS_ID")
roomID = os.environ.get("ROOM_ID")
areaID = os.environ.get("AREA_ID")
buildID = os.environ.get("BUILD_ID")
wxPushID = os.environ.get("WXPUSH_ID")
appToken = os.environ.get("APP_TOKEN")

def get_eleresult(sysid, roomid, areaid, buildid):
    url = 'http://epay.sues.edu.cn/epay/wxpage/wanxiao/eleresult?sysid={0}&roomid={1}&areaid={2}&buildid={3}'.format(
        sysid, roomid, areaid, buildid)
    # requests.packages.urllib3.disable_warnings()

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}

    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    # print(soup.prettify()) #打印网页内容

    result = soup.find_all("input", class_="weui-input")
    res_str = str(result)
    res = re.findall(r'left-degree="(.+?)"', res_str)
    item = ''.join(res)
    res_float = float(item)
    return res_float


def wx_push(power, ID, app_token):
    if power <= 15.0:
        content = ("请尽快充值！剩余电量：{0}度".format(power))
    else:
        content = ("剩余电量：{0}度".format(power))
    headers = {"content-type": "application/json"}
    webapi = 'https://wxpusher.zjiecode.com/api/send/message'
    data = {
        "appToken": app_token,
        "content": content,  # 主体内容
        "contentType": 1,  # 文本
        "topicIds": [ID],  # 应用列表的ID
    }
    result = requests.post(url=webapi, json=data, headers=headers)
    return result.text



if __name__ == '__main__':
    while True:
        try:
            # 获取电量
            power_Get = get_eleresult(sysID, roomID, areaID, buildID)
            # 推送电量
            wx_push(power_Get, wxPushID, app_token)
        except:
            print("<error>网络异常")
            pass
