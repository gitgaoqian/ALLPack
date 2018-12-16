#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:ros
import rospy
from robot_voice.srv import call
from voice_robot import VoiceRobot
import time
cloud_recv_wav = "/home/ros/voice/cloud_recv.wav"
cloud_send_wav = "/home/ros/voice/cloud_send.wav"

def HandleRequest(data):
	recvBytes = data.sendBytes
	# with open(cloud_recv_wav,'wb') as f:
	# 	f.write(recvBytes)
	vr = VoiceRobot()
	asr_result = vr.ASR(recvBytes)
	nlu_result = vr.NLU(asr_result)
	tts_reslut = vr.TTS(nlu_result)
	sendBytes = tts_reslut
	print ("sendBytesType:\n")
	print (type(sendBytes))
	# with open(cloud_send_wav,'rb') as ff:
	# 	sendBytes = ff.read()
	return sendBytes

def Server():
	rospy.init_node('voice_server')
	rospy.Service('voice_service', call, HandleRequest)
	print ("voice_server ready for client.")
	rospy.spin()
if __name__ == "__main__":
	Server()