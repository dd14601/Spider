#coding:utf-8

import re
import os
import time
import threading
from multiprocessing import Pool, cpu_count
import requests
from bs4 import BeautifulSoup

headers = {'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/56.0.2924.87 Safari/537.36',
           'Cookie':'Hm_lvt_dbc355aef238b6c32b43eacbbf161c3c=1498563425; Hm_lpvt_dbc355aef238b6c32b43eacbbf161c3c=1499090610'}

dir_path = r"G:\mzitu"
def get_urls():
    page_urls = ['http://www.mzitu.com/page/{cnt}'.format(cnt=cnt) for cnt in range(1, 143)]
    print("please wait for second...")
    img_urls = []
    for page_url in page_urls:
        try:
            bs = BeautifulSoup(requests.get(page_url, headers=headers, timeout=10).text, 'lxml').find('ul', id="pins")
            result = re.findall(r"(?<=href=)\S+",str(bs))
            img_url = [url.replace('"', "")for url in result]
            img_urls.extend(img_url)
        except Exception as e:
            print(e)
    return set(img_urls)


lock = threading.Lock()
def urls_spider(url):
    try:
        r = requests.get(url,headers=headers,timeout=10).text
        folder_name = BeautifulSoup(r,'lxml').find('h2',{'class':'main-title'}).get_text()
        with lock:
            if make_dir(folder_name):
                max_cout =  BeautifulSoup(r,'lxml').find('div',{'class':'pagenavi'}).find_all('span')[-2].get_text()
                page_urls = [url + '/' + str(i) for i in range(int(max_cout)+1)]
                img_urls= []
                for _,page_url in enumerate(page_urls):
                    time.sleep(0.6)
                    result = requests.get(page_url,headers=headers,timeout=10).text
                    img_url = BeautifulSoup(result,'lxml').find('div', class_="main-image").find('p').find('a').find('img')['src']
                    img_urls.append(img_url)
                for cnt,url in enumerate(img_urls):
                    save_pic(url,cnt)
    except Exception as e:
        print(e)

def save_pic(pic_src,pic_cnt):
    try:
        img = requests.get(pic_src,headers=headers,timeout=10)
        imgname = "pic_cnt_{}.jpg".format(pic_cnt+1)
        with open(imgname,'ab') as f:
            f.write(img.content)
            print(imgname)
    except Exception as e:
        print(e)


def make_dir(folder_name):
    path = os.path.join(dir_path,folder_name)
    if not os.path.exists(path):
        os.makedirs(path)
        print(path)
        os.chdir(path)
        return True
    print("Folden has existed!")
    return False

def delete_empty_dir(dir):
    if os.path.exists(dir):
        if os.path.isdir(dir):
            for d in os.listdir(dir):
                path = os.path.join(dir,d)
                if os.path.isdir(path):
                    delete_empty_dir(path)
        if not os.listdir(dir):
            os.rmdir(dir)
            print("remove the empty dir:{}".format(dir))
    else:
        print("please start your performance")

if __name__ == "__main__":
    urls =get_urls()
    pool = Pool(processes=cpu_count())
    try:
        delete_empty_dir(dir_path)
        pool.map(urls_spider,urls)
    except Exception as e:
        time.sleep(30)
        delete_empty_dir(dir_path)
        pool.map(urls_spider,urls)


