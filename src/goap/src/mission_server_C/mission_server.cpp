#include "ros/ros.h"
#include <stdio.h>


void mission()
{
    ROS_INFO("in void mission");
}

int main(int argc, char **argv)
{
    ros::init(argc, argv, "mission_server"); //初始化node
    ros::NodeHandle n; // node handler

    ros::ServiceServer service = n.advertiseService("mission", mission); //定義service server以及callback function
    ROS_INFO("Ready to add two ints.");
    ros::spin(); //持續運行此node
    // rospy.init_node('mission_big_server')
    // s = rospy.Service('mission_big', mission_srv, mission)
    // rospy.spin()         
    return 0;
   }