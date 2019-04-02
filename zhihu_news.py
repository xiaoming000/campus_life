# coding: utf-8

import requests
from bs4 import BeautifulSoup

url = "https://www.zhihu.com/hot"
head = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
       (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
    "cookie": '_zap=d14c4ec7-1cca-4453-bd60-dba59e65a63e; d_c0="ABBopROzeQ6PTj2TnIddbvUqMl8e1EcGDOI=|1541465285"; \
        q_c1=69c30bbac4d641dca3cb2bb2b6eb1049|1541465286000|1541465286000; _xsrf=UR2M5MiftzZCRJ26ZzMVSGcd9zqF9R3D; \
        __utma=51854390.1935890995.1544004897.1544004897.1544004897.1; __utmz=51854390.1544004897.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __\
        utmv=51854390.000--|3=entry_date=20181106=1; tgw_l7_route=116a747939468d99065d12a386ab1c5f; capsion_ticket="2|1:0|10:1553649019|14:capsion_ticket|44:ZTA4ZDk2ZmUxYjY1NDk0NWI3MWExZDhlZTlmMmQ3NDE=|9fa0abed528d1300c90e328fddd68c821fa3e108b0767011d2b4b11e9c385655"; z_c0="2|1:0|10:1553649032|4:z_c0|92:Mi4xaWlmcUNnQUFBQUFBRUdpbEU3TjVEaVlBQUFCZ0FsVk5pQnVJWFFBSUtGS01kOHh3UkxLclByUDBsSngwNkhXb2dR|e47f4deb61cf9870d3688d8eead18f5b10917546f018fb56999043a2fede996d"; tst=h'
    }


def get_html(url):
    html = requests.get(url, headers=head)
    req = html.text.encode(html.encoding).decode("utf-8")
    # 确定网页的编码方式后进行编码，编码格式为utf-8
    # print(req)
    return req


def get_soup(req):
    soup = BeautifulSoup(req, 'lxml')   # 使用里写满了解析器解析网页代码为soup对象
    section = soup.select('.HotItem')
    hot = []
    for i in section:
        top = i.select('.HotItem-rank')[0].text
        title = i.select('.HotItem-content > a > h2')[0].text
        link = i.select('.HotItem-content > a')[0]['href']
        heat = i.select('.HotItem-content > .HotItem-metrics > svg')[0].next_sibling
        # print(heat)
        hot.append([top, title, link, heat])
    print(hot)


# res = get_html(url)
get_soup(get_html(url))
