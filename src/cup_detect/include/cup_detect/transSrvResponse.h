// Generated by gencpp from file cup_detect/transSrvResponse.msg
// DO NOT EDIT!


#ifndef CUP_DETECT_MESSAGE_TRANSSRVRESPONSE_H
#define CUP_DETECT_MESSAGE_TRANSSRVRESPONSE_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace cup_detect
{
template <class ContainerAllocator>
struct transSrvResponse_
{
  typedef transSrvResponse_<ContainerAllocator> Type;

  transSrvResponse_()
    : robot_x(0)
    , robot_y(0)  {
    }
  transSrvResponse_(const ContainerAllocator& _alloc)
    : robot_x(0)
    , robot_y(0)  {
  (void)_alloc;
    }



   typedef int64_t _robot_x_type;
  _robot_x_type robot_x;

   typedef int64_t _robot_y_type;
  _robot_y_type robot_y;





  typedef boost::shared_ptr< ::cup_detect::transSrvResponse_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::cup_detect::transSrvResponse_<ContainerAllocator> const> ConstPtr;

}; // struct transSrvResponse_

typedef ::cup_detect::transSrvResponse_<std::allocator<void> > transSrvResponse;

typedef boost::shared_ptr< ::cup_detect::transSrvResponse > transSrvResponsePtr;
typedef boost::shared_ptr< ::cup_detect::transSrvResponse const> transSrvResponseConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::cup_detect::transSrvResponse_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::cup_detect::transSrvResponse_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::cup_detect::transSrvResponse_<ContainerAllocator1> & lhs, const ::cup_detect::transSrvResponse_<ContainerAllocator2> & rhs)
{
  return lhs.robot_x == rhs.robot_x &&
    lhs.robot_y == rhs.robot_y;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::cup_detect::transSrvResponse_<ContainerAllocator1> & lhs, const ::cup_detect::transSrvResponse_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace cup_detect

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::cup_detect::transSrvResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::cup_detect::transSrvResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::cup_detect::transSrvResponse_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::cup_detect::transSrvResponse_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::cup_detect::transSrvResponse_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::cup_detect::transSrvResponse_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::cup_detect::transSrvResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "22866a3f0d5a7fc274de61f32634b715";
  }

  static const char* value(const ::cup_detect::transSrvResponse_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x22866a3f0d5a7fc2ULL;
  static const uint64_t static_value2 = 0x74de61f32634b715ULL;
};

template<class ContainerAllocator>
struct DataType< ::cup_detect::transSrvResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "cup_detect/transSrvResponse";
  }

  static const char* value(const ::cup_detect::transSrvResponse_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::cup_detect::transSrvResponse_<ContainerAllocator> >
{
  static const char* value()
  {
    return "int64 robot_x\n"
"int64 robot_y\n"
;
  }

  static const char* value(const ::cup_detect::transSrvResponse_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::cup_detect::transSrvResponse_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.robot_x);
      stream.next(m.robot_y);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct transSrvResponse_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::cup_detect::transSrvResponse_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::cup_detect::transSrvResponse_<ContainerAllocator>& v)
  {
    s << indent << "robot_x: ";
    Printer<int64_t>::stream(s, indent + "  ", v.robot_x);
    s << indent << "robot_y: ";
    Printer<int64_t>::stream(s, indent + "  ", v.robot_y);
  }
};

} // namespace message_operations
} // namespace ros

#endif // CUP_DETECT_MESSAGE_TRANSSRVRESPONSE_H
