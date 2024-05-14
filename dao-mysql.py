# -*-coding:utf-8-*-
import mysql.connector
from mysql.connector import Error


def create_server_connection(host_name, user_name, user_password, db_name):
    """
    创建到MySQL服务器的连接
    :param host_name: MySQL服务器地址
    :param user_name: 数据库用户名
    :param user_password: 用户密码
    :param db_name: 要连接的数据库名称
    :return: 连接对象或None(如果连接失败)
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print('成功连接MySQL数据库')
    except Error as e:
        print(f'连接失败: {e}')

    return connection


def execute_query(connection, query):
    '''
    执行SQL查询并返回结果
    :param connection: 数据库连接对象
    :param query: 要执行的SQL查询语句
    :return: 查询结果集
    '''
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        print('查询成功')
    except Error as e:
        print(f'查询失败: {e}')
    finally:
        cursor.close()
    return result


def main():
    # 请根据实际情况替换以下信息
    host = '192.168.2.152'
    user = 'lapis'
    password = '123456'
    database = 'real_estate'

    # 创建数据库连接
    conn = create_server_connection(host, user, password, database)

    if conn is not None:
        # 示例查询：获取某个表的所有数据，这里以一个假设的表名为example
        query = 'SELECT * FROM example'
        results = execute_query(conn, query)

        # 打印查询结果，根据实际需求处理这些数据
        for row in results:
            print(row)

        # 关闭数据库连接
        conn.close()
    else:
        print('无法创建数据库连接')


if __name__ == '__main__':
    main()
