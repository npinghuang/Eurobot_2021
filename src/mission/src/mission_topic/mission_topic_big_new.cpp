#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Int32.h>
#include <std_msgs/Float32MultiArray.h>
#include "mission/maintomission.h"
// #include "mission/missiontomain.h"
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
#include<queue>
#include<vector>
#include<math.h>
// #include<dos.h>   //for delay()
#include <time.h>
#include "ros/time.h"
#include "mission/mission_camera.h"
#include <cstdlib>
using namespace std;

#include "mission/mission_action.h"

// ros::Duration onesec(0, 1000000000);
// ros::Duration onesec(0, 0);
//time
ros::WallTime begin_time;
ros::WallTime now_time;
// #include "mission/mission_function.h"
ros::Publisher tomain;
// ros::Publisher forCamera;
ros::Publisher forST2;
std_msgs::Int32MultiArray for_st2;
ros::Publisher forST2com;
ros::Subscriber sub;
// ros::Subscriber subCamera;
ros::Subscriber subST2;
ros::Subscriber subST2com;
ros::ServiceClient camera_client;
mission::mission_camera srv;
// mission::missiontomain to_main;
std_msgs::Int32MultiArray to_main;
// std_msgs::Int32 to_camera;

int initialize = 1;
std::vector<int> hand{0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
std::vector<int> ST2_tx{0,0,0,0,0,0};
std::vector<int> ST2_rx{0,0,0,0,0,0};
std::vector<int> old_tx{0,0,0,0,0,0};
std::vector<int> old_command{0,0,0,0,0};// action, cup1, cup2, hand1, hand2
std::vector<int> cup_camera_red;
std::vector<int> cup_camera_green;
std::vector<float> current_pos{0,0,0};

int state_planer = 0;
int state_ST2 = 0;
int state_mission = 2;
int tx = 101;
int team;
bool publish_planer;
int success = 1, fail = 0, ing = 2, stop = 3, little_mission = 4; // mission state
int timestep = 1;//for main
// for camera
int number_of_cups = 0;
int timestamp_camera = 0;
int timestamp_camera_previous = 0;
bool camera_data = 0; // if camera data is most recent 
int current_cup_no;
int getcup_hand;
int cupx, cupy, cupcolor; //for param test camera
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
            prepare = pre;
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
void print_tx(){
    ROS_INFO("TX { %d %d %d %d %d %d}", ST2_tx[0],ST2_tx[1],ST2_tx[2],ST2_tx[3],ST2_tx[4],ST2_tx[5]);
}
int angle_test;
int suction_count = 0;
int suction_up_count = 0;
// float suction_delay = 0.3;
// float suction_up_delay = 0.2;
ros::WallDuration suction_delay(1.0);
ros::WallDuration suction_up_delay;
// float suction_delay = 0;
// float suction_up_delay = 0;
// float doing_time;
ros::WallDuration doing_time;
bool checkST2_state(std::vector<int> &tx){
    // if st2 tx == rx
    int state = 1;
    bool newact = false;
    if (old_tx [0] != tx[0] || old_tx [1] != tx[1] || old_tx [2] != tx[2] || old_tx [3] != tx[3] || old_tx [4] != tx[4]){
        suction_count = 0;
        suction_up_count = 0;
    }
    if ( (ST2_rx[3] != 2 || ST2_rx[4] != 2)  && ST2_rx[2] == 404){ // if platform is at down position we need to add a delay to it 
        if ( state == 1){
            if (suction_count == 0){
                begin_time = ros::WallTime::now();
                suction_count = 1;
            }
            now_time = ros::WallTime::now();
            doing_time = (now_time - begin_time);
            if ( doing_time < suction_delay ){
                state = 0;
                if (ST2_rx[3] == 1 || ST2_rx[4] == 1){
                    // ROS_INFO("down suction doing time %f %f %d",begin_time.toSec(), doing_time, suction_count);
                    ROS_INFO("down delay");
                }
                else if (ST2_rx[0] == 2 || ST2_rx[4] == 0){
                    // ROS_INFO("up suction doing time %f %f %d",begin_time.toSec(), doing_time, suction_count);
                    ROS_INFO("up delay");

                }
            }
            else if (doing_time >= suction_delay){
                state = 1;
            }
        }
    }
    else if (ST2_rx[2] != 404) { // if i give a angle to ST2 there's some certain way of communication
        for ( int i = 0; i < 6; i++){
            if ( tx[i] != ST2_rx[i] && i != 1){
                state = 0;
                break;
            }
        }
    }
    else if ( ST2_rx[2] == 404){
        for ( int i = 0; i < 6; i++){
            if ( tx[i] != ST2_rx[i]){
                state = 0;
                break;
            }
        }    
    }
    for ( int i = 0; i < 6; i++){
        old_tx[i] = tx[i]; 
    }
    return state;
}
void tx_ST2( int hand, int suction_state,  int degree, int platform_right, int platform_left, int hand_state){
    ST2_tx[0] = hand;  // hand
    ST2_tx[1] = suction_state;  //suction : 0 for close, 1 for open ( suck ), 2 for no change
    ST2_tx[2] = degree;  // 404 for no degree
    ST2_tx[3] = platform_right;  // 0 for up. 1 for down, 2 for no change
    ST2_tx[4] = platform_left; // 0 for up. 1 for down, 2 for no change
    ST2_tx[5] = hand_state; // 0 for down. 1 for up, 2 for no change
}
int cup_x = 0;
int cup_y = 0;
std::vector<int> cup_pos_current{0, 0, 0};
int cup_color_req = 0; // 0 for green 1 for red
std::vector<int>  coordinate_transform( std::vector<int> &coordinate, int hand ){
    int xi = coordinate[0];
    int yi = coordinate[1];
    int half_of_robot_width = 170/2; // mm
    if ( hand < 6){// front side of the robot : axis rotate (theta)
        // coordinate[0] = cos ( coordinate[2] - M_PI_2) * xi - sin ( coordinate[2] - M_PI_2) * yi;
        // coordinate[1] = sin ( coordinate[2] - M_PI_2) * xi - cos ( coordinate[2] - M_PI_2) * yi - half_of_robot_width;  
        coordinate[0] = -cos ( current_pos[2] ) * yi + sin ( current_pos[2] ) * xi;
        coordinate[1] = sin ( current_pos[2] ) * yi + cos ( current_pos[2]  ) * xi - half_of_robot_width;  
    }
    else if ( hand >= 6 && hand < 12){// back side of the robot : axis rotate (theta + 180)
        coordinate[0] = -cos ( current_pos[2] + M_PI) * yi + sin ( current_pos[2] + M_PI ) * xi;
        coordinate[1] = sin ( current_pos[2] + M_PI) * yi + cos ( current_pos[2]  + M_PI) * xi - half_of_robot_width; 
        // coordinate[0] = cos ( coordinate[2] + M_PI_2) * xi - sin ( coordinate[2] + M_PI_2) * yi;
        // coordinate[1] = sin ( coordinate[2] + M_PI_2) * xi - cos ( coordinate[2] + M_PI_2) * yi - half_of_robot_width;  
    }
    // bug! maybe front and back of the robot have different value
    // turn unit from mm to cm
    coordinate[0] = coordinate[0] / 10;
    coordinate[1] = coordinate[1] / 10;
    return coordinate;
}
int camera(){
    // hand 12 cm long
    float angle_hand;
    int hand_x_r = 6;//cm distance of on the x axis from the middle point of the robot
    int hand_x_l = -6;
    // cup_pos_current[0]= 100+85 ;
    // cup_pos_current[1] = -60-60;
    // cup_pos_current[2] = 0;
    current_pos[0] = 0;
    current_pos[1] = 0;
    current_pos[2] =  0;
    // for real
    // cup_pos_current[0]= cup_pos[current_cup_no - 1][0];
    // cup_pos_current[1] = cup_pos[current_cup_no - 1][1];
    // cup_pos_current[2] = (int)current_pos[2];
    // green test
    // cup_pos_current[0]= 6;
    // cup_pos_current[1] = 12;
    // cup_color_req = cup_color [0];
    // red test
    // cup_pos_current[0]= -6;
    // cup_pos_current[1] = 12;
    // cup_color_req = cup_color [1];
    
    ROS_INFO("current pos x [%f], y [%f], theta [%f]", current_pos[0], current_pos[1], current_pos[2]);
    // cup_color_req = cup_color [current_cup_no - 1];
    // cup_pos_current = coordinate_transform(cup_pos_current, getcup_hand);
    
    // param
    cup_pos_current[0]= cupx;
    cup_pos_current[1] = cupy;
    cup_color_req =  cupcolor;
    ROS_INFO("cup relative pos x [%d], y [%d], theta [%d]", cup_pos_current[0], cup_pos_current[1], cup_pos_current[2]);
    srv.request.coordinate_mission.resize(2);
    srv.request.coordinate_mission[0] = cup_pos_current[0];
    srv.request.coordinate_mission[1] = cup_pos_current[1];
    srv.request.cup_color_mission = cup_color_req;
    srv.request.cup_color_mission = 1; // green
    camera_client.call(srv);
    ROS_INFO("1st call cup x [%d] y [%d] color [%d]", srv.response.coordinate_camera[0],srv.response.coordinate_camera[1], srv.response.cup_color_camera );
    if (camera_client.call(srv)){
        ROS_INFO("2nd call cup x [%d] y [%d] color [%d]", srv.response.coordinate_camera[0],srv.response.coordinate_camera[1], srv.response.cup_color_camera );
        if ( srv.response.cup_color_camera == 0){ // green cup :  get cup using right side hand
            
            ROS_INFO(" [0] %d, hand %d = %f",cup_pos_current[0], hand_x_r, double(cup_pos_current[0] - hand_x_r));
            ROS_INFO("atan(0), %f", atan2( double( cup_pos_current[1]), double(cup_pos_current[0] - hand_x_r)));
            angle_hand = M_PI_2 - atan2( double( cup_pos_current[1]), -double(cup_pos_current[0] - hand_x_r));
            ROS_INFO("angle rad, %f, y %f, x %d", angle_hand, double( cup_pos_current[1]), (cup_pos_current[0] - hand_x_r));
            angle_hand = angle_hand * 180  / M_PI; // tranform unit from rad to degree
            ROS_INFO("angle degree %f", angle_hand);
        }
        else if ( srv.response.cup_color_camera == 1){ // red cup :  get cup using left side hand
            angle_hand = M_PI_2 -atan2( double( cup_pos_current[1]), -double(cup_pos_current[0] - hand_x_l));
            angle_hand = angle_hand * 180  / M_PI; // tranform unit from rad to degree
        }
        else if ( srv.response.cup_color_camera == -1){ // no cup
             angle_hand = 404;
        }
        
    }
    else{
        angle_hand = 404;
        ROS_ERROR("Failed to call service camera");
    }
    if ( angle_hand > 30.0 && angle_hand != 404){
        ROS_ERROR("angle too big : [%f]", angle_hand);
        angle_hand = 30;
    }
    else if ( angle_hand < -30.0 ){
        angle_hand = -30;
        ROS_ERROR("angle too small: [%f]", angle_hand);
    }
    ROS_INFO("hand angle %f", angle_hand);
    return angle_hand;
}
void placecup(int hand, int degree){
    state_mission = ing;
    if ( state_planer == 1){
            switch (placecup_h.count)
            {
            case  0:
                tx_ST2( hand, 0, degree, 2, 2, 2 ); //first action hand to assigned degree
                placecup_h.count ++;    
                state_mission = ing;
                break;
            case 1:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if (  hand == 51 || hand == 3264 ){ 
                        tx_ST2( hand, 2, 404, 2, 2, 1);// second action hand turn to down
                    }
                    else if (  hand == 12 || hand == 768 ){ 
                        tx_ST2( hand, 2, 404, 2, 2, 0);// second action hand turn to up
                    }
                    placecup_h.count ++;  
                    }
                break;
            case 2:
                if ( checkST2_state(ST2_tx) == 1 ){
                    tx_ST2( hand, 2, 404, 1, 1, 2);// fourth action platform down
                    placecup_h.count ++;
                }
                break;
            case 3:
                if ( checkST2_state(ST2_tx) == 1 ){
                    tx_ST2( hand, 0, 404, 2, 2, 2);// third close suction
                    placecup_h.count ++;
                }
                break;
            case 4:
                if ( checkST2_state(ST2_tx) == 1 ){
                    tx_ST2( hand, 2, 404, 0, 0, 2);// fifth action platform up
                    placecup_h.count ++;
                }
                break;
            case 5:
                if ( checkST2_state(ST2_tx) == 1 ){
                    placecup_h.count = 0;
                    state_mission = success;
                }
                break;
            default:
                break;
            }
    }
}
void init(){
    ROS_INFO("initialize");
}
int angle = 0;
void getcup_one( int hand){
    state_mission = ing;
    // ROS_INFO("mission hand %d %d", hand, hand);
    ROS_INFO("count [%d]", getcup.count);
    // ROS_INFO("check ST2 [%d]", checkST2_state(ST2_tx));
    int handd = pow(2,hand);   
    int platform_down_r, platform_down_l, platform_up_r, platform_up_l; 
    if ( hand % 2 == 0){ // hand is on right platform
        platform_down_r = 1;
        platform_down_l = 2;
        platform_up_r = 0;
        platform_up_l = 2;
    }
    else if ( hand % 2 == 1){ // hand is on left platform
        platform_down_r = 2;
        platform_down_l = 1;
        platform_up_r = 2;
        platform_up_l = 0;
    }
    if ( state_planer == 1){
        switch (getcup.count)
        {
            case 0:
                if ( hand == 0 || hand == 1 || hand == 6 || hand == 7){ // inner suction
                    tx_ST2( handd, 1, 404, 2, 2, 2);//first action open suction
                }
                else{
                    // angle = camera();
                    angle = 404;
                    if ( angle == 404 ){ // can't get data from camera
                        if (hand == 2 ||  hand == 4 ||  hand == 9  || hand == 11 ){ // due cordination degree need to be postive or negative
                            tx_ST2( handd, 1, getcup_theta[1], 2, 2, 2);//first action hand to assigned degree
                        }
                        else{
                            tx_ST2( handd, 1, getcup_theta[0], 2, 2, 2);//first action hand to assigned degree
                        }
                    }
                    else{//first action hand to assigned degree
                        tx_ST2( handd, 1, angle, 2, 2, 2);
                    }
                }
                getcup.count ++;    
                state_mission = ing;
                break;
            case 1:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if ( hand == 0 || hand == 1 || hand == 6 || hand == 7){ // inner suction
                        tx_ST2( handd, 2, 404, platform_down_r, platform_down_l, 2);// second action paltform down
                    }
                    else if (  hand == 2 ||  hand == 3 ||  hand == 8 ||  hand == 9 ){ //bug gggg hand % 2 == 1 
                        tx_ST2( handd, 2, 404, 2, 2, 0); // second action hand turn to down
                    }
                    else if (  hand == 4 ||  hand == 5 ||  hand == 10 ||  hand == 11 ){ //bug gggg hand % 2 == 1 
                        tx_ST2( handd, 2, 404, 2, 2, 1); // second action hand turn to down
                    }
                    getcup.count ++;  
                }
                break;
            case 2:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if ( hand == 0 || hand == 1 || hand == 6 || hand == 7){ // inner suction
                        tx_ST2( handd, 2, 404, platform_up_r, platform_up_l, 2);// third action platform up
                    }
                    else{
                        tx_ST2( handd, 1, 404, 2, 2, 2); // third open suction
                    }
                    getcup.count ++;
                }
                break;
            case 3:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if ( hand == 0 || hand == 1 || hand == 6 || hand == 7){ // inner suction
                        getcup.count = 0;
                        state_mission = success;
                    }
                    else{
                        tx_ST2( handd, 2, 404, platform_down_r, platform_down_l, 2); // fourth action platform down
                        getcup.count ++;
                    }
                }
                break;
            case 4:
                if ( checkST2_state(ST2_tx) == 1 ){
                    tx_ST2( handd, 2, 404, platform_up_r, platform_up_l, 2);  // fifth action platform up
                    getcup.count ++;
                }
                break;
            case 5:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if (  hand == 2 ||  hand == 3 ||  hand == 8 ||  hand == 9 ){
                        tx_ST2( handd, 2, 404, 2, 2, 1);
                    }
                    getcup.count ++;
                }
                break;
            case 6:
                if ( checkST2_state(ST2_tx) == 1 ){
                    if (hand == 2 ||  hand == 4 ||  hand == 9  || hand == 11 ){ // due cordination degree need to be postive or negative
                        tx_ST2( handd, 1, getcup_theta[3], 2, 2, 2);// seventh action hand move away from camera
                    }
                    else{
                        tx_ST2( handd, 1, getcup_theta[2], 2, 2, 2);// seventh action hand move away from camera
                    }
                    getcup.count ++;
                }
                break;
            case 7:
                if ( checkST2_state(ST2_tx) == 1 ){
                    getcup.count = 0;
                    state_mission = success;
                }
                break;
            default:
                break;
        }
    }   
    else{
        state_mission = ing;
    }
}
void do_nothing(){
    if ( state_planer == 1){
            state_mission = 1; //no action need to be done by ST2 so always return success
        }
    else{
        state_mission = ing;
    }
}
// for fake ST2
void chatterCallback_ST2(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    // ROS_INFO("I heard ST2: [%d]", msg->data[0]);
    for ( int i = 0; i < 6; i++){
        ST2_rx[i] = msg -> data[i];
    }
}
bool newaction(const mission::maintomission::ConstPtr& msg){
    if (old_command [0] == msg-> action && old_command [1] == msg -> cup[0] &&
        old_command [2] == msg -> cup[1] && old_command [3] == msg -> hand[0] &&
        old_command [4] == msg -> hand[1]){
        return false;
    }
    else{
        return true;
    }
}
// for running on pi
void chatterCallback_ST2com(const std_msgs::Int32MultiArray::ConstPtr& msg){
    // ROS_INFO("I heard ST2: [%d]", msg->data[0]);
    for ( int i = 0; i < 6; i++){
        ST2_rx[i] = msg -> data[i];
    }   
}
void chatterCallback(const mission::maintomission::ConstPtr& msg)
{
    ROS_INFO("-------------");
    // ROS_INFO("cup [%d]", msg->cup[0]);
    ROS_INFO("get cup count [%d]", getcup.count);
    ROS_INFO("get cup 12 count [%d]", getcup_12.count);
    ROS_INFO("I heard action: [%d]", msg->action);
    tx++;
    state_planer = msg->planer_state;
    team = msg->team;
    getcup_hand =  msg->cup[1];
    for ( int i = 0; i <  3; i ++){
        current_pos[i] = msg->action_pos[i];
    }
    if ( initialize == 1){
        init();
        initialize = 0;
    }
    if (msg->emerg == 1){
        tx_ST2(0, 2, 404, 2, 2, 2);
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
                tx_ST2(1, 2, 404, 2, 2, 2);
                state_mission = success;
                break; 
            case 1: {//windsock
                // ST2_tx[0] = action1_ST2_blue[0];  
                if ( state_planer == 1){
                    if ( checkST2_state(ST2_tx)== 1){
                        state_mission = success;
                    }
                    else{
                        state_mission = ing;
                    }    
                }
                else{
                    state_mission = ing;
                }  
                break;
                }
            case 15:{ // windsock 2
                // ST2_tx[0] = action1_ST2_blue[1];  
                if ( state_planer == 1){
                    if ( checkST2_state(ST2_tx)== 1){
                        state_mission = success;
                    }
                    else{
                        state_mission = ing;
                    }    
                }
                else{
                    state_mission = ing;
                }  
                break;
            }
            case 2:// lhouse 
            case 16: //lhouse 2
            case 17: //lhouse 3
            case 3: // flag
            case 4: // anchorN
            case 5: // anchorS
            case 6: // reef_l
            case 7: // reef_r
            case 8: // reef_p
                do_nothing();
                break;
            case 9: {// placecup_h// place 4 or 2 cup at the same time and need to cordinate with planer
                placecup( placecup_hand[0], placecup_theta[0]);
                break;
            }
            case 18:{ //placecup h 2 = 2 hand
                placecup( placecup_hand[1], placecup_theta[1]);
                break;
            }
            case 19: // placecup h back away
            case 20: // placecup h spin        
                do_nothing();
                break;
            case 21:{ //placecup h 2 = 4 hand
                placecup( placecup_hand[2], placecup_theta[0]);

                break;
            }
            case 22:{ //placecup h 2 = 2 hand
                placecup( placecup_hand[3], placecup_theta[1]);
                break;
            }
            case 23: // placecup h back away
            case 10: // placecup_p 
                do_nothing();
                break;
            case 12:{ // getcup
                current_cup_no = msg -> cup[0]; // make cup_no into gobal variable so that I can access it in camera()
                getcup_one( msg->cup[1]);
                break;
            }
            case 13: 
            case 14:{// getcup12
                int hand_1 = 0;
                if ( msg->cup[1] == 21){
                    hand_1 = pow(2, 0) +  pow(2, 1);
                }
                else if (msg->cup[1] == 34){
                    hand_1 = pow(2, 6) +  pow(2, 7);
                }
                if ( state_planer == 1 ){
                    switch ( getcup_12.count){
                        case 0:
                            tx_ST2( hand_1, 1, 404, 2, 2, 2);// open suction
                            getcup_12.count ++;    
                            state_mission = ing;
                            break;
                        case 1:
                            if ( checkST2_state(ST2_tx) == 1){
                                tx_ST2( hand_1, 2, 404, 1, 1, 2); // second action platform down
                                getcup_12.count ++;  
                            }
                            break;
                        case 2:
                            if ( checkST2_state(ST2_tx) == 1){
                                tx_ST2( hand_1, 2, 404, 0, 0, 2); // third action platform up
                                getcup_12.count ++;  
                            }
                            break;
                        case 3:
                            if ( checkST2_state(ST2_tx) == 1){
                                getcup_12.count = 0;
                                state_mission = success;
                            }
                            break;
                        default:
                            break;
                    }
                }
                else{
                    state_mission = ing;
                }
                break;
            }
            default:
                do_nothing();
                break;
        }
    }
    old_command[0] = msg->action;
    old_command[1] = msg->cup[0];
    old_command[2] = msg->cup[1];
    old_command[3] = msg->hand[0];
    old_command[4] = msg->hand[1];
    to_main.data[0]=state_mission;
    to_main.data[1]=timestep;
    timestep ++;
    tomain.publish(to_main);
}

// Hi, Nice to meet you:)))
int main(int argc, char **argv)
{
    ros::init(argc, argv, "mission");
    ros::NodeHandle n;
    ros::Time::init();

    // forCamera = n.advertise<std_msgs::Int32>("missiontoCamera", 100);
    forST2 = n.advertise<std_msgs::Int32MultiArray>("MissionToST2", 1);
    forST2com = n.advertise<std_msgs::Int32MultiArray>("txST2", 1);
    tomain = n.advertise<std_msgs::Int32MultiArray>("missionToMain", 10);
    sub = n.subscribe("mainToMission", 100, chatterCallback);
    subST2 = n.subscribe("ST2ToMission", 1000, chatterCallback_ST2);
    subST2com = n.subscribe("rxST2", 1000, chatterCallback_ST2com);
    // subCamera =  n.subscribe("opencv_Cups", 100, camera);

    camera_client = n.serviceClient<mission::mission_camera>("camera_fake_server");

    ros::Rate loop_rate(100);
    ROS_INFO("mission publish");
    
    int count = 0;
    to_main.data = {2, 1};
    // to_camera.data = 0;
    while (ros::ok())
    {
        n.getParam("/angle", angle_test); 
        n.getParam("//cupx",  cupx);  
        n.getParam("/cupy", cupy);
        n.getParam("/cupcolor", cupcolor);    
        for ( int i = 0; i < 6; i++){
            for_st2.data.push_back(ST2_tx[i]);
            // ROS_INFO("publish in for %d %d", ST2_tx[i], for_st2.data[i]);
        }
        forST2.publish(for_st2);
        forST2com.publish(for_st2);
        for_st2.data.clear(); 
        ros::spinOnce();

        loop_rate.sleep();
        ++count;
    }
    return 0;
}