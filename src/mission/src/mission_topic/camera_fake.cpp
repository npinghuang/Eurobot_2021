#include "ros/ros.h"
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Int32.h>
#include <sstream>
#include<vector>
using namespace std;
ros::Publisher cameratomission;
ros::Subscriber subcamera;
std_msgs::Int32MultiArray for_mission;
std::vector<int> fake_camera_data{2, 0, 12, 6, 1, -6, 10};

int timestamp = 1;
void chatterCallback(const std_msgs::Int32::ConstPtr& msg)
{
    if ( msg -> data == 1){
        for ( int i = 0; i < 7; i++){
             for_mission.data.push_back( fake_camera_data[i]);
            // ROS_INFO("ST2 tx %d", msg->data[i]);
        }
        for_mission.data.push_back( timestamp);
        cameratomission.publish(for_mission);
        for_mission.data.clear();
        timestamp ++;
        ROS_INFO("i got from mission [%d]", msg -> data);
    }    
    else{
        ROS_INFO("stop camera");
    }
}
int state_mission;

int main(int argc, char **argv)
{
    ros::init(argc, argv, "camera_fake");
    ros::NodeHandle n;
    cameratomission = n.advertise<std_msgs::Int32MultiArray>("opencv_Cups", 100);
    subcamera = n.subscribe("missiontoCamera", 100, chatterCallback);
    for_mission.data.clear();
    ros::Rate loop_rate(10);

    int count = 0;
    while (ros::ok())
    {
        ros::spinOnce();
        loop_rate.sleep();
    }
    return 0;
}