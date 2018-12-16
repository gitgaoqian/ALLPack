#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ros
#topic实现形式
# from audio_common_msgs.msg import AudioData
# import rospy
#
# def callback(data):
#     recvBytes = data.data
#     with open("/home/ros/voice/recv.wav",'wb') as f:
#         f.write(recvBytes)
#
# rospy.init_node("voice_recv",anonymous=True)
# voice_subcribe = rospy.Subscriber("voice_topic",AudioData,callback)
# rospy.spin()
#srv实现形式
import rospy
from robot_voice.srv import call
def HandleRequest(data):
	recvBytes = data.sendBytes
	with open("/home/ros/voice/recv.wav",'wb') as f:
		f.write(recvBytes)
	with open("/home/ros/voice/tts.wav",'rb') as ff:
		return_Bytes = ff.read()
	return return_Bytes

def Server():
	rospy.init_node('voice_server')
	rospy.Service('voice_service', call, HandleRequest)
	print "voice_server ready for client."
	rospy.spin()
if __name__ == "__main__":
	Server()