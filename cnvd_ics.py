# -*- coding: utf-8 -*-
__author__ = 'peter.dong'
__time__ = '2017/11/17'
#cnvd工控漏洞信息收集
import requests
from bs4 import BeautifulSoup
import re
import csv
from fake_useragent import UserAgent

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

def spider():
    url = "http://ics.cnvd.org.cn/"
    date_list =['2017-11-16', '2017-11-17']
    ics_list = []
    r = requests.get(url, headers=headers).text
    soup = BeautifulSoup(r, "html.parser")
    tr_lists = soup.find("tbody").find_all("tr")
    for tr_ in tr_lists:
        tr_date = tr_.select('td:nth-of-type(6)')[0].get_text().strip()
        for date in date_list:
            if tr_date == date:
                url_detail =tr_.find('a').get('href')
                cnvd_id = re.search(r"(CNVD-\d+-\d+)", url_detail).group()
                title = tr_.find('a').get('title')
                ics_list.append([title,url_detail,cnvd_id])
    return ics_list


def writeCSV(file_name,data_list):
    with open(file_name, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['漏洞标题', 'url', '编号'])
        for row in data_list:
            writer.writerow(row)

if __name__ == '__main__':
    writeCSV('cnvd.csv',spider())

# def spider_list(url_list):
#
#     headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
#                'Cookie':'__jsluid=5c71e470aafddccfcb0fbbf1c1a2a863; bdshare_firstime=1496300843497; JSESSIONID=70AB50ECBB33C8D315D0D377A2C17557; __jsl_clearance=1510998723.911|0|XJ2RANgFn5BekWrkdlcNlfs%2FlMg%3D'
#                }
#     for url in url_list:
#         re2 = requests.get(url, headers=headers, timeout=60).text
#         soup = BeautifulSoup(re2, "html.parser")
#         print(soup)
#         title = soup.find('h1')
#         cnvd_id = re.search(r"(CNVD-\d+-\d+)", url).group()
#         print(title,cnvd_id)
#


# url_list = ['http://www.cnvd.org.cn/flaw/show/CNVD-2017-34216','http://www.cnvd.org.cn/flaw/show/CNVD-2017-34491']

