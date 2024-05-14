# coding=utf-8

import requests
from lxml import etree
import re
import json
import pandas as pd
import openpyxl

from repository import save_to_json

cookies = {
    '87a4bcbf0b1ea517_gr_session_id': '0424be0b-0f5c-4007-9f04-edc8377b6a08',
    '87a4bcbf0b1ea517_gr_session_id_sent_vst': '0424be0b-0f5c-4007-9f04-edc8377b6a08',
    'SUV': '17155902561318cra87',
    'city_short_code': 'hz',
    'cld': '20240513165056',
    'clt': '1715590256',
    'focus_city_c': '330100',
    'focus_city_p': 'hz',
    'focus_city_s': 'hz',
    'focus_pc_city_p': 'hz',
    'focus_wap_city_p': 'hz',
    'gr_user_id': '64762c19-e241-49a7-a0de-6db7922c9a84',
    'vt_shjdpc_channel_321': 1,

}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    # 'Cookie': 'lianjia_uuid=d63243c2-9abd-4016-a428-7272d9bd4265; crosSdkDT2019DeviceId=-5xmwrm-pv43pu-kiaob2z7e31vj11-vs7ndc7b3; select_city=330100; digv_extends=%7B%22utmTrackId%22%3A%22%22%7D; ke_uuid=bac7de379105ba27d257312d20f54a59; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22%24device_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lianjia_ssid=6734443f-a11a-49c9-989e-8c5d2dc51185',
    'Referer': 'https://m.focus.cn/author/99000193248/newslist',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


# get area name and route
def getPageInfo(page):
    url = f'https://graphql.focus.cn/alias/query?name=/baseApi/authorNewsList&param=uid%3D99000193248%26pageNo%3D{page}&graphProjectId=7'
    response = requests.get(url)

    if response.status_code == 200:
        # 获取JSON数据
        data = response.json()
        return data
        # 现在可以解析和使用data变量中的JSON数据
    else:
        print(f'Failed to retrieve data: {response.status_code}')


def getWeekData(word):
    # 1.获取json数据，并入pageList列表
    pageList = []
    for i in range(1, 2):
        data = getPageInfo(i)
        pageList.extend(data['data']['userDetails']['newsListByAuthorUid']['list'])

    # 这里先把数据存到本地，这样下次就不用再请求了
    save_to_json(pageList)


    # 1.从列表中找出需要的数据存入weekList列表
    weekList = []
    dfInfos = pd.DataFrame()
    for item in pageList:
        title = item['title']
        if word in title:
            weekList.append(item)

    # 3.获取url中对应的数据

    print(weekList)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    getWeekData('杭州成交周报')
    pass
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
