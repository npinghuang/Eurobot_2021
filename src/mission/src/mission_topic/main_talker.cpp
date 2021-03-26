#include "ros/ros.h"
#include "std_msgs/String.h"
#include "mission/maintomission.h"
#include <std_msgs/Int32MultiArray.h>
// #include "mission/missiontomain.h"
#include <sstream>

int state_mission;
int mission_var = 1;
void chatterCallback(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
  ROS_INFO("I heard mission state: [%d]", msg-> data[0]);
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
    // to_mission.action = 0 + count / 2;
    // mission_var = 6;
    // to_mission.action = mission_var;
    int input;
    
    
    // if ( mode == 1){
    //   ROS_INFO( "action = ");
    //   scanf (" %d", &input);  
    //   to_mission.action =  input;
    //   if ( input == 12 || input == 13 || input == 14){
    //   int a ,b;
    //   ROS_INFO( "hand a b = ");
    //   scanf (" %d %d", &a, &b);  
    //   to_mission.hand = {a,b};
    //   }
    //   else{
    //     to_mission.hand = {1,2};
    //   }
    // }  
    // else if ( mode == 2 ){
    //   to_mission.action =  11;
    //   to_mission.hand = {3,4};
    // }
    to_mission.action =  12;
    to_mission.hand = {3,4};
    to_mission.action_pos = { 0, 0, 0 };
    to_mission.cup = {1,2};
    to_mission.NS = false;
    to_mission.reef = {0,1,0,1,0};
    to_mission.planer_state = 1;
    to_mission.team = 0;

    chatter_pub.publish(to_mission);
    if ( state_mission == 1){
      mission_var = 11;
      // if ( mission_var == 15){
      //   mission_var = 12;
      // }
    }
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}