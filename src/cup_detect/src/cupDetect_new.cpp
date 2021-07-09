#include <ros/ros.h>
#include <image_transport/image_transport.h>
#include <cv_bridge/cv_bridge.h>
#include <sensor_msgs/image_encodings.h>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <std_msgs/String.h>
#include <std_msgs/Int32MultiArray.h>
#include <std_msgs/Int32.h>
#include <vector>
#include "cup_detect/transSrv2.h"
#include "cup_detect/mission_camera.h"

static const std::string GREEN_WINDOW = "Green Cup Window";
static const std::string RED_WINDOW = "Red Cup Window";
static const std::string RESULT_WINDOW = "Result Window";
static const std::string ORIGINAL_WINDOW = "Original Image";
static const std::string CANNY_WINDOW = "Canny Image";
static const std::string CANNY_FIX_WINDOW = "Contrast+ Canny Image";
static const std::string CANNY_ADD_WINDOW = "2 Canny Together Image";
static const std::string MASK_WINDOW = "Mask  Image";
static const std::string MASK3_WINDOW = "Mask 3 Image";

class ImageConverter
{
      ros::NodeHandle nh_;
      image_transport::ImageTransport it_;
      image_transport::Subscriber image_sub_;
      image_transport::Publisher image_pub_;
      ros::ServiceClient cli_ = nh_.serviceClient<cup_detect::transSrv2>("cameraTransformation");
      cup_detect::transSrv2 t_srv;
      cup_detect::transSrv2 t2_srv;
      ros::Publisher pub_ = nh_.advertise<std_msgs::String>("opencv_Cups", 100);
      ros::ServiceServer ser_;

      double green_lowH;
      double green_lowS;
      double green_lowV;
      double green_highH;
      double green_highS;
      double green_highV;

      double red1_lowH;
      double red1_lowS;
      double red1_lowV;
      double red1_highH;
      double red1_highS;
      double red1_highV;

      double red2_lowH;
      double red2_lowS;
      double red2_lowV;
      double red2_highH;
      double red2_highS;
      double red2_highV;

      int Gblur_ColorContour;
      double smallestLimitSize;
      double smallCanny;
      int cannyStrongEdge;
      int cannyWeakEdge;

      double contrastAlpha; //  Simple contrast control   1.0-3.0
      int brightnessBeta;   //  Simple brightness control  0-100

      int centerY_up;
      int centerY_down;
      int centerX_up;
      int centerX_down;

      std::vector<std::vector<double>> resultCup; // {ellipseRect.center.x, ellipseRect.center.y, 0, 0, 0, 0, 1, color}   color [ 1 for red , 0 for green ]
      std::vector<cv::RotatedRect> resultRect;
      int detectTimes;

      int mis_resultX = -1000;
      int mis_resultY = -1000;
      int needColor;
      int mis_color;
      bool letdo5;

      sensor_msgs::ImageConstPtr pic;

public:
      ImageConverter()
          : it_(nh_)
      {
            //image_sub_ = it_.subscribe("/usb_cam/image_raw", 1, &ImageConverter::imageCb, this);
            image_sub_ = it_.subscribe("/usb_cam/image_rect_color", 1, &ImageConverter::savePic, this);
            ser_ = nh_.advertiseService("mission_camera", &ImageConverter::mission_camera, this);
            // cv::namedWindow(RESULT_WINDOW);
      }

      ~ImageConverter()
      {
            cv::destroyAllWindows();
      }

      bool mission_camera(cup_detect::mission_camera::Request &mis, cup_detect::mission_camera::Response &cam)
      {
            t2_srv.request.camera_x = mis.coordinate_mission[0];
            t2_srv.request.camera_y = mis.coordinate_mission[1];
            t2_srv.request.reverse = true;
            if (cli_.call(t2_srv))
            {
                  centerX_up = t2_srv.response.robot_x + 50;
                  centerX_down = t2_srv.response.robot_x - 50;
                  centerY_up = t2_srv.response.robot_y + 50;
                  centerY_down = t2_srv.response.robot_y - 50;
                  printf("\t %d\n\n", centerY_down);
                  printf("   %d\tCenter\t%d\n\n", centerX_down, centerX_up);
                  printf("\t %d\n\n", centerY_up);
            };
            needColor = mis.cup_color_mission;
            resultCup.clear();
            resultRect.clear();
            printf("Processing........\n\n");
            for (int i = 0; i < 5; i++)
            {
                  imageCb(pic);
            }
            cam.coordinate_camera = {mis_resultX, mis_resultY};
            cam.cup_color_camera = mis_color;
            printf("Get Result : ");
            if (mis_resultX == -1000 && mis_resultY == -1000)
            {
                  printf("There is no Mission Target\n\n");
            }
            else
            {
                  printf("Mission Target In [ %d , %d ]   ", mis_resultX, mis_resultY);
                  if (mis_color)
                  {
                        printf("This Cup Is Red\n\n");
                  }
                  else
                  {
                        printf("This Cup Is Green\n\n");
                  }
            }
            printf("Possible Results : \n");
            for (int i = 0; i < resultCup.size(); i++)
            {
                  printf("[ %f , %f  ] ", resultCup[i][0], resultCup[i][1]);
                  printf(" Times = %d ", (int)(resultCup[i][2] + resultCup[i][3] + resultCup[i][4] + resultCup[i][5] + resultCup[i][6]));
                  if (resultCup[i][7])
                  {
                        printf(" Red\n");
                  }
                  else
                  {
                        printf(" Green\n");
                  }
            }
            printf("\n");
            return true;
      }
      void savePic(const sensor_msgs::ImageConstPtr &msg)
      {
            pic = msg;
      }

      void imageCb(const sensor_msgs::ImageConstPtr &msg)
      {
            cv_bridge::CvImagePtr cv_ptr;
            try
            {
                  cv_ptr = cv_bridge::toCvCopy(msg, sensor_msgs::image_encodings::BGR8);
            }
            catch (cv_bridge::Exception &e)
            {
                  ROS_ERROR("cv_bridge exception: %s", e.what());
                  return;
            }
            imageProcess(cv_ptr->image);
            cv::waitKey(1);
      }
      void imageProcess(cv::Mat img)
      {
            // cv::Mat img_test;
            cv::Mat img_hsv;
            cv::Mat img_gray;
            cv::Mat img_equalizeHist;
            cv::Mat img_green;
            cv::Mat img_red;
            cv::Mat img_red1;
            cv::Mat img_red2;
            cv::Mat img_cup;
            cv::Mat img_mask;
            cv::Mat img_mask2;
            cv::Mat img_canny;
            cv::Mat img_result;
            std::vector<std::vector<cv::Point>> contours_red;
            std::vector<cv::Vec4i> hierarchy_red;
            std::vector<std::vector<cv::Point>> contours_green;
            std::vector<cv::Vec4i> hierarchy_green;
            std::vector<std::vector<cv::Point>> contours_canny;
            std::vector<cv::Vec4i> hierarchy_canny;

            nh_.getParam("/green_lowH", green_lowH);
            nh_.getParam("/green_lowS", green_lowS);
            nh_.getParam("/green_lowV", green_lowV);
            nh_.getParam("/green_highH", green_highH);
            nh_.getParam("/green_highS", green_highS);
            nh_.getParam("/green_highV", green_highV);

            nh_.getParam("/red1_lowH", red1_lowH);
            nh_.getParam("/red1_lowS", red1_lowS);
            nh_.getParam("/red1_lowV", red1_lowV);
            nh_.getParam("/red1_highH", red1_highH);
            nh_.getParam("/red1_highS", red1_highS);
            nh_.getParam("/red1_highV", red1_highV);

            nh_.getParam("/red2_lowH", red2_lowH);
            nh_.getParam("/red2_lowS", red2_lowS);
            nh_.getParam("/red2_lowV", red2_lowV);
            nh_.getParam("/red2_highH", red2_highH);
            nh_.getParam("/red2_highS", red2_highS);
            nh_.getParam("/red2_highV", red2_highV);

            nh_.getParam("/smallCanny", smallCanny);
            nh_.getParam("/cannyStrongEdge", cannyStrongEdge);
            nh_.getParam("/cannyWeakEdge", cannyWeakEdge);

            nh_.getParam("/Gaussian_Blur", Gblur_ColorContour);
            nh_.getParam("/smallestLimitSize", smallestLimitSize);
            nh_.getParam("/contrastAlpha", contrastAlpha);
            nh_.getParam("/brightnessBeta", brightnessBeta);
            nh_.getParam("/detectTimes", detectTimes);

            // ------------------------------Start Processing------------------------------ //

            cv::cvtColor(img, img_hsv, CV_BGR2HSV);
            cv::cvtColor(img, img_gray, CV_BGR2GRAY);

            cv::inRange(img_hsv, cv::Scalar(green_lowH, green_lowS, green_lowV), cv::Scalar(green_highH, green_highS, green_highV), img_green);
            cv::inRange(img_hsv, cv::Scalar(red1_lowH, red1_lowS, red1_lowV), cv::Scalar(red1_highH, red1_highS, red1_highV), img_red1);
            cv::inRange(img_hsv, cv::Scalar(red2_lowH, red2_lowS, red2_lowV), cv::Scalar(red2_highH, red2_highS, red2_highV), img_red2);
            cv::bitwise_or(img_red1, img_red2, img_red);
            cv::bitwise_or(img_red, img_green, img_cup);
            img.copyTo(img_result);
            img.copyTo(img_mask, img_cup);

            cv::GaussianBlur(img_green, img_green, cv::Size(Gblur_ColorContour, Gblur_ColorContour), 0);
            cv::GaussianBlur(img_red, img_red, cv::Size(Gblur_ColorContour, Gblur_ColorContour), 0);

            cv::Canny(img_mask, img_canny, cannyWeakEdge, cannyStrongEdge);
            cv::threshold(img_canny, img_canny, 100, 255, CV_THRESH_BINARY);

            //cv::imshow(CANNY_WINDOW, img_canny);
            cv::dilate(img_canny, img_canny, cv::getStructuringElement(cv::MORPH_RECT, cv::Size(5, 5)));
            img_canny = 255 - img_canny;
            cv::GaussianBlur(img_canny, img_canny, cv::Size(1, 1), 0);
            img_mask.copyTo(img_mask2, img_canny);

            cv::cvtColor(img_mask2, img_mask2, CV_BGR2HSV);
            cv::inRange(img_mask2, cv::Scalar(green_lowH, green_lowS, green_lowV), cv::Scalar(green_highH, green_highS, green_highV), img_green);
            cv::inRange(img_mask2, cv::Scalar(red1_lowH, red1_lowS, red1_lowV), cv::Scalar(red1_highH, red1_highS, red1_highV), img_red1);
            cv::inRange(img_mask2, cv::Scalar(red2_lowH, red2_lowS, red2_lowV), cv::Scalar(red2_highH, red2_highS, red2_highV), img_red2);
            cv::bitwise_or(img_red1, img_red2, img_red);
            cv::findContours(img_red, contours_red, hierarchy_red, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);
            cv::findContours(img_green, contours_green, hierarchy_green, CV_RETR_EXTERNAL, CV_CHAIN_APPROX_NONE);

            // ------------------------------Result Processing (Filter)------------------------------ //

            for (int i = 0; i < resultCup.size(); i++)
            {
                  for (int j = 3; j <= 6; j++)
                  {
                        resultCup[i][j - 1] = resultCup[i][j];
                  }
                  resultCup[i][6] = 0;
            }
            for (int i = 0; i < contours_red.size(); i++)
            {
                  if (cv::contourArea(contours_red[i]) > smallestLimitSize)
                  {
                        find_Ellipse(contours_red[i], 1);
                  }
            }
            for (int i = 0; i < contours_green.size(); i++)
            {
                  if (cv::contourArea(contours_green[i]) > smallestLimitSize)
                  {
                        find_Ellipse(contours_green[i], 0);
                  }
            }
            for (int i = 0; i < resultCup.size(); i++)
            {
                  if (resultCup[i][2] + resultCup[i][3] + resultCup[i][4] + resultCup[i][5] + resultCup[i][6])
                  {
                  }
                  else
                  {
                        resultCup.erase(resultCup.begin() + i);
                        i--;
                  }
            }
            printEllipse(img_result);

            // cv::imshow(ORIGINAL_WINDOW, img);
            // cv::resize(img_canny, img_canny, cv::Size(img_canny.cols * 1.1, img_canny.rows * 1.1));
            // cv::imshow(CANNY_ADD_WINDOW, img_canny);
            // cv::resize(img_result, img_result, cv::Size(img_result.cols * 2.2, img_result.rows * 2.2));
            // cv::imshow(RESULT_WINDOW, img_result);
            // cv::resize(img_mask, img_mask, cv::Size(img_mask.cols * 1.1, img_mask.rows * 1.1));
            // cv::imshow(MASK_WINDOW, img_mask);
            // cv::imshow(MASK3_WINDOW, img_mask2);
            // cv::imshow(GREEN_WINDOW, img_green);
            // cv::imshow(RED_WINDOW, img_red);
            // cv::imshow(CANNY_WINDOW, img_canny);

            cv::waitKey(1);
      }

      // -----------------------------------------------------------------------------------------------------我是分隔線-----------------------------------------------------------------------------------------------------------

      bool checkCoor(float x, float y)
      {
            return (y >= centerY_down && y <= centerY_up && x >= centerX_down && x <= centerX_up);
      }

      // -----------------------------------------------------------------------------------------------------我是分隔線-----------------------------------------------------------------------------------------------------------

      void find_Ellipse(std::vector<cv::Point> processContours_i, double color)
      {
            int pushed = 0;
            if (processContours_i.size() < 6)
            {
                  return;
            }
            cv::RotatedRect ellipseRect = cv::fitEllipse(processContours_i);
            if (ellipseRect.angle < 140 && ellipseRect.angle > 40 /*&& checkCoor(ellipseRect.center.x, ellipseRect.center.y)*/)
            {
                  for (int i = 0; i < resultCup.size(); i++)
                  {
                        if (fabs(resultCup[i][0] - ellipseRect.center.x) < 15 && fabs(resultCup[i][1] - ellipseRect.center.y) < 15 && resultCup[i][7] == color)
                        {
                              resultCup[i][6] = 1;
                              resultRect[i] = ellipseRect;
                              int times = 0;
                              for (int j = 2; j <= 6; j++)
                              {
                                    times += resultCup[i][j];
                              }
                              resultCup[i][0] = (resultCup[i][0] * (times - 1) + ellipseRect.center.x) / times;
                              resultCup[i][1] = (resultCup[i][1] * (times - 1) + ellipseRect.center.y) / times;
                              pushed = 1;
                              break;
                        }
                  }
                  if (pushed == 0)
                  {
                        std::vector<double> aNewCup = {ellipseRect.center.x, ellipseRect.center.y, 0, 0, 0, 0, 1, color};
                        resultCup.push_back(aNewCup);
                        resultRect.push_back(ellipseRect);
                  }
            }
      }

      void printEllipse(cv::Mat img_result)
      {
            std::string color_String;
            cv::Scalar color_Scalar;
            int red_cup = 0;
            int green_cup = 0;
            int min_i = -1;
            float distance = 10000000;
            for (int i = 0; i < resultCup.size(); i++)
            {

                  if (pow(distance, 2) > (pow(t2_srv.response.robot_x - resultCup[i][0], 2) + pow(t2_srv.response.robot_y - resultCup[i][1], 2)) && (resultCup[i][2] + resultCup[i][3] + resultCup[i][4] + resultCup[i][5] + resultCup[i][6]) >= detectTimes && needColor == resultCup[i][7] && checkCoor(resultCup[i][0], resultCup[i][1]))
                  {
                        distance = pow((pow(t2_srv.response.robot_x - resultCup[i][0], 2) + pow(t2_srv.response.robot_y - resultCup[i][1], 2)), 0.5);
                        //printf("Check [ %f , %f  ] \n", resultCup[i][0], resultCup[i][1]);
                        min_i = i;
                  }
            }
            if (min_i == -1)
            {
                  mis_resultX = -1000;
                  mis_resultY = -1000;
                  mis_color = -1;
            }
            else
            {
                  if (resultCup[min_i][7] == 1)
                  {
                        t_srv.request.camera_x = resultRect[min_i].center.x;
                        t_srv.request.camera_y = resultRect[min_i].center.y;
                        t_srv.request.reverse = false;
                        if (cli_.call(t_srv))
                        {
                              mis_resultX = t_srv.response.robot_x;
                              mis_resultY = t_srv.response.robot_y;
                        }
                        mis_color = 1;
                  }
                  else if (resultCup[min_i][7] == 0)
                  {
                        t_srv.request.camera_x = resultRect[min_i].center.x;
                        t_srv.request.camera_y = resultRect[min_i].center.y;
                        t_srv.request.reverse = false;
                        if (cli_.call(t_srv))
                        {
                              mis_resultX = t_srv.response.robot_x;
                              mis_resultY = t_srv.response.robot_y;
                        }
                        mis_color = 0;
                  }
                  for (int i = 0; i < resultCup.size(); i++)
                  {
                        if (i == min_i)
                        {
                              if (resultCup[i][7] == 1)
                              {
                                    color_String = "Mission Target : Red Cup";
                                    color_Scalar = cv::Scalar(0, 0, 255);
                              }
                              else
                              {
                                    color_String = "Mission Target : Green Cup";
                                    color_Scalar = cv::Scalar(0, 255, 0);
                              }
                        }
                        else
                        {
                              if (resultCup[i][7] == 1)
                              {
                                    color_String = "Other Red Cup";
                                    color_Scalar = cv::Scalar(0, 0, 255);
                              }
                              else
                              {
                                    color_String = "Other Green Cup";
                                    color_Scalar = cv::Scalar(0, 255, 0);
                              }
                        }
                        cv::ellipse(img_result, resultRect[i], cv::Scalar(255, 255, 255), 2, CV_AA);
                        cv::circle(img_result, resultRect[i].center, 3, cv::Scalar(255, 255, 255), 2);
                        cv::putText(img_result, color_String, resultRect[i].center, CV_FONT_HERSHEY_SIMPLEX, 0.5, color_Scalar, 2);
                        // std::string position_x = std::to_string((int)ellipseRect.center.x);
                        // std::string position_y = std::to_string((int)ellipseRect.center.y);
                        // cv::putText(img_result, position_x, cv::Point(ellipseRect.center.x, ellipseRect.center.y + 20), CV_FONT_HERSHEY_SIMPLEX, 0.5, color_Scalar, 2);
                        // cv::putText(img_result, position_y, cv::Point(ellipseRect.center.x, ellipseRect.center.y + 40), CV_FONT_HERSHEY_SIMPLEX, 0.5, color_Scalar, 2);
                  }
            }
      }
};

int main(int argc, char **argv)
{
      ros::init(argc, argv, "cupDetect");
      ROS_INFO(" <<<  Starting Mission Camera Service Node  >>>\n");
      ImageConverter ic;
      while (ros::ok())
      {
            ros::spinOnce();
      }
      return 0;
}