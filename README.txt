Node 1 was implemented in c++, instead node 2 was implemented in python.
Based on requests, node 1 implements the text UI to allow the user to select the turtle and provide values for the velocities, the linear one along the x and y axes and the angular one along the z axis.
In node 1 a check was also implemented to make sure that the user's choice concerns only turtle 1 or turtle 2, instead no checks on the input velocities were implemented.
In node 2 the distance calculation logic is stored, to stop the turtles if they are too close to each other, and the boundary check, the turtle will react differently in these two cases.
If a turtle gets too close to the other it will be stopped and other provided velocities will be accepted after being evaluated by the "not_move_to_other_direction" function, which analyzes if the given velocity has only a linear part or also an angular part. 
In case it is only a linear velocity, the control is based on the scalar product between the distance vector among turtles and the velocity vector, and a new movement is accepted only if these two vectors include an angle of at least 45 degrees.
In case the input velocity also has an angular part, the control is not implemented using the scalar product, but the information about the angular and linear velocity are used to calculate the future position of the turtle in the next period (defined by the rate) and it is checked whether the future distance between the turtles will be greater or less than the initial one, the movement is allowed only in the first case mentioned.
If one of the two turtles gets too close to the boundaries, the problem is approached in a different way, the turtle's velocity will be reversed and it will start to go backwards until it stops.

Istruction to install and run the software:

Get into ROS workspace, in the src folder, and clone the repo with the given url:

	cd ~/<workspace_folder>/src
	git clone <repo-url> assignment1_rt

Now get back to the workspace folder:

	cd ..

Then, compile the workspace with te following command:

	catkin_make

If all is gone well, is possibile to run the software:
- First run the ROS master node

	roscore

- Open three new tabs and run following commands:

	rosrun turtlesim turtlesim_node
	rosrun assignment1_rt UI_node1
	rosrun assignment1_rt Distance_node2.py






