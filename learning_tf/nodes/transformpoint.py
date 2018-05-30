#!/usr/bin/env python

import roslib
roslib.load_manifest('learning_tf')
import rospy

import tf
import geometry_msgs.msg

if __name__ == '__main__':
    rospy.init_node('tf_transformpoint')
    #设置turtle1中的一个点坐标
    turtle1point=geometry_msgs.msg.PointStamped()
    turtle1point.header.frame_id='turtle1'
    turtle1point.point.x=4
    turtle1point.point.y=3
    turtle1point.point.z=2
    #turtle１中的点坐标转换到world中去
    worldpoint=geometry_msgs.msg.PointStamped()
    listener = tf.TransformListener()
    listener.transformPoint('world',turtle1point,worldpoint)
    print worldpoint.point.x
    