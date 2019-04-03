### Individual Submission

* Name: Ibrahim Hamed El-Shal
* Email: i.hamedelshal@gmail.com

### Contents

* [About Capstone Project](#About-Capstone-Project)
* [Implementation](#Implementation)
 	* [Waypoint Updater Node](#Waypoint-Updater-Node)
	* [Controllers](#Controllers)
	* [Waypoint Loader Node](#Waypoint-Loader-Node)
	* [Traffic Light Detection Node](#Traffic-Light-Detection-Node)

## About Capstone Project

This is the project repo for the final project of the Udacity Self-Driving Car Nanodegree: Programming a Real Self-Driving Car. For more information about the project, see the project introduction [here](https://classroom.udacity.com/nanodegrees/nd013/parts/6047fe34-d93c-4f50-8336-b70ef10cb4b2/modules/e1a23b06-329a-4684-a717-ad476f0d8dff/lessons/462c933d-9f24-42d3-8bdc-a08a5fc866e4/concepts/5ab4b122-83e6-436d-850f-9f4d26627fd9).

![](imgs/udacity-car.jpg)

The project is built using ROS nodes that communicate with each other using ros-topics as shown in the following figure:
![](imgs/final-project-ros-graph-v2.png)

### Project requirements
Using the Robot Operating System (ROS). This is the Capstone project for the Udacity Self-Driving Car Nanodegree. I developed software to guide a real self-driving car around a test track and created nodes for traffic light detection and classification, trajectory planning, and control. 

* Smoothly follows waypoints in the simulator.
* Respects the target top speed set for the waypoints' twist.twist.linear.x in waypoint_loader.py. Works by testing with different values for kph velocity parameter in /ros/src/waypoint_loader/launch/waypoint_loader.launch. 
* Stops at traffic lights when needed.
* Stops and restarts PID controllers depending on the state of /vehicle/dbw_enabled.
* Publishes throttle, steering, and brake commands at 50hz.
* The acceleration of the car should not exceed 10 m/s^2, and the jerk should not exceed 10 m/s^2.
* Launches correctly using the launch files provided in the capstone repo. 

### Implementation 

#### Waypoint Updater Node
Ros node is responsible for giving the simulator a list of points (Trajectory) for the next T seconds so that the car can follow. This node is responsible for the acceleration and the deceleration of the car. It accelerates as long as there is no red or yellow traffic in front of it, and decelerates otherwise. It subscribes to the base way points to follow the basic way points of the road for the mid lane. It also subscribes to the traffic waypoint to know the location of the traffic sign and its state to determine wheter the car will accelerate or decelerate.

#### Controllers
We use PID controller with low pass filtering over current linear velocity and stop accelearation for acceleration/breaking and a Udacity provided YawController for steering. PID controller that controls the throttle of the car. I used the P,I, and D configurations used in the PID project which are:
P = 0.3, I = 0.001 and D = 10.0

also set the maximum acceleration of the car to be 0.2.
The car fully stops if we apply a force of 700 N*m

#### Waypoint Loader Node
I set the maximum speed of the car to approximately 10MPH.
 
#### Traffic Light Detection Node
* Used open-cv to detect the traffic signs and its colors to obation the speed of classification. 
* Used computer-vision with the threshold values to get the red, yellow and green pixels in the traffic so that I can know if it is red, yellow or green sign.
* Model can classify the images with a very high acuracy due to the accuracy of the detection for the yellow traffic and classifying red, and green is much more easier 
because our image is RGB which means that it has the R component and G component that can be exctracted.

### Native Installation

* Be sure that your workstation is running Ubuntu 16.04 Xenial Xerus or Ubuntu 14.04 Trusty Tahir. [Ubuntu downloads can be found here](https://www.ubuntu.com/download/desktop).
* If using a Virtual Machine to install Ubuntu, use the following configuration as minimum:
  * 2 CPU
  * 2 GB system memory
  * 25 GB of free hard drive space

  The Udacity provided virtual machine has ROS and Dataspeed DBW already installed, so you can skip the next two steps if you are using this.

* Follow these instructions to install ROS
  * [ROS Kinetic](http://wiki.ros.org/kinetic/Installation/Ubuntu) if you have Ubuntu 16.04.
  * [ROS Indigo](http://wiki.ros.org/indigo/Installation/Ubuntu) if you have Ubuntu 14.04.
* [Dataspeed DBW](https://bitbucket.org/DataspeedInc/dbw_mkz_ros)
  * Use this option to install the SDK on a workstation that already has ROS installed: [One Line SDK Install (binary)](https://bitbucket.org/DataspeedInc/dbw_mkz_ros/src/81e63fcc335d7b64139d7482017d6a97b405e250/ROS_SETUP.md?fileviewer=file-view-default)
* Download the [Udacity Simulator](https://github.com/udacity/CarND-Capstone/releases).

### Docker Installation
[Install Docker](https://docs.docker.com/engine/installation/)

Build the docker container
```bash
docker build . -t capstone
```

Run the docker file
```bash
docker run -p 4567:4567 -v $PWD:/capstone -v /tmp/log:/root/.ros/ --rm -it capstone
```
### Usage

1. Clone the project repository
```bash
git clone https://github.com/ahmedmbakr/CarND-Capstone.git
```

2. Install python dependencies
```bash
cd CarND-Capstone
pip install -r requirements.txt
```

2.1 For Workspace Case 
```bash
sudo apt-get update
sudo apt-get install -y ros-kinetic-dbw-mkz-msgs
cd ros
rosdep install --from-paths src --ignore-src --rosdistro=kinetic -y
pip install --upgrade catkin_pkg_modules
```

3. Make and run styx
```bash
cd ros
catkin_make
source devel/setup.sh
roslaunch launch/styx.launch
```
4. Run the simulator

### Real world testing
1. Download [training bag](https://s3-us-west-1.amazonaws.com/udacity-selfdrivingcar/traffic_light_bag_file.zip) that was recorded on the Udacity self-driving car.
2. Unzip the file
```bash
unzip traffic_light_bag_file.zip
```
3. Play the bag file
```bash
rosbag play -l traffic_light_bag_file/traffic_light_training.bag
```
4. Launch your project in site mode
```bash
cd CarND-Capstone/ros
roslaunch launch/site.launch
```
5. Confirm that traffic light detection works on real life images
