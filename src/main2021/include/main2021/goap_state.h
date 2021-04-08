#ifndef GOAP_STATE_H_
#define GOAP_STATE_H_

#include <ros/ros.h>
#include "main2021/goap_srv.h"
#include "../include/main2021/position_state.h"
#include "../include/main2021/friend_state.h"
#include "../include/main2021/state.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

class goap_data{
public:
    goap_data(float, float, int);

    void give_action();

    void give_goap(State*, Friend*, Position*);

    int getaction();
    float get_action_x();
    float get_action_y();
    float get_action_th();
    int get_action_color();
    int get_action_cup();
    int get_action_hand();

    bool samePosOrNot();
    bool sameActionOrNot();

private:
    ros::NodeHandle n;
    ros::ServiceClient client_goap;
    main2021::goap_srv g_srv;

    int first;
    int now_action;
    float now_x;
    float now_y;
    float now_th;
    int now_color;
    int now_cup;
    int now_hand;
    float old_x;
    float old_y;
    float old_th;
    int old_action;
    int old_cup;
    int old_hand;
    vector<int> oldaction;
    vector<float> oldpos;
    vector<int> oldcup;
    vector<int> action;
    vector<float> pos;
    vector<int> cup;
};

#endif