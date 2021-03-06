// Generated by gencpp from file cup_detect/transSrv2.msg
// DO NOT EDIT!


#ifndef CUP_DETECT_MESSAGE_TRANSSRV2_H
#define CUP_DETECT_MESSAGE_TRANSSRV2_H

#include <ros/service_traits.h>


#include <cup_detect/transSrv2Request.h>
#include <cup_detect/transSrv2Response.h>


namespace cup_detect
{

struct transSrv2
{

typedef transSrv2Request Request;
typedef transSrv2Response Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct transSrv2
} // namespace cup_detect


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::cup_detect::transSrv2 > {
  static const char* value()
  {
    return "d90380bbd55bb0361e3e7a4d97f00566";
  }

  static const char* value(const ::cup_detect::transSrv2&) { return value(); }
};

template<>
struct DataType< ::cup_detect::transSrv2 > {
  static const char* value()
  {
    return "cup_detect/transSrv2";
  }

  static const char* value(const ::cup_detect::transSrv2&) { return value(); }
};


// service_traits::MD5Sum< ::cup_detect::transSrv2Request> should match
// service_traits::MD5Sum< ::cup_detect::transSrv2 >
template<>
struct MD5Sum< ::cup_detect::transSrv2Request>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::transSrv2 >::value();
  }
  static const char* value(const ::cup_detect::transSrv2Request&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::transSrv2Request> should match
// service_traits::DataType< ::cup_detect::transSrv2 >
template<>
struct DataType< ::cup_detect::transSrv2Request>
{
  static const char* value()
  {
    return DataType< ::cup_detect::transSrv2 >::value();
  }
  static const char* value(const ::cup_detect::transSrv2Request&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::cup_detect::transSrv2Response> should match
// service_traits::MD5Sum< ::cup_detect::transSrv2 >
template<>
struct MD5Sum< ::cup_detect::transSrv2Response>
{
  static const char* value()
  {
    return MD5Sum< ::cup_detect::transSrv2 >::value();
  }
  static const char* value(const ::cup_detect::transSrv2Response&)
  {
    return value();
  }
};

// service_traits::DataType< ::cup_detect::transSrv2Response> should match
// service_traits::DataType< ::cup_detect::transSrv2 >
template<>
struct DataType< ::cup_detect::transSrv2Response>
{
  static const char* value()
  {
    return DataType< ::cup_detect::transSrv2 >::value();
  }
  static const char* value(const ::cup_detect::transSrv2Response&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // CUP_DETECT_MESSAGE_TRANSSRV2_H
