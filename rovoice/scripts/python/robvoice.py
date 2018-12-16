#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ros
import requests
import json
import base64
# import urllib.request
import urllib2

class VoiceRobot:
    def __init__(self):
        # 使用百度API需要到的参数
        self.apiKey = "KLB4LNxGRAiX58sBLpZOycEn"
        self.secretKey = "2xCMsnTurRFGTrRZg04UKwYqy9RNsyXK "
        self.cuid = "64:00:6A:69:07:E2"
        #获取百度语音访问Token的函数
        self.auth_url = "https://openapi.baidu.com/oauth/2.0/token"
        # 语音合成的resturl
        self.tts_url = "http://tsn.baidu.com/text2audio"
        # 语音识别的resturl
        self.asr_url = 'http://vop.baidu.com/server_api'
        # 语义理解的resturl
        self.nlu_url = "http://openapi.tuling123.com/openapi/api/v2"
        self.token = self.GetToken()
    def TTS(self, text):
        # 2. 向Rest接口提交数据
        param={'tex':text,'lan':'zh','cuid':self.cuid,'ctp':'1','tok':self.token}
        r=requests.post(self.tts_url,params=param,stream=True)
        rr = r.raw.read()
        # print ("tts type:")
        # print (type(rr))
        return rr
        # voice_fp = open('/home/ros/voice/cloud_send.wav','wb')
        # voice_fp.write(r.raw.read())
        # voice_fp.close()
        # os.system("mplayer /home/ros/tts.wav")
    def ASR(self,voice_data):
        # 2. 必要参数
        data = {"format":"wav","rate":16000, "channel":1,"token":self.token,"cuid":self.cuid,"lan":"zh"}
        # # 可选参数
        # wav_fp = open(audio,'rb')
        # voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')
        post_data = json.dumps(data).encode('utf-8')
        r=requests.post(self.asr_url,data=post_data,headers={'content-type': 'application/json'})
        # 3.处理返回数据
        return_msg = r.json()
        err_msg = return_msg["err_msg"]
        if err_msg == "success.":#说明识别成功
            result = return_msg['result'][0].encode("utf-8")
            #print (type(result))
            # self.NLU(result)
            # self.TTS(r)
        else:
            result = "语音识别失败"
            #self.TTS(result)
        return result
    def NLU(self,text):
        req = {
            "perception":
                {
                    "inputText":
                        {
                            "text": text
                        },

                    "selfInfo":
                        {
                            "location":
                                {
                                    "city": "沈阳",
                                    "province": "辽宁",
                                    "street": "文化路"
                                }
                        }
                },

            "userInfo":
                {
                    "apiKey": "3aa5231887234e20b7867a3c656941da",
                    "userId": "OnlyUseAlphabet"
                }
        }
        # 将字典格式的req编码为utf8
        req_data = json.dumps(req).encode('utf8')
        response = requests.post(self.nlu_url, data=req_data, headers={'content-type': 'application/json'})
        data = response.json()
        resultType = data['results'][0]['resultType']
        if resultType == 'text':
            values = data['results'][0]['values']['text']
            print ("NLU RESULTS:"+values)
            return values.encode("utf-8")
        else:
            return u"我没有理解你说的话"
    def GetToken(self):
        auth_url = self.auth_url + "?grant_type=client_credentials&client_id=" \
                    + self.apiKey + "&client_secret=" + self.secretKey
        res = urllib2.urlopen(auth_url)
        json_data = res.read().decode('utf-8')#由json字节转成json字符串
        # print (json_data)
        return json.loads(json_data)['access_token']
        #使用request的post方式但是错误
        # data = {"grant_type":"client_credentials","client_id":self.apiKey,"client_secret":self.secretKey}
        # r = requests.post(self.auth_url,data=json.dumps(data))
        # print r.json()
