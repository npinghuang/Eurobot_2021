#include <ros/ros.h>

#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "nav_msgs/Odometry.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

int main(int argc, char** argv){
    ros::init(argc, argv, "location_node");
    ros::NodeHandle n;

    ros::Publisher pub_enemy1 = n.advertise<geometry_msgs::PoseStamped>("/enemy_pose", 1000);
    ros::Publisher pub_enemy2 = n.advertise<geometry_msgs::PoseStamped>("/enemy_pose2", 1000);
    ros::Publisher pub_location = n.advertise<nav_msgs::Odometry>("/global_filter", 1000);

    geometry_msgs::PoseStamped enemy1;
    geometry_msgs::PoseStamped enemy2;
    nav_msgs::Odometry location;

    while (ros::ok())
    {
        ROS_INFO("LOCATION");
        location.pose.pose.position.x = 1.3;
        location.pose.pose.position.y = 0.9;
        location.pose.pose.position.z = 0;
        location.pose.pose.orientation.x = 0;
        location.pose.pose.orientation.y = 0;
        location.pose.pose.orientation.z = 0;
        location.pose.pose.orientation.w = 1;
        ROS_INFO("PUB");
        pub_location.publish(location);
    }

    return 0;
}