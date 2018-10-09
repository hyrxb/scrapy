#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests

imgurl = "http://img.ivsky.com/img/tupian/t/201411/01/xiaohuangren_tupian-007.jpg"


imgdata = requests.get(imgurl).content

with open('s.jpg','wb') as f:
    f.write(imgdata)