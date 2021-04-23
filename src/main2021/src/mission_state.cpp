#include <ros/ros.h>
#include "std_msgs/Int32MultiArray.h"
#include "main2021/maintomission.h"

#include "../include/main2021/mission_state.h"
#include "../include/main2021/state.h"
#include "../include/main2021/goap_state.h"

#include <iostream>
#include <stdlib.h>
#include <vector>
#include <algorithm>
#include <math.h>


mission_data::mission_data(float x, float y){
    pub_mission = n.advertise<main2021::maintomission>("mainToMission", 100);
    sub_mission = n.subscribe<std_msgs::Int32MultiArray>("missionToMain", 1, &mission_data::m_res, this);

    //initial
    m_msg.team = 1;
    m_msg.action = 0;
    m_msg.planer_state = 0;
    m_msg.action_pos.push_back(x); //x
    m_msg.action_pos.push_back(y); //y
    m_msg.action_pos.push_back(M_PI); //degree
    m_msg.cup = {0, 0};
    m_msg.hand = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
    m_msg.reef = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
    m_msg.NS = 0;
    m_msg.emerg = false;


    give = 0;
    give_old = 0;
    m_count = 0;
    old_count = 0;
    //0:FALSE 1:SUCCES 2:DOING 3:EMERG
    status = 0;
}

void mission_data::m_res(const std_msgs::Int32MultiArray::ConstPtr& msg){
    if(msg->data[1] != m_count){
        status = msg->data[0];
        m_count = msg->data[1];
    }
    ROS_INFO("mr_count: %d", msg->data[1]);
}

void mission_data::update_hand(int a, int h){
    if(a == 9 || a == 10)
        hand = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    else if(a == 12)
        hand[h-1] = 1;
    else if(a == 13){
        hand[0] = 1; //hand 1
        hand[1] = 1; //hand 2
    }
    else if(a == 14){
        hand[2] = 1; //hand 3
        hand[3] = 1; //hand 4
    }
}

void mission_data::give_mission(State *sta, goap_data *g){
    //request mission
    m_msg.team = sta->get_team();
    m_msg.action = g->getaction();
    m_msg.planer_state = sta->get_p_state();
    m_msg.action_pos[0] = g->get_action_x(); //action_x
    m_msg.action_pos[1] = g->get_action_y(); //action_y
    m_msg.action_pos[2] = g->get_action_th(); //action_degree
    m_msg.cup[0] = g->get_action_cup(); //action_cup
    m_msg.cup[1] = g->get_action_hand(); //action_hand
    m_msg.hand.assign(sta->get_hand().begin(), sta->get_hand().end()); //hand_status
    m_msg.reef.assign(sta->get_color().begin(), sta->get_color().end()); //five cups' color
    m_msg.NS = sta->get_ns(); //ns
    m_msg.emerg = sta->emergOrNot();

    pub_mission.publish(m_msg);

    if(g->sameActionOrNot() == false){
        give++;
        status = 2;        
    }
}

void mission_data::setstate(int s){
    status = s;
}
void mission_data::set_hand(std::vector<int>* h){
    hand.assign(h->begin(), h->end());
}

int mission_data::getstate(State sta, goap_data g){
    ros::spinOnce();

    // ROS_INFO("M_RES: %d", status);
    // ROS_INFO("give: %d", give);
    // ROS_INFO("give_old: %d", give_old);
    // ROS_INFO("m_count: %d", m_count);
    // ROS_INFO("count_old: %d", old_count);

    if(give != give_old){//new action
        give_old = give;
        status = 2;
    }
    else{
        if(m_count != old_count){//new receive
            old_count = m_count;
            if(status == 1){
                set_hand(&sta.get_hand());
                update_hand(g.getaction(), g.get_action_hand());
            }            
        }
    }
    // ROS_INFO("MISSIONSTATE:%d", status);
    return status;
}
std::vector<int>& mission_data::get_hand(){ return hand;}
