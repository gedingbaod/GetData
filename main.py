# coding=utf-8

import requests
from lxml import etree
import re
import json
import pandas as pd
import openpyxl

# cookies = {
#     'lianjia_uuid': 'd63243c2-9abd-4016-a428-7272d9bd4265',
#     'crosSdkDT2019DeviceId': '-5xmwrm-pv43pu-kiaob2z7e31vj11-vs7ndc7b3',
#     'select_city': '330100',
#     'digv_extends': '%7B%22utmTrackId%22%3A%22%22%7D',
#     'ke_uuid': 'bac7de379105ba27d257312d20f54a59',
#     'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22%24device_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
#     'lianjia_ssid': '6734443f-a11a-49c9-989e-8c5d2dc51185',
# }
cookies = {
    'lianjia_uuid': '8dd65417-0231-1910-0de0-1bf752948fa1',
    'Lianjia-Device-Id': 'db8e9d53-7a1d-4a96-969c-6f83f6ecb8d7',
    'select_city': '330100',
    'digv_extends': '%7B%22utmTrackId%22%3A%22%22%7D',
    'ke_uuid': 'bac7de379105ba27d257312d20f54a59',
    'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22%24device_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D',
    'lianjia_ssid': 'bdb8db76-c245-453c-95fb-c417a8bdc58a',
}


headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    # 'Cookie': 'lianjia_uuid=d63243c2-9abd-4016-a428-7272d9bd4265; crosSdkDT2019DeviceId=-5xmwrm-pv43pu-kiaob2z7e31vj11-vs7ndc7b3; select_city=330100; digv_extends=%7B%22utmTrackId%22%3A%22%22%7D; ke_uuid=bac7de379105ba27d257312d20f54a59; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22%24device_id%22%3A%2218a8d4f86e46b6-0a2c26d29b1766-4f641677-2073600-18a8d4f86e5f7e%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D; lianjia_ssid=6734443f-a11a-49c9-989e-8c5d2dc51185',
    'Referer': 'https://hz.ke.com/ershoufang/pg2/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
}

# get area name and route
def getAreasInfo(city):
    responseinit = requests.get(
        f'https://{city}.ke.com/ershoufang', cookies=cookies, headers=headers)
    html_text_init = etree.HTML(responseinit.text)
    districts = [z for z in zip(html_text_init.xpath('//a[@class=" CLICKDATA"]/text()'),
                                html_text_init.xpath('//a[@class=" CLICKDATA"]/@href'))]
    return districts


# get page data
def getSinglePageInfo(city, areaname, pathname):
    response1 = requests.get(
        f'https://{city}.ke.com{pathname}pg1/', cookies=cookies, headers=headers)
    html_text1 = etree.HTML(response1.text)
    # get page sum
    pageInfo = html_text1.xpath(
        '//div[@class="page-box house-lst-page-box"]/@page-data')

    # 数据较多，可以先设置2页，看看是否可以导出
    # pageTotal = json.loads(pageInfo[0])['totalPage']
    pageTotal = 2

    title = []
    position = []
    house = []
    follow = []
    totalPrice = []
    unitPrice = []
    url = []

    for i in range(1, pageTotal + 1):
        response = requests.get(
            f'https://{city}.ke.com{pathname}pg{i}/', cookies=cookies, headers=headers)
        html_text = etree.HTML(response.text)
        ullist = html_text.xpath(
            '//ul[@class="sellListContent"]//li[@class="clear"]')
        for li in ullist:
            liChildren = li.getchildren()[1]
            # 名称
            title.append(liChildren.xpath('./div[@class="title"]/a/text()')[0])
            # url 地址
            url.append(liChildren.xpath('./div[@class="title"]/a/@href')[0])
            # 小区名称
            position.append(liChildren.xpath(
                './div/div/div[@class="positionInfo"]/a/text()')[0])
            # 房屋信息
            houselis = liChildren.xpath(
                './div/div[@class="houseInfo"]/text()')
            house.append([x.replace('\n', '').replace(' ', '')
                          for x in houselis][1])
            # 上传时间
            followlis = liChildren.xpath(
                './div/div[@class="followInfo"]/text()')
            follow.append([x.replace('\n', '').replace(' ', '')
                           for x in followlis][1])
            # 总价
            totalPrice.append(liChildren.xpath(
                './div/div[@class="priceInfo"]/div[@class="totalPrice totalPrice2"]/span/text()')[0].strip())
            # 单价
            unitPrice.append(liChildren.xpath(
                './div/div[@class="priceInfo"]/div[@class="unitPrice"]/span/text()')[0].replace('元/平', ""))

    return pd.DataFrame(
        dict(zip(['行政区域', '名称', '小区名', '房屋信息', '发布时间', '总价（万）', '单价（元/平）', '地址'],
                 [areaname, title, position, house, follow, totalPrice, unitPrice, url])))


def getSalesData(city):
    districts = getAreasInfo(city)
    dfInfos = pd.DataFrame()
    for district in districts:
        dfInfo = getSinglePageInfo(city, district[0], district[1])
        dfInfos = pd.concat([dfInfos, dfInfo], axis=0)
    dfInfos.to_excel(f'{city}二手房销售数据.xlsx', index=False)
    print('generation finished')

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    getSalesData('hz')
    pass
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
