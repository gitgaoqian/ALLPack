#!/usr/bin/env python
# coding: utf-8
'''
created in 2018-6-7
利用图灵机器人的web api实现聊天功能(语义理解):https://segmentfault.com/a/1190000013900291
'''
import json
import requests
import rospy
from std_msgs.msg import String
return_data = None
class NLU()
    def __init__(self):
        self.api_url = "http://openapi.tuling123.com/openapi/api/v2"
        rospy.init_node('nlu', anonymous=True)
        rate = rospy.Rate(10)  # 10hz
        nlu_sub = rospy.Subscriber("asr_topic",String,self.NLUCallback)
        nlu_pub = rospy.Publisher("nlu_topic", String, queue_size=1)

    def NLUCallback(self,data):
        global return_data
        asr_msg = data.data
        req = {
            "perception":
                {
                    "inputText":
                        {
                            "text": asr_msg
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
        self.req_data = json.dumps(req).encode('utf8')  # 将字典格式的req编码为utf8
        response = requests.post(self.api_url, data=self.req_data, headers={'content-type': 'application/json'})
        data = response.json()
        return_data = data['results'][0]['values']['text']
    def NLUPub(self):
        global return_data
        rate = rospy.Rate(5)  # 10hz
        while not rospy.is_shutdown():
        nlu_msg = String()
        nlu_msg.data = return_data


if __name__ == "__main__":
    NLU()

