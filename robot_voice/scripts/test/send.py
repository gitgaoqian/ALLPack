#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ros
#topic形式实现
# from audio_common_msgs.msg import AudioData
# import rospy
#
# rospy.init_node("voice_send",anonymous=True)
# rate = rospy.Rate(10)
# voice_publish = rospy.Publisher("voice_topic",AudioData,queue_size=10)
#
# while not rospy.is_shutdown():
#     voice_msg = AudioData()#在python3理解为字节类型
#     with open('/home/ros/voice/send.wav','rb') as f:
#         readBytes = f.read()#全部读取内容
#     voice_msg.data = readBytes
#     voice_publish.publish(voice_msg)
#     rate.sleep()
#srv形式实现
import sys
import rospy
from robot_voice.srv import call

def Client(sendBytes):
    rospy.wait_for_service('voice_service')
    try:
        client = rospy.ServiceProxy('voice_service', call)
        resp= client(sendBytes)
        print (type(resp.returnBytes))
        with open("/home/ros/voice/return.wave",'wb') as ff:
             ff.write(resp.returnBytes)
    except rospy.ServiceException:
        print ("Service call failed")

if __name__ == "__main__":
    with open('/home/ros/voice/send.wav', 'rb') as f:
        sendBytes = f.read()#全部读取内容
    print ("send voice bytes")
    Client(sendBytes)

