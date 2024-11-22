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




def inverse_velocity(current_velocity):
	
	my_vel = Twist()
	my_vel.linear.x = -current_velocity.linear.x
	my_vel.linear.y = -current_velocity.linear.y
	my_vel.angular.z = -current_velocity.angular.z
	
	return my_vel
	

def not_move_to_other_direction(current_pose1, current_pose2, velocity, turtle_id, distance, rate):
    
    if turtle_id == 1:
        x = current_pose1.x
        y = current_pose1.y
        theta = current_pose1.theta
        
        dx = current_pose2.x - x
        dy = current_pose2.y - y
        
    elif turtle_id == 2:
        x = current_pose2.x
        y = current_pose2.y
        theta = current_pose2.theta
        
        dx = current_pose1.x - x
        dy = current_pose1.y - y

    if velocity.angular.z == 0:
        scalar_product = dx * velocity.linear.x + dy * velocity.linear.y
        norm_dist = calculate_module(dx, dy)
        norm_vel = calculate_module(velocity.linear.x, velocity.linear.y)

        cos_angle = scalar_product / (norm_dist * norm_vel)
        angle = math.acos(cos_angle)

        return angle < math.radians(45)
        
    else:
        delta_t = 1 / rate
        r = velocity.linear.x / abs(velocity.angular.z)
        theta_future = theta + velocity.angular.z * delta_t
        
        if velocity.angular.z > 0:
            x_c = x - r * math.sin(theta)
            y_c = y + r * math.cos(theta)
            
            x_future = x_c + r * math.sin(theta_future)
            y_future = y_c - r * math.cos(theta_future)
        else:
            x_c = x + r * math.sin(theta)
            y_c = y - r * math.cos(theta)
            
            x_future = x_c - r * math.sin(theta_future)
            y_future = y_c + r * math.cos(theta_future)
            
        if turtle_id == 1:
            dx_future = x_future - current_pose2.x
            dy_future = y_future - current_pose2.y
        else:
            dx_future = x_future - current_pose1.x
            dy_future = y_future - current_pose1.y
        
        distance_future = calculate_module(dx_future, dy_future)
        
        return distance_future < distance


        
        
        
        
        




	
	
def calculate_module(x, y):

	return math.sqrt((x)**2+(y)**2)


def is_out_of_limits(pose, low_limit, high_limit):

    return pose.x < low_limit or pose.x > high_limit or pose.y < low_limit or pose.y > high_limit


def is_not_zero(twist):

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

	treshold = 2.0
	low_lim = 1.0
	high_lim = 10.0

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
    
	while not rospy.is_shutdown():

		dist_x = current_pose1.x-current_pose2.x
		dist_y = current_pose1.y-current_pose2.y
		
		distance = calculate_module(dist_x, dist_y)
		
		
		if distance < treshold:
		
			my_vel.linear.x = 0.0;
			my_vel.linear.y = 0.0;
			my_vel.angular.z = 0.0;
		
			if is_not_zero(current_vel1) and not_move_to_other_direction(current_pose1, current_pose2, current_vel1,1, distance, 10):
			
				pub_vel1.publish(my_vel)
				print("turtle1 stopped, and the distance is %f",distance)
				
			elif is_not_zero(current_vel2) and not_move_to_other_direction(current_pose1, current_pose2, current_vel2,2, distance, 10):
			
				pub_vel2.publish(my_vel)
				print("turtle2 stopped and the distance is %f",distance)
				
				
		if is_out_of_limits(current_pose1, low_lim, high_lim):
			
			my_vel = inverse_velocity(current_vel1)
			pub_vel1.publish(my_vel)
				
		elif is_out_of_limits(current_pose2, low_lim, high_lim):
			
			my_vel = inverse_velocity(current_vel2)
			pub_vel2.publish(my_vel)
				
			
		
		rate.sleep()
		
		

if __name__ == '__main__':

	try:	
		checkDistance()
        
	except rospy.ROSInterruptException:
        	pass
