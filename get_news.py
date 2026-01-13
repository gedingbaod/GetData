# -*-coding:utf-8-*-
import requests
import json
from lxml import etree

from dao_mongo import save_to_collection, save_to_collection_batch

"""
根据API接口获取json数据，并存入mongodb中
数据包含各省的交易日报以及周报
"""


# get area name and route
def get_page_info(page):
    url = f'https://graphql.focus.cn/alias/query?name=/baseApi/authorNewsList&param=uid%3D99000193248%26pageNo%3D{page}&graphProjectId=7'
    response = requests.get(url)

    if response.status_code == 200:
        # 获取JSON数据
        data = response.json()
        return data
        # 现在可以解析和使用data变量中的JSON数据
    else:
        print(f'Failed to retrieve data: {response.status_code}')


def get_api_info(url):
    """
    从API中获取JSON护具
    :param url:
    :return:
    """
    url = 'https:' + url
    response = requests.get(url)
    if response.status_code == 200:
        html_text1 = etree.HTML(response.text)
        # 获取JSON数据
        data = response.json()
        return data
        # 现在可以解析和使用data变量中的JSON数据
    else:
        print(f'Failed to retrieve data: {response.status_code}')


def get_page_news(db):
    # 1.获取json数据，并入pageList列表
    page_list = []
    # 20240514时间点共1369页
    # 20240531时间点共42页
    # 20240815时间点共1595页
    # 20260102时间点共2412页
    for i in range(3, 5):
        data = get_page_info(i)
        page_list.extend(data['data']['userDetails']['newsListByAuthorUid']['list'])

    # 单个存入数据库中，可以保证循序插入
    save_to_collection(db, 'page_info', page_list)
    # 批量存入数据库中
    #save_to_collection_batch(db, 'page_info', page_list)
