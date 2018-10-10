#!/usr/bin/env python
# -*- coding:utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pymongo
import os

client = pymongo.MongoClient(host='localhost',port=27017)

collection = client['spiders']['ip']


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36"
}

def get_ip(url):
    r = requests.get(url,headers=headers)

    if r.status_code ==200:
        soup = BeautifulSoup(r.text,'lxml')
        #查找table
        table = soup.find("table",id="ip_list")
        #从第一个tr开始
        for tr in  table.find_all("tr")[1:]:
            tds = tr.find_all('td')
            img_src = tds[0].img['src'] if tds[0].img else None
            ip_addr = tds[1].string
            ip_port = tds[2].string
            address = tds[3].a.string if tds[3].a else None
            type = tds[4].string
            scheme = tds[5].string
            #测试是否可用
            delay_time = os.popen("ping -c 1 " + ip_addr.string + " | awk 'NR==2{print}' -")

            spend_time = str(delay_time.read()).split("time=")[-1].strip("\r\n")

            print("time = " + spend_time)

            collection.insert({"img_src":img_src,"ip_addr":ip_addr,"ip_port":ip_port,"address":address,"type":type,"scheme":scheme})

            print("success")

if __name__ == "__main__":
    url = "http://www.xicidaili.com/nn/1"
    get_ip(url)
