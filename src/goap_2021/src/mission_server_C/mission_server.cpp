#include "ros/ros.h"
#include <ros/package.h> //not sure if needed

#include <stdio.h>
#include <iostream>
#include <string>

#include <goap_2021/mission_srv.h> // the header file generated from the srv file that we created earlier

// must use bool
bool mission(goap_2021::mission_srv::Request  &req,
         goap_2021::mission_srv::Response &res){
    // ROS_INFO("in void mission");
    int state = 0;
    state = req.action[0] + req.cup[0];
    res.state = state;
    ROS_INFO("in bool mission state = %d",  state);
    return true;
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "mission_server"); 
    ros::NodeHandle n; // node handler

    ros::ServiceServer service = n.advertiseService("mission", mission); 
    ROS_INFO("mission initialize\n");
    ros::spin(); 
  
    return 0;
   }

