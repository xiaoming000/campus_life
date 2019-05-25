import requests
from bs4 import BeautifulSoup


class NewsSpider(object):

    def __init__(self):
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36"
        }

    def get_baidu_news(self, url):
        html = requests.get(url, headers=self.header)
        # 确定网页的编码方式后进行编码，编码格式为gbk
        req = html.text.encode(html.encoding).decode("gbk")
        soup = BeautifulSoup(req, 'lxml')   # 使用里写满了解析器解析网页代码为soup对象
        li = soup.select('#hot-list > li')
        hot = []
        for i in li:
            top = i.select('span')[0].text
            title = i.select('.list-title')[0]['title']
            link = i.select('.list-title')[0]['href']
            heat = i.select('.icon-rise')[0].text if i.select('.icon-rise') else i.select('.icon-fall')[0].text
            hot.append({'top': int(top), 'title': title, 'link': link, 'heat': int(int(heat)/10000)})
        # print(hot)
        return hot

    def get_zhihu_news(self, url):
        html = requests.get(url, headers=self.header)
        # 确定网页的编码方式后进行编码，编码格式为utf-8
        req = html.text.encode(html.encoding).decode("utf-8")
        soup = BeautifulSoup(req, 'lxml')   # 使用里写满了解析器解析网页代码为soup对象
        # print(soup.prettify())
        section = soup.select('.HotItem')
        # print(section)
        hot = []
        for i in section:
            top = i.select('.HotItem-rank')[0].text
            title = i.select('.HotItem-content > a > h2')[0].text
            link = i.select('.HotItem-content > a')[0]['href']
            heat = i.select('.HotItem-content > .HotItem-metrics > svg')[0].next_sibling
            # print(heat)
            hot.append({'top': int(top), 'title': title, 'link': link, 'heat': heat})
        # print(hot)
        return hot


if __name__ == "__main__":
    spider = NewsSpider()
    # baidu_url = "http://top.baidu.com/index.html"
    zhihu_url = "https://www.zhihu.com/hot"
    # spider.get_baidu_news(baidu_url)
    spider.get_zhihu_news(zhihu_url)
