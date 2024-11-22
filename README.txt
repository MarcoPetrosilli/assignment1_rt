The node 1 has been implemented in c++, instead the node 2 has been implemented in python.
Following the requests, node 1 implements the textual UI to allow the user to select the turtle and provide values for velocities, the linear one along the x and y axes and the angular one alon the z axis.
In node 1 has been implemented also a control to be sure that user's choice is only about turtle 1 or turtle 2, hasn't been implemented instead controls on velocities input.
In node 2 is stored the distance computation logic, in order to stop turtles if too close to each other, and the boundaries control, the turtle will react in differnt ways in these two cases.
If a turtle get too much close to the other it will be stopped, and other velocities given to its will be accepted only if 
