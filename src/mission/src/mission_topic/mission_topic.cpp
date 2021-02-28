#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include "mission/maintomission.h"
#include "mission/missiontomain.h"
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
using namespace std;

// #include "mission_setting.h"

#include "mission/mission_action.h"
// #include "mission/mission_action.h"
int ST1_rx = 9;
int ST2_rx = 8;
int ST1_tx = 88;
int ST2_tx = 99;
int state_ST1 = 0;
int state_ST2 = 0;
int state_planer = 0;
int state_mission;
int tx = 101;
int team;
class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        int action[10];
        int prepare;
        mission_setting(int num, string name, int no,  int pre){//int array[],
            mission_no = num;
            mission_name = name;
            count = no;
            // for( int i = 0; i < 10; i++){
            //     action[ i ] = array[ i ];
            // }
            prepare = pre;
            // setting_( num, name, count );
        }
}; mission_setting emergency(0, "emergency", 0, 0);//[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    mission_setting windsock( 1, "windsock", 0, 2);
    mission_setting lhouse(2, "lhouse", 0, 0);
    mission_setting flag( 3, "flag", 0, 0);
    mission_setting anchorN(4, "anchorN", 0, 0);
    mission_setting anchorS(5, "anchorS", 0, 0);
    mission_setting reef_l( 6, "reef_l", 0, 0);
    mission_setting reef_r( 7, "reef_r", 0, 0);
    mission_setting reef_p( 8, "reef_p", 0, 0);
    mission_setting placecup_h( 9, "placecup_h", 0, 0);
    mission_setting placecup_p( 10, "placecup_p", 0, 0);
    mission_setting placecup_r( 11, "placecup_r", 0, 0);
    mission_setting getcup(12, "getcup", 0, 0);
    mission_setting getcup_12( 13, "getcup_12", 0, 0);
    mission_setting getcup_34( 14, "getcup_34", 0, 0);


void chatterCallback_ST1(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard action: [%d]", msg->data[0]);
    state_ST1 = msg -> data[0] ;
}
void chatterCallback_ST2(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard action: [%d]", msg.data[0]);
    state_ST2 = msg -> data[0];
}
void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
//   ROS_INFO("I heard action: [%d]", msg->action);
  tx++;
  state_planer = msg->planer_state;
  team = msg->team;
  int success = 1, fail = 0, ing = 2, stop = 3;
  switch (msg->action)
  {
  case 0: //emergency
      state_mission = stop;
      break;
  case 1: //windsock
    if ( windsock.count < windsock.prepare){
        ST1_tx = action_1[windsock.count];
        ST2_tx = action_1[windsock.count];  
        if( state_ST2 == 1 && state_ST1 == 1){
            windsock.count ++; 
        }
    }
    else if (windsock.count >= windsock.prepare && state_planer == 1)
    {
        ST1_tx = action_1[windsock.count];
        ST2_tx = action_1[windsock.count];  
        if( state_ST2 == 1 && state_ST1 == 1){
            windsock.count ++; 
        }
    }
    ROS_INFO("windsock action: [%d]", action_1[windsock.count - 1]);  
    // ROS_INFO("debug windsock action: [%d]", action_1[4]);  
    if (windsock.count >= (sizeof(action_1)/sizeof(*action_1))){ //
        windsock.count = 0;
        state_mission = success;
        ROS_INFO("flag success");  
    }
    else{
        // ROS_INFO("debug windsock action: [%d], state = %d", windsock.count, state_mission);  
        state_mission = ing;
    }
    break;
  case 2: // lhouse
      state_mission = success;
      break;
  case 3: // flag
      state_mission = success;
      break;
  case 4: // anchorN
      state_mission = success;
      break;
  case 5: // anchorS
      state_mission = success;
      break;
  case 6: // reef_l
      state_mission = success;
      break;
  case 7: // reef_r
      state_mission = success;
      break;
  case 8: // reef_p
      state_mission = success;
      break;
  case 9: // placecup_h
      state_mission = success;
      break;
  case 10: // placecup_p 
      state_mission = success;
      break;
  case 11: // placecup_r
      state_mission = success;
      break;
  case 12: // getcup
      state_mission = success;
      break;
  case 13: // getcup12
      state_mission = success;
      break;
  case 14: // getcup34
      state_mission = success;
      break;
  default:
      break;
  }

}

int main(int argc, char **argv)
{
 
  ros::init(argc, argv, "mission");
  ros::NodeHandle n;

  ros::Publisher forST1 = n.advertise<std_msgs::Int32MultiArray>("for_ST1", 1);
  ros::Publisher forST2 = n.advertise<std_msgs::Int32MultiArray>("for_ST2", 1);
  // ros::Publisher forST1 = n.advertise<std_msgs::String>("forST1", 1);
  // ros::Publisher forST2 = n.advertise<std_msgs::String>("forST2", 1);
  ros::Publisher tomain = n.advertise<mission::missiontomain>("mission", 1);

  ros::Subscriber sub = n.subscribe("main", 1000, chatterCallback);
  ros::Subscriber subST1 = n.subscribe("ST1_to_mission", 1, chatterCallback_ST1);
  ros::Subscriber subST2 = n.subscribe("ST2_to_mission", 1, chatterCallback_ST2);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  ros::Rate loop_rate(10);

    int count = 0;
  while (ros::ok())
  {
    mission::missiontomain to_main;
    // to_main.state = state_mission;
    to_main.state = state_mission;
    tomain.publish(to_main);

    std_msgs::Int32MultiArray for_st1;
    for_st1.data.push_back(ST1_tx);
    for_st1.data.push_back(ST1_rx);
    std_msgs::Int32MultiArray for_st2;
    for_st2.data.push_back(ST2_tx);
    for_st2.data.push_back(ST2_rx);

    // std_msgs::String msg;

    // std::stringstream ss;
    // ss << "hello world " << ST1_tx + count;
    // msg.data = ss.str();

    // forST1.publish(msg);
    // forST2.publish(msg);
    forST1.publish(for_st1);
    forST2.publish(for_st2);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}