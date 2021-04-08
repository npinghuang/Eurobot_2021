#include <ros/ros.h>
#include <iostream>
#include <aruco_pose/MarkerArray.h>
#include <aruco_pose/Marker.h>
#include "std_msgs/String.h"
#include "math.h"

//using namespace std;

#define anggleMargin  20

class Camera {
	ros::NodeHandle n;

public:
  int MarkerCplt;

  int CupCplt;

  ros::Subscriber aruco;

  ros::Subscriber cup;

  ros::Publisher  pub;

	int count;

	float sum;

	float last_data;

	float angle;

	float angle2;

	float angle3;

  float last_data2;

  float last_data3;

	std_msgs::String str;
	Camera() {
    MarkerCplt = 0;
    CupCplt = 0;
    pub = n.advertise<std_msgs::String>("Cup_NS",1);
		aruco = n.subscribe("aruco_detect/markers", 1000, &Camera::markersCallback,this);
    cup = n.subscribe("aruco_detect/markers", 1000, &Camera::CupCallback,this);
		count = 0;
		sum = 0;
		last_data = 0;
		angle = 0;
		angle2 = 0;
		angle3 = 0;
    last_data2 = 0;
    last_data3 = 0;
	}

	void markersCallback(const aruco_pose::MarkerArray::ConstPtr& markers) {
		std::stringstream strMarker;
		if(!markers->markers.empty()) {
			if(markers->markers[0].id == 17) {
				last_data = angle;
				last_data2 = angle2;
				last_data2 = angle3;
				ROS_INFO("id:%ld",markers->markers[0].id );
				angle = atan2(
						2 * (markers->markers[0].pose.orientation.w * markers->markers[0].pose.orientation.z +
								markers->markers[0].pose.orientation.x * markers->markers[0].pose.orientation.y),
						1 - 2 * (markers->markers[0].pose.orientation.z * markers->markers[0].pose.orientation.z +
								markers->markers[0].pose.orientation.y * markers->markers[0].pose.orientation.y));
				angle *= -1;
				angle /= (3.1415926);
				angle *= 180;
				if(angle < 0)
				angle += 360;

				angle2 = asin(
						2 * (markers->markers[0].pose.orientation.w * markers->markers[0].pose.orientation.y -
								markers->markers[0].pose.orientation.x * markers->markers[0].pose.orientation.z));
				angle2 *= -1;
				angle2 /= (3.1415926);
				angle2 *= 180;
				if(angle2 < 0)
				angle2 += 360;

				angle3 = atan2(
						2 * (markers->markers[0].pose.orientation.y * markers->markers[0].pose.orientation.z +
								markers->markers[0].pose.orientation.x * markers->markers[0].pose.orientation.w),
						1 - 2 * (markers->markers[0].pose.orientation.z * markers->markers[0].pose.orientation.z +
								markers->markers[0].pose.orientation.w * markers->markers[0].pose.orientation.w));
				angle3 *= -1;
				angle3 /= (3.1415926);
				angle3 *= 180;
				if(angle3 < 0)
				  angle3 += 360;

				if( (angle > last_data - 10 || angle < last_data + 10) ){
          count ++;
				  //ROS_INFO("angle = %f", angle);
				  if(count == 5) {
            if(angle >= 360 - anggleMargin || angle <= 0 + anggleMargin )
              strMarker << 1;
            else 
              strMarker << 0;  
					  count = 0;
            MarkerCplt = 1;
            // strBufferMarker.data = strBuffer.str();
            // pub.publish(strBufferMarker);
					  ROS_INFO("angle = %f", angle);
				  }
        }


				if( (angle2 > last_data2 - 10 || angle2 < last_data2 + 10) )
				  count ++;
				//ROS_INFO("angle = %f", angle);
				if(count == 5) {
					count = 0;
					// ROS_INFO("angle2 = %f", angle2);
				}

				if( (angle3 > last_data3 - 10 || angle3 < last_data3 + 10) )
				  count ++;
				//ROS_INFO("angle = %f", angle);
				if(count == 5) {
					count = 0;
					// ROS_INFO("angle3 = %f", angle3);
				}
			}
			ROS_INFO("x:%f",markers->markers[0].pose.position.x );
			ROS_INFO("y:%f",markers->markers[0].pose.position.y );
			ROS_INFO("z:%f",markers->markers[0].pose.position.z );
			//ROS_INFO("w:%f",markers->markers[0].pose.orientation.w);
			//ROS_INFO("angle = %f", angle);
		}
		else {
			ROS_INFO("None");
		}
	}


  void CupCallback(const std_msgs::String::ConstPtr& msg){
    // ROS_INFO("I heard: [%s]", msg->data.c_str());
    ROS_INFO("%s", msg->data.c_str());
    std::stringstream strCup;
    strCup << msg->data.c_str();
    CupCplt = 1;
  }

};





int main(int argc, char **argv) {

	ros::init(argc, argv, "CameraResult");
	//ros::Subscriber sub2 = n.subscribe("pub", 1, chatterCallback);
  Camera camera;
	while (ros::ok()) {
    if(CupCplt == 1 && MarkerCplt == 1){
      std::stringstream strForAssemble;
      strForAssemble << strCup.str() << strMarker.str();
      camera.str.data = strForAssemble.str();
      camera.pub.publish(camera.str);
      CupCplt = 0;
      MarkerCplt = 0;
    }
		ros::Duration(2).sleep();
		ros::spinOnce();
  }
  return 0;
}

