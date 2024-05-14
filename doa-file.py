import json

def save_to_json(data, filename='data.json'):
    """
    将Python对象保存为JSON文件。

    参数:
    data (dict): 要保存的数据，通常是一个字典。
    filename (str): JSON文件的名称，默认为'data.json'。
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f'数据已成功保存到{filename}')
    except Exception as e:
        print(f'保存数据时发生错误: {e}')

# 示例数据
example_data = {
    'name': '张三',
    'age': 30,
    'city': '北京'
}


def read_from_json(filename='data.json'):
    """
    从JSON文件读取数据并返回Python对象。

    参数:
    filename (str): JSON文件的名称，默认为'data.json'。

    返回:
    dict: 从JSON文件读取的数据。
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f'文件{filename}未找到。')
        return None
    except Exception as e:
        print(f'读取数据时发生错误: {e}')
        return None