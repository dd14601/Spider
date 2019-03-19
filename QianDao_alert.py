#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# @time     :    20:56
# @Author   : Peter.Dong
# File      : QianDao_alert.py
#微信提醒工作日钉钉签到
import time
import requests
import json
import schedule

from wxpy import *
bot = Bot()

#获取群
groups = bot.groups(update=True)
group = groups.search('1重要日报提醒')[0]

#group.send('test')
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
#判断日期是否为工作日
def worktime():
    nowTime = time.strftime('%Y%m%d',time.localtime())
    data = nowTime
    api_url = 'http://api.goseek.cn/Tools/holiday?date='
    re = requests.get(api_url+data, headers=headers)
    time_data = json.loads(re.text)
    if time_data['data'] == 0 or time_data['data'] == 2:
        group.send('温馨提醒：请及时填写日报！')
        time.sleep(1)
        group.send('温馨提醒：请及时填写日报！')
        time.sleep(1)
        group.send('温馨提醒：请及时填写日报！')




schedule.every().day.at("17:30").do(worktime)
while True:
    schedule.run_pending()
    time.sleep(1)
embed()