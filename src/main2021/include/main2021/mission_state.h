#ifndef MISSION_STATE_H_
#define MISSION_STATE_H_

#include <ros/ros.h>
#include "std_msgs/Int32MultiArray.h"
#include "main2021/maintomission.h"

#include "../include/main2021/state.h"
#include "../include/main2021/goap_state.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

class mission_data{
public:
    mission_data(float, float);

    void m_res(const std_msgs::Int32MultiArray::ConstPtr&);

    void update_hand(int, int);

    void give_mission(State*, goap_data*);

    void setstate(int);
    void set_hand(vector<int>*);

    int getstate(State, goap_data);
    vector<int>& get_hand();


private:
    ros::NodeHandle n;
    ros::Publisher pub_mission;
    ros::Subscriber sub_mission;

    // std_msgs::Int32MultiArray m_pub;
    main2021::maintomission m_msg;
    


    int give;
    int give_old;
    int m_count;
    int old_count;
    int status;
    vector<int> hand;
};

#endif
