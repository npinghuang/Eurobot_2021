#include <ros/ros.h>
#include "main2021/goap_srv.h"

#include "../include/main2021/goap_state.h"
#include "../include/main2021/position_state.h"
#include "../include/main2021/friend_state.h"
#include "../include/main2021/state.h"

#include <iostream>
#include <stdlib.h>
#include <vector>
#include <algorithm>
#include <math.h>


goap_data::goap_data(float x, float y, int c){
    client_goap = n.serviceClient<main2021::goap_srv>("goap");
    
    //initial
    g_srv.request.my_pos.push_back(x); //x
    g_srv.request.my_pos.push_back(y); //y
    g_srv.request.my_pos.push_back(M_PI); //degree
    g_srv.request.friend_pos.push_back(0); //x
    g_srv.request.friend_pos.push_back(0); //y
    g_srv.request.friend_pos.push_back(0); //degree
    g_srv.request.ns = 0;
    g_srv.request.emergency = 0;
    g_srv.request.team = 1;
    g_srv.request.time = 0;
    g_srv.request.friend_action = {0};
    g_srv.request.action_list = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
    g_srv.request.cup_color = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
    g_srv.request.cup = c; //1111 1111 1111 1111 1111 1111
    g_srv.request.hand = {0, 0, 0, 0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ,0};
    g_srv.request.enemy1_pos = {0, 0};
    g_srv.request.enemy2_pos = {0, 0};
    g_srv.request.strategy = 0;

    first = 0;
    now_action = 0;
    now_x = 0;
    now_y = 0;
    now_th = 0;
    now_color = 0;
    now_cup = 0;
    now_hand = 0;
    old_x = 0;
    old_y = 0;
    old_th = 0;
    old_action = 0;
    old_cup = 0;
    old_hand = 0;
    oldaction = {0};
    oldpos = {0};
    oldcup = {0};
    action = {0};
    pos = {0};
    cup = {0};
}

void goap_data::give_action(){
    now_action = action.back();
    action.pop_back();
    now_x = pos.back();
    pos.pop_back();
    now_y = pos.back();
    pos.pop_back();
    now_th = pos.back();
    pos.pop_back();
    now_cup = cup.back();
    cup.pop_back();
    now_hand = cup.back();
    cup.pop_back();
    now_color = cup.back();
    cup.pop_back();    
}

void goap_data::give_goap(State *sta, Friend *f, Position *p){
    //request GOAP
    g_srv.request.my_pos[0] = sta->getx(); //x
    g_srv.request.my_pos[1] = sta->gety(); //y
    g_srv.request.my_pos[2] = sta->getth(); //degree
    g_srv.request.friend_pos[0] = f->getf_x(); //x
    g_srv.request.friend_pos[1] = f->getf_y(); //y
    g_srv.request.friend_pos[2] = f->getf_degree(); //degree
    g_srv.request.ns = sta->get_ns();
    g_srv.request.emergency = sta->emergOrNot();
    g_srv.request.team = sta->get_team();
    g_srv.request.time = sta->get_time();
    g_srv.request.friend_action.assign(f->getf_action().begin(), f->getf_action().end());
    g_srv.request.action_list.assign(sta->get_list().begin(), sta->get_list().end());//{0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    g_srv.request.cup_color = sta->get_color();
    g_srv.request.cup = sta->get_cup(); //1111 1111 1111 1111
    g_srv.request.hand.assign(sta->get_hand().begin(), sta->get_hand().end());
    g_srv.request.enemy1_pos = {p->get_e1_x(), p->get_e1_y()};
    g_srv.request.enemy2_pos = {p->get_e2_x(), p->get_e2_y()};
    g_srv.request.strategy = sta->get_script();

    int i = 0;
    while(i == 0){
        if(client_goap.call(g_srv)){
            if(first == 0){
                ROS_INFO("FIRST ACTION");

                action.assign(g_srv.response.action.begin(), g_srv.response.action.end());
                // ROS_INFO("ACTION[0]:%d", action[0]);
                // ROS_INFO("ACTION[1]:%d", action[1]);

                oldaction.assign(action.begin(), action.end());
                oldpos.assign(pos.begin(), pos.end());
                oldcup.assign(cup.begin(), cup.end());                  

                reverse(action.begin(), action.end());

                //X,Y,THETA
                pos.assign(g_srv.response.position.begin(), g_srv.response.position.end());
                // ROS_INFO("POS[0]:%f", pos[0]);
                // ROS_INFO("POS[1]:%f", pos[1]);
                // ROS_INFO("POS[2]:%f", pos[2]);
                reverse(pos.begin(), pos.end());

                //CUP NUMBER, HAND, COLOR
                cup.assign(g_srv.response.cup.begin(), g_srv.response.cup.end());
                // ROS_INFO("CUP[0]:%d", cup[0]);
                // ROS_INFO("CUP[1]:%d", cup[1]);
                reverse(cup.begin(), cup.end());

                give_action();

                // old_x = now_x;
                // old_y = now_y;
                // old_th = now_th;
 
                first = 1;
                i = 1; 
            }
            else{
                ROS_INFO("NEW ACTION");

                // old_x = now_x;
                // old_y = now_y;
                // old_th = now_th;
                // ROS_INFO("ACTION LEN: %ld", action.size());
                oldaction.assign(action.begin(), action.end());
                // ROS_INFO("POS LEN: %ld", pos.size());  
                oldpos.assign(pos.begin(), pos.end());
                // ROS_INFO("CUP LEN: %ld", cup.size());
                oldcup.assign(cup.begin(), cup.end());
                // ROS_INFO("SRV LEN: %ld", g_srv.response.action.size());
                action.assign(g_srv.response.action.begin(), g_srv.response.action.end());
                // ROS_INFO("ACTION[0]:%d", action[0]);
                // ROS_INFO("ACTION[1]:%d", action[1]);
                reverse(action.begin(), action.end());

                //X,Y,THETA
                pos.assign(g_srv.response.position.begin(), g_srv.response.position.end());
                // ROS_INFO("POS[0]:%f", pos[0]);
                // ROS_INFO("POS[1]:%f", pos[1]);
                // ROS_INFO("POS[2]:%f", pos[2]);
                reverse(pos.begin(), pos.end());
                
                //CUP NUMBER, HAND, COLOR(0:no cup, 2:green, 3:red)
                cup.assign(g_srv.response.cup.begin(), g_srv.response.cup.end());
                // ROS_INFO("CUP[0]:%d", cup[0]);
                // ROS_INFO("CUP[1]:%d", cup[1]);
                reverse(cup.begin(), cup.end());

                give_action();
                //ROS_INFO("GET DONE");
                i = 1;                
            }
        }
        else{
            ROS_INFO("NOT GET MESSAGE");
        }            
    }
}

int goap_data::getaction(){ 
    return now_action;
}
float goap_data::get_action_x(){ 
    return now_x;
}
float goap_data::get_action_y(){ 
    return now_y;
}
float goap_data::get_action_th(){ 
    return now_th;
}
int goap_data::get_action_color(){ 
    return now_color;
}
int goap_data::get_action_cup(){ 
    return now_cup;
}
int goap_data::get_action_hand(){
    return now_hand;
}
bool goap_data::samePosOrNot(){
    if(now_x == old_x && now_y == old_y && now_th == old_th){
        // ROS_INFO("SAME POS");
        // old_x = now_x;
        // old_y = now_y;
        // old_th = now_th;
        return true;//(1)
    }
    else{
        old_x = now_x;
        old_y = now_y;
        old_th = now_th;        
        // ROS_INFO("NEW POS");
        return false;//(0)
    }  
}

bool goap_data::sameActionOrNot(){
    // ROS_INFO("OA: %d, OC: %d, OH: %d", old_action, old_cup, old_hand);
    // ROS_INFO("A: %d, C: %d, H: %d", now_action, now_cup, now_hand);

    if(now_action == old_action && now_cup == old_cup && now_hand == old_hand){
        // ROS_INFO("SAME ACT");
        // old_x = now_x;
        // old_y = now_y;
        // old_th = now_th;
        return true;//(1)
    }
    else{
        old_action = now_action;
        old_cup = now_cup;
        old_hand = now_hand;        
        // ROS_INFO("NEW ACT");
        return false;//(0)
    }  
}
