#!/usr/bin/env python

import rospy
import math
from std_msgs.msg import Float32
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist

current_pose1 = Pose()
current_pose2 = Pose()

current_vel1 = Twist()
current_vel2 = Twist()

def is_out_of_limits(pose, low_limit, high_limit):
    return pose.x < low_limit or pose.x > high_limit or pose.y < low_limit or pose.y > high_limit


def is_non_zero(twist):
	return any(v != 0 for v in [twist.linear.x, twist.linear.y, twist.angular.z])

def callback_vel(cmd_vel,turtle_name):

	global current_vel1
	global current_vel2
	
	if turtle_name == 'turtle1':
		current_vel1 = cmd_vel
	elif turtle_name == 'turtle2':
		current_vel2 = cmd_vel

def callback_pose(pose,turtle_name):

	global current_pose1
	global current_pose2
	
	if turtle_name == 'turtle1':
		current_pose1 = pose
	elif turtle_name == 'turtle2':
		current_pose2 = pose
	
	#rospy.loginfo("The position of %s is: %f, %f, %f",turtle_name ,pose.x, pose.y, pose.theta);

def checkDistance(): 

	treshold = 2
	low_lim = 1
	high_lim = 10 

	rospy.init_node('Distance_node2', anonymous=True)
	    
	pub_dis = rospy.Publisher('distance', Float32, queue_size=10)
	    
	rospy.Subscriber('turtle1/pose', Pose, callback_pose, callback_args='turtle1')
	rospy.Subscriber('turtle1/cmd_vel', Twist, callback_vel, callback_args='turtle1')
	pub_vel1 = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
	
	    
	rospy.Subscriber('turtle2/pose', Pose, callback_pose, callback_args='turtle2')
	rospy.Subscriber('turtle2/cmd_vel', Twist, callback_vel, callback_args='turtle2')
	pub_vel2 = rospy.Publisher('turtle2/cmd_vel', Twist, queue_size=10)
	
	
	    
	rate = rospy.Rate(10)
	
	distance = Float32()
	
	my_vel = Twist()
	my_vel.linear.x = 0.0;
	my_vel.linear.y = 0.0;
	my_vel.angular.z = 0.0;
    
    
	while not rospy.is_shutdown():
	
		distance = math.sqrt((current_pose1.x-current_pose2.x)**2+(current_pose1.y-current_pose2.y)**2)
		
		if distance < treshold or is_out_of_limits(current_pose1, low_lim, high_lim) or is_out_of_limits(current_pose2, low_lim, high_lim):
			if is_non_zero(current_vel1):
				pub_vel1.publish(my_vel)
				print("turtle1 stopped, and the distance is %f",distance)
				
			elif is_non_zero(current_vel2):
				pub_vel2.publish(my_vel)
				print("turtle2 stopped and the distance is %f",distance)
		
		rate.sleep()

if __name__ == '__main__':

	try:	
		checkDistance()
        
	except rospy.ROSInterruptException:
        	pass
