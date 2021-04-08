#ifndef GUI_STATE_H_
#define GUI_STATE_H_

#include <ros/ros.h>
#include <std_msgs/Int32.h>

#include <iostream>
#include <stdlib.h>

using namespace std;

class GUI{
public:
    GUI();
    void countScore(int, int);
    void pubToGUI(int);
    void strategy_sub_callback(const std_msgs::Int32::ConstPtr&);
    void status_sub_callback(const std_msgs::Int32::ConstPtr&);
    void set_strategy();
    int changState();

    int get_script();
    int get_team();
    float get_bigX();
    float get_bigY();
    float get_smallX();
    float get_smallY();

private:
    ros::NodeHandle n;
    ros::Publisher score_pub;
    std_msgs::Int32 pub_score;
    ros::Publisher status_pub;
    std_msgs::Int32 pub_gui;
    ros::Subscriber status_sub;
    ros::Subscriber strategy_sub;

    int change_sta;
    int strategy;
    int script;
    int team;
    float big_x;
    float big_y;
    float small_x;
    float small_y;
};

#endif