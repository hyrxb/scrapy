#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import re


r = requests.get("http://2018.ip138.com/ic.asp")

if r.status_code ==200:
    con = r.content.decode("gb2312")
    m = re.search(r'\[(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\]',con,re.DOTALL)
    print("您的ip是：",m.group(1))
    #您的ip是： 124.207.180.37
