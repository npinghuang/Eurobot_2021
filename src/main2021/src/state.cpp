#include <ros/ros.h>

#include <iostream>
#include <stdlib.h>
#include <vector>
#include <algorithm>

#include "../include/main2021/state.h"
#include "../include/main2021/goap_state.h"


using namespace std;

State::State(float x, float y, float th, int c){
    my_x = x;
    my_y = y;
    my_z = 0.;
    degree = th;
    cup_color = {0, 1, 0, 1, 0, 1, 0, 1, 0, 1};
    hand = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    cup = c;
    ns = 0;
    team = 1; //blue:0, yellow:1
    emerg = false;
    time = 0;
    script = 0;
    status = 0;
    planer_state = SUCCESS;
    mission_state = SUCCESS;
    score = 0;

    red = 0;
    green = 0;
}


float State::getx(){ return my_x;}
float State::gety(){ return my_y;}
float State::getz(){ return my_z;}
float State::getth(){ return degree;}

std::vector<int>& State::get_hand(){ return hand;}
std::vector<int>& State::get_list(){ return actionList;}
std::vector<int>& State::get_color(){ return cup_color;}
int State::get_cup(){ return cup;}
bool State::get_ns(){ return ns;}
bool State::get_team(){ return team;}
bool State::emergOrNot(){ return emerg;}
float State::get_time(){ return time;}
int State::get_script(){ return script;}    
int State::get_status(){ return status;}
int State::get_score(){ return score;}

int State::get_p_state(){ return planer_state;}
int State::get_m_state(){ return mission_state;}

void State::setpos(float x, float y, float z, float th){
    my_x = x;
    my_y = y;
    my_z = z;
    degree = th;

    // ROS_INFO("state x: %f", my_x);
    // ROS_INFO("state y: %f", my_y);   
    // ROS_INFO("state th: %f", degree);   
}
void State::set_hand(std::vector<int>* h){
    hand.assign(h->begin(), h->end());
}
void State::set_list(std::vector<int>* a){
    actionList.assign(a->begin(), a->end());
}
void State::set_color(std::vector<int>* c){
    cup_color.assign(c->begin(), c->end());
}
void State::set_script(int sc){
    script = sc;
}
void State::set_cup(int c, int m){
    if(m == 12){
        c = 1 << (c-1);
        // ROS_INFO("state c: %d", c);
        // ROS_INFO("state cup 1: %d", cup);
        if((c & cup) != 0)
            cup = (c ^ cup);
        // ROS_INFO("state cup 2: %d", cup);
    }
    else if(m == 13){ //blue0:get cup2 and cup4-->10, yellow1::get cup22 and cup24-->10485760
        if(team == 0){
            if((10 & cup) != 0)
                cup = (10 ^ cup);            
        }
        else if(team == 1){
            if((10485760 & cup) != 0)
                cup = (10485760 ^ cup);            
        }        

    } 
    else if(m == 14){ //blue0:get cup1 and cup3-->5, yellow1::get cup21 and cup23-->5242880
        if(team == 0){
            if((5 & cup) != 0)
                cup = (5 ^ cup);            
        }
        else if(team == 1){
            if((5242880 & cup) != 0)
                cup = (5242880 ^ cup);            
        }    
    }
}
void State::updatecup(int c){ cup = c;}
void State::set_ns(bool n){ ns = n;}
void State::set_team(bool tm){ team = tm;}
void State::set_time(float t){ time = t;}
void State::set_status(int s){ status = s;}
void State::set_p_state(int state){ planer_state = state;}
void State::set_m_state(int state){ 
    if(state == 3)
        emerg = true;
    mission_state = state;
}
void State::set_emerg(bool e){ emerg = e;}
void State::set_score(int action, int color){
    if(action == 1) //windsock
        score += 15;
    else if(action == 2) //light house
        score += 10;
    else if(action == 3) //flag
        score += 10;
    else if(action == 4 || action == 5) //go home
        score += 10;
    else if(action == 12){ //get one cup
        score += 2;
        if(color == 2)
            green++;
        else if(color == 3)
            red++;        
    }     
    else if(action == 13 || action == 14){ //get two cup
        score += 2*2;
        if(color == 5){ //1 green, 1 red
            green++;
            red++;
        }
    }
    else if(action == 6 || action == 7 || action == 8){ //get five cup; 6:left, 7:right, 8:private
        score += 2*5;
        //1:red 0:green
        if(action == 6){ //left
            for(int i = 0 ; i < 5 ; i++){
                if(cup_color[i] == 0)
                    green++;                
                else if(cup_color[i] == 1)
                    red++;
            }
        }
        else if(action == 7){ //right
            for(int i = 5 ; i < 10 ; i++){
                if(cup_color[i] == 0)
                    green++;                
                else if(cup_color[i] == 1)
                    red++;
            }           
        }
        else if(action == 8){ //private; blue:(1, 0, 1, 0, 1), yellow:(0, 1, 0, 1, 0) 
            if(team == 0){ //blue
                green += 2;
                red += 3;
            } 
            else if(team == 1){ //yellow
                green += 3;
                red += 2;
            }
        }
    }
   
    //1 pair = 1 red + 1 green
    if(red != 0 && green != 0){
        if(red <= green){
            score += 2*red;
            green -= red;
            red = 0;
        }
        else{
            score += 2*green;
            red -= green;
            green = 0;
        }       
    }

    // ROS_INFO("SCORE: %d", score);
}
