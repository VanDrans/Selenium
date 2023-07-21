# 导入所需模块
import requests
from bs4 import BeautifulSoup

# 传入请求头里的信息，将爬虫伪装成浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 Edg/114.0.1823.82',
    'Referer': 'https://www.toutiao.com/?wid=1633679184428'
}

# 将API链接的查询字符串传给Params参数（为了使URL看起来更整洁）
params = {
    'origin': 'toutiao_pc',
    '_signature': '_02B4Z6wo00d01S2y5jAAAIDCeDBtryaVlW0tluKAAC.Xbf'
}
res = requests.get('https://www.toutiao.com/hot-event/hot-board/', headers=headers, params=params)

# 返回结果为JSON格式，调用json()方法解析
items = res.json()

num = [i for i in range(len(items['data']))]
for x in num:
    print(items['data'][x]['Title'])
