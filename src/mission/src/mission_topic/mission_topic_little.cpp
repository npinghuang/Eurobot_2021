#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
// #include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Float32MultiArray.h>
#include<geometry_msgs/PoseStamped.h>
#include "mission/maintomission.h"
#include <std_msgs/Int32.h>
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
#include<math.h>
using namespace std;

#include "mission/mission_action.h"
ros::Publisher tomain;
ros::Publisher forST2;
ros::Publisher forplaner;
std_msgs::Int32MultiArray for_st2;
ros::Publisher forST2com;
ros::Subscriber sub;
ros::Subscriber subplaner;
ros::Subscriber subST2;
std_msgs::Int32 to_main;
std_msgs::Float32MultiArray for_planer;
float planer_rx = 9;
int ST2_rx = 8;
int initialize = 1;
// int planer_tx = 88;
std::vector<int> hand{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
std::vector<float> planer_tx{0,0,0};
std::vector<int> ST2_tx{0,0,0};
std::vector<int> claw{0,0,0,0,0};
std::vector<int> claw_color{0,0,0,0,0};
std::vector<int> reefl_color{2, 3, 2, 3, 2};
std::vector<int> reefr_color{3, 2, 3, 2, 3};
std::vector<int> reefp_color{2, 3, 2, 3, 2};
std::vector<int> reef_null{0, 0, 0, 0, 0};
int state_planer = 0;
int state_ST2 = 0;
int state_mission;
int success = 1, fail = 0, ing = 2, stop = 3;
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
    mission_setting windsock( 1, "windsock", 0, 1);
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

void publish_ST2( int platform, int servo, int claw){
    ST2_tx[0] = platform;// up down of platform
    ST2_tx[1] = servo;//windsock servo and tightness servo
    ST2_tx[2] = claw;// determine servos open or close
    for ( int i = 0; i < 3; i++){
        for_st2.data.push_back(ST2_tx[i]);
        // ROS_INFO("publish in for %d ", ST2_tx[i]);
    }
    ROS_INFO("publish ST2 %d %d %d", ST2_tx[0],  ST2_tx[1], ST2_tx[2]);
    forST2.publish(for_st2);
    ST2_tx.clear(); 
    for_st2.data.clear(); 
}
void publish_planner(){
    for_planer.data.push_back(planer_tx[0]);
    for_planer.data.push_back(planer_tx[1]);
    for_planer.data.push_back(planer_tx[2]);
    forplaner.publish(for_planer);
    for_planer.data.clear();
}
int claw_trans( std::vector<int> &vector ){
    int temp = 0;
    for ( int i = 0; i < vector.size(); i++){
        if ( vector[i] == 1){
            temp += pow( 2, i );
        }
    }
    ROS_INFO(" check %d", temp);
    return temp;
}
void claw_action(int color, int state, std::vector<int> &reef_color){
    switch (state)
    {
    case 0:{ // placecup depending on color determine which claw to open
        for ( int i = 0; i < claw_color.size(); i++){
            if ( claw_color[i] == color){
                claw[i] = 1;
                claw_color[i] = reef_color[i];
                ROS_INFO("claw action servo :%d action : %d", i, claw[i] );
            }
            ROS_INFO("claw color %d", reef_color[i] );
        }
        break;
    }
    case 1:{ // getcup
        for ( int i = 0; i < claw.size(); i++){
            claw[i] = 0; // 0 for close 1 for open 
            claw_color[i] = reef_color[i];
            ROS_INFO("claw color %d", reef_color[i] );
        }
        break;
    }
    default:
        break;
    }
    
    if ( state_planer == 1){
        int hd = claw_trans(claw);
        publish_ST2( 3, 2, hd);
    }
    if ( state_ST2 == 1){
        state_mission = success;
        // for ( int i = 0; i < reef_color.size(); i++){
        //     claw_color[i] = reef_color[i];
        //     ROS_INFO("claw color %d", reef_color[i] );
        // }
    }
    else{
        state_mission = ing;
    }
}

int degree_transform( int d ){
    int theta;
    theta = d;
    return theta;
}
void init(){
    ROS_INFO("initialize");
}

void chatterCallback_planer(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard action: [%d]", msg->data[0]);
    state_planer = msg -> data[0] ;
}
void chatterCallback_ST2(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard ST2: [%d]", msg->data[0]);
    state_ST2 = msg -> data[0];
}
void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
  ROS_INFO("I heard action: [%d]", msg->action);
  tx++;
  state_planer = msg->planer_state;
  team = msg->team;
  
  if ( initialize == 1){
      init();
      initialize = 0;
  }
  switch (msg->action)
  {
  case 0: //emergency
      state_mission = stop;
      break;
//   case 1: {//windsock
//     if ( windsock.count < windsock.prepare){
//         ROS_INFO("before at pos count [%d]", windsock.count);
//         if (action1[windsock.count] == 2){
//             ST2_tx[0] = action1_ST2_blue[windsock.count_ST2];  
//             publish_ST2();
//         }
//         if ( state_ST2 == 1){
//             windsock.count++;
//             windsock.count_ST2++;
//         }
//     }
    
//     else if ( windsock.count >= windsock.prepare && state_planer == 1){
//         ROS_INFO("at pos count [%d]", windsock.count);
//         switch (action1[windsock.count]){
//         case 1:{
//             for (int i = 0; i < 3;  i++) {
//                 if ( team == 0 ){
//                     planer_tx[i] = action1_planer_blue[windsock.count_planer][i];
//                 }
//             }
//             windsock.count++;
//             windsock.count_planer++;
//            publish_planner(); 
//             break;
//         }
//         case 2:{
//             windsock.count++;
//             windsock.count_ST2++;
//             break;
//         }
//         default:
//             break;
//         }
//         // ROS_INFO("windsock action: [%f]", planer_tx[0]);  
//     // ROS_INFO("debug windsock action: [%d]", action_1[4]);  
//         if (windsock.count >= action1.size()){ //
//             windsock.count = 0;
//             windsock.count_planer = 0;
//             windsock.count_ST2 = 0;
//             state_mission = success;
//             // ROS_INFO("flag success");  
//         }
//         else{claw_action(0,1, reefp_color);
//         }
//     }
//     break;
//     }
//   case 2:{ // lhouse
//     if ( state_planer == 1){
//         if ( msg->team == 0){
//             // planer_tx_transform( action2_planer_blue[lhouse.count][0], action2_planer_blue[lhouse.count][1], action2_planer_blue[lhouse.count][2]);
//         }
//         else if ( msg->team == 1){
//             // planer_tx_transform( action2_planer_yellow[lhouse.count][0], action2_planer_yellow[lhouse.count][1], action2_planer_yellow[lhouse.count][2]);
//         }
//         lhouse.count++;
        
//     }
//     if ( lhouse.count >= action2_planer_blue.size()){
//             lhouse.count = 0;
//             state_mission = success;
//         }
//     else{
//     // ROS_INFO("debug windsock action: [%d], state = %d", windsock.count, state_mission);  
//         state_mission = ing;
//     }    
//     break;
//     }
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
    claw_action(0,1, reefl_color);
    break;
  case 7: // reef_r
    claw_action(0,1, reefr_color);
      break;
  case 8: // reef_p
    claw_action(0,1, reefp_color);
      break;
  case 11: // placecup_r
    for ( int color = 2; color <= 3; color ++){
        claw_action(color, 0, reef_null);
    }
    
    //   state_mission = success;
      break;
  default:
      break;
  }
//   ROS_INFO("hand vector: ");
//     for( int i = 0; i < 13; i ++){
//         ROS_INFO("%d, ", hand[i]);
//     }
//     ROS_INFO("\n");
}

int main(int argc, char **argv)
{

ros::init(argc, argv, "mission");
ros::NodeHandle n;

forplaner = n.advertise<std_msgs::Float32MultiArray>("MissionToplaner", 1);
forST2 = n.advertise<std_msgs::Int32MultiArray>("MissionToST2", 1);
forST2com = n.advertise<std_msgs::Int32MultiArray>("txST1", 1);
// ros::Publisher forNavigation = n.advertise<geometry_msgs::PoseStamped>("move_base_simple/goal", 1);
// ros::Publisher forplaner = n.advertise<std_msgs::String>("forplaner", 1);
// ros::Publisher forST2 = n.advertise<std_msgs::String>("forST2", 1);
tomain = n.advertise<std_msgs::Int32>("MissionToMain", 100);
sub = n.subscribe("MainToMission", 1000, chatterCallback);
subplaner = n.subscribe("planerToMission", 1000, chatterCallback_planer);
subST2 = n.subscribe("ST2ToMission", 1000, chatterCallback_ST2);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
ros::Rate loop_rate(10);

    int count = 0;
  while (ros::ok())
  {
    
    // to_main.state = state_mission;
    to_main.data = state_mission;
    tomain.publish(to_main);
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}