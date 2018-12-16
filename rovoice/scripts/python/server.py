#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author:ros
import rospy
from rovoice.srv import call
from robvoice import VoiceRobot

def HandleRequest(data):
	recvBytes = data.sendBytes
	vr = VoiceRobot()
	asr_result = vr.ASR(recvBytes)
	print asr_result
	print ("asr_result type:")
	print type(asr_result)
	if asr_result == "语音识别失败":
		nlu_result = "语音识别失败"
	else:
		nlu_result = vr.NLU(asr_result)
	print ("nlu_result type:")
	print (type(nlu_result))
	print nlu_result
	tts_reslut = vr.TTS(nlu_result)
	print ("tts_result type:")
	print type(tts_reslut)
	sendBytes = tts_reslut
	print ("sendBytesType:\n")
	return sendBytes

def Server():
	rospy.init_node('voice_server')
	rospy.Service('voice_service', call, HandleRequest)
	print ("voice_server ready for client.")
	rospy.spin()
if __name__ == "__main__":
	Server()
