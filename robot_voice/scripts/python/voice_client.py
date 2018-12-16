#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author:ros
import rospy
from record import Recorder
from robot_voice.srv import call
import os

def Client(sendBytes):
    rospy.wait_for_service('voice_service')
    try:
        client = rospy.ServiceProxy('voice_service', call)
        resp = client(sendBytes)
        print (type(resp))
        print (type(resp.returnBytes))
        with open("/home/ros/voice/robot_recv.wav",'wb') as ff:
             ff.write(resp.returnBytes)
    except rospy.ServiceException:
        print ("Service call failed")

if __name__ == "__main__":
    while True:
        #键盘唤醒
        print ("INPUT WAKEUP KEY:")
        key = input()
        if (key == "w"):
            r = Recorder()
            recordBytes = r.recorder()
            # with open('/home/ros/voice/robot_send.wav', 'rb') as f:
            #     sendBytes = f.read()#全部读取内容
            print ("send voice bytes")
            Client(recordBytes)
            os.system("mplayer /home/ros/voice/robot_recv.wav")
        else:
            print ("wakeup failed")



