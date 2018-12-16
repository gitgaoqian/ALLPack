#!/usr/bin/env python
# coding: utf-8
'''
created in 2018-6-7
利用百度AI的web api实现语音合成:https://ai.baidu.com/docs#/TTS-API/top
'''
import requests
import os
import time

token = "24.b7770e1dec06b4d8fe71b9ad34759279.2592000.1530932383.282335-11363408"
Mac = "64:00:6A:69:07:E2"
text = "欢迎您使用百度智能语音web api"
base_url = "http://tsn.baidu.com/text2audio"
param_dic = {'tex':text,'ctp':'1','lan':'zh','cuid':Mac,'tok':token}

r = requests.get(url=base_url,params=param_dic,stream=True)
voice_fp = open('/home/ros/tts.wav', 'wb')
voice_fp.write(r.raw.read())
voice_fp.close()
os.system('mplayer /home/ros/tts.wav')