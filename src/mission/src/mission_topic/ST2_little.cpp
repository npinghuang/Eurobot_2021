#include "ros/ros.h"
#include "std_msgs/String.h"
#include <std_msgs/Int32MultiArray.h>
#include <sstream>

int ST2_little_rx = 9;
int ST2_little_tx = 88;
int state = 1;
ros::Publisher ST2_littletomission;
std_msgs::Int32MultiArray for_mission;
void chatterCallback(const std_msgs::Int32MultiArray::ConstPtr& msg)
{
    state = 1;
    for_mission.data.clear();
    for ( int i = 0; i < 9; i++){
      // if ( i == 0 && for_mission.data.size() != 0){
      //   
      // }
      for_mission.data.push_back (msg->data[i]);
      // ROS_INFO("ST2_little tx %d", msg->data[i]);
    }
    ST2_littletomission.publish(for_mission);
    // ROS_INFO("I heard action: [%d]", msg.data[0]);
}
int main(int argc, char **argv)
{
  ros::init(argc, argv, "ST2_little");

  ros::NodeHandle n;

ST2_littletomission = n.advertise<std_msgs::Int32MultiArray>("ST2_littleToMission", 1);
  ros::Subscriber sub = n.subscribe("MissionToST2_little", 1, chatterCallback);
  ros::Rate loop_rate(10);

  int count = 0;
  while (ros::ok())
  {
    
    // for_mission.data.push_back(state);
    // for_mission.data.push_back(ST2_little_rx);

    

    ros::spinOnce();

    loop_rate.sleep();
    ++count;
  }


  return 0;
}