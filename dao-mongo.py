# coding:utf-8
from pymongo import MongoClient

# 连接到MongoDB，这里假设您的MongoDB服务运行在本地，默认端口为27017
client = MongoClient('192.168.0.188', 27017)
# 连接数据库,账号密码认证
db = client.admin    # 连接系统默认数据库admin

# 选择或创建一个数据库，例如'demo_db'
db = client['demo_db']

# 在数据库中创建或选择一个集合（类似SQL中的表），例如'users'
collection = db['users']

# 插入一个文档（数据记录）
user_document = {
    'username': 'example_user',
    'email': 'example@example.com',
    'created_at': '2023-04-01T12:00:00Z'
}
result = collection.insert_one(user_document)
print(f'Inserted document ID: {result.inserted_id}')

# 查询文档
query = {'username': 'example_user'}
found_user = collection.find_one(query)
if found_user:
    print('Found user:')
    print(found_user)
else:
    print('User not found.')