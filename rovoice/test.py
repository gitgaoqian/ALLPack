#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ros

import binascii
#16进制整数转ASCii编码字符串
b = str(hex(100))
b = b[2:]   #截取掉'0x'
c = binascii.a2b_hex(b) #转换成ASCii编码的字符串
print("b:%s,c:%s" %(b,c))
print type(b)
print type(c)