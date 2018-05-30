#!/usr/bin/env python
import rospy
import tf
import math
from nav_msgs.msg import Odometry
if __name__ == '__main__':
    rospy.init_node("odom_publisher")
    odom_broadcatser= tf.TransformBroadcaster()
    x = 0.0
    y = 0.0;
    th = 0.0;
 
    vx = 0.1;
    vy = -0.1;
    vth = 0.1;
    current_time=rospy.Time.now()
    last_time=rospy.Time.now()
    while not rospy.is_shutdown():
             current_time=rospy.Time.now()
             dt = (current_time - last_time)
             dt=dt.to_sec
             delta_x = 0.1
             delta_y = 0.2
             delta_th = vth 
             
             x += delta_x
             y += delta_y
             th += delta_th
             
             odom_quat=Odometry.pose.pose.orientation()
             odom_quat=tf.transformations.quaternion_from_euler(0,0,th)
             
             odom_trans=Odometry()
             odom_trans.header.stamp=current_time
             odom_trans.header.frame_id="odom"
             odom_trans.child_frame_id="base_footprint"
             
             odom_trans.pose.pose.position.x=x
             odom_trans.pose.pose.position.y=y
             odom_trans.pose.pose.position.z=0
             odom_trans.pose.pose.orientation=odom_quat
             
             odom_broadcatser.sendTransform(odom_trans)
      
 


