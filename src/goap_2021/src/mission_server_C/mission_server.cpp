#include "ros/ros.h"
#include <ros/package.h> //not sure if needed

#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

#include <goap_2021/mission_srv.h>

// #include "mission_setting.h"

class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        mission_setting(int num, string name, int count){
            setting_( num, name, count );
        }
        void setting_ (int num, string name, int no ){
            mission_no = num;
            mission_name = name;
            count = no;
            printf("hi there : %d \n", mission_no);
        }
}; mission_setting emergency(0, "emergency", 0);
    mission_setting windsock( 1, "windsock", 0);
    mission_setting lhouse(2, "lhouse", 0);
    mission_setting flag( 3, "flag", 0);
    mission_setting anchorN(4, "anchorN", 0);
    mission_setting anchorS(5, "anchorS", 0);
    mission_setting reef_l( 6, "reef_l", 0);
    mission_setting reef_r( 7, "reef_r", 0);
    mission_setting reef_p( 8, "reef_p", 0);
    mission_setting placecup_h( 9, "placecup_h", 0);
    mission_setting placecup_p( 10, "placecup_p", 0);
    mission_setting placecup_r( 11, "placecup_r", 0);
    mission_setting getcup(12, "getcup", 0);
    mission_setting getcup_12( 13, "getcup_12", 0);
    mission_setting getcup_34( 14, "getcup_34", 0);

bool mission_main( goap_2021::mission_srv::Request  &req,
         goap_2021::mission_srv::Response &res ){
    // ROS_INFO("in void mission");
    int state = 0;
    switch (req.action[0])
    {
    case 0:
        state = req.action[0] + req.cup[0];
        res.state = state;

        ROS_INFO("case 0, name %d, count %d\n", emergency.mission_no, emergency.count );
        emergency.count ++;
        break;
    case 1:
        state = req.action[0] *10 + req.cup[0];
        res.state = state;
        break;
    default:
        break;
    }
    
    ROS_INFO("in bool mission case = %d, state = %d", req.action[0],  state);
    return true;
}

int main(int argc, char **argv)
{
    // // define each mission

    ROS_INFO("main, no %d\n", emergency.mission_no );

    // ROS_INFO("main, no %d\n", mi.mission_no );
    // ROS_INFO("main, name %s\n", emergency.mission_name ); bug here
    ros::init(argc, argv, "mission_server"); 
    ros::NodeHandle n; // node handler

    ros::ServiceServer service = n.advertiseService("mission", mission_main); 
    ROS_INFO("mission initialize\n");
    ros::spin(); 

    return 0;
   }

