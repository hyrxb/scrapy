#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

import re

import os

import time

import hashlib

url = "http://www.ivsky.com/tupian/xiaohuangren_t21343/"

data = requests.get(url).text


regex = r'<img src="(.*?)".*?>'

img_list = re.findall(regex,data)

img_dir = os.getcwd() + '/imgs'

print(img_dir)

if not os.path.exists(img_dir):
    os.mkdir(img_dir)

for img in img_list:
    ext=os.path.splitext(img)[1]

    hash = hashlib.md5(str(time.time()).encode("utf-8"))

    filename = hash.hexdigest()  + ext

    print("down:",img)

    imgdata = requests.get(img).content

    with open(img_dir+'/'+filename,'wb') as f:
        f.write(imgdata)

print('success!')
