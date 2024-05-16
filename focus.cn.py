# coding=utf-8

import requests
from lxml import etree
import re
import json
import pandas as pd
import openpyxl

from dao_file import save_to_json
from dao_mongo import connect_mongodb, query_coll_with_field, query_coll_all, query_coll_with_like
from get_news import get_page_news

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


def parse_daily_title_data(page):
    """
    解析周交易数据
    :param title:
    :return:
    """

    title = page['title']
    publish = page['publishTimeForShow']
    # 创建一个空字典
    daily_object = {}
    # 使用正则表达式匹配所需的变量
    # 【杭州成交日报】03月26日新房成交275套、二手房288套;涨价房源108套
    match = re.search(r"【杭州成交日报】(\d+)月(\d+)日新房成交(\d+)套、二手房(\d+)套;涨价房源(\d+)套", title)
    if match:
        month = match.group(1)
        day = match.group(2)
        new = match.group(3)
        resold = match.group(4)
        rise = match.group(5)
        daily_object['month'] = month
        daily_object['day'] = day
        daily_object['new'] = new
        daily_object['resold'] = resold
        daily_object['rise'] = rise
        # print(f"N【杭州成交周报】第{week}周新房成交{new}套,二手房{resold}套,涨价房源{rise}套")
    else:
        print(f"No match found at {publish}  {title}")
    return daily_object


def parse_daily_pages(pages):
    """
    从列表中找出需要的数据存入daily_list列表
    :param pages:
    :return:
    """

    daily_list = []
    for page in pages:
        daily_data = parse_daily_title_data(page)
        daily_list.append(daily_data)
        # print(page)
    return daily_list


def get_daily_data(db):
    """
    获取日数据并生成Excel
    :param db:
    :return:
    """
    # cursor = query_coll_with_field(db, 'page_info', 'citySuffix', 'hz')
    result_condition = {'_id': 0, 'citySuffix': 1, 'url': 1, 'title': 1, 'publishTimeForShow': 1}
    pages = query_coll_with_like(db, 'page_info', 'title', '【杭州成交日报】', result_condition)

    daily_list = parse_daily_pages(pages)

    # 存入Excel
    # months = []
    # days = []
    # news = []
    # resolds = []
    # rises = []
    # for item in daily_list:
    #     if item:
    #         months.append(item['month'])
    #         days.append(item['day'])
    #         news.append(item['new'])
    #         resolds.append(item['resold'])
    #         rises.append(item['rise'])
    # df_week = pd.DataFrame(
    #     dict(zip(['月', '日', '新房成交', '二手房成交', '涨价房源'],
    #              [months, days, news, resolds, rises])))
    # df_week.to_excel(f'杭州成交日报.xlsx', index=False)
    print('generation finished')


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    # mongodb连接
    db = connect_mongodb("192.168.0.188", "real_estate", "root", "123456")
    # get_page_news(db)
    # get_week_data(db)
    get_daily_data(db)
    pass
