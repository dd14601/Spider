# -*- coding: utf-8 -*-
__author__ = 'peter.dong'
__time__ = '2017/9/13'
#穆总安排的test测试文件编号后加漏洞tag转换脚本
import os
import re

dir = "path" #文件所在文件夹
file_num = 'number' #需要匹配的文件名称
file_tag = 'tag' #漏洞tag
file_re = str(file_num+'\d{2}') #拼凑正则
for file in os.listdir(dir):
    OldDir = os.path.join(dir,file) #源文件路径
    filename = os.path.splitext(file)[0] #文件名
    filetype = os.path.splitext(file)[1] #文件后缀
    if re.match(file_re,filename):
        new_filename = str(filename+'.'+file_tag)  #新文件名
        NewDir = os.path.join(dir,new_filename+filetype)
        os.rename(OldDir,NewDir) #更新
