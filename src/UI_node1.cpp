#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "turtlesim/Spawn.h"
#include <iostream>


int main(int argc, char **argv){
	ros::init(argc,argv,"UI_node1");
	ros::NodeHandle n;
	
	ros::Publisher turtle_pub1 = n.advertise<geometry_msgs::Twist>("turtle1/cmd_vel", 10);
	ros::Publisher turtle_pub2 = n.advertise<geometry_msgs::Twist>("turtle2/cmd_vel", 10);
	
	ros::ServiceClient turtle_client = n.serviceClient<turtlesim::Spawn>("/spawn");
	
	
	//Assuming we've already started turtlesim before call the serivice, otherwise we need to use the following command that wait turtlesim be run
	//turtle_client.waitForService()
	
	turtlesim::Spawn my_spawn;
	
	my_spawn.request.x = 8.0;
	my_spawn.request.y = 9.0;
	my_spawn.request.theta = 0.0;
	my_spawn.request.name = "turtle2";
	
	
	turtle_client.call(my_spawn);
	
	ros::Rate loop_rate(1);
	
	geometry_msgs::Twist my_vel;
	
	int turtle_id;
	bool valid_choice = false;
	
	while(ros::ok()){
	
		do{
			std::cout<<"Specify turtle [1/2]: "<<std::endl;
			std::cin>>turtle_id;
			
			if(turtle_id == 1 || turtle_id == 2)
				valid_choice = true;
			else
				std::cout<<"Selected turtle doesn't exists!"<<std::endl;
				
		}while(!valid_choice);
		
		std::cout<<"Insert x linear vel: "<<std::endl;
		std::cin>>my_vel.linear.x;
			
		std::cout<<"Insert y linear vel: "<<std::endl;
		std::cin>>my_vel.linear.y;
			
		std::cout<<"Insert z angular vel: "<<std::endl;
		std::cin>>my_vel.angular.z;
		
		if(turtle_id==1)
			turtle_pub1.publish(my_vel);
				
		else
			turtle_pub2.publish(my_vel);
		
		valid_choice = false;

		ros::spinOnce();
		loop_rate.sleep();

	}
	
	return 0;
}
