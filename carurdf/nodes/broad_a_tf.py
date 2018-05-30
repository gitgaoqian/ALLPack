#!/usr/bin/env python 
import rospy
import tf
import math

if __name__ == '__main__':
    rospy.init_node('tfransform')
    br = tf.TransformBroadcaster()
    rate = rospy.Rate(10.0)
    while not rospy.is_shutdown():
        t = rospy.Time.now().to_sec() * math.pi
        br.sendTransform((0.2 * math.sin(t), 0.2 * math.cos(t), 0.0),
                        (0.0, 0.0, 0.0, 1.0),
                        rospy.Time.now(),
                        "base_footprint",
                        "map")
        rate.sleep()
