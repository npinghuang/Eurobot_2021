#include <ros/ros.h>
#include <std_msgs/Int32.h>
#include "main2021/gui_state.h"

#include <iostream>
#include <stdlib.h>

GUI::GUI(){

	//publish to gui
	status_pub = n.advertise<std_msgs::Int32>("pub_status", 10);
    score_pub = n.advertise<std_msgs::Int32>("score", 10);
	status_sub = n.subscribe<std_msgs::Int32>("update_status", 10, &GUI::status_sub_callback,this);
    strategy_sub = n.subscribe<std_msgs::Int32>("strategy", 10, &GUI::strategy_sub_callback,this);


    change_sta = 0;
    strategy = 0;
}

void GUI::countScore(int big, int small){
    pub_score.data = (big + small);

    score_pub.publish(pub_score);
}

void GUI::pubToGUI(int state){
    pub_gui.data = state;
    
    status_pub.publish(pub_gui);
}

void GUI::strategy_sub_callback(const std_msgs::Int32::ConstPtr& msg){
    strategy = msg->data;
}

void GUI::status_sub_callback(const std_msgs::Int32::ConstPtr& msg){
    change_sta = msg->data;
}

void GUI::set_strategy(){
    ros::spinOnce();

    if(strategy == 1){ //we are team blue(0)
        script = 0;
        team = 0;
        big_x = 690.;
        big_y = 250.;
        small_x = 800.;
        small_y = 250.;
    }
    else if(strategy == 2){ //we are team yellow(1)
        script = 0;
        team = 1;
        big_x = 690.;
        big_y = 2820.;
        small_x = 980.;
        small_y = 2805.;
    }
    else if(strategy == 3){ //we are team blue(0) with script
        script = 1;
        team = 0;
        big_x = 690.;
        big_y = 250.;
        small_x = 800.;
        small_y = 250.;
    }
    else if(strategy == 4){ //we are team yellow(1) with script
        script = 1;
        team = 1;
        big_x = 690.;
        big_y = 2820.;
        small_x = 980.;
        small_y = 2805.;
    }

}

int GUI::changState(){
    ros::spinOnce();

    return change_sta;
}

int GUI::get_script(){ return script;}
int GUI::get_team(){ return team;}
float GUI::get_bigX(){ return big_x;}
float GUI::get_bigY(){ return big_y;}
float GUI::get_smallX(){ return small_x;}
float GUI::get_smallY(){ return small_y;}