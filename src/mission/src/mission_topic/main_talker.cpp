#include "ros/ros.h"
#include "std_msgs/String.h"
#include "mission/maintomission.h"
#include "mission/missiontomain.h"
#include <sstream>

void chatterCallback(const mission::missiontomain::ConstPtr& msg)
{
  ROS_INFO("I heard mission state: [%d]", msg->state);
}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "main_talker");

  ros::NodeHandle n;

  ros::Publisher chatter_pub = n.advertise<mission::maintomission>("main", 1000);
  ros::Subscriber sub = n.subscribe("mission", 1000, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    mission::maintomission to_mission;
    // to_mission.action = 0 + count / 2;
    to_mission.action = 1;
    to_mission.action_pos = { 0, 0, 0 };
    to_mission.cup = {0};
    to_mission.hand = {0};
    to_mission.planer_state = 1;
    to_mission.team = 0;

    chatter_pub.publish(to_mission);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}