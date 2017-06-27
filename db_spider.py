# coding: utf-8

import requests
from bs4 import BeautifulSoup
import re
import sys
import csv
import codecs
import threading


def spider(url_lists):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Cookie": "__unam=d0030f5-15c38515312-64b85969-134; PHPSESSID=upnppon2uhghl7k1qocks84mu3; _ga=GA1.3.261928195.1495593473; _gid=GA1.3.8028"
    }
    #url = 'https://www.exploit-db.com/dos/'
    url_list = []
    for url in url_lists:
        r = requests.get(url, headers=header, verify=False)
        s = r.text
        soup = BeautifulSoup(s, "html.parser")
        soup_list = soup.find("tbody").find_all('tr')
        for tr_td in soup_list:       #匹配时间
            if tr_td.find(text=['2017-06-22','2017-06-21','2017-06-20','2017-06-19']) != None:  #时间如果选择正确的话，选取url
                tr_td_des = tr_td.find('td',{'class':'description'})
                tr_td_url = tr_td_des.find('a').get('href')    #获取链接
                url_list.append(tr_td_url)

    return url_list


def spider_list(url_list):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
        "Cookie": "__unam=d0030f5-15c7b6e83b8-53ce64ff-73; PHPSESSID=6fed2296luc35qsnapimq0tqs5; _ga=GA1.3.1828391708.1496719375; _gid=GA1.3.86998437.1498099131"
    }
    dblist = []     #将想要的结果写入列表中
    for url in url_list:
        r = requests.get(url, headers=header, verify=False)
        s = r.text
        soup = BeautifulSoup(s, "html.parser")
        title = soup.find('title').get_text()
        db_list = soup.find_all('table',{'class':'exploit_list'},limit=1)
        for db in db_list:
            cve_list = db.find(text=re.compile("CVE-\d+-\d+"))
            edb_id = soup.find(text='EDB-ID').parent.parent.get_text()  #获取edb-id的父节点的父节点里的内容是 EDB-ID:xxxxx
            if cve_list == None:
                id = edb_id
            else:
                id = re.match(r'(CVE):\s+(CVE-\d+-\d+)',soup.find(text='CVE').parent.parent.get_text()).group(2)  #用正则匹配CVE编号
            #edb = re.match(r'(EDB-ID):\s+(\d{5})', soup.find(text='EDB-ID').parent.parent.get_text()).group(2)

            # type = soup.find(text='Type').parent.parent.get_text()
            type = re.match(r'Type:\s(\w+)', soup.find(text='Type').parent.parent.get_text()).group(1)

            pla = re.match(r'Platform:\s(\w+)', soup.find(text='Platform').parent.parent.get_text()).group(1)
            dblist.append([title,url,id,type,pla])
        #print(title,url,id,type,pla)
    return dblist

def writeCSV(file_name,data_list):
    with open(file_name, 'w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['漏洞标题', 'url', '编号', '漏洞类别', '属性'])
        for row in data_list:
            writer.writerow(row)

if __name__ == '__main__':
    url = ['https://www.exploit-db.com/remote/','https://www.exploit-db.com/webapps/', 'https://www.exploit-db.com/local/', 'https://www.exploit-db.com/dos/']
    url_list = spider(url)
    print(url_list)
    data_list = spider_list(url_list)
    #print(data_list)
    writeCSV('test.csv', data_list)
