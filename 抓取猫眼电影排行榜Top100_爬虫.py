import requests
import json
import re

'''
获取电影排名、电影海报链接、电影名称、主演、上映时间、评分
定义了4个函数：请求函数、解析函数、存储信息函数、启动函数
'''


# 请求函数
def get_one_page(url):
    # url：https://maoyan.com/board/4
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.43'
                      '24.190 Safari/537.36',
        'Cookie': '__mta=142572429.1612963581945.1614231069157.1614231095339.45; uuid_n_v=v1; _lxsdk_cuid=1778c1f0e9ec'
                  '8-013ed1e9a65a89-53e3566-1a298c-1778c1f0e9ec8; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __'
                  'mta=142572429.1612963581945.1613874763341.1614218852447.39; uuid=B9844FC0772A11EB963CF9FD0B38DF14EE'
                  '347FF799E847A68D738DFF95649E2C; _csrf=c50f07eeb26b93d472463d6c6dd3f46ef4f5cb74aea1451c94e3972d1cd3d0'
                  'de; lt=xNmIGxe8s5YlQRD-As0yhPsfLRsAAAAA5gwAAGSSnf_tge_NmUffi8ViVej8Nib1KxZjpf0JQCrOgNtOc7RLNNhCwyDt'
                  'p7DIUKJxwQ; lt.sig=ph-cgBTmiWkohdEWRGPINt7bQNA; uid=2979241370; uid.sig=b0zhcsmIn786qFOQvkAVQxy43xE;'
                  ' Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1613034161,1613874744,1614218850,1614231095; Hm_lpvt_703e94'
                  '591e87be68cc8da0da7cbd0be2=1614231095; _lxsdk=B9844FC0772A11EB963CF9FD0B38DF14EE347FF799E847A68D738'
                  'DFF95649E2C; _lxsdk_s=177d7ab5dd3-47a-af5-cc7%7C%7C5'
    }
    response = requests.get(url, headers=headers)
    html = response.text
    return html


# 解析函数
def parse_one_page(html):
    # 设定一个re正则表达式语句对象。方便以后随时调取。re.S修饰符,使点匹配换行符在内的所有字符
    template = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?<img.*?data-src="(.*?)".*?name.*?a.*?>(.*?)</a>.*?star.*?>'
                          '(.*?)</p>.*?releasetime.*?>(.*?)</p>.*?integer.*?>(.*?)</i>.*?fraction.*?>(.*?)</i>.*?</dd>',
                          re.S)
    # 使用re模块的findall()方法查询所有符合条件的数据，参数1是正则表达式，参数2是待匹配的文本
    items = re.findall(template, html)
    for item in items:
        yield {
            'index': item[0].strip(),
            'image': item[1].strip(),
            'title': item[2].strip(),
            'star': item[3].strip(),
            'time': item[4].strip(),
            'score': item[5].strip() + item[6].strip()
        }


# 存储信息函数（写入文件）
def write_file(item):
    with open('猫眼_电影信息.txt', 'a', encoding='utf-8') as f:
        # ensure_ascii=False：表示不按照ascii格式
        f.write(json.dumps(item, ensure_ascii=False)+'\n')


# 启动函数
def main(i):
    url = 'https://maoyan.com/board/4?offset=%d' % (i*10)
    html = get_one_page(url)
    for item in parse_one_page(html):
        write_file(item)


if __name__ == '__main__':
    # 进行多页提取使用
    for i in range(10):
        main(i)

