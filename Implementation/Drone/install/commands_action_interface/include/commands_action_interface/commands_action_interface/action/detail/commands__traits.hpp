// generated from rosidl_generator_cpp/resource/idl__traits.hpp.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "commands_action_interface/action/commands.hpp"


#ifndef COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__TRAITS_HPP_
#define COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__TRAITS_HPP_

#include <stdint.h>

#include <sstream>
#include <string>
#include <type_traits>

#include "commands_action_interface/action/detail/commands__struct.hpp"
#include "rosidl_runtime_cpp/traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_Goal & msg,
  std::ostream & out)
{
  out << "{";
  // member: commands_list
  {
    if (msg.commands_list.size() == 0) {
      out << "commands_list: []";
    } else {
      out << "commands_list: [";
      size_t pending_items = msg.commands_list.size();
      for (auto item : msg.commands_list) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: commands_list
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.commands_list.size() == 0) {
      out << "commands_list: []\n";
    } else {
      out << "commands_list:\n";
      for (auto item : msg.commands_list) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_Goal & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_Goal & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_Goal & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_Goal>()
{
  return "commands_action_interface::action::Commands_Goal";
}

template<>
inline const char * name<commands_action_interface::action::Commands_Goal>()
{
  return "commands_action_interface/action/Commands_Goal";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_Goal>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<commands_action_interface::action::Commands_Goal>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_Result & msg,
  std::ostream & out)
{
  out << "{";
  // member: plan_result
  {
    if (msg.plan_result.size() == 0) {
      out << "plan_result: []";
    } else {
      out << "plan_result: [";
      size_t pending_items = msg.plan_result.size();
      for (auto item : msg.plan_result) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: plan_result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.plan_result.size() == 0) {
      out << "plan_result: []\n";
    } else {
      out << "plan_result:\n";
      for (auto item : msg.plan_result) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_Result & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_Result & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_Result & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_Result>()
{
  return "commands_action_interface::action::Commands_Result";
}

template<>
inline const char * name<commands_action_interface::action::Commands_Result>()
{
  return "commands_action_interface/action/Commands_Result";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_Result>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_Result>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<commands_action_interface::action::Commands_Result>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_Feedback & msg,
  std::ostream & out)
{
  out << "{";
  // member: command_status
  {
    if (msg.command_status.size() == 0) {
      out << "command_status: []";
    } else {
      out << "command_status: [";
      size_t pending_items = msg.command_status.size();
      for (auto item : msg.command_status) {
        rosidl_generator_traits::value_to_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: command_status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.command_status.size() == 0) {
      out << "command_status: []\n";
    } else {
      out << "command_status:\n";
      for (auto item : msg.command_status) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "- ";
        rosidl_generator_traits::value_to_yaml(item, out);
        out << "\n";
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_Feedback & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_Feedback & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_Feedback & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_Feedback>()
{
  return "commands_action_interface::action::Commands_Feedback";
}

template<>
inline const char * name<commands_action_interface::action::Commands_Feedback>()
{
  return "commands_action_interface/action/Commands_Feedback";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_Feedback>
  : std::integral_constant<bool, false> {};

template<>
struct is_message<commands_action_interface::action::Commands_Feedback>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'goal'
#include "commands_action_interface/action/detail/commands__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_SendGoal_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: goal
  {
    out << "goal: ";
    to_flow_style_yaml(msg.goal, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: goal
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal:\n";
    to_block_style_yaml(msg.goal, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_SendGoal_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_SendGoal_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_SendGoal_Request & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_SendGoal_Request>()
{
  return "commands_action_interface::action::Commands_SendGoal_Request";
}

template<>
inline const char * name<commands_action_interface::action::Commands_SendGoal_Request>()
{
  return "commands_action_interface/action/Commands_SendGoal_Request";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_SendGoal_Request>
  : std::integral_constant<bool, has_fixed_size<commands_action_interface::action::Commands_Goal>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_SendGoal_Request>
  : std::integral_constant<bool, has_bounded_size<commands_action_interface::action::Commands_Goal>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_SendGoal_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_SendGoal_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: accepted
  {
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << ", ";
  }

  // member: stamp
  {
    out << "stamp: ";
    to_flow_style_yaml(msg.stamp, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: accepted
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "accepted: ";
    rosidl_generator_traits::value_to_yaml(msg.accepted, out);
    out << "\n";
  }

  // member: stamp
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "stamp:\n";
    to_block_style_yaml(msg.stamp, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_SendGoal_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_SendGoal_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_SendGoal_Response & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_SendGoal_Response>()
{
  return "commands_action_interface::action::Commands_SendGoal_Response";
}

template<>
inline const char * name<commands_action_interface::action::Commands_SendGoal_Response>()
{
  return "commands_action_interface/action/Commands_SendGoal_Response";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_SendGoal_Response>
  : std::integral_constant<bool, has_fixed_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_SendGoal_Response>
  : std::integral_constant<bool, has_bounded_size<builtin_interfaces::msg::Time>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_SendGoal_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_SendGoal_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_SendGoal_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_SendGoal_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_SendGoal_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_SendGoal_Event & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_SendGoal_Event>()
{
  return "commands_action_interface::action::Commands_SendGoal_Event";
}

template<>
inline const char * name<commands_action_interface::action::Commands_SendGoal_Event>()
{
  return "commands_action_interface/action/Commands_SendGoal_Event";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_SendGoal_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_SendGoal_Event>
  : std::integral_constant<bool, has_bounded_size<commands_action_interface::action::Commands_SendGoal_Request>::value && has_bounded_size<commands_action_interface::action::Commands_SendGoal_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_SendGoal_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<commands_action_interface::action::Commands_SendGoal>()
{
  return "commands_action_interface::action::Commands_SendGoal";
}

template<>
inline const char * name<commands_action_interface::action::Commands_SendGoal>()
{
  return "commands_action_interface/action/Commands_SendGoal";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_SendGoal>
  : std::integral_constant<
    bool,
    has_fixed_size<commands_action_interface::action::Commands_SendGoal_Request>::value &&
    has_fixed_size<commands_action_interface::action::Commands_SendGoal_Response>::value
  >
{
};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_SendGoal>
  : std::integral_constant<
    bool,
    has_bounded_size<commands_action_interface::action::Commands_SendGoal_Request>::value &&
    has_bounded_size<commands_action_interface::action::Commands_SendGoal_Response>::value
  >
{
};

template<>
struct is_service<commands_action_interface::action::Commands_SendGoal>
  : std::true_type
{
};

template<>
struct is_service_request<commands_action_interface::action::Commands_SendGoal_Request>
  : std::true_type
{
};

template<>
struct is_service_response<commands_action_interface::action::Commands_SendGoal_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_GetResult_Request & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_GetResult_Request & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_GetResult_Request & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_GetResult_Request & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_GetResult_Request>()
{
  return "commands_action_interface::action::Commands_GetResult_Request";
}

template<>
inline const char * name<commands_action_interface::action::Commands_GetResult_Request>()
{
  return "commands_action_interface/action/Commands_GetResult_Request";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_GetResult_Request>
  : std::integral_constant<bool, has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_GetResult_Request>
  : std::integral_constant<bool, has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_GetResult_Request>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'result'
// already included above
// #include "commands_action_interface/action/detail/commands__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_GetResult_Response & msg,
  std::ostream & out)
{
  out << "{";
  // member: status
  {
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << ", ";
  }

  // member: result
  {
    out << "result: ";
    to_flow_style_yaml(msg.result, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: status
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "status: ";
    rosidl_generator_traits::value_to_yaml(msg.status, out);
    out << "\n";
  }

  // member: result
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "result:\n";
    to_block_style_yaml(msg.result, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_GetResult_Response & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_GetResult_Response & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_GetResult_Response & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_GetResult_Response>()
{
  return "commands_action_interface::action::Commands_GetResult_Response";
}

template<>
inline const char * name<commands_action_interface::action::Commands_GetResult_Response>()
{
  return "commands_action_interface/action/Commands_GetResult_Response";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_GetResult_Response>
  : std::integral_constant<bool, has_fixed_size<commands_action_interface::action::Commands_Result>::value> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_GetResult_Response>
  : std::integral_constant<bool, has_bounded_size<commands_action_interface::action::Commands_Result>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_GetResult_Response>
  : std::true_type {};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_GetResult_Event & msg,
  std::ostream & out)
{
  out << "{";
  // member: info
  {
    out << "info: ";
    to_flow_style_yaml(msg.info, out);
    out << ", ";
  }

  // member: request
  {
    if (msg.request.size() == 0) {
      out << "request: []";
    } else {
      out << "request: [";
      size_t pending_items = msg.request.size();
      for (auto item : msg.request) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
    out << ", ";
  }

  // member: response
  {
    if (msg.response.size() == 0) {
      out << "response: []";
    } else {
      out << "response: [";
      size_t pending_items = msg.response.size();
      for (auto item : msg.response) {
        to_flow_style_yaml(item, out);
        if (--pending_items > 0) {
          out << ", ";
        }
      }
      out << "]";
    }
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_GetResult_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: info
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "info:\n";
    to_block_style_yaml(msg.info, out, indentation + 2);
  }

  // member: request
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.request.size() == 0) {
      out << "request: []\n";
    } else {
      out << "request:\n";
      for (auto item : msg.request) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }

  // member: response
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    if (msg.response.size() == 0) {
      out << "response: []\n";
    } else {
      out << "response:\n";
      for (auto item : msg.response) {
        if (indentation > 0) {
          out << std::string(indentation, ' ');
        }
        out << "-\n";
        to_block_style_yaml(item, out, indentation + 2);
      }
    }
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_GetResult_Event & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_GetResult_Event & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_GetResult_Event & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_GetResult_Event>()
{
  return "commands_action_interface::action::Commands_GetResult_Event";
}

template<>
inline const char * name<commands_action_interface::action::Commands_GetResult_Event>()
{
  return "commands_action_interface/action/Commands_GetResult_Event";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_GetResult_Event>
  : std::integral_constant<bool, false> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_GetResult_Event>
  : std::integral_constant<bool, has_bounded_size<commands_action_interface::action::Commands_GetResult_Request>::value && has_bounded_size<commands_action_interface::action::Commands_GetResult_Response>::value && has_bounded_size<service_msgs::msg::ServiceEventInfo>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_GetResult_Event>
  : std::true_type {};

}  // namespace rosidl_generator_traits

namespace rosidl_generator_traits
{

template<>
inline const char * data_type<commands_action_interface::action::Commands_GetResult>()
{
  return "commands_action_interface::action::Commands_GetResult";
}

template<>
inline const char * name<commands_action_interface::action::Commands_GetResult>()
{
  return "commands_action_interface/action/Commands_GetResult";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_GetResult>
  : std::integral_constant<
    bool,
    has_fixed_size<commands_action_interface::action::Commands_GetResult_Request>::value &&
    has_fixed_size<commands_action_interface::action::Commands_GetResult_Response>::value
  >
{
};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_GetResult>
  : std::integral_constant<
    bool,
    has_bounded_size<commands_action_interface::action::Commands_GetResult_Request>::value &&
    has_bounded_size<commands_action_interface::action::Commands_GetResult_Response>::value
  >
{
};

template<>
struct is_service<commands_action_interface::action::Commands_GetResult>
  : std::true_type
{
};

template<>
struct is_service_request<commands_action_interface::action::Commands_GetResult_Request>
  : std::true_type
{
};

template<>
struct is_service_response<commands_action_interface::action::Commands_GetResult_Response>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__traits.hpp"
// Member 'feedback'
// already included above
// #include "commands_action_interface/action/detail/commands__traits.hpp"

namespace commands_action_interface
{

namespace action
{

inline void to_flow_style_yaml(
  const Commands_FeedbackMessage & msg,
  std::ostream & out)
{
  out << "{";
  // member: goal_id
  {
    out << "goal_id: ";
    to_flow_style_yaml(msg.goal_id, out);
    out << ", ";
  }

  // member: feedback
  {
    out << "feedback: ";
    to_flow_style_yaml(msg.feedback, out);
  }
  out << "}";
}  // NOLINT(readability/fn_size)

inline void to_block_style_yaml(
  const Commands_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  // member: goal_id
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "goal_id:\n";
    to_block_style_yaml(msg.goal_id, out, indentation + 2);
  }

  // member: feedback
  {
    if (indentation > 0) {
      out << std::string(indentation, ' ');
    }
    out << "feedback:\n";
    to_block_style_yaml(msg.feedback, out, indentation + 2);
  }
}  // NOLINT(readability/fn_size)

inline std::string to_yaml(const Commands_FeedbackMessage & msg, bool use_flow_style = false)
{
  std::ostringstream out;
  if (use_flow_style) {
    to_flow_style_yaml(msg, out);
  } else {
    to_block_style_yaml(msg, out);
  }
  return out.str();
}

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_generator_traits
{

[[deprecated("use commands_action_interface::action::to_block_style_yaml() instead")]]
inline void to_yaml(
  const commands_action_interface::action::Commands_FeedbackMessage & msg,
  std::ostream & out, size_t indentation = 0)
{
  commands_action_interface::action::to_block_style_yaml(msg, out, indentation);
}

[[deprecated("use commands_action_interface::action::to_yaml() instead")]]
inline std::string to_yaml(const commands_action_interface::action::Commands_FeedbackMessage & msg)
{
  return commands_action_interface::action::to_yaml(msg);
}

template<>
inline const char * data_type<commands_action_interface::action::Commands_FeedbackMessage>()
{
  return "commands_action_interface::action::Commands_FeedbackMessage";
}

template<>
inline const char * name<commands_action_interface::action::Commands_FeedbackMessage>()
{
  return "commands_action_interface/action/Commands_FeedbackMessage";
}

template<>
struct has_fixed_size<commands_action_interface::action::Commands_FeedbackMessage>
  : std::integral_constant<bool, has_fixed_size<commands_action_interface::action::Commands_Feedback>::value && has_fixed_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct has_bounded_size<commands_action_interface::action::Commands_FeedbackMessage>
  : std::integral_constant<bool, has_bounded_size<commands_action_interface::action::Commands_Feedback>::value && has_bounded_size<unique_identifier_msgs::msg::UUID>::value> {};

template<>
struct is_message<commands_action_interface::action::Commands_FeedbackMessage>
  : std::true_type {};

}  // namespace rosidl_generator_traits


namespace rosidl_generator_traits
{

template<>
struct is_action<commands_action_interface::action::Commands>
  : std::true_type
{
};

template<>
struct is_action_goal<commands_action_interface::action::Commands_Goal>
  : std::true_type
{
};

template<>
struct is_action_result<commands_action_interface::action::Commands_Result>
  : std::true_type
{
};

template<>
struct is_action_feedback<commands_action_interface::action::Commands_Feedback>
  : std::true_type
{
};

}  // namespace rosidl_generator_traits


#endif  // COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__TRAITS_HPP_
