#!/usr/bin/env python
# -*- coding: utf-8 -*-  
# @time     :    14:33
# @Author   : Peter.Dong
# File      : TopIDS_log.py

from openpyxl import Workbook
wb = Workbook()  # 创建工作簿
ws = wb.active  # 创建sheet
tag = ['时间','级别','事件号','次数','协议','源地址','源端口','接口','目的地址','目的端口','目的接口','动作','事件描述']
ws.append(tag)
with open('log.txt','r',encoding='UTF-8') as f:

    for i in f.readlines():
        log_line = []
        line_ = i.split(',')
        for line in line_:
            m = str(line.split('=')[1])
            log_line.append(m)
        ws.append(log_line)
wb.save('topsec_log.xlsx')
