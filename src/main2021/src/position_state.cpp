#include <ros/ros.h>
#include "std_msgs/Int32MultiArray.h"

#include "../include/main2021/position_state.h"

//tf2 must
#include <tf2_ros/transform_broadcaster.h>
#include "tf2_ros/transform_listener.h"
#include <tf2/LinearMath/Quaternion.h>
#include "tf2/LinearMath/Transform.h"
#include <tf2/LinearMath/Scalar.h>
//not sure
#include "tf2/convert.h"
#include "tf2/utils.h"
#include "tf2_geometry_msgs/tf2_geometry_msgs.h"
#include "tf2_ros/buffer.h"
#include "tf2_ros/message_filter.h"
#include "message_filters/subscriber.h"

#include "nav_msgs/Odometry.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

Position::Position(float x, float y){
    sub_planner = n.subscribe<std_msgs::Int32MultiArray>("plan_state", 1, &Position::P_callback, this);
    // pub_state = n.advertise<std_msgs::Int32MultiArray>("plan_state", 1);
    pub_planner = n.advertise<geometry_msgs::PoseStamped>("/move_base_simple/goal", 1000);
    pub_cup = n.advertise<std_msgs::Int32MultiArray>("plan_cup", 10);
    sub_enemy1 = n.subscribe<geometry_msgs::PoseStamped>("/enemy_pose", 1000, &Position::E1_callback, this);
    sub_enemy2 = n.subscribe<geometry_msgs::PoseStamped>("/enemy_pose2", 1000, &Position::E2_callback, this);
    sub_location = n.subscribe<nav_msgs::Odometry>("/global_filter", 1000, &Position::L_callback, this);

    e1_x = 0.;
    e1_y = 0.;
    e2_x = 0.;
    e2_y = 0.;
    px = x;
    py = y;
    pz = 0.;

    p_count = 0;
    count_old = 0;
    give = 0;
    give_old = 0;

    p_degree_R = 0;
    p_degree_P = 0;
    p_degree_Y = 0;
    p_state = {1, 0};

    // p_sta.data = {1, 0, 0};

}

void Position::give_plan(float action_x, float action_y, float action_th){
    transformStamped.header.stamp = ros::Time::now();
    transformStamped.header.frame_id = "map";
    //publish is meter
    transformStamped.pose.position.x = (action_x/1000);//meter
    transformStamped.pose.position.y = (action_y/1000);//meter
    transformStamped.pose.position.z = 0;
    odom_quat.setRPY(0, 0, action_th);
    transformStamped.pose.orientation.x = odom_quat.x();
    transformStamped.pose.orientation.y = odom_quat.y();
    transformStamped.pose.orientation.z = odom_quat.z();
    transformStamped.pose.orientation.w = odom_quat.w();

    pub_planner.publish(transformStamped);

    p_state[0] = 0;
    give++;
    // p_sta.data[0] = 0;
    // p_sta.data[1] = 0;

    // pub_state.publish(p_sta);
}

void Position::give_cup(int c, int m, bool team){
    if(m == 12){
        p_cup.data.push_back(c);
    }
    else if(m == 13){ //blue0:get cup2 and cup4-->10, yellow1::get cup22 and cup24-->10485760
        if(team == 0){
            p_cup.data.push_back(2);
            p_cup.data.push_back(4);
        }
        else if(team == 1){
            p_cup.data.push_back(22);
            p_cup.data.push_back(24);            
        }        

    } 
    else if(m == 14){ //blue0:get cup1 and cup3-->5, yellow1::get cup21 and cup23-->5242880
        if(team == 0){
            p_cup.data.push_back(1);
            p_cup.data.push_back(3);           
        }
        else if(team == 1){
            p_cup.data.push_back(21);
            p_cup.data.push_back(23);           
        }    
    }

    pub_cup.publish(p_cup);
}

void Position::P_callback(const std_msgs::Int32MultiArray::ConstPtr& msg){
    //p_state[0] = done or not, p_state[1] = cannot find
    if(msg->data[2] != count_old){
        p_state.assign(msg->data.begin(), msg->data.end());
        p_count = msg->data[2];        
    }
    // ROS_INFO("P_RES: %d", p_state[0]);
}
void Position::E1_callback(const geometry_msgs::PoseStamped::ConstPtr& msg){
    //receive is meter
    e1_x = (msg->pose.position.x * 1000);
    e1_y = (msg->pose.position.y * 1000);
}
void Position::E2_callback(const geometry_msgs::PoseStamped::ConstPtr& msg){
    //receive is meter
    e2_x = (msg->pose.position.x * 1000);
    e2_y = (msg->pose.position.y * 1000);
}
void Position::L_callback(const nav_msgs::Odometry::ConstPtr& msg){
    //receive is meter
    px = (msg->pose.pose.position.x * 1000);
    py = (msg->pose.pose.position.y * 1000);
    pz = (msg->pose.pose.position.z * 1000);
    // ROS_INFO("position px: %f", px);
    // ROS_INFO("position py: %f", py);

    tf2::Quaternion q(msg->pose.pose.orientation.x, msg->pose.pose.orientation.y, msg->pose.pose.orientation.z, msg->pose.pose.orientation.w);
    tf2::Matrix3x3 m(q);
    m.getRPY(p_degree_P, p_degree_R, p_degree_Y);
    // ROS_INFO("position th: %f", p_degree_Y);  
}

//can plan?
bool Position::findWay(){
    if(p_state[1] == 1)
        return false;//(0)
    else
        return true;//(1)
}
int Position::get_p_state(){//{FALSE = 0, SUCCESS, DOING, emerg};
    ros::spinOnce();
    // // ROS_INFO("Pcall");
    // ROS_INFO("P_RES: %d", p_state[0]);
    // ROS_INFO("give: %d", give);
    // ROS_INFO("give_old: %d", give_old);
    // ROS_INFO("p_count: %d", p_count);
    // ROS_INFO("count_old: %d", count_old);
    if(findWay()){
        if(give != give_old){ //give new action
            // give_old++;
            give_old = give;
            p_state[0] = 0;
            return 2;            
        }
        else{
            if(p_count != count_old) //new rescive
                count_old = p_count;
            if(p_state[0] == 0)
                return 2;
            else
                return 1;                        
        }
    }   
    else
        return 0;//--> cannot find
}
float Position::get_e1_x(){ return e1_x;}
float Position::get_e1_y(){ return e1_y;}
float Position::get_e2_x(){ return e2_x;}
float Position::get_e2_y(){ return e2_y;}
float Position::get_px(){ return px;}
float Position::get_py(){ return py;}
float Position::get_pz(){ return pz;}
float Position::getdegree(){ return (float)p_degree_Y;}
