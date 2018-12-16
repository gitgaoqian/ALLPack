#!/usr/bin/env python
# coding: utf-8
'''
created in 2018-6-7
利用百度AI的web api实现语音识别:https://ai.baidu.com/docs#/TTS-API/top
'''
import requests
import time
import json
import base64
import urllib2
import rospy
from std_msgs.msg import String

class ASR():
    def __init__(self):
        self.apiKey = "KLB4LNxGRAiX58sBLpZOycEn"
        self.secretKey = "2xCMsnTurRFGTrRZg04UKwYqy9RNsyXK "
        self.cuid = "64:00:6A:69:07:E2"
        self.asr_url = "http://vop.baidu.com/server_api"
        self.auth_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=" \
                        + self.apiKey + "&client_secret=" + self.secretKey
        self.token = self.GetToken()
        rospy.init_node('asr', anonymous=True)
        rate = rospy.Rate(10)  # 10hz
        asr_pub = rospy.Publisher("asr_topic",String,queue_size=1)
        while not rospy.is_shutdown():
            asr_msg = String()
            asr_msg.data = self.VoiceToTxt(audio="/home/ros/voice/asr.wav")
            asr_pub.publish(asr_msg)
            rate.sleep()

    def GetToken(self):
        res = urllib2.urlopen(self.auth_url)
        json_data = res.read()
        return json.loads(json_data)['access_token']
    def VoiceToTxt(self,audio):
        data = {"format": "wav", "rate": 16000, "channel": 1, "token": self.token, "cuid": self.cuid, "lan": "zh"}
        # 语音的一些参数
        wav_fp = open(audio, 'rb')
        voice_data = wav_fp.read()  # 字节型数据
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')  # 变成字符型
        # 从音频文件中读取的是二进制类型数据（字节型），需要把它解码成字符型。但是这里不能直接voice_data.decode('utf-8'),会出错，原因不知
        post_data = json.dumps(data).encode('utf-8')
        r = requests.post(self.asr_url, data=post_data)
        data = r.json()
        return data['result'][0]

if __name__ == "__main__":
    asr = ASR()





