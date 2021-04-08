#include <ros/ros.h>
#include <iostream>
#include <aruco_pose/MarkerArray.h>
#include <aruco_pose/Marker.h>
#include "std_msgs/String.h"
#include "std_msgs/Int32.h"
#include "math.h"
#include <geometry_msgs/PointStamped.h>
#include <tf/transform_listener.h>
#include <tf/transform_broadcaster.h>
#include <aruco_pose/cup.h>
#include <aruco_pose/ns.h>

//using namespace std;

class Camera
{

public:
    ros::NodeHandle n;

    ros::ServiceServer service1;

    ros::ServiceServer service2;

    int MarkerCplt;

    int CupCplt;

    ros::Subscriber aruco;

    ros::Subscriber cup;

    ros::Subscriber machineStatus;

    // ros::Timer timer;

    ros::Publisher pub;

    int count1;

    int count2;

    int count3;

    float sum;

    float last_data;

    float angle;

    float angle2;

    float angle3;

    float last_data2;

    float last_data3;

    ros::Time start_time;
    
    ros::Time now_time;

    std::stringstream strBufferMarker;

    std::stringstream strBufferCup;

    std_msgs::String str;

    std_msgs::String CupTempBuffer;

    std_msgs::String CupDataPast;
    
    std_msgs::String CupDataChecked;

    std_msgs::String N_S_Result;

    int CupDataStable;

    int N_S_DataStable;

    int N_S_DataPast;
 
    float markerX;

    float markerY;

    float markerZ;

    int CupCheckTime;

    int N_S_CheckTime;

    int machineState;
    
    int angleMargin;
    
    bool NS_Start;
    
    bool Cup_Start;
    
    int testStart;
    
    int MarkerStart;

    Camera()
    {
        MarkerCplt = 0;
        CupCplt = 0;
        markerX = 0;
        markerY = 0;
        markerZ = 0;
        pub = n.advertise<std_msgs::String>("Cup_NS", 1);
        aruco = n.subscribe("aruco_detect/markers", 1000, &Camera::markersCallback, this);
        machineStatus = n.subscribe("pub_status",1,&Camera::updateStatus,this);
        machineState = 0;
        cup = n.subscribe("cup", 1000, &Camera::CupCallback, this);
        service1 = n.advertiseService("cup", &Camera::CupService,this);
        service2 = n.advertiseService("ns", &Camera::N_S_Service,this);
        // timer = n.createTimer(ros::Duration(1), &Camera::timerCallback,this);
        count1 = 0;
        count2 = 0;
        count3 = 0;
        sum = 0;
        last_data = 0;
        angle = 0;
        angle2 = 0;
        angle3 = 0;
        last_data2 = 0;
        last_data3 = 0;
        CupCheckTime = 0;
        N_S_DataStable = 0;
        N_S_CheckTime = 0;
        CupDataStable = 0;
        N_S_DataPast = 0;
        Cup_Start = false;
        NS_Start = false;
        MarkerStart = 0;
        strBufferCup << "11111";
    }




    void AngleTransform(float x, float y, float z, float w){
        angle = atan2(2 * (w * z + x * y), 1 - 2 * (z * z + y * y));
        angle *= -1;
        angle /= 3.1415926;
        angle *= 180;
        if(angle < 0)
            angle += 360;
        ROS_INFO("angle = %f",angle);    
        angle2 = asin( 2 * (w * y - x * z));
        angle2 *= -1;
        angle2 /= 3.1415926;
        angle2 *= 180;
        if(angle2 < 0 )
            angle2 += 360;
        angle3 = atan2(2 * (y * z + x * w), 1 - 2 * (z * z - w * w));
        angle3 *= -1;
        angle3 /= 3.1415926;
        angle3 *= 180;
        if(angle3 < 0)
            angle3 += 360;
    }

    void markersCallback(const aruco_pose::MarkerArray::ConstPtr &markers)
    {
        n.getParam("CameraResultWithoutMachineStatus/angleMargin",angleMargin);
        if (!markers->markers.empty())
        {
            //n.getParam("CameraResult/testStart",testStart);
            //ROS_INFO("now = %lf",now_time);
            //ROS_INFO("start = %lf",start_time);
            //ROS_INFO("time = %f",(now_time-start_time).toSec());
            //if ((now_time - start_time).toSec() >= 25){
           if(markers->markers[0].id == 17) {

                        last_data = angle;   // target angle (Used for NS detection)
                        last_data2 = angle2;
                        last_data2 = angle3;
                        // ROS_INFO("id:%ld",markers->markers[0].id );
                        AngleTransform(markers->markers[0].pose.orientation.x,markers->markers[0].pose.orientation.y,markers->markers[0].pose.orientation.z,markers->markers[0].pose.orientation.w);
                        ROS_INFO("angle = %f",angle);
                        ROS_INFO("NS_Stable = %d",N_S_DataStable);
                        if ((angle > last_data - 20 || angle < last_data + 20)){
                            count1++;
                            //count 5 time to check the angle is stable
                            //ROS_INFO("angle = %f", angle);
                            if (count1 == 5){
                            //if the angle is stable find out the final result of NS after getting 5 identical result( N or S)
                                if (angle >= 360 - angleMargin || angle <= 0 + angleMargin){
                                    strBufferMarker << 0;
                                    N_S_Result.data = strBufferMarker.str();
                                    ROS_INFO("%d", N_S_Result.data[0]);
                                    MarkerCplt = 1;
                                    // ROS_INFO("Heading to North");
                                }

                                else if (angle >= 180 - angleMargin && angle <= 180 + angleMargin){
                                    strBufferMarker << 1;
                                    N_S_Result.data = strBufferMarker.str();
                                    ROS_INFO("%d", N_S_Result.data[0]);
                                    MarkerCplt = 1;
                                    // ROS_INFO("Heading to South");
                                }


                                if (N_S_DataStable != 1){
                                    if (N_S_DataPast != N_S_Result.data[0]){
                                        N_S_CheckTime = 0;
                                        N_S_DataPast = N_S_Result.data[0];
                                    }
                                    else{
                                        N_S_CheckTime++;
                                        if (N_S_CheckTime == 5)
                                            N_S_DataStable = 1;
                                    }
                                }
                                count1 = 0;
                                
                                 //strBufferMarker.data = strBuffer.str();
                                 //pub.publish(N_S_Result);
                                // ROS_INFO("angle = %f", angle);
                            }
                        }
                        //if ((angle2 > last_data2 - 10 || angle2 < last_data2 + 10))
                            //count2++;
                        //if (count2 == 5)
                           // count2 = 0;
                        //if ((angle3 > last_data3 - 10 || angle3 < last_data3 + 10))
                            //count3++;
                        //if (count3 == 5)
                            //count3 = 0;
                    }
                    


        }

    }


    void updateStatus(const std_msgs::Int32::ConstPtr & msg){
        //ROS_INFO("%d",msg->data);
        if(msg->data == 4 && Cup_Start == false){
            Cup_Start = true;
        }
        else if (msg->data == 5 && NS_Start == false)
        {
            NS_Start = true;
            ROS_INFO("gogo");
            //start_time = ros::Time::now();
        }
    }

    void CupCallback(const std_msgs::String::ConstPtr &msg)
    {
		if(Cup_Start == true){
			if (CupCplt != 1){
				if(CupCheckTime != 5){
					strBufferCup << msg->data.c_str();
				CupTempBuffer.data = strBufferCup.str();
					for (int QAQ = 0; QAQ < 5; QAQ++)
					{
						if (CupTempBuffer.data[QAQ] != CupDataPast.data[QAQ])   
						//check if data is stable for 5 times
						{
							CupCheckTime = 0;
							for (int OUO = 0; OUO < 5; OUO++){
								CupDataPast.data[OUO] = CupTempBuffer.data[OUO];
							}
							//if not identical for two data  
							//recount 5 times for a new check
							break;
						}
						else{
							if (QAQ == 4)
								CupCheckTime++;
						}
					}
				}
				
				if (CupCheckTime == 5)
					CupDataStable = 1;
				// ROS_INFO("%d", CupTempBuffer.data[0]);
				if (CupDataStable == 1)
				{
					
					CupDataPast.data = CupTempBuffer.data;
					CupDataChecked.data = CupTempBuffer.data;
					// ROS_INFO("%s",CupDataPast.data);
					//pub.publish(CupDataPast);
				}
			}
		}	

        
    }

    bool CupService(aruco_pose::cup::Request &req, aruco_pose::cup::Response &res)
    {
        if(req.OUO == 1){
            if(CupDataStable == 1){
                for (int count = 0; count < 5; count++){
                   ROS_INFO("%d", CupDataChecked.data[count]);
                   res.CupResult.push_back(CupDataChecked.data[count]-48);
                }
                return true;
                //1 means
            }
        }
        else if(req.OUO == 2){
            CupCplt = 1;
            return true;
        }
        else if(req.OUO == 3){
            CupDataStable == 0;
            CupCheckTime = 0;
            return false;
        }
        else if(req.OUO == 4){
        
        }
        
    }
    bool N_S_Service(aruco_pose::ns::Request &req, aruco_pose::ns::Response &res)
    {
        if(req.OAO == 1){
            if(N_S_DataStable == 1){
                res.ns = N_S_Result.data[0] - 48;
                return true;
                // 0 represent N
                //1 represent S
            }
        }
        else if(req.OAO == 2){
            MarkerCplt = 1;
            return true;
        }
        else if(req.OAO == 3){
            N_S_DataStable = 0;
            N_S_CheckTime = 0;
            return false;
        }
        else if(req.OAO == 4){
        
        }
        else if(req.OAO == 5){
        
        }
        else if(req.OAO == 10){
            MarkerStart = 1;
            ROS_INFO("%d",MarkerStart);
            res.ns = 10;
        }

    }

    void Publish()
    {
        // if (CupCplt == 1 && MarkerCplt == 1)
       if (MarkerCplt == 1){
        // ROS_INFO("FUCK Brian");
            std::stringstream strForAssemble;
            strForAssemble << strBufferCup.str() << strBufferMarker.str();
            //strForAssemble << strBufferMarker.str();
            str.data = strForAssemble.str();
            pub.publish(str);
        // CupCplt = 0;
            MarkerCplt = 0;
        //strBufferCup.str("");
        //strBufferCup.clear();
            strBufferMarker.str("");
            strBufferMarker.clear();
       }
    }

    void transformPoint(const tf::TransformListener &listener){
        geometry_msgs::PointStamped Camera_point;
        Camera_point.header.frame_id = "base_Camera";
        //we'll just use the most recent transform available for our simple example
        Camera_point.header.stamp = ros::Time();
        //just an arbitrary point in space
        Camera_point.point.x = markerX;
        Camera_point.point.y = markerY;
        Camera_point.point.z = markerZ;
        try
        {
            geometry_msgs::PointStamped base_point;
            listener.transformPoint("base_link", Camera_point, base_point);
            // ROS_INFO("base_Camera: (%.2f, %.2f. %.2f) -----> base_link: (%.2f, %.2f, %.2f) at time %.2f",
            //         Camera_point.point.x, Camera_point.point.y, Camera_point.point.z,
            //         base_point.point.x, base_point.point.y, base_point.point.z, base_point.header.stamp.toSec());
        }

        catch (tf::TransformException &ex)
        {

            ROS_ERROR("Received an exception trying to transform a point from \"base_laser\" to \"base_link\": %s", ex.what());
        }
    }
};

int main(int argc, char **argv)
{

    ros::init(argc, argv, "CameraResult");
    //tf::TransformListener listener(ros::Duration(10));
    //ros::Subscriber sub2 = n.subscribe("pub", 1, chatterCallback);
    Camera camera;
    camera.MarkerStart = 1;
    while(ros::ok())
    {
        camera.Publish();
         if(camera.machineState == 1){
            //camera.now_time = ros::Time::now();
        }
        ros::spinOnce();
    }
    
    // ros::Timer timer = camera.n.createTimer(ros::Duration(1.0), boost::bind(Camera::transformPoint, boost::ref(listener)));

    return 0;
}
