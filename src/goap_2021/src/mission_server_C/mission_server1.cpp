#include "ros/ros.h"
#include <ros/package.h> //not sure if needed
#include "std_msgs/String.h"
#include <sstream>
#include <stdio.h>
#include <iostream>
#include <string>
using namespace std;

#include <goap_2021/mission_srv.h>

// #include "mission_setting.h"
#include "mission_action.h"

int tx = 101;
class mission_setting{
    public:
        int mission_no;
        string mission_name;
        int count;
        int action[10];
        int prepare;
        mission_setting(int num, string name, int no,  int pre){//int array[],
            mission_no = num;
            mission_name = name;
            count = no;
            // for( int i = 0; i < 10; i++){
            //     action[ i ] = array[ i ];
            // }
            prepare = pre;
            // setting_( num, name, count );
        }
}; mission_setting emergency(0, "emergency", 0, 0);//[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 
    mission_setting windsock( 1, "windsock", 0, 0);
    mission_setting lhouse(2, "lhouse", 0, 0);
    mission_setting flag( 3, "flag", 0, 0);
    mission_setting anchorN(4, "anchorN", 0, 0);
    mission_setting anchorS(5, "anchorS", 0, 0);
    mission_setting reef_l( 6, "reef_l", 0, 0);
    mission_setting reef_r( 7, "reef_r", 0, 0);
    mission_setting reef_p( 8, "reef_p", 0, 0);
    mission_setting placecup_h( 9, "placecup_h", 0, 0);
    mission_setting placecup_p( 10, "placecup_p", 0, 0);
    mission_setting placecup_r( 11, "placecup_r", 0, 0);
    mission_setting getcup(12, "getcup", 0, 0);
    mission_setting getcup_12( 13, "getcup_12", 0, 0);
    mission_setting getcup_34( 14, "getcup_34", 0, 0);

bool mission_main( goap_2021::mission_srv::Request  &req,
         goap_2021::mission_srv::Response &res ){
    tx++;
    ROS_INFO("222 %d", tx);
    int success = 1, fail = 0, ing = 2, stop = 3;
    switch (req.action)
    {
    case 0: //emergency
        res.state = stop;
        
        // ROS_INFO("case 0, name %d, count %d\n", emergency.mission_no, emergency.count );
        ROS_INFO("case 0, name %d, count %d, action %d, tx %d\n", emergency.mission_no, emergency.count, action_0[0], tx );
        break;
    case 1: //windsock
        res.state = success;
        break;
    case 2: // lhouse
        res.state = success;
        break;
    case 3: // flag
        res.state = success;
        break;
    case 4: // anchorN
        res.state = success;
        break;
    case 5: // anchorS
        res.state = success;
        break;
    case 6: // reef_l
        res.state = success;
        break;
    case 7: // reef_r
        res.state = success;
        break;
    case 8: // reef_p
        res.state = success;
        break;
    case 9: // placecup_h
        res.state = success;
        break;
    case 10: // placecup_p 
        res.state = success;
        break;
    case 11: // placecup_r
        res.state = success;
        break;
    case 12: // getcup
        res.state = success;
        break;
    case 13: // getcup12
        res.state = success;
        break;
    case 14: // getcup34
        res.state = success;
        break;
    default:
        break;
    }

    // ros::init(argc, argv, "talker");
    ros::NodeHandle n; // node handler
    ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1); 
    ros::Rate loop_rate(10);
    std_msgs::String msg;
    std::stringstream ss;
    ss << "hello world " << tx;
    msg.data = ss.str();
    chatter_pub.publish(msg);
    ros::spin(); 
    // loop_rate.sleep();
    ROS_INFO("in bool mission case = %d", req.action);
    return true;
}

int main(int argc, char **argv)
{
    ROS_INFO("mission initialize\n");
    ros::init(argc, argv, "talker");
    ros::init(argc, argv, "mission_server"); 
    ros::NodeHandle n; // node handler
    // ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1); 
    // ros::Rate loop_rate(10);

    
    // ros::spin(); 

    ros::ServiceServer service = n.advertiseService("mission", mission_main); 
    ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1000); 
    ros::Rate loop_rate(10);
    std_msgs::String msg;
    std::stringstream ss;
    ss << "hello world " << tx;
    msg.data = ss.str();
    chatter_pub.publish(msg);
    loop_rate.sleep();
    ROS_INFO("%s", msg.data.c_str());
    ROS_INFO("2 state ");
    // int count = 0;
    // while (ros::ok()){
        
    // }
    //     std_msgs::String msg;
    //     std::stringstream ss;
    //     ss << "hello world " << tx;
    //     msg.data = ss.str();

        // ros::ServiceServer service = n.advertiseService("mission", mission_main); 
        // 
        
        // ROS_INFO("%s", msg.data.c_str());
        // chatter_pub.publish(msg);
        ros::spin(); 
        // loop_rate.sleep();
        // ++count;
    // }

    // ros::init(argc, argv, "talker");
    // ros::NodeHandle n; // node handler
    // ros::Publisher chatter_pub = n.advertise<std_msgs::String>("chatter", 1); 
    // ros::Rate loop_rate(10);
    // std_msgs::String msg;
    // std::stringstream ss;
    // ss << "hello world " << tx;
    // msg.data = ss.str();
    // chatter_pub.publish(msg);
    // ros::spin(); 
    // loop_rate.sleep();
    return 0;
}

