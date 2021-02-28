#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include<geometry_msgs/PoseStamped.h>
#include "mission/maintomission.h"
#include "mission/missiontomain.h"
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
using namespace std;

int state_mission = 0;

void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
    state_mission = 1;
}

int main(int argc, char **argv)
{
 
ros::init(argc, argv, "mission");
ros::NodeHandle n;

ros::Publisher tomain = n.advertise<mission::missiontomain>("MissionToMain", 1);
ros::Subscriber sub = n.subscribe("MainToMission", 1, chatterCallback);

ros::Rate loop_rate(10);


  while (ros::ok())
  {
    mission::missiontomain to_main;

    to_main.state =  state_mission;
    tomain.publish(to_main);

    ros::spinOnce();

    loop_rate.sleep();

  }


  return 0;
}