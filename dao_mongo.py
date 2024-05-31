# coding:utf-8
from pymongo import MongoClient


# # 连接到MongoDB，这里假设您的MongoDB服务运行在本地，默认端口为27017
# client = MongoClient('192.168.0.188', 27017)
# # 连接系统默认数据库admin
# db = client['real_estate']
# # 连接数据库,账号密码认证，需要在real_estate数据库中创建User：root
# db.authenticate('root', '123456')
# # 选择或创建一个数据库，例如'demo_db'
# db = client['real_estate']

def connect_mongodb(host, db, user, password):
    # 连接到MongoDB，这里假设您的MongoDB服务运行在本地，默认端口为27017
    client = MongoClient(host, 27017)
    # 连接系统默认数据库admin
    db = client[db]
    # 连接数据库,账号密码认证，需要在real_estate数据库中创建User：root
    db.authenticate(user, password)
    return db


def save_to_collection_batch(db, coll_name, page_list):
    collection = db[coll_name]
    results = collection.insert_many(page_list)
    print(f'Inserted document ID: {results.inserted_ids}')


def save_to_collection(db, coll_name, page_list):
    collection = db[coll_name]
    for item in page_list:
        result = collection.insert_one(item)
        print(f'Inserted document ID: {result.inserted_id}')


def query_coll_all(db, coll_name):
    """
    返回cursor
    可以通过list获取集合：docs = list(cursor)
    或者使用 for item in cursor遍历
    """
    collection = db[coll_name]
    cursor = collection.find()
    return cursor


def query_coll_with_field(db, coll_name, field_name, field_value, result_condition):
    """
    返回查询结果
    """
    collection = db[coll_name]
    query = {field_name: field_value}
    # 如果指定返回字段
    if result_condition:
        cursor = collection.find(query, result_condition)
    else:
        cursor = collection.find(query)
    return cursor


def query_coll_with_like(db, coll_name, field_name, field_value, result_condition=None, sort_field=None, sort_asc=None):
    """
    返回cursor
    可以通过list获取集合：docs = list(cursor)
    或者使用 for item in cursor遍历
    """
    collection = db[coll_name]
    query = {field_name: {'$regex': field_value}}
    # 如果指定返回字段
    if result_condition:
        if sort_field:
            cursor = collection.find(query, result_condition).sort(sort_field, sort_asc)
        else:
            cursor = collection.find(query, result_condition)
    else:
        cursor = collection.find(query)
        # .sort('publishTimeForShow', 1)
    pages = list(cursor)
    return pages

# # 查询文档
# query = {'username': 'example_user'}
# found_user = collection.find_one(query)
# if found_user:
#     print('Found user:')
#     print(found_user)
# else:
#     print('User not found.')
