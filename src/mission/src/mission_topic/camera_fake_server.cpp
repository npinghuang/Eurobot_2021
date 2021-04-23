#include "ros/ros.h"
#include "mission/mission_camera.h"

bool camera(mission::mission_camera::Request  &req,
         mission::mission_camera::Response &res)
{
    for ( int i = 0; i < 2; i++){
        res.coordinate_camera[i] = req.coordinate_mission[i];
    }
    res.cup_color_camera = req.cup_color_mission;
  
//   ROS_INFO("request: x=%ld, y=%ld", (long int)req.a, (long int)req.b);
//   ROS_INFO("sending back response: [%ld]", (long int)res.sum);
  return true;
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "camera_fake_server");
  ros::NodeHandle n;

  ros::ServiceServer service = n.advertiseService("camera_fake_server", camera);
//   ROS_INFO("Ready to add two ints.");
  ros::spin();

  return 0;
}