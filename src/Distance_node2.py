#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

current_pose1 = None
current_pose2 = None

def callback_turtle(pose,turtle_name):

	global current_pose1
	global current_pose2
	
	if turtle_name == 'turtle1':
		current_pose1 = pose
	else:
		current_pose2 = pose
	
	rospy.loginfo("The position of %s is: %f, %f, %f",turtle_name ,pose.x, pose.y, pose.theta);

def checkDistance(): 

	treshold = 1
	low_lim = 1
	high_lim = 10 

	rospy.init_node('Distance_node2', anonymous=True)
	    
	pub_dis = rospy.Publisher('distance', Float32, queue_size=10)
	    
	rospy.Subscriber('turtle1/pose', Pose, callback_turtle, callback_args='turtle1')
	pub_vel1 = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	    
	rospy.Subscriber('turtle2/pose', Pose, callback_turtle, callback_args='turtle2')
	pub_vel2 = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size=10)
	    
	rate = rospy.Rate(10)
	
	distance = Float32()
	
	my_vel1 = Twist()
	my_vel2 = Twist()
    
    
	while not rospy.is_shutdown():
	
		distance = math.sqrt((current_pose1.x-current_pose2.x)**2+(current_pose1.y-current_pose2.y)**2)
		
		if distance < treshold:
			
		else:
		
		pub.publish(hello_str)
		rate.sleep()

if __name__ == '__main__':

	try:	
		checkDistance()
        
	except rospy.ROSInterruptException:
        	pass
