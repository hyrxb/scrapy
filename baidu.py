#!/usr/bin/env python
# -*- coding:utf-8 -*-


import urllib.request


data = urllib.request.urlopen("http://www.baidu.com")


data = data.read()

print(data.decode('utf-8'))
