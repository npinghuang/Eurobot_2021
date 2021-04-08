#include <ros/ros.h>
#include <iostream>
#include <aruco_pose/MarkerArray.h>
#include <aruco_pose/Marker.h>
#include <message_filters/subscriber.h>
#include <message_filters/synchronizer.h>
#include <message_filters/sync_policies/approximate_time.h>
#include "Header.h"

using namespace message_filters;

void callback(const aruco_pose::MarkerArray::ConstPtr& markers1, const aruco_pose::MarkerArray::ConstPtr& markers2)
{
  ROS_INFO("id1 : %ld",markers1->markers[0].id );
  ROS_INFO("x1 : %f",markers1->markers[0].pose.position.x );
  ROS_INFO("y1 : %f",markers1->markers[0].pose.position.y );
  ROS_INFO("id2 : %ld",markers2->markers[0].id );
  ROS_INFO("x2 : %f",markers2->markers[0].pose.position.x );
  ROS_INFO("y2 : %f",markers2->markers[0].pose.position.y );
}


int main(int argc, char **argv)
{
  
  ros::init(argc, argv, "mapping");

  ros::NodeHandle nh;

  message_filters::Subscriber<aruco_pose::MarkerArray> node1_sub(nh, "node1/aruco_detect/markers", 20);
  message_filters::Subscriber<aruco_pose::MarkerArray> node2_sub(nh, "node2/aruco_detect/markers", 20);

  typedef sync_policies::ApproximateTime<aruco_pose::MarkerArray, aruco_pose::MarkerArray> MySyncPolicy;
  // ApproximateTime takes a queue size as its constructor argument, hence MySyncPolicy(10)
  Synchronizer<MySyncPolicy> sync(MySyncPolicy(10), node1_sub, node2_sub);
  sync.registerCallback(boost::bind(&callback, _1, _2));

  ros::spin();

  return 0;
}






