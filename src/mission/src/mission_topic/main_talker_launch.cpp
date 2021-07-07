#include "ros/ros.h"
#include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include "mission/maintomission.h"
// #include "mission/missiontomain.h"
#include <sstream>
#include<vector>
int state_mission;
int mission_var = 1;
const std::vector<std::vector<int>> cup_pos_all{
    { 400, 300 }, {1200, 300}, {1200, 300 }, {1085, 445 },
    { 100, 670 }, {400, 956}, {1955, 1005}, { 1655, 1065 },
    { 800, 1100 }, { 1200, 1270 }, { 1655, 1335 }, { 1955, 1395 },
    { 1955, 1605 }, { 1655, 1665 }, { 1200, 1730 }, {800, 1900},
    {1655, 1935 }, { 1955, 1995 }, { 400, 2044 }, { 100, 2330 },
    { 515, 2555 }, { 1085, 2555 }, { 400, 2700 }, { 1200, 2700 }
};
std::vector<int> cup_pos;
void chatterCallback(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
  ROS_INFO("I heard mission state: [%d]", msg->data[0]);
  state_mission = msg -> data[0];
}

int main(int argc, char **argv)
{

  ros::init(argc, argv, "main_talker");

  ros::NodeHandle n;

  ros::Publisher chatter_pub = n.advertise<mission::maintomission>("mainToMission", 100);
  ros::Subscriber sub = n.subscribe("missionToMain", 10, chatterCallback);
  ros::Rate loop_rate(10);
  int mode;
  int count = 0;
  // ROS_INFO( " mode 1 key in action; 2 fix action = ");
  // scanf ("%d", &mode);
  while (ros::ok())
  {
    mission::maintomission to_mission;
    int input;
    int param, hand1_param, hand2_param, cup_param;
    n.getParam("/mission_param", param);  
    n.getParam("/hand1", hand1_param);
    n.getParam("/hand2", hand2_param);    
    n.getParam("/cup_no", cup_param);    
    cup_pos = cup_pos_all[cup_param - 1];
    to_mission.action =  param;
    to_mission.hand = {hand1_param, cup_param};//, cup_pos[0], cup_pos[1]
    to_mission.action_pos = { 0, 0, 3.14 };
    to_mission.cup = { cup_param, hand1_param};
    // to_mission.cup = { 25, 2};
    to_mission.NS = false;
    to_mission.reef = {1,1,0,1,0,0,1,0,1,1};
    to_mission.planer_state = 1;
    to_mission.team = 0;

    chatter_pub.publish(to_mission);
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}