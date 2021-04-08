#include <ros/ros.h>
#include "main2021/cup_camera.h"

#include <iostream>
#include <stdlib.h>
#include <vector>

using namespace std;

typedef struct c
{
	pair<float, float> pos;
	int color;
}CUP;

CUP cup[24] = {
    {.pos = pair<float, float>(400., 300.), .color = 3}, {.pos = pair<float, float>(1200., 300.), .color = 2},
	{.pos = pair<float, float>(515., 445.), .color = 2}, {.pos = pair<float, float>(1085., 445.), .color = 3},
	{.pos = pair<float, float>(100., 670.), .color = 2}, {.pos = pair<float, float>(400., 956.), .color = 3}, 
	{.pos = pair<float, float>(1955., 1005.), .color = 3}, {.pos = pair<float, float>(1655., 1065.), .color = 2},
	{.pos = pair<float, float>(800., 1100.), .color = 2}, {.pos = pair<float, float>(1200., 1270.), .color = 3},
	{.pos = pair<float, float>(1655., 1335.), .color = 3}, {.pos = pair<float, float>(1955., 1395.), .color = 2},
	{.pos = pair<float, float>(1955., 1605.), .color = 3}, {.pos = pair<float, float>(1655., 1665.), .color = 2},
	{.pos = pair<float, float>(1200., 1730.), .color = 2}, {.pos = pair<float, float>(800., 1900.), .color = 3},
	{.pos = pair<float, float>(1655., 1935.), .color = 3}, {.pos = pair<float, float>(1955., 1995.), .color = 2},
	{.pos = pair<float, float>(400., 2044.), .color = 2}, {.pos = pair<float, float>(100., 2330.), .color = 3},
	{.pos = pair<float, float>(515., 2555.), .color = 2}, {.pos = pair<float, float>(1085., 2555.), .color = 3},
	{.pos = pair<float, float>(400., 2700.), .color = 3}, {.pos = pair<float, float>(1200., 2700.), .color = 2}
};


bool callbackfun(main2021::cup_camera::Request &req, main2021::cup_camera::Response &res){
    ROS_INFO("call");
    if(req.req == true){
        res.color.clear();
        res.cup_pos.clear();
        for(int i = 0 ; i < 24 ; i ++){
            ROS_INFO("TRUE");
            res.color.push_back(cup[i].color);
            res.cup_pos.push_back(cup[i].pos.first);
            res.cup_pos.push_back(cup[i].pos.second);
            res.cup_pos.push_back(0);
        }
    }
    else{
        ROS_INFO("FALSE");
        res.color = {0};
        res.cup_pos = {0};
    }
    return true;
}

int main(int argc, char** argv){
    ros::init(argc, argv, "camera_node");
    ros::NodeHandle n;
    ros::ServiceServer c_srv;
    c_srv = n.advertiseService("cup_camera", callbackfun);
    
    // while (ros::ok())
    // {
        for(int j = 0 ; j < 24 ; j++){
            ROS_INFO("X:%f", cup[j].pos.first);
            ROS_INFO("Y:%f", cup[j].pos.second);
            ROS_INFO("COLOR:%d", cup[j].color);
        }
            
        ROS_INFO("CAMERA");
        ros::spin();        
    // }


    return 0;
}