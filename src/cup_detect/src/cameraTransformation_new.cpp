#include <ros/ros.h>
#include <iostream>
#include <fstream>
#include <stdlib.h>
#include "cup_detect/transSrv2.h"

std::vector<std::vector<int>> data;
std::vector<int> data_2;

bool coordinateTrans(cup_detect::transSrv2::Request &cam, cup_detect::transSrv2::Response &coor)
{
      if (!cam.reverse)
      {
            int distance, leastDis, firstNum = 1;
            for (int i = 0; i < data.size(); i++)
            {
                  distance = pow(cam.camera_x - data[i][0], 2) + pow(cam.camera_y - data[i][1], 2);
                  if (firstNum)
                  {
                        leastDis = distance;
                        firstNum = 0;
                  }
                  else if (leastDis > distance)
                  {
                        coor.robot_x = data[i][2];
                        coor.robot_y = data[i][3];
                        leastDis = distance;
                  }
            }
      }
      else
      {
            int distance, leastDis, firstNum = 1;
            for (int i = 0; i < data.size(); i++)
            {
                  distance = pow(cam.camera_x - data[i][2], 2) + pow(cam.camera_y - data[i][3], 2);
                  if (firstNum)
                  {
                        leastDis = distance;
                        firstNum = 0;
                  }
                  else if (leastDis > distance)
                  {
                        coor.robot_x = data[i][0];
                        coor.robot_y = data[i][1];
                        leastDis = distance;
                  }
            }
      }
      return true;
};
int main(int argc, char **argv)
{
      ros::init(argc, argv, "cameraTransformation");
      ros::NodeHandle nh_;
      ros::ServiceServer ser_ = nh_.advertiseService("cameraTransformation", coordinateTrans);
      std::ifstream inFile;
      // FILE * file;
      // file = fopen("/home/shark/catkin_ws/src/cup_detect/src/camera_Transformation.csv","a+");
      inFile.open("/home/shark/catkin_ws/src/cup_detect/src/camera_Transformation.csv", std::ios::in);
      if (inFile.fail())
      {
            std::cout << "Could Not Open File\n";
      }
      std::string value;
      std::string line;
      std::string field;
      while (getline(inFile, line)) //getline(inFile, line)表示按行讀取CSV檔案中的資料
      {
            std::istringstream sin(line); //將整行字串line讀入到字串流sin中  //將字串流sin中的字元讀入到field字串中，以逗號為分隔符  //將剛剛讀取的字串轉換成int
            getline(sin, field, ',');
            data_2.push_back(atoi(field.c_str()));
            // std::cout << atoi(field.c_str()) << " ";
            getline(sin, field, ',');
            data_2.push_back(atoi(field.c_str()));
            // std::cout << atoi(field.c_str()) << " ";
            getline(sin, field, ',');
            data_2.push_back(atoi(field.c_str()));
            // std::cout << atoi(field.c_str()) << " ";
            getline(sin, field);
            data_2.push_back(atoi(field.c_str()));
            // std::cout << atoi(field.c_str()) << std::endl;
            data.push_back(data_2);
            data_2.clear();
      }

      ROS_INFO_STREAM("Camera Coordinate Transformation Node Service Activate");
      inFile.close();

      while (ros::ok())
      {
            ros::spinOnce();
      }
      return 0;
}