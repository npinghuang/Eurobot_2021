#include "ros/ros.h"
#include "std_msgs/String.h"
#include "mission/maintomission.h"
#include "mission/missiontomain.h"
#include <sstream>

int state_mission;
int mission_var = 1;
void chatterCallback(const mission::missiontomain::ConstPtr& msg)
{
  ROS_INFO("I heard mission state: [%d]", msg->state);
  state_mission = msg -> state;
}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "main_talker");

  ros::NodeHandle n;

  ros::Publisher chatter_pub = n.advertise<mission::maintomission>("MainToMission", 1000);
  ros::Subscriber sub = n.subscribe("MissionToMain", 1000, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    mission::maintomission to_mission;
    // to_mission.action = 0 + count / 2;
    // to_mission.action = mission_var;
    to_mission.action = 14;
    to_mission.action_pos = { 0, 0, 0 };
    to_mission.cup = {1,2};
    to_mission.hand = {1,2};
    to_mission.planer_state = 1;
    to_mission.team = 0;

    chatter_pub.publish(to_mission);
    if ( state_mission == 1){
      mission_var++;
      if ( mission_var == 2){
        mission_var = 1;
      }
    }
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}