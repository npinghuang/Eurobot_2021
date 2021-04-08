#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include<geometry_msgs/PoseStamped.h>
#include "main2021/maintomission.h"

#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
using namespace std;
std_msgs::Int32MultiArray to_main;
int state_mission = 0;
int timestep = 1;
void chatterCallback(const main2021::maintomission::ConstPtr& msg)
{
    state_mission = 1;
}

int main(int argc, char **argv)
{
to_main.data = {2, 1};
ros::init(argc, argv, "mission");
ros::NodeHandle n;

ros::Publisher tomain = n.advertise<std_msgs::Int32MultiArray>("missionToMain", 10);
ros::Subscriber sub = n.subscribe("mainToMission", 100, chatterCallback);

ros::Rate loop_rate(10);


  while (ros::ok())
  {

    to_main.data[0]=state_mission;
    to_main.data[1]=timestep;
    timestep ++;
    tomain.publish(to_main);

    ros::spinOnce();

    loop_rate.sleep();

  }


  return 0;
}