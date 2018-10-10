#！/usr/bin/env python
# -*- coding:utf-8 -*-


import requests
import json
import pymongo
import os

client = pymongo.MongoClient(host='localhost',port=27017)

collection = client['spiders']['meinv']

def download_img(item):
    print('正在下载图片：',item['title'])
    json_data = {
        "title":item['title'],
        "tags":item['tags'],
        "width":item['width'],
        "height":item['height'],
        "ori_pic_url":item['ori_pic_url'],
        "thumbUrl":item['thumbUrl']
    }
    #数据保持到mongodb
    collection.insert(json_data)
    #创建图片下载目录
    img_dir = os.getcwd() + "/imgs/"
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)
    #读取图片内容
    pic_content = requests.get(item['ori_pic_url']).content
    #图片写入本地文件
    with open(img_dir + str(item['id']) + '.jpg',"wb") as f:
        f.write(pic_content)

    print('success!')

def main(url):
    r = requests.get(url)
    if r.status_code ==200:
        data = json.loads(r.text)
        for item in data['all_items']:
            download_img(item)


if __name__ == '__main__':
    category = input("請輸入要下載的壁紙关键词:>>")
    url ="http://pic.sogou.com/pics/channel/getAllRecomPicByTag.jsp?category="+category+"&tag=%E6%B8%B8%E6%88%8F&start=0&len=15&width=1366&height=768"
    main(url)