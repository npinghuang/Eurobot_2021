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
mission::missiontomain to_main;
std_msgs::Float32MultiArray for_planer;
float planer_rx = 9;
int ST2_rx = 8;
int initialize = 1;
// int planer_tx = 88;
std::vector<int> hand{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
std::vector<float> planer_tx{0,0,0};
std::vector<int> ST2_tx{0,0,0};

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

int hand_ST2( int num){ // due to different numbering between ST2 and GOAP
    int hand; 
    switch (num)
    {
        // claw
    case 1://frontleft
        hand = 1;
        break;
    case 2://front right
        hand = 0;
        break;
    case 3: // back left
        hand = 7;
        break;
    case 4:// back right
        hand = 6;
        break;
    // suction servo hand
    case 5:// front left up 
        hand = 5;
        break;
    case 6:// front left down
        hand = 3;
        break;
    case 7:// front right up 
        hand = 4;
        break;
    case 8:// front right down
        hand = 2;
        break;
    case 9:// back left up
        hand = 11;
        break;
    case 10: //back left down
        hand = 9;
        break;
    case 11:// back right up
        hand = 10;
        break;
    case 12:// back right down
        hand = 8;
        break;
    default:
        hand = -1;
        break;
    }
    return hand;
}
void publish_ST2(){
    for ( int i = 0; i < 3; i++){
        for_st2.data.push_back(ST2_tx[i]);
        // ROS_INFO("publish in for %d ", ST2_tx[i]);
    }
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
void planer_tx_transform( float x, float y, float theta){
    planer_tx[0] = x;
    planer_tx[1] = y;
    planer_tx[2] = theta;
    publish_planner();
}
void ST2_tx_transform_outterhand( int hand, bool suck, int degree){
    ST2_tx[0] = pow(2,hand);
    ST2_tx[1] = suck;
    ST2_tx[2] = degree;
    ROS_INFO("outterhand: hand = [%d], suck = [%d], degree = [%d]", hand, suck, degree);
    publish_ST2();
}
void ST2_tx_transform_innerhand( int hand1, int hand2, bool suck){
    if ( hand2 == -1){
        ST2_tx[0] =  pow(2,hand1);   
    }
    else if ( hand2 == 0 || hand2 == 1){
        ST2_tx[0] = 3;
    }
    else if ( hand2 == 6 || hand2 == 7){
        ST2_tx[0] =  pow(2,hand1) +  pow(2,hand2);
    }
    ST2_tx[1] = suck;
    ST2_tx[2] = 0;
    ROS_INFO("innerhand: hand = [%d, %d], suck = [%d], hand ST2 [%d]", hand1, hand2, suck, ST2_tx[0]);
    publish_ST2();
}
void placecup(int hand, int degree){
    // int h = 0;
    // for ( int i = 0; i < 4; i++){
    //     if ( hand[i] != -1){
    //         h += 2^hand[i];
    //     }
    // }
    ST2_tx[0] = hand;
    ST2_tx[1] = 0;
    ST2_tx[2] = degree;
    ROS_INFO("placecup %d %d %d", ST2_tx[0], ST2_tx[1], ST2_tx[2]);
    publish_ST2();
}
int cup_color(int num){
    if ( num == 1 || num == 3 || num == 6 ||num == 8 || num ==10 || num == 12 || num ==13 || num ==16 ){
        return 1;
    }
    else if ( num == 2 || num == 4 || num == 5 ||num == 7 || num == 9 || num == 11 || num ==14 || num ==15 ){
        return 2;
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
  int success = 1, fail = 0, ing = 2, stop = 3;
  if ( initialize == 1){
      init();
      initialize = 0;
  }

  switch (msg->action)
  {
  case 0: //emergency
      state_mission = stop;
      break;
  case 1: {//windsock
    if ( windsock.count < windsock.prepare){
        ROS_INFO("before at pos count [%d]", windsock.count);
        if (action1[windsock.count] == 2){
            ST2_tx[0] = action1_ST2_blue[windsock.count_ST2];  
            publish_ST2();
        }
        if ( state_ST2 == 1){
            windsock.count++;
            windsock.count_ST2++;
        }
    }
    
    else if ( windsock.count >= windsock.prepare && state_planer == 1){
        ROS_INFO("at pos count [%d]", windsock.count);
        switch (action1[windsock.count]){
        case 1:{
            for (int i = 0; i < 3;  i++) {
                if ( team == 0 ){
                    planer_tx[i] = action1_planer_blue[windsock.count_planer][i];
                }
            }
            windsock.count++;
            windsock.count_planer++;
           publish_planner(); 
            break;
        }
        case 2:{
            windsock.count++;
            windsock.count_ST2++;
            break;
        }
        default:
            break;
        }
        // ROS_INFO("windsock action: [%f]", planer_tx[0]);  
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
    }
    break;
    }
  case 2:{ // lhouse
    if ( state_planer == 1){
        if ( msg->team == 0){
            planer_tx_transform( action2_planer_blue[lhouse.count][0], action2_planer_blue[lhouse.count][1], action2_planer_blue[lhouse.count][2]);
        }
        else if ( msg->team == 1){
            planer_tx_transform( action2_planer_yellow[lhouse.count][0], action2_planer_yellow[lhouse.count][1], action2_planer_yellow[lhouse.count][2]);
        }
        lhouse.count++;
        
    }
    if ( lhouse.count >= action2_planer_blue.size()){
            lhouse.count = 0;
            state_mission = success;
        }
    else{
    // ROS_INFO("debug windsock action: [%d], state = %d", windsock.count, state_mission);  
        state_mission = ing;
    }    
    break;
    }
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
  case 9: {// placecup_h
  // place 4 or 2 cup at the same time and need to cordinate with planer
  // uses numbering of chiao min's
    int count_p = 0;
    int hd = 0;
    ROS_INFO("wtf state st2 %d", state_ST2);
    state_ST2 = 1;
    while (count_p <= 3)
    {
        // ROS_INFO("wtf %d", count_p);
        state_mission = ing;
        if ( state_ST2 == 1){ // need to add planer state later on
            for ( int i = 0; i < 4; i++){
                if ( placecup_hand[count_p][i] != -1){
                    hd += pow(2, placecup_hand[count_p][i]);
                    // ROS_INFO("wtf %d %d", count_p, hd);
                }
            }
            // int *tmp = &(placecup_theta[count_p]);
            int tmp = placecup_theta.at(count_p);
            // ROS_INFO("debug %d, at: %d", placecup_theta[count_p], placecup_theta.at(count_p));
            // placecup( hd, tmp);
            placecup( hd, placecup_theta[count_p]);
            ROS_INFO("in case %d %d %d", ST2_tx[0], ST2_tx[1], ST2_tx[2]);
            count_p ++;
        }
    }
    count_p = 0;
    state_mission = success;
    break;
    }
  case 10: // placecup_p 
      state_mission = success;
      break;
  case 11: // placecup_r
      state_mission = success;
      break;
  case 12:{ // getcup
    int degree;
    degree = 0;
    degree = degree_transform(degree);
    int handd;
    if ( state_planer == 1){
        if ( msg->hand[0] < 4 ){
            // handd = hand_ST2( msg -> hand[0]);
            ST2_tx_transform_innerhand( hand_ST2( msg -> hand[0]), -1, true); 
        }
        else if ( msg->hand[0] >= 4){
            // handd = hand_ST2( msg -> hand[0]);
            ST2_tx_transform_outterhand( hand_ST2( msg -> hand[0]), true, degree);     
        }
    }   
    if (state_ST2 == 1){
        state_mission = success;    
        hand[msg->hand[0]] = cup_color( msg->cup[0]);
        // ROS_INFO("debug %d, %d, %d",msg->hand[0], msg->cup[0],  hand[msg->hand[0]]);
    }
    else if ( state_ST2 == 0 or state_planer == 0){
        state_mission = ing;
    }
    break;
    }
  case 13: {// getcup12
  int handd[2];
    if ( state_planer == 1){
        handd[0] = hand_ST2( msg -> hand[0]);
        handd[1] = hand_ST2 ( msg-> hand[1]);
        ST2_tx_transform_innerhand( handd[0], handd[1], true); 
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
      }
    case 14:{ // getcup34
        int handd[2];
        if ( state_planer == 1){
            handd[0] = hand_ST2( msg -> hand[0]);
            handd[1] = hand_ST2 ( msg-> hand[1]);
            ST2_tx_transform_innerhand( handd[0], handd[1], true); 
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
            // ROS_INFO("debug %d, %d, %d",msg->hand[0], msg->cup[0],  hand[msg->hand[0]]);
        }
        else if ( state_ST2 == 0 or state_planer == 0 ){
            state_mission = ing;
        }
      break;
      }
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
tomain = n.advertise<mission::missiontomain>("MissionToMain", 1);
sub = n.subscribe("MainToMission", 1000, chatterCallback);
subplaner = n.subscribe("planerToMission", 1000, chatterCallback_planer);
subST2 = n.subscribe("ST2ToMission", 1000, chatterCallback_ST2);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
ros::Rate loop_rate(10);

    int count = 0;
  while (ros::ok())
  {
    
    // to_main.state = state_mission;
    to_main.state = state_mission;
    tomain.publish(to_main);
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}