#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include<geometry_msgs/PoseStamped.h>
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
float planer_rx = 9;
int ST2_rx = 8;
// int planer_tx = 88;
std::vector<int> hand{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
std::vector<float> planer_tx{0,0,0};
int ST2_tx = 99;
int state_planer = 0;
int state_ST2 = 0;
int state_mission;
int tx = 101;
int team;
bool publish_planer;
class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        int count_planer = 0;
        int count_ST2 = 0;
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
    mission_setting lhouse(2, "lhouse", 0, 2);
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
void planer_tx_transform( float x, float y, float theta){
    planer_tx[0] = x;
    planer_tx[1] = y;
    planer_tx[2] = theta;
}
void ST2_tx_transform_outterhand( int hand, bool suck, float degree){
    ST2_tx = hand;
    ROS_INFO("outterhand: hand = [%d], suck = [%d], degree = [%f]", hand, suck, degree);
}
void ST2_tx_transform_innerhand( int hand1, int hand2, bool suck){
    ST2_tx = hand1;
    ROS_INFO("innerhand: hand = [%d, %d], suck = [%d]", hand1, hand2, suck);
}

int cup_color(int num){
    if ( num == 1 || num == 3 || num == 6 ||num == 8 || num ==10 || num == 12 || num ==13 || num ==16 ){
        return 1;
    }
    else if ( num == 2 || num == 4 || num == 5 ||num == 7 || num == 9 || num == 11 || num ==14 || num ==15 ){
        return 2;
    }
}
void chatterCallback_planer(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard action: [%d]", msg->data[0]);
    state_planer = msg -> data[0] ;
}
void chatterCallback_ST2(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard action: [%d]", msg.data[0]);
    state_ST2 = msg -> data[0];
}
void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
  ROS_INFO("I heard action: [%d]", msg->action);
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
        // planer_tx = action_1[windsock.count];
        // ST2_tx = action_1[windsock.count];  
        for (int i = 0; i < 3; i++) {
            if ( team == 0 ){
                planer_tx[i] = action1_planer_blue[windsock.count_planer][i];
            }
            else if ( team == 1 ){
                planer_tx[i] = action1_planer_yellow[windsock.count_planer][i];
            }
        }
        // ROS_INFO("debug h[ %2f ]", action1_planer_blue[0][0]);
        // ROS_INFO("debug main[ %2f]", planer_tx[0]);
        ST2_tx = action1_ST2_blue[windsock.count_ST2];  
        if( state_ST2 == 1 && state_planer == 1){
            windsock.count ++; 
        }
    }
    else if (windsock.count >= windsock.prepare && state_planer == 1)
    {
        for (int i = 0; i < 3; i++) {
            if ( team == 0 ){
                planer_tx[i] = action1_planer_blue[windsock.count_planer][i];
            }
            else if ( team == 1 ){
                planer_tx[i] = action1_planer_yellow[windsock.count_planer][i];
            }
        }
        ST2_tx = action1_ST2_blue[windsock.count_ST2];  
        if( state_ST2 == 1 && state_planer == 1){
            windsock.count ++; 
        }
    }
    ROS_INFO("windsock action: [%f]", planer_tx[0]);  
    // ROS_INFO("debug windsock action: [%d]", action_1[4]);  
    if (windsock.count >= action1.size()){ //
        windsock.count = 0;
        windsock.count_planer = 0;
        windsock.count_ST2 = 0;
        state_mission = success;
        // ROS_INFO("flag success");  
    }
    else{
        // ROS_INFO("debug windsock action: [%d], state = %d", windsock.count, state_mission);  
        state_mission = ing;
    }
    break;
  case 2: // lhouse
    if ( lhouse.count < lhouse.prepare){
        ROS_INFO("before at pos count [%d]", lhouse.count);
        if (action2[lhouse.count] == 2){
            ST2_tx = action1_ST2_blue[lhouse.count_ST2];  
        }
        if ( state_ST2 == 1){
            lhouse.count++;
            lhouse.count_ST2++;
        }
    }
    
    else if ( lhouse.count >= lhouse.prepare && state_planer == 1){
        ROS_INFO("at pos count [%d]", lhouse.count);
        switch (action2[lhouse.count]){
        case 1:
            for (int i = 0; i < 3; i++) {
                if ( team == 0 ){
                    planer_tx[i] = action2_planer_blue[lhouse.count_planer][i];
                }
                else if ( team == 1 ){
                    planer_tx[i] = action2_planer_yellow[lhouse.count_planer][i];
                }
            }
            if ( state_planer == 1){
                lhouse.count++;
                lhouse.count_planer++;
            }
            break;
        case 2:
            ST2_tx = action1_ST2_blue[lhouse.count_ST2];  
            if ( state_ST2 == 1){
                lhouse.count++;
                lhouse.count_ST2++;
            }
            break;
        default:
            break;
        }
        ROS_INFO("lhouse action: [%f]", planer_tx[0]);  
    // ROS_INFO("debug lhouse action: [%d]", action_1[4]);  
        if (lhouse.count >= action2.size()){ //
            lhouse.count = 0;
            lhouse.count_planer = 0;
            lhouse.count_ST2 = 0;
            state_mission = success;
            // ROS_INFO("flag success");  
        }
        else{
        // ROS_INFO("debug windsock action: [%d], state = %d", windsock.count, state_mission);  
            state_mission = ing;
        }
    }
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
    int degree;
    degree = 0;
    if ( state_planer == 1){
        if ( msg->hand[0] < 4 ){
            ST2_tx_transform_innerhand( msg->hand[0], -1, true); 
        }
        else if ( msg->hand[0] >= 4){
            ST2_tx_transform_outterhand( msg->hand[0], true, degree);     
        }
    }   
    if (state_ST2 == 1){
        state_mission = success;    
        hand[msg->hand[0]] = cup_color( msg->cup[0]);
    }
    else if ( state_ST2 == 0 or state_planer == 0){
        state_mission = ing;
    }
    break;
  case 13: // getcup12
    if ( state_planer == 1){
            ST2_tx_transform_innerhand( msg->hand[0], msg->hand[1], true); 
        } 
    if (state_ST2 == 1){
        state_mission = success;    
        hand[msg->hand[0]] = cup_color( msg->cup[0]);
        hand[msg->hand[1]] = cup_color( msg->cup[1]);
    }
    else if ( state_ST2 == 0 or state_planer == 0 ){
        state_mission = ing;
        } 
    if (state_ST2 == 1){
        state_mission = success;    
        hand[msg->hand[0]] = cup_color( msg->cup[0]);
        hand[msg->hand[1]] = cup_color( msg->cup[1]);
    }
    else if ( state_ST2 == 0 or state_planer == 0 ){
        state_mission = ing;
    }
      break;
  default:
      break;
  }

}

int main(int argc, char **argv)
{
 
ros::init(argc, argv, "mission");
ros::NodeHandle n;

ros::Publisher forplaner = n.advertise<std_msgs::Float32MultiArray>("MissionToplaner", 1);
ros::Publisher forST2 = n.advertise<std_msgs::Int32MultiArray>("MissionToST2", 1);
ros::Publisher forST2com = n.advertise<std_msgs::Int32MultiArray>("txST1", 1);
// ros::Publisher forNavigation = n.advertise<geometry_msgs::PoseStamped>("move_base_simple/goal", 1);
// ros::Publisher forplaner = n.advertise<std_msgs::String>("forplaner", 1);
// ros::Publisher forST2 = n.advertise<std_msgs::String>("forST2", 1);
ros::Publisher tomain = n.advertise<mission::missiontomain>("MissionToMain", 1);
ros::Subscriber sub = n.subscribe("MainToMission", 1, chatterCallback);
ros::Subscriber subplaner = n.subscribe("planerToMission", 1, chatterCallback_planer);
ros::Subscriber subST2 = n.subscribe("ST2ToMission", 1, chatterCallback_ST2);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
ros::Rate loop_rate(10);

    int count = 0;
  while (ros::ok())
  {
    mission::missiontomain to_main;
    // to_main.state = state_mission;
    to_main.state = state_mission;
    tomain.publish(to_main);

    std_msgs::Float32MultiArray for_planer;
    // ROS_INFO("debug windsock action: [%f]", planer_tx[0]);  
    for_planer.data.push_back(planer_tx[0]);
    for_planer.data.push_back(planer_tx[1]);
    for_planer.data.push_back(planer_tx[2]);
    std_msgs::Int32MultiArray for_st2;
    for_st2.data.push_back(ST2_tx);
    // for_st2.data.push_back(ST2_rx);

    // std_msgs::String msg;

    // std::stringstream ss;
    // ss << "hello world " << planer_tx + count;
    // msg.data = ss.str();

    // forplaner.publish(msg);
    // forST2.publish(msg);
    forplaner.publish(for_planer);
    forST2.publish(for_st2);

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}