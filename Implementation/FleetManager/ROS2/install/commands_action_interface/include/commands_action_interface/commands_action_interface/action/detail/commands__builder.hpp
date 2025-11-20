// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "commands_action_interface/action/commands.hpp"


#ifndef COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__BUILDER_HPP_
#define COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "commands_action_interface/action/detail/commands__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_Goal_commands_list
{
public:
  Init_Commands_Goal_commands_list()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::commands_action_interface::action::Commands_Goal commands_list(::commands_action_interface::action::Commands_Goal::_commands_list_type arg)
  {
    msg_.commands_list = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_Goal msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_Goal>()
{
  return commands_action_interface::action::builder::Init_Commands_Goal_commands_list();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_Result_plan_result
{
public:
  Init_Commands_Result_plan_result()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::commands_action_interface::action::Commands_Result plan_result(::commands_action_interface::action::Commands_Result::_plan_result_type arg)
  {
    msg_.plan_result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_Result msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_Result>()
{
  return commands_action_interface::action::builder::Init_Commands_Result_plan_result();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_Feedback_command_status
{
public:
  Init_Commands_Feedback_command_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::commands_action_interface::action::Commands_Feedback command_status(::commands_action_interface::action::Commands_Feedback::_command_status_type arg)
  {
    msg_.command_status = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_Feedback msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_Feedback>()
{
  return commands_action_interface::action::builder::Init_Commands_Feedback_command_status();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_SendGoal_Request_goal
{
public:
  explicit Init_Commands_SendGoal_Request_goal(::commands_action_interface::action::Commands_SendGoal_Request & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_SendGoal_Request goal(::commands_action_interface::action::Commands_SendGoal_Request::_goal_type arg)
  {
    msg_.goal = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Request msg_;
};

class Init_Commands_SendGoal_Request_goal_id
{
public:
  Init_Commands_SendGoal_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_SendGoal_Request_goal goal_id(::commands_action_interface::action::Commands_SendGoal_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Commands_SendGoal_Request_goal(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_SendGoal_Request>()
{
  return commands_action_interface::action::builder::Init_Commands_SendGoal_Request_goal_id();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_SendGoal_Response_stamp
{
public:
  explicit Init_Commands_SendGoal_Response_stamp(::commands_action_interface::action::Commands_SendGoal_Response & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_SendGoal_Response stamp(::commands_action_interface::action::Commands_SendGoal_Response::_stamp_type arg)
  {
    msg_.stamp = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Response msg_;
};

class Init_Commands_SendGoal_Response_accepted
{
public:
  Init_Commands_SendGoal_Response_accepted()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_SendGoal_Response_stamp accepted(::commands_action_interface::action::Commands_SendGoal_Response::_accepted_type arg)
  {
    msg_.accepted = std::move(arg);
    return Init_Commands_SendGoal_Response_stamp(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_SendGoal_Response>()
{
  return commands_action_interface::action::builder::Init_Commands_SendGoal_Response_accepted();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_SendGoal_Event_response
{
public:
  explicit Init_Commands_SendGoal_Event_response(::commands_action_interface::action::Commands_SendGoal_Event & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_SendGoal_Event response(::commands_action_interface::action::Commands_SendGoal_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Event msg_;
};

class Init_Commands_SendGoal_Event_request
{
public:
  explicit Init_Commands_SendGoal_Event_request(::commands_action_interface::action::Commands_SendGoal_Event & msg)
  : msg_(msg)
  {}
  Init_Commands_SendGoal_Event_response request(::commands_action_interface::action::Commands_SendGoal_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Commands_SendGoal_Event_response(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Event msg_;
};

class Init_Commands_SendGoal_Event_info
{
public:
  Init_Commands_SendGoal_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_SendGoal_Event_request info(::commands_action_interface::action::Commands_SendGoal_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Commands_SendGoal_Event_request(msg_);
  }

private:
  ::commands_action_interface::action::Commands_SendGoal_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_SendGoal_Event>()
{
  return commands_action_interface::action::builder::Init_Commands_SendGoal_Event_info();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_GetResult_Request_goal_id
{
public:
  Init_Commands_GetResult_Request_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::commands_action_interface::action::Commands_GetResult_Request goal_id(::commands_action_interface::action::Commands_GetResult_Request::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Request msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_GetResult_Request>()
{
  return commands_action_interface::action::builder::Init_Commands_GetResult_Request_goal_id();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_GetResult_Response_result
{
public:
  explicit Init_Commands_GetResult_Response_result(::commands_action_interface::action::Commands_GetResult_Response & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_GetResult_Response result(::commands_action_interface::action::Commands_GetResult_Response::_result_type arg)
  {
    msg_.result = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Response msg_;
};

class Init_Commands_GetResult_Response_status
{
public:
  Init_Commands_GetResult_Response_status()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_GetResult_Response_result status(::commands_action_interface::action::Commands_GetResult_Response::_status_type arg)
  {
    msg_.status = std::move(arg);
    return Init_Commands_GetResult_Response_result(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Response msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_GetResult_Response>()
{
  return commands_action_interface::action::builder::Init_Commands_GetResult_Response_status();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_GetResult_Event_response
{
public:
  explicit Init_Commands_GetResult_Event_response(::commands_action_interface::action::Commands_GetResult_Event & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_GetResult_Event response(::commands_action_interface::action::Commands_GetResult_Event::_response_type arg)
  {
    msg_.response = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Event msg_;
};

class Init_Commands_GetResult_Event_request
{
public:
  explicit Init_Commands_GetResult_Event_request(::commands_action_interface::action::Commands_GetResult_Event & msg)
  : msg_(msg)
  {}
  Init_Commands_GetResult_Event_response request(::commands_action_interface::action::Commands_GetResult_Event::_request_type arg)
  {
    msg_.request = std::move(arg);
    return Init_Commands_GetResult_Event_response(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Event msg_;
};

class Init_Commands_GetResult_Event_info
{
public:
  Init_Commands_GetResult_Event_info()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_GetResult_Event_request info(::commands_action_interface::action::Commands_GetResult_Event::_info_type arg)
  {
    msg_.info = std::move(arg);
    return Init_Commands_GetResult_Event_request(msg_);
  }

private:
  ::commands_action_interface::action::Commands_GetResult_Event msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_GetResult_Event>()
{
  return commands_action_interface::action::builder::Init_Commands_GetResult_Event_info();
}

}  // namespace commands_action_interface


namespace commands_action_interface
{

namespace action
{

namespace builder
{

class Init_Commands_FeedbackMessage_feedback
{
public:
  explicit Init_Commands_FeedbackMessage_feedback(::commands_action_interface::action::Commands_FeedbackMessage & msg)
  : msg_(msg)
  {}
  ::commands_action_interface::action::Commands_FeedbackMessage feedback(::commands_action_interface::action::Commands_FeedbackMessage::_feedback_type arg)
  {
    msg_.feedback = std::move(arg);
    return std::move(msg_);
  }

private:
  ::commands_action_interface::action::Commands_FeedbackMessage msg_;
};

class Init_Commands_FeedbackMessage_goal_id
{
public:
  Init_Commands_FeedbackMessage_goal_id()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  Init_Commands_FeedbackMessage_feedback goal_id(::commands_action_interface::action::Commands_FeedbackMessage::_goal_id_type arg)
  {
    msg_.goal_id = std::move(arg);
    return Init_Commands_FeedbackMessage_feedback(msg_);
  }

private:
  ::commands_action_interface::action::Commands_FeedbackMessage msg_;
};

}  // namespace builder

}  // namespace action

template<typename MessageType>
auto build();

template<>
inline
auto build<::commands_action_interface::action::Commands_FeedbackMessage>()
{
  return commands_action_interface::action::builder::Init_Commands_FeedbackMessage_goal_id();
}

}  // namespace commands_action_interface

#endif  // COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__BUILDER_HPP_
