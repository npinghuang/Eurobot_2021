// Generated by gencpp from file cup_detect/mission_camera.msg
// DO NOT EDIT!


#ifndef CUP_DETECT_MESSAGE_MISSION_CAMERA_H
#define CUP_DETECT_MESSAGE_MISSION_CAMERA_H

#include <ros/service_traits.h>


#include <cup_detect/mission_cameraRequest.h>
#include <cup_detect/mission_cameraResponse.h>


namespace cup_detect
{

struct mission_camera
{

typedef mission_cameraRequest Request;
typedef mission_cameraResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct mission_camera
} // namespace cup_detect


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::cup_detect::mission_camera > {
  static const char* value()
  {
    return "21a18da0693a50b6cde67125054bddd4";
  }

  static const char* value(const ::cup_detect::mission_camera&) { return value(); }
};

template<>
struct DataType< ::cup_detect::mission_camera > {
  static const char* value()
  {
    return "cup_detect/mission_camera";
  }

  static const char* value(const ::cup_detect::mission_camera&) { return value(); }
};


// service_traits::MD5Sum< ::cup_detect::mission_cameraRequest> should match
// service_traits::MD5Sum< ::cup_detect::mission_camera >
template<>
struct MD5Sum< ::cup_detect::mission_cameraRequest>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::mission_camera >::value();
  }
  static const char* value(const ::cup_detect::mission_cameraRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::mission_cameraRequest> should match
// service_traits::DataType< ::cup_detect::mission_camera >
template<>
struct DataType< ::cup_detect::mission_cameraRequest>
{
  static const char* value()
  {
    return DataType< ::cup_detect::mission_camera >::value();
  }
  static const char* value(const ::cup_detect::mission_cameraRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::cup_detect::mission_cameraResponse> should match
// service_traits::MD5Sum< ::cup_detect::mission_camera >
template<>
struct MD5Sum< ::cup_detect::mission_cameraResponse>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::mission_camera >::value();
  }
  static const char* value(const ::cup_detect::mission_cameraResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::mission_cameraResponse> should match
// service_traits::DataType< ::cup_detect::mission_camera >
template<>
struct DataType< ::cup_detect::mission_cameraResponse>
{
  static const char* value()
  {
    return DataType< ::cup_detect::mission_camera >::value();
  }
  static const char* value(const ::cup_detect::mission_cameraResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // CUP_DETECT_MESSAGE_MISSION_CAMERA_H