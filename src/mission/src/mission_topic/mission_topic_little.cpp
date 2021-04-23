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

//1 for red 0 for green
//0 for N 1 for S
#include "mission/mission_action.h"
ros::Publisher tomain;
ros::Publisher forST2_little;
ros::Publisher forplaner;
std_msgs::Int32MultiArray for_ST2_little;
//time
ros::Time begin_time;
ros::Time now_time;
float doing_time;
float wait_sec = 0.0; //wait for big chicken 10.0
ros::Publisher forST2_littlecom;
ros::Subscriber sub;
ros::Subscriber subplaner;
ros::Subscriber subST2_little;
ros::Subscriber subST2_littlecom;
std_msgs::Int32MultiArray to_main;
std_msgs::Float32MultiArray for_planer;
float planer_rx = 9;
std::vector<int> ST2_little_rx{0,0,0,0,0,0,0,0,0};
int initialize = 1;
// int planer_tx = 88;
std::vector<int> hand{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
std::vector<float> planer_tx{0,0,0};
std::vector<int> ST2_little_tx{0,1,1,1,1,1,1,1,1};
std::vector<int> claw{0,0,0,0,0};
std::vector<int> claw_color{0,0,0,0,0};
// std::vector<int> reefl_color{2, 3, 2, 3, 2};
// std::vector<int> reefr_color{3, 2, 3, 2, 3};
std::vector<int> reefp_color{1,1,0,0,0};
std::vector<int> reef_null{0, 0, 0, 0, 0};
std::vector<int> old_command{0,0,0,0,0};// action, cup1, cup2, hand1, hand2

int state_planer = 0;
int state_ST2_little = 0;
int state_mission = 2;
int success = 1, fail = 0, ing = 2, stop = 3;
int tx = 101;
int team;
int data_len = 9;
int timestep = 1;
bool publish_planer;
class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        int count_planer = 0;
        int count_ST2_little = 0;
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
    mission_setting mission_wait( 31, "wait", 0, 0);
void publish_ST2_little(int platform, int servo, int claw ){//
    ST2_little_tx[0] = platform;// up down of platform
    ST2_little_tx[1] = servo;//windsock servo and tightness servo
    ST2_little_tx[2] = claw;// determine servos open or close
    // for ( int i = 0; i < 9; i++){
    //     for_ST2_little.data.push_back(ST2_little_tx[i]);
    //     // ROS_INFO("publish in for %d ", ST2_little_tx[i]);
    // }
    // ROS_INFO("publish ST2_little %d %d %d", ST2_little_tx[0],  ST2_little_tx[1], ST2_little_tx[2]);
    // forST2_little.publish(for_ST2_little);
    // // ST2_little_tx.clear(); 
    // for_ST2_little.data.clear(); 
}
bool checkST2_state(std::vector<int> &tx){
    // if st2 tx == rx
    int state = 1;
    for ( int i = 0; i < data_len; i++){
        ROS_INFO("check rx %d %d",i, ST2_little_rx[i]);
        if ( tx[i] != ST2_little_rx[i] ){ // return 3 from performing action
            state = 0;
            break;
        }
    }
    return state;
}
void do_nothing(){
    if ( state_planer == 1){
            state_mission = 1; //no action need to be done by ST2 so always return success
        }
    else{
        state_mission = ing;
    }
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
            ST2_little_tx[ 1+ i ] = 0;
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
        publish_ST2_little( 3, 2, hd);
    }
    if ( checkST2_state( {ST2_little_tx})  == 1){
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
    ST2_little_tx[0] = 0;
    for ( int i = 1; i < data_len; i++){
        ST2_little_tx[i] = 1;
    }
    ROS_INFO("initialize");
}
bool newaction(const mission::maintomission::ConstPtr& msg){
    if (old_command [0] == msg-> action &&
    old_command [1] == msg -> cup[0] &&
    old_command [2] == msg -> cup[1] &&
    old_command [3] == msg -> hand[0] &&
    old_command [4] == msg -> hand[1]){
        return false;
    }
    else{
        return true;
    }
}
void chatterCallback_planer(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    ROS_INFO("I heard PLANER:  [%d]", msg->data[0]);
    //state_planer = msg -> data[0] ;
}
void chatterCallback_ST2_little(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    ROS_INFO("I heard ST2_little: [%d]", msg->data[0]);
    for ( int i = 0; i < data_len; i++){
       ST2_little_rx[i] = msg -> data[i];
   }
}
void chatterCallback_ST2_littlecom(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
     
    for ( int i = 0; i < data_len; i++){
        ST2_little_rx[i] = msg -> data[i];
//ROS_INFO("I heard ST2_little:%d [%d]",i, msg->data[i]);
    }
}
void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
    ROS_INFO("I heard action: [%d]", msg->action);
    tx++;
    state_planer = msg->planer_state;
    ROS_INFO("I heard PLANER: [%d]", state_planer);
    team = msg->team;
  
    // initialize here st2 will give number 5 initially
//   if ( initialize == 1 && ST2_little_rx[0] == 5){
//       init();
//       initialize = 0;
//   }
    if ( newaction(msg) == 1){
        mission_wait.count = 0;
    }
    if (msg->emerg == 1){
        // ST2_little_tx[0] = 0;
        // ST2_little_tx[1] = 2;
        // ST2_little_tx[2] = 404;
        // ST2_little_tx[3] = 2;
        // ST2_little_tx[4] = 2;
        // ST2_little_tx[5] = 2;
        state_mission = stop;
    }
    else if ( state_mission == success && newaction(msg) == 0 ){
        state_mission = success;
        ROS_INFO("old action!");
    }
    else if ( state_mission != success || newaction(msg) == 1){
        switch (msg->action)
        {
            case 0: //emergency
                state_mission = success;
            //   do_nothing();
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
                do_nothing();
                break;
            case 24 :
                if ( state_planer == 1){
                    switch (reef_l.count)
                    {
                        case 0://open claw
                            state_mission = ing;
                            ST2_little_tx[0] = 0;
                            for ( int i = 1; i < 8; i++){
                                ST2_little_tx[i] = 1;
                            }
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_l.count ++;
                            }
                            break;
                        case 1:
                            ST2_little_tx[8] = 2;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_l.count ++;
                            }
                            break;
                        case 2:
                            for ( int i = 1; i < 6; i ++){
                                ST2_little_tx[i] = 0;
                            }
                                if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_l.count ++;
                            }
                            break;
                        case 3: // raise platform
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_l.count ++;
                            }
                            break;
                        case 4: // mission done
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                state_mission = success;
                                reef_l.count  = 0;
                            }
                            break;
                        default:
                            break;
                    }            
                }
                else{
                    state_mission = ing;
                }
                // claw_action(0,1, reefl_color);
                for ( int i = 0; i < 5; i++){
                    claw [i] = msg->reef[i ];
                }
                break;
            case 25: // reef_l
                do_nothing();
                break;
            case 7: // reef_r
                do_nothing();
                break;
            case 26:
            ROS_INFO("reef r count %d", reef_r.count);
                if ( state_planer == 1){
                    switch (reef_r.count)
                    {
                        // ROS_INFO("reef r")
                        case 0://open claw
                            state_mission = ing;
                            ST2_little_tx[0] = 0;
                            for ( int i = 1; i < 8; i++){
                                ST2_little_tx[i] = 1;
                            }
                            ST2_little_tx[8] = 1;
                            ROS_INFO("reef state %d", checkST2_state(ST2_little_tx));
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_r.count ++;
                            }
                            break;
                        case 1:
                            ST2_little_tx[8] = 2;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_r.count ++;
                            }
                            break;
                        case 2:
                            for ( int i = 1; i < 6; i ++){
                                ST2_little_tx[i] = 0;
                            }
                                if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_r.count ++;
                            }
                            break;
                        case 3: // raise platform
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_r.count ++;
                            }
                            break;
                        case 4: // mission done
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                state_mission = success;
                                reef_r.count  = 0;
                            }
                            break;
                        default:
                            break;
                        }            
                }
                else{
                    state_mission = ing;
                }
                for ( int i = 0; i < 5; i++){
                    claw [i] = msg->reef[i + 5];
                }
                break;
            case 27: // reef_r
                do_nothing();
                break;
            case 8: // reef_p
                do_nothing();
                break;
            case 28: // reef_p
                if ( state_planer == 1){
                    switch (reef_p.count)
                    {
                        case 0://open claw
                            state_mission = ing;
                            ST2_little_tx[0] = 0;
                            for ( int i = 1; i < 8; i++){
                                ST2_little_tx[i] = 1;
                            }
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_p.count ++;
                            }
                            break;
                        case 1:
                            ST2_little_tx[8] = 2;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_p.count ++;
                            }
                            break;
                        case 2:
                            for ( int i = 1; i < 6; i ++){
                                ST2_little_tx[i] = 0;
                            }
                                if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_p.count ++;
                            }
                            break;
                        case 3: // raise platform
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                reef_p.count ++;
                            }
                            break;
                        case 4: // mission done
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                state_mission = success;
                                reef_p.count  = 0;
                            }
                            break;
                        default:
                            break;
                        }            
                }
                else{
                    state_mission = ing;
                }
                for ( int i = 0; i < 5; i++){
                    claw [i] = reefp_color[i];
                }
                break;
            case 29: // reef_r
                do_nothing();
                break;
            //   case 11: // placecup_r
            //     for ( int color = 2; color <= 3; color ++){
            //         claw_action(color, 0, reef_null);
            //     }

            //     //   state_mission = success;
            //       break;
            case 11: // placecup_r for 0418 demo
                ROS_INFO("placecup count %d", placecup_r.count);
                if ( state_planer == 1 ){
                    switch ( placecup_r.count )
                    {
                        case 0 :// lower platform
                            state_mission = ing;
                            ST2_little_tx[0] = 0;
                            // for ( int i = 1; i < claw_color.size() + 1; i++){
                            //         ST2_little_tx[i] = 0;
                            // }
                            ST2_little_tx[6] = 1;
                            ST2_little_tx[7] = 1;
                            ST2_little_tx[8] = 0;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                placecup_r.count ++;
                            }
                            break;
                        case 1: // open claw for greeen cup
                            ST2_little_tx[0] = 0;
                            for ( int i = 1; i < claw_color.size() + 1; i++){
                                if ( msg -> NS == 0 ){ // N green -> red 
                                        if ( claw [ i - 1] == 0 ){//green
                                            ST2_little_tx[i] = 1;
                                        }
                                        else{
                                            ST2_little_tx[i] = 0;
                                        }
                                    //ST2_little_tx[i] = 1;
                                }
                                else{ // S red
                                        if ( claw [ i - 1 ] == 1 ){//red
                                            ST2_little_tx[i] = 1;
                                        }
                                        else{
                                            ST2_little_tx[i] = 0;
                                        }
                                    //ST2_little_tx[i] = 1;
                                }
                            }
                            ST2_little_tx[6] = 1;
                            ST2_little_tx[7] = 1;
                            ST2_little_tx[8] = 0;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                placecup_r.count ++;
                            }
                            break;
                        case 2: //raise platform
                            ST2_little_tx[8] = 1;
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                placecup_r.count ++;
                            }
                            break;
                        case 3: // mission done
                            if ( checkST2_state(ST2_little_tx) == 1 ){
                                state_mission = success;
                                placecup_r.count  = 0;
                            }
                            break;
                        default:
                            break;
                    }
                        
                    
                }
                else{
                    state_mission = ing;
                }
                // for ( int color = 2; color <= 3; color ++){
                //     claw_action(color, 0, reef_null);
                // }

            //   state_mission = success;
                break;
            case 30: // place cup 2nd color
                if ( state_planer == 1){
                    switch ( placecup_r.count )
                    {
                    case 0 :// lower platform
                        state_mission = ing;
                        ST2_little_tx[0] = 0;
                        // for ( int i = 1; i < claw_color.size() + 1; i++){
                        //         ST2_little_tx[i] = 0;
                        // }
                        ST2_little_tx[6] = 1;
                        ST2_little_tx[7] = 1;
                        ST2_little_tx[8] = 0;
                        if ( checkST2_state(ST2_little_tx) == 1 ){
                            placecup_r.count ++;
                        }
                        break;
                    case 1: // open claw for cup
                        ST2_little_tx[0] = 0;
                        for ( int i = 1; i < claw_color.size() + 1; i++){
                            ST2_little_tx[i] = 1;
                        }
                        if ( checkST2_state(ST2_little_tx) == 1 ){
                            placecup_r.count ++;
                        }
                        break;
                    case 2: //raise platform
                        ST2_little_tx[8] = 1;
                        if ( checkST2_state(ST2_little_tx) == 1 ){
                            placecup_r.count ++;
                        }
                        break;
                    case 3: // mission done
                        if ( checkST2_state(ST2_little_tx) == 1 ){
                            state_mission = success;
                            placecup_r.count  = 0;
                        }
                        break;
                    default:
                        break;
                    }
                        
                    
                }
                else{
                    state_mission = ing;
                }
                // for ( int color = 2; color <= 3; color ++){
                //     claw_action(color, 0, reef_null);
                // }

            //   state_mission = success;
                break;
            // case 12:{
            //     ST2_little_tx[0] = 8787;
            //     for_ST2_little.data[0] = ST2_little_tx[0];
            //     forST2_little.publish(for_ST2_little);
            //     break;
            // }
            case 31:{ // delay wait for big chicken to walk away
                if (state_planer == 1){
                    if (mission_wait.count == 0){
                        begin_time = ros::Time::now();
                        mission_wait.count = 1;
                    }
                    now_time = ros::Time::now();
                    doing_time = (now_time - begin_time).toSec();
                    if (doing_time < wait_sec){
                        state_mission = ing;
                    }
                    else{
                        state_mission = success;
                    }
                }
                else{
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
    old_command[0] = msg->action;
    old_command[1] = msg->cup[0];
    old_command[2] = msg->cup[1];
    old_command[3] = msg->hand[0];
    old_command[4] = msg->hand[1];
    to_main.data[0]=state_mission;
    to_main.data[1]=timestep;
    timestep++;
    tomain.publish(to_main);
}


int main(int argc, char **argv)
{
for_ST2_little.data = {0,1,1,1,1,1,1,1,1};
ros::init(argc, argv, "mission");
ros::NodeHandle n;
to_main.data={ 0, 0};
forplaner = n.advertise<std_msgs::Float32MultiArray>("missionToplaner", 1);
forST2_little = n.advertise<std_msgs::Int32MultiArray>("MissionToST2_little", 1);
forST2_littlecom = n.advertise<std_msgs::Int32MultiArray>("txST2", 1);
// ros::Publisher forNavigation = n.advertise<geometry_msgs::PoseStamped>("move_base_simple/goal", 1);
// ros::Publisher forplaner = n.advertise<std_msgs::String>("forplaner", 1);
// ros::Publisher forST2_little = n.advertise<std_msgs::String>("forST2_little", 1);
tomain = n.advertise<std_msgs::Int32MultiArray>("missionToMain", 100);
sub = n.subscribe("mainToMission", 1000, chatterCallback);
subplaner = n.subscribe("planerToMission", 1000, chatterCallback_planer);
subST2_little = n.subscribe("ST2_littleToMission", 1000, chatterCallback_ST2_little);
subST2_littlecom = n.subscribe("rxST2", 1000, chatterCallback_ST2_littlecom);
//   ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000);
ros::Rate loop_rate(10);
// ROS_INFO("debug outside while");
int count = 0;

  while (ros::ok())
  {
    // ROS_INFO("debug inside while");
    for ( int i = 0; i < data_len; i++){
        //for_ST2_little.data.push_back(ST2_little_tx[i]);
        for_ST2_little.data[i] = ST2_little_tx[i];
        ROS_INFO("publish in for %d ", for_ST2_little.data[i]);
    }
    forST2_little.publish(for_ST2_little);
    forST2_littlecom.publish(for_ST2_little);
    //for_ST2_little.data.clear(); 
    //for_ST2_littlecom.data.clear();
    // to_main.state = state_mission;
    
    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}