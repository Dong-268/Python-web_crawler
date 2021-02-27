# coding: utf-8
import os
import requests
from hashlib import md5
from urllib.parse import urlencode


# 请求函数
def one_page(url, offset, keyword):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.43'
                      '24.190 Safari/537.36'
    }
    # 一些必要参数
    parameter = {
        'aid': 24,
        'app_name': 'web_search',
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
    }
    # 使用urlencode()方法构造请求参数，然后和url拼接
    new_url = url+urlencode(parameter)
    response = requests.get(new_url, headers=headers)
    try:
        if response.status_code == 200:
            return response.json()
        else:
            print('status_code：', response.status_code, 'url：', url)
    # ConnectionError：未知服务器错误
    except requests.ConnectionError:
        return None


# 解析函数
def parse_page(json):
    if json.get('data'):
        items = json.get('data')
        for item in items:
            title = item.get('title')
            image_list = item.get('image_list')
            if title and image_list:
                yield {
                    'title': title,
                    'image_list': image_list
                }
    else:
        print('无法获取数据')


# 持久化存储函数
def save_file(item):
    # 判断当前路径下是否存在以title命名的文件夹
    if not os.path.exists(item['title']):
        # 创建以title命名的文件夹
        os.mkdir(item['title'])
        try:
            for image in item['image_list']:
                response = requests.get(image['url'])
                # md5(response.content).hexdigest()： 将response.content通过md5加密，然后转换为16进制的字符串
                file_path = "{}/{}.jpg".format(item['title'], md5(response.content).hexdigest())
                with open(file_path, 'wb') as f:
                    f.write(response.content)
        except requests.ConnectionError:
            return None
    else:
        print('数据已经保存')


if __name__ == '__main__':
    key_word = input('请输入关键词 >>>')
    web_url = 'https://www.toutiao.com/api/search/content/?'
    json_data = one_page(web_url, 0, key_word)
    for i in parse_page(json_data):
        save_file(i)

    # for index in range(10):
    #     json_data = one_page(web_url, index*10, key_word)
    #     for i in parse_page(json_data):
    #         save_file(i)

