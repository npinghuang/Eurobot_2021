#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include "goap_2021/maintomission.h"
#include "goap_2021/missiontomain.h"
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
using namespace std;

// #include "mission_setting.h"
#include "mission_action.h"

int ST1_rx = 9;
int ST2_rx = 8;
int ST1_tx = 88;
int ST2_tx = 99;
int tx = 101;
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
    mission_setting windsock( 1, "windsock", 0, 0);
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

int state;
void chatterCallback(const goap_2021::maintomission::ConstPtr& msg)
{
  ROS_INFO("I heard action: [%d]", msg->action);
  tx++;
  // ROS_INFO("222 %d", tx);
  int success = 1, fail = 0, ing = 2, stop = 3;
  switch (msg->action)
  {
  case 0: //emergency
      state = stop;

      break;
  case 1: //windsock
    ROS_INFO("windsock action: [%d]", action_1[windsock.count]);
    windsock.count ++;
    if (windsock.count >= (sizeof(action_1)/sizeof(*action_1))){ //
        windsock.count = 0;
    }
    // if (action_0[windsock.count] == NULL){ ///sizeof(*action_0)
    //     windsock.count = 0;
    // }
    // printf("%d", action_0[ windsock.count]);
    state = success;
    break;
  case 2: // lhouse
      state = success;
      break;
  case 3: // flag
      state = success;
      break;
  case 4: // anchorN
      state = success;
      break;
  case 5: // anchorS
      state = success;
      break;
  case 6: // reef_l
      state = success;
      break;
  case 7: // reef_r
      state = success;
      break;
  case 8: // reef_p
      state = success;
      break;
  case 9: // placecup_h
      state = success;
      break;
  case 10: // placecup_p 
      state = success;
      break;
  case 11: // placecup_r
      state = success;
      break;
  case 12: // getcup
      state = success;
      break;
  case 13: // getcup12
      state = success;
      break;
  case 14: // getcup34
      state = success;
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
  ros::Publisher tomain = n.advertise<goap_2021::missiontomain>("mission", 1);

  ros::Subscriber sub = n.subscribe("main", 1000, chatterCallback);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
  ros::Rate loop_rate(10);

    int count = 0;
  while (ros::ok())
  {
    goap_2021::missiontomain to_main;
    to_main.state = state;
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