# coding: utf-8
import requests
from lxml import html
import time
import pandas as pd
import openpyxl
from fake_useragent import UserAgent

ua = UserAgent()  #随机的header,模拟人类访问
headers = {'User-Agent': 'ua.random'}
def spider():
    house_list = []  #list列表存放 爬取后的字典信息
    for i in range(1,50):


        #url = 'http://www.ziroom.com/z/nl/z2.html?qwd=&p='+str(i)  #自如合租
        url = 'http://www.ziroom.com/z/nl/z1.html?p='+str(i)   #自如整租
        r = requests.get(url,headers=headers).content
        sel = html.fromstring(r)
        houses = sel.xpath('//li[@class="clearfix"]') #获取每个房子的主节点
        for house in houses:
            info = {}
            tilte = house.xpath('div[@class="txt"]/h3/a/text()') #获取房间的位置
            info['位置']=''.join(tilte)
            position = house.xpath('div[@class="txt"]/h4/a/text()') #获取房间的具体位置
            info['具体位置']=''.join(position)
            detail = house.xpath('div[@class="txt"]/div[@class="detail"]/p/span/text()')  #获取房间的细节
            area = detail[0].replace(" ","").replace("\n","").replace("\t\t","") #去掉房间的面积的空格等
            info['面积']=''.join(area)
            floor = detail[1] #房间楼层
            info['楼层']=''.join(floor)
            structure = detail[2] #房间结构
            info['房间结构']=''.join(structure)
            subway = detail[-1] #距离地铁站的位置
            info['交通']=''.join(subway)
            tags = house.xpath('div[@class="txt"]/p[@class="room_tags clearfix"]/span/text()') #房间特色
            info['特点']=''.join(tags)
            price = house.xpath('div[@class="priceDetail"]/p[@class="price"]/text()')[0].replace(" ","").replace("\n","")
            info['价钱']=''.join(price)
            #rint(tilte,position,area,floor,structure,subway,tags,price)
            house_list.append(info)
        print('OK')

    return house_list

def data_process(data):
    df = pd.DataFrame(data)  #将数据格式化后处理
    #print(data)
    df.to_excel('ziru_zhengzu.xlsx')  #写入xlsx中

if __name__ == '__main__':
    house_list = spider()
    data_process(house_list)