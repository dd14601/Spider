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
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}


def is_login():
    #通过个人中心登录返回状态吗判断是否登录
    inbox_url = "https://www.zhihu.com/inbox"
    response = session.get(inbox_url, headers=header, allow_redirects=False)
    if response.status_code != 200:
        return False
    else:
        return True


def get_xsrf():

    response = session.get("https://www.zhihu.com", headers=header).content
    #print(response.text)
    sel = html.fromstring(response)
    xsrf = sel.xpath('//form[@method="POST"]/input/@value')[0]
    if xsrf:

        return xsrf
    else:
        return ""


def zhihu_login(account, password):
    if re.match("^1\d{10}", account):
        print("手机号码登录")
        post_url = "https://www.zhihu.com/login/phone_num"
        post_data = {
            "_xsrf": get_xsrf(),
            "phone_num": account,
            "password": password
        }
        response_text = session.post(post_url, data=post_data, headers=header)
        session.cookies.save()

#zhihu_login('18335124849', 'axd@2265965')
is_login()