import requests
from bs4 import BeautifulSoup


class QuerySpider(object):

    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Connection": "keep-alive",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 \
           (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        }
        self.url = "http://zhjw1.jju.edu.cn:81/"
        self.code_url = "http://zhjw1.jju.edu.cn:81/CheckCode.aspx"
        self.post_url = "http://zhjw1.jju.edu.cn:81/default2.aspx"
        self.session = requests.Session()
        self.number = ""
        self.password = ""
        self.value = ""
        self.course_link = ""
        self.grade_link = ""

    def get_img(self, img_url):
        response = self.session.get(self.url, headers=self.headers)
        response.encoding = 'gbk'
        cookies = requests.utils.dict_from_cookiejar(response.cookies)
        soup = BeautifulSoup(response.text, 'lxml')
        self.value = soup.select("#form1 > input")[0]['value']
        image = self.session.get(self.code_url, headers=self.headers)
        with open(img_url, 'wb') as f:
            f.write(image.content)
        return [cookies, self.value]

    def login(self, number, password, code, value, cookies):
        self.value = value
        self.session.cookies = requests.utils.cookiejar_from_dict(cookies)
        self.number = number
        self.password = password
        post_data = {
            "__VIEWSTATE": self.value,
            "txtUserName": self.number,
            "TextBox1": "",
            "TextBox2": self.password,
            "txtSecretCode": code,
            "RadioButtonList1": "%D1%A7%C9%FA",
            "Button1": "",
            "lbLanguage": "",
            "hidPdrs": "",
            "hidsc": ""

        }
        response = self.session.post(self.post_url, data=post_data, headers=self.headers)
        if response.status_code == 200:
            print("登入成功！")

    def get_index(self):
        index_url = "http://zhjw1.jju.edu.cn:81/xs_main.aspx?xh=" + self.number
        response = self.session.get(index_url, headers=self.headers)
        response.encoding = 'gbk'
        soup = BeautifulSoup(response.text, 'lxml')
        links = soup.select('.top > .sub > li > a')
        self.course_link = "http://zhjw1.jju.edu.cn:81/" + links[6]['href']
        self.grade_link = "http://zhjw1.jju.edu.cn:81/" + links[8]['href']

    def get_course(self):
        self.get_index()
        header = self.headers
        header['Referer'] = "http://zhjw1.jju.edu.cn:81/xskbcx.aspx?xh=20150202232&xm=%D0%A4%D0%A1%C3%F7&gnmkdm=N121603"
        r = self.session.post(self.course_link, headers=header, allow_redirects=False)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'lxml')
        info = {
            'xnd': soup.select('#xnd > option[selected="selected"]')[0].text,
            'xqd': soup.select('#xqd > option[selected="selected"]')[0].text,
            'number': soup.select('.trbg1 > td > #Label5')[0].text,
            'name': soup.select('.trbg1 > td > #Label6')[0].text,
            'faculty': soup.select('.trbg1 > td > #Label7')[0].text,
            'major': soup.select('.trbg1 > td > #Label8')[0].text,
            'a_class': soup.select('.trbg1 > td > #Label9')[0].text,
            'course_table': soup.select('#Table1')[0].prettify()
        }
        return info

    def get_grade(self, year, term):
        self.get_index()
        header = self.headers
        header['Referer'] = "http://zhjw1.jju.edu.cn:81/xscj_gc2.aspx?xh=20150202232&xm=%D0%A4%D0%A1%C3%F7&gnmkdm=N121605"
        r = self.session.get(self.grade_link, headers=header, allow_redirects=False)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'lxml')
        post_value = soup.select("#Form1 input[name='__VIEWSTATE']")
        post_data = {
            "__VIEWSTATE": post_value[0]['value'],
            "ddlXN": year,
            "ddlXQ": term,
            "Button1": "按学期"
        }
        r = self.session.post(self.grade_link, data=post_data, headers=header, allow_redirects=False)
        r.encoding = 'gbk'
        soup = BeautifulSoup(r.text, 'lxml')
        grades_table = soup.select("#Datagrid1 > tr")
        grades = []
        for i in range(0, len(grades_table)):
            tds = grades_table[i].select("td")
            temp = []
            for td in tds:
                temp.append(td.text)
            grades.append(temp)
        info = {
            'xnd': soup.select('#ddlXN > option[selected="selected"]')[0].text,
            'xqd': soup.select('#ddlXQ > option[selected="selected"]')[0].text,
            'number': soup.select('.searchbox > p > #Label5')[0].text,
            'name': soup.select('.searchbox > p #Label6')[0].text,
            'faculty': soup.select('.searchbox > p > #Label6')[0].text,
            'major': soup.select('.searchbox > p > #Label7')[0].text,
            'a_class': soup.select('.searchbox > p > #Label8')[0].text,
            'grades': grades
        }
        return info


if __name__ == "__main__":
    number = "20150202232"
    password = "950909ming"
    qs = QuerySpider()
    static_url = "F:/desktop/Python/Python web/Django/campus_life/static/code/test.jpg"
    res = qs.get_img(static_url)
    cookies = res[0]
    value = res[1]
    check_code = input("请输入验证码：")
    qs.login(number, password, check_code, value, cookies)
    # qs.get_course()
    qs.get_grade('2018-2019', '1')

