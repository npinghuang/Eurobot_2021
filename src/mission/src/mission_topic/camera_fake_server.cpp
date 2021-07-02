#include "ros/ros.h"
#include "mission/mission_camera.h"

bool camera(mission::mission_camera::Request  &req,
         mission::mission_camera::Response &res)
{
    ROS_INFO("into bool");
    res.coordinate_camera.resize(3);
    for ( int i = 0; i < 2; i++){
      ROS_INFO("into for");
      res.coordinate_camera[i] = req.coordinate_mission[i];
        // ROS_ERROR("failed to get coordinate");
    }
    // res.coordinate_camera = new int [2];
    // int size = sizeof(res.coordinate_camera)/sizeof(res.coordinate_camera[0]);
    // ROS_INFO("ros %d", size);
    // res.coordinate_camera[0] = req;//req.x
    // res.coordinate_camera[1] = 87;//req.y
    res.cup_color_camera = req.cup_color_mission;
  
  ROS_INFO("request: x=%d, y=%d", req.coordinate_mission[0], req.coordinate_mission[1]);
//   ROS_INFO("sending back response: [%ld]", (long int)res.sum);
  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "camera_fake_server");
  ros::NodeHandle n;

  ros::ServiceServer service = n.advertiseService("camera_fake_server", camera);
  ROS_INFO("Ready camera fake");
  ros::spin();

  return 0;
}