#include <ros/ros.h>

#include <iostream>
#include <stdlib.h>
#include <vector>

#include "../include/main2021/friend_state.h"

Friend::Friend(){
    f_x = 0;
    f_y = 0;
    f_z = 0;
    f_degree = 0;
    for(int i = 0 ; i < 2 ; i++)
        f_action.push_back(0);
}

void Friend::setf_x(float x){ 
    f_x = x;
}
void Friend::setf_y(float y){ 
    f_y = y;
}
void Friend::setf_z(float z){ 
    f_z = z;
}
void Friend::setf_degree(float d){ 
    f_degree = d;
}
void Friend::setf_action(std::vector<int>* a){
    f_action.assign(a->begin(), a->end());
}

float Friend::getf_x(){ 
    return f_x;
}
float Friend::getf_y(){ 
    return f_y;
}
float Friend::getf_z(){ 
    return f_z;
}
float Friend::getf_degree(){ 
    return f_degree;
}
std::vector<int>& Friend::getf_action(){ 
    return f_action;
}
