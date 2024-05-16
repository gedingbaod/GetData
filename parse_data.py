# -*-coding:utf-8-*-
import requests
from lxml import etree

from dao_mongo import query_coll_with_like




def parse_week_title_data(title):
    """
    解析周交易数据
    :param title:
    :return:
    """
    # 创建一个空字典
    week_object = {}
    # 使用正则表达式匹配所需的变量
    match = re.search(r"【杭州成交周报】第(\d+)周新房成交(\d+)套,二手房(\d+)套,涨价房源(\d+)套", title)
    if match:
        week = match.group(1)
        new = match.group(2)
        resold = match.group(3)
        rise = match.group(4)
        week_object['week'] = week
        week_object['new'] = new
        week_object['resold'] = resold
        week_object['rise'] = rise
        # print(f"N【杭州成交周报】第{week}周新房成交{new}套,二手房{resold}套,涨价房源{rise}套")
    else:
        print("No match found.")
    return week_object


def parse_week_pages(pages):
    """
    从列表中找出需要的数据存入weekList列表
    :param pages:
    :return:
    """
    week_list = []
    for page in pages:
        week_data = parse_week_title_data(page['title'])
        week_list.append(week_data)
        # print(page)
    return week_list


def get_week_data(db):
    """
    获取星期数据并生成Excel
    :param db:
    :return:
    """
    # cursor = query_coll_with_field(db, 'page_info', 'citySuffix', 'hz')
    result_condition = {'_id': 0, 'citySuffix': 1, 'url': 1, 'title': 1}
    pages = query_coll_with_like(db, 'page_info', 'title', '【杭州成交周报】', result_condition)

    week_list = parse_week_pages(pages)

    # 存入Excel
    weeks = []
    news = []
    resolds = []
    rises = []
    for item in week_list:
        if item:
            weeks.append(item['week'])
            news.append(item['new'])
            resolds.append(item['resold'])
            rises.append(item['rise'])
    df_week = pd.DataFrame(
            dict(zip(['第周', '新房成交', '二手房成交', '涨价房源'],
                     [weeks, news, resolds, rises])))
    df_week.to_excel(f'杭州成交周报.xlsx', index=False)
    print('generation finished')

