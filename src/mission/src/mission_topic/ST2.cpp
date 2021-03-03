#include "ros/ros.h"
#include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <sstream>

int ST2_rx = 9;
int ST2_tx = 88;
int state = 1;
void chatterCallback(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    state = 1;
    // ROS_INFO("I heard action: [%d]", msg.data[0]);
}
int main(int argc, char **argv)
{
  ros::init(argc, argv, "ST2");

  ros::NodeHandle n;

  ros::Publisher ST2tomission = n.advertise<std_msgs::Int32MultiArray>("ST2ToMission", 1);
  ros::Subscriber sub = n.subscribe("MissionToST2", 1, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    std_msgs::Int32MultiArray for_mission;
    for_mission.data.push_back(state);
    // for_mission.data.push_back(ST2_rx);

    ST2tomission.publish(for_mission);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}