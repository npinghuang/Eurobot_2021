#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <std_msgs/String.h>
#include "std_msgs/Int32.h"

#include <iostream>
#include <vector>
using namespace std;
static const std::string OPENCV_WINDOW = "Image window";



class ImageConverter
{
  ros::NodeHandle nh_;
  image_transport::ImageTransport it_;
  image_transport::Subscriber image_sub_;
  image_transport::Publisher image_pub_;

public:
  ros::Publisher pub = nh_.advertise<std_msgs::String>("cup", 1);
  std_msgs::String str;
  int xPosition;
  int yPosition;
  int width;
  int height;
  int CupDistance;
  int machineState; 
  double green_lowH;
  double green_lowS;
  double green_lowV;
  double green_highH;
  double green_highS;
  double green_highV;
  double red_lowH;
  double red_lowS;
  double red_lowV;
  double red_highH;
  double red_highS;
  double red_highV;
  double white_lowR;
  double white_lowG;
  double white_lowB;
  double white_highR;
  double white_highG;
  double white_highB;
  double black_lowR;
  double black_lowG;
  double black_lowB;
  double black_highR;
  double black_highG;
  double black_highB;
  int Cupdetected;
  int circleSize;
  int checkFinished;
  ImageConverter()
      : it_(nh_){
    // Subscrive to input video feed and publish output video feed
    // image_sub_ = it_.subscribe("camera/color/image_raw", 1, &ImageConverter::imageCb, this);
    image_sub_ = it_.subscribe("image_raw", 1, &ImageConverter::imageCb, this);
    image_pub_ = it_.advertise("/image_converter/output_video", 1);
    nh_.getParam("width",width);
    nh_.getParam("height",height);
    xPosition = 0;
    yPosition = 0;
    checkFinished = 0;
    cv::namedWindow(OPENCV_WINDOW);
  }

  ~ImageConverter()
  {
    cv::destroyWindow(OPENCV_WINDOW);
  }
  int checkRow(int posRow ,int posCol,int circle,cv_bridge::CvImagePtr final){
    int whiteCount = 0;
    int blackCount = 0;
    for(int now = posRow; now < posRow + circle ; now +=2)
      if(now > 0 && now < height){
        vector<int> tmp;
        tmp = final->image.row(now).col(posCol);
        if(tmp[0] == 255)
          whiteCount ++;
        else
          blackCount ++;
      }
    if(whiteCount >= blackCount)
      return 1;
    return 0;  
  }

  int checkCol(int posRow ,int posCol,int circle,cv_bridge::CvImagePtr final){
    int whiteCount = 0;
        int blackCount = 0;
        for(int now = posCol; now < posCol + circle ; now +=2)
          if(now > 0 && now < width){
            vector<int> tmp;
            tmp = final->image.row(posRow).col(now);
            if(tmp[0] == 255)
              whiteCount ++;
            else
              blackCount ++; 
          }
        if(whiteCount >= blackCount)
          return 1;
        return 0;  
  }

  int checkCupPos(int circle ,cv_bridge::CvImagePtr final){
    for(int row = 0; row < height; row += 0.5 * circle )
      for(int col = 0; col < width; col += 0.5 * circle)
        if(checkCol(row,col,circle,final) && checkRow(row,col,circle,final)){
          xPosition = col + 0.5 * circle ;
          yPosition = row  + 0.5 * circle;
          return 1;
        }
    return 0;    
  }

  void findCupPosition(cv_bridge::CvImagePtr final){
    
    // if(checkFinished != 1)
    checkFinished = checkCupPos(circleSize, final);
    // cout << checkFinished <<endl;
    cv::circle(final->image, cv::Point(xPosition, yPosition), circleSize, CV_RGB(255, 255, 255));
    cv::imshow("Final Window",final->image);  
  }

  void imageCb(const sensor_msgs::ImageConstPtr &msg){
    cv_bridge::CvImagePtr cv_ptr;
    cv_bridge::CvImagePtr cv_ptr_green_;
    cv_bridge::CvImagePtr cv_ptr_red_;
    cv_bridge::CvImagePtr cv_final;
    cv_bridge::CvImagePtr cv_ptr_white_;
    cv_bridge::CvImagePtr cv_ptr_black_;
    try{
      cv_ptr =  cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      cv_ptr_green_ = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      cv_ptr_red_ = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      cv_final = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      cv_ptr_white_ = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
      cv_ptr_black_ = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
    }
    catch (cv_bridge::Exception &e){
      ROS_ERROR("cv_bridge exception: %s", e.what());
      return;
    }
    
    nh_.getParam("/green_lowH", green_lowH);
    nh_.getParam("/green_lowS", green_lowS);
    nh_.getParam("/green_lowV", green_lowV);
    nh_.getParam("/green_highH",green_highH);
    nh_.getParam("/green_highS",green_highS);
    nh_.getParam("/green_highV",green_highV);

    nh_.getParam("/red_lowH", red_lowH);
    nh_.getParam("/red_lowS", red_lowS);
    nh_.getParam("/red_lowV", red_lowV);
    nh_.getParam("/red_highH",red_highH);
    nh_.getParam("/red_highS",red_highS);
    nh_.getParam("/red_highV",red_highV);


    nh_.getParam("/white_lowR", white_lowR);
    nh_.getParam("/white_lowG", white_lowG);
    nh_.getParam("/white_lowB", white_lowB);
    nh_.getParam("/white_highR",white_highR);
    nh_.getParam("/white_highG",white_highG);
    nh_.getParam("/white_highB",white_highB);

    nh_.getParam("/black_lowR", black_lowR);
    nh_.getParam("/black_lowG", black_lowG);
    nh_.getParam("/black_lowB", black_lowB);
    nh_.getParam("/black_highR",black_highR);
    nh_.getParam("/black_highG",black_highG);
    nh_.getParam("/black_highB",black_highB);

    // nh_.getParam("/xPose",xPosition);
    // nh_.getParam("/yPose",yPosition);
    nh_.getParam("/circleSize",circleSize);


    
    cv::GaussianBlur(cv_ptr->image,cv_ptr->image,cv::Size(301, 101),5);

    // cv::circle(cv_ptr->image, cv::Point(xPosition, yPosition), circleSize, CV_RGB(0, 255, 0));
    cv::cvtColor(cv_ptr->image,cv_ptr_green_->image,cv::COLOR_BGR2HSV);
    cv::cvtColor(cv_ptr->image,cv_ptr_red_->image,cv::COLOR_BGR2HSV);
    
    // Update GUI Window
    // cout<<cv_ptr->image.col(xPosition).row(yPosition)<<endl;
    // cout<<"green_lowH , "<<green_lowH<<", green_lowS , "<<green_lowS<<", green_lowV , "<<green_lowV<<endl;
    // cout<<"green_highH , "<<green_highH<<", green_highS , "<<green_highS<<", green_highV , "<<green_highV<<endl;
    // cout<<"red_lowH , "<<red_lowH<<", red_lowS , "<<red_lowS<<", red_lowV , "<<red_lowV<<endl;
    // cout<<"red_highH , "<<red_highH<<", red_highS , "<<red_highS<<", red_highV , "<<red_highV<<endl;
    // cout<<"white_lowR , "<<white_lowR<<", white_lowG , "<<white_lowG<<", white_lowB , "<<white_lowB<<endl;
    // cout<<"white_highR , "<<white_highR<<", white_highG , "<<white_highG<<", white_highB , "<<white_highB<<endl;    
    // cv::imshow(OPENCV_WINDOW, cv_ptr->image);
    cv::waitKey(3);
    cv::inRange(cv_ptr_green_->image,cv::Scalar(green_lowH,green_lowS,green_lowV),cv::Scalar(green_highH,green_highS,green_highV),cv_ptr_green_->image);
    cv::inRange(cv_ptr_red_->image,cv::Scalar(red_lowH,red_lowS,red_lowV),cv::Scalar(red_highH,red_highS,red_highV),cv_ptr_red_->image);
    cv::inRange(cv_ptr_white_->image,cv::Scalar(white_lowR,white_lowG,white_lowB),cv::Scalar(white_highR,white_highG,white_highB),cv_ptr_white_->image);
    cv::inRange(cv_ptr_black_->image,cv::Scalar(black_lowR,black_lowG,black_lowB),cv::Scalar(black_highR,black_highG,black_highB),cv_ptr_black_->image);


    // cv::imshow("black window", cv_ptr_black_->image);

    cv::threshold(cv_ptr_red_->image,cv_ptr_red_->image,254,255,1);

    
    
    cv::waitKey(3);
    // cv::imshow("Red inverted Window",cv_ptr_red_->image);
    // cv::imshow("Green Window",cv_ptr_green_->image);
    // cv::waitKey(3);
    // cv::imshow("Red Window",cv_ptr_red_->image);
    // cv::waitKey(3);
    cv::addWeighted(cv_ptr_red_->image,1,cv_ptr_green_->image,1,0.0,cv_final->image);
    cv::subtract(cv_final->image, cv_ptr_white_->image ,cv_final->image);
    cv::subtract(cv_final->image, cv_ptr_black_->image ,cv_final->image);

    // Output modified video stream
    // image_pub_.publish(cv_ptr->toImageMsg());
    findCupPosition(cv_final);
    cv::circle(cv_ptr->image, cv::Point(xPosition, yPosition), circleSize, CV_RGB(255, 255, 255));
    cv::imshow(OPENCV_WINDOW,cv_ptr->image);
  }
};

int main(int argc, char **argv)
{
  ros::init(argc, argv, "cvTest");
  ImageConverter ic;
  while (ros::ok())
  {
    ros::spinOnce();
  }
  return 0;
}
