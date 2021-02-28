#include "ros/ros.h"
#include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include <sstream>

int ST1_rx = 9;
int ST1_tx = 88;
int state = 0;
void chatterCallback(const std_msgs::Float32MultiArray::ConstPtr& msg)
{
    state = 1;
    // ROS_INFO("I heard action:");
}
int main(int argc, char **argv)
{
  ros::init(argc, argv, "ST1");

  ros::NodeHandle n;

  ros::Publisher ST1tomission = n.advertise<std_msgs::Int32MultiArray>("ST1ToMission", 1);
  ros::Subscriber sub = n.subscribe("MissionToST1", 1, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::Int32MultiArray for_mission;
    for_mission.data.push_back(state);
    // for_mission.data.push_back(state + 1);

    ST1tomission.publish(for_mission);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}