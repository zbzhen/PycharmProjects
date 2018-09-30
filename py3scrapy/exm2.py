#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/8/28 15:50
# @Author  : BingZhen Zhou
# @contact : zbzhen@smail.hunnu.edu.cn
# @File    : exm2.py
# @version : Python 2.7.6
import urllib2
response = urllib2.urlopen("http://www.baidu.com")
print response.read()