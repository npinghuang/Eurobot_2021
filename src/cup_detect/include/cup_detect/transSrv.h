// Generated by gencpp from file cup_detect/transSrv.msg
// DO NOT EDIT!


#ifndef CUP_DETECT_MESSAGE_TRANSSRV_H
#define CUP_DETECT_MESSAGE_TRANSSRV_H

#include <ros/service_traits.h>


#include <cup_detect/transSrvRequest.h>
#include <cup_detect/transSrvResponse.h>


namespace cup_detect
{

struct transSrv
{

typedef transSrvRequest Request;
typedef transSrvResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct transSrv
} // namespace cup_detect


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::cup_detect::transSrv > {
  static const char* value()
  {
    return "6edc2e60b6c20707703d1abcd89664a3";
  }

  static const char* value(const ::cup_detect::transSrv&) { return value(); }
};

template<>
struct DataType< ::cup_detect::transSrv > {
  static const char* value()
  {
    return "cup_detect/transSrv";
  }

  static const char* value(const ::cup_detect::transSrv&) { return value(); }
};


// service_traits::MD5Sum< ::cup_detect::transSrvRequest> should match
// service_traits::MD5Sum< ::cup_detect::transSrv >
template<>
struct MD5Sum< ::cup_detect::transSrvRequest>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::transSrv >::value();
  }
  static const char* value(const ::cup_detect::transSrvRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::transSrvRequest> should match
// service_traits::DataType< ::cup_detect::transSrv >
template<>
struct DataType< ::cup_detect::transSrvRequest>
{
  static const char* value()
  {
    return DataType< ::cup_detect::transSrv >::value();
  }
  static const char* value(const ::cup_detect::transSrvRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::cup_detect::transSrvResponse> should match
// service_traits::MD5Sum< ::cup_detect::transSrv >
template<>
struct MD5Sum< ::cup_detect::transSrvResponse>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::transSrv >::value();
  }
  static const char* value(const ::cup_detect::transSrvResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::transSrvResponse> should match
// service_traits::DataType< ::cup_detect::transSrv >
template<>
struct DataType< ::cup_detect::transSrvResponse>
{
  static const char* value()
  {
    return DataType< ::cup_detect::transSrv >::value();
  }
  static const char* value(const ::cup_detect::transSrvResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // CUP_DETECT_MESSAGE_TRANSSRV_H
