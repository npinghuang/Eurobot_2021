#include "ros/ros.h"
#include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include <sstream>

int planer_rx = 9;
int planer_tx = 88;
int state = 0;
void chatterCallback(const std_msgs::Float32MultiArray::ConstPtr& msg)
{
    state = 1;
    // ROS_INFO("I heard action:");
}
int main(int argc, char **argv)
{
  ros::init(argc, argv, "planer");

  ros::NodeHandle n;

  ros::Publisher planertomission = n.advertise<std_msgs::Int32MultiArray>("planerToMission", 1);
  ros::Subscriber sub = n.subscribe("MissionToplaner", 1, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::Int32MultiArray for_mission;
    for_mission.data.push_back(state);
    // for_mission.data.push_back(state + 1);

    planertomission.publish(for_mission);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}