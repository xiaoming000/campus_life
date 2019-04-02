# coding: utf-8

import requests
from bs4 import BeautifulSoup

url = "http://top.baidu.com/index.html"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
       (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
    }


def get_html(url):
    html = requests.get(url, headers=head)
    req = html.text.encode(html.encoding).decode("gbk")
    # 确定网页的编码方式后进行编码，编码格式为utf-8
    return req


def get_soup(req):
    soup = BeautifulSoup(req, 'lxml')   # 使用里写满了解析器解析网页代码为soup对象
    li = soup.select('#hot-list > li')
    hot = []
    for i in li:
        top = i.select('span')[0].text
        title = i.select('.list-title')[0]['title']
        link = i.select('.list-title')[0]['href']
        hot.append([top, title, link])
    print(hot)


# res = get_html(url)
get_soup(get_html(url))
