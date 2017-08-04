import requests
import http.cookiejar as cookielib
import re
from lxml import html

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename="cookie.txt")
try:
    session.cookies.load(ignore_discard=True)
except:
    print("cookie未载入")



header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.130 Safari/537.36',
    'Referer': 'https://www.zhihu.com/',
}


def is_login():
    #通过个人中心登录返回状态吗判断是否登录
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        print("FALSE")
    else:
        print("OK")


def get_xsrf():

    response = session.get("https://www.zhihu.com", headers=header).content
    #print(response.text)
    sel = html.fromstring(response)
    xsrf = sel.xpath('//form[@method="POST"]/input/@value')[0]
    if xsrf:

        return xsrf
    else:
        return ""


def get_capther():

    base_url = "https://www.zhihu.com"
    pattern_captcha_timestmp = r'<script type="text/json" class="json-inline" data-name="ga_vars">{"user_created":0,"now":(.*?),'
    response = session.get("https://www.zhihu.com", headers=header).content
    _captcha_timestmp = re.findall(pattern_captcha_timestmp, response, re.S | re.I)
    timestamp = _captcha_timestmp[0]
    captcha_url = base_url + '/captcha.gif?r=' + timestamp + "&type=login&lang=cn"
    session = requests.session()
    captcha_f = session.get(captcha_url, headers=header)
    with open('captcha.jpg', 'wb') as f:
        f.write(captcha_f.content)
        f.close

    def location(a, b):
        a = 20 * int(a) + 2
        b = 20 * int(b) + 2
        if b != 0:
            captcha = "{\"img_size\":[200,44],\"input_points\":[[%s,26.45],[%s,29.45]]}" % (int(a), int(b))
        else:
            captcha = "{\"img_size\":[200,44],\"input_points\":[[%s,26.45]]}" % (a)
        return captcha

    # input captcha relate_location
    locationa = input("input captcha location 1:")
    locationb = input("input captcha location 2:")
    captcha = location(locationa, locationb)
    return captcha


def location(a, b):
    a = 20 * int(a) + 2
    b = 20 * int(b) + 2
    if b != 0:
        captcha = "{\"img_size\":[200,44],\"input_points\":[[%s,26.45],[%s,29.45]]}" % (int(a), int(b))
    else:
        captcha = "{\"img_size\":[200,44],\"input_points\":[[%s,26.45]]}" % (a)
    return captcha
def zhihu_login(account, password):
    #前面的都是废话，这是重点
    if re.match("^1\d{10}", account):

        response = session.get("https://www.zhihu.com", headers=header).content
        # print(response.text)
        sel = html.fromstring(response)
        xsrf = sel.xpath('//form[@method="POST"]/input/@value')[0]

        header['X-Xsrftoken'] = '%s' %(xsrf)

        base_url = "https://www.zhihu.com"
        pattern_captcha_timestmp = sel.xpath('//script[@data-name="ga_vars"]/text()')[0]

        _captcha_timestmp = re.match('.*"now":(.*?),',pattern_captcha_timestmp, re.DOTALL)
        timestamp = _captcha_timestmp[1]
        captcha_url = base_url + '/captcha.gif?r=' + timestamp + "&type=login&lang=cn"

        captcha_f = session.get(captcha_url, headers=header)
        with open('captcha.jpg', 'wb') as f:
            f.write(captcha_f.content)
            f.close

        # input captcha relate_location
        locationa = input("input captcha location 1:")
        locationb = input("input captcha location 2:")
        captcha = location(locationa, locationb)

        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {'_xsrf':xsrf,'password':password,'captcha':captcha,'captcha_type':'cn','phone_num':account}


    response_text = session.post(post_url, data=post_data, headers=header)
    print(response_text.text)
    session.cookies.save()


#zhihu_login('15525608182', 'topsec123')
is_login()