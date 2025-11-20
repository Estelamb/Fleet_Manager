// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice

// IWYU pragma: private, include "commands_action_interface/action/commands.h"


#ifndef COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__STRUCT_H_
#define COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Include directives for member types
// Member 'commands_list'
#include "rosidl_runtime_c/string.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_Goal
{
  rosidl_runtime_c__String__Sequence commands_list;
} commands_action_interface__action__Commands_Goal;

// Struct for a sequence of commands_action_interface__action__Commands_Goal.
typedef struct commands_action_interface__action__Commands_Goal__Sequence
{
  commands_action_interface__action__Commands_Goal * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_Goal__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'plan_result'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_Result
{
  rosidl_runtime_c__String__Sequence plan_result;
} commands_action_interface__action__Commands_Result;

// Struct for a sequence of commands_action_interface__action__Commands_Result.
typedef struct commands_action_interface__action__Commands_Result__Sequence
{
  commands_action_interface__action__Commands_Result * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_Result__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'command_status'
// already included above
// #include "rosidl_runtime_c/string.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_Feedback
{
  rosidl_runtime_c__String__Sequence command_status;
} commands_action_interface__action__Commands_Feedback;

// Struct for a sequence of commands_action_interface__action__Commands_Feedback.
typedef struct commands_action_interface__action__Commands_Feedback__Sequence
{
  commands_action_interface__action__Commands_Feedback * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_Feedback__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
#include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'goal'
#include "commands_action_interface/action/detail/commands__struct.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_SendGoal_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
  commands_action_interface__action__Commands_Goal goal;
} commands_action_interface__action__Commands_SendGoal_Request;

// Struct for a sequence of commands_action_interface__action__Commands_SendGoal_Request.
typedef struct commands_action_interface__action__Commands_SendGoal_Request__Sequence
{
  commands_action_interface__action__Commands_SendGoal_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_SendGoal_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'stamp'
#include "builtin_interfaces/msg/detail/time__struct.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_SendGoal_Response
{
  bool accepted;
  builtin_interfaces__msg__Time stamp;
} commands_action_interface__action__Commands_SendGoal_Response;

// Struct for a sequence of commands_action_interface__action__Commands_SendGoal_Response.
typedef struct commands_action_interface__action__Commands_SendGoal_Response__Sequence
{
  commands_action_interface__action__Commands_SendGoal_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_SendGoal_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
#include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  commands_action_interface__action__Commands_SendGoal_Event__request__MAX_SIZE = 1
};
// response
enum
{
  commands_action_interface__action__Commands_SendGoal_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_SendGoal_Event
{
  service_msgs__msg__ServiceEventInfo info;
  commands_action_interface__action__Commands_SendGoal_Request__Sequence request;
  commands_action_interface__action__Commands_SendGoal_Response__Sequence response;
} commands_action_interface__action__Commands_SendGoal_Event;

// Struct for a sequence of commands_action_interface__action__Commands_SendGoal_Event.
typedef struct commands_action_interface__action__Commands_SendGoal_Event__Sequence
{
  commands_action_interface__action__Commands_SendGoal_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_SendGoal_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_GetResult_Request
{
  unique_identifier_msgs__msg__UUID goal_id;
} commands_action_interface__action__Commands_GetResult_Request;

// Struct for a sequence of commands_action_interface__action__Commands_GetResult_Request.
typedef struct commands_action_interface__action__Commands_GetResult_Request__Sequence
{
  commands_action_interface__action__Commands_GetResult_Request * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_GetResult_Request__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'result'
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_GetResult_Response
{
  int8_t status;
  commands_action_interface__action__Commands_Result result;
} commands_action_interface__action__Commands_GetResult_Response;

// Struct for a sequence of commands_action_interface__action__Commands_GetResult_Response.
typedef struct commands_action_interface__action__Commands_GetResult_Response__Sequence
{
  commands_action_interface__action__Commands_GetResult_Response * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_GetResult_Response__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'info'
// already included above
// #include "service_msgs/msg/detail/service_event_info__struct.h"

// constants for array fields with an upper bound
// request
enum
{
  commands_action_interface__action__Commands_GetResult_Event__request__MAX_SIZE = 1
};
// response
enum
{
  commands_action_interface__action__Commands_GetResult_Event__response__MAX_SIZE = 1
};

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_GetResult_Event
{
  service_msgs__msg__ServiceEventInfo info;
  commands_action_interface__action__Commands_GetResult_Request__Sequence request;
  commands_action_interface__action__Commands_GetResult_Response__Sequence response;
} commands_action_interface__action__Commands_GetResult_Event;

// Struct for a sequence of commands_action_interface__action__Commands_GetResult_Event.
typedef struct commands_action_interface__action__Commands_GetResult_Event__Sequence
{
  commands_action_interface__action__Commands_GetResult_Event * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_GetResult_Event__Sequence;

// Constants defined in the message

// Include directives for member types
// Member 'goal_id'
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__struct.h"
// Member 'feedback'
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"

/// Struct defined in action/Commands in the package commands_action_interface.
typedef struct commands_action_interface__action__Commands_FeedbackMessage
{
  unique_identifier_msgs__msg__UUID goal_id;
  commands_action_interface__action__Commands_Feedback feedback;
} commands_action_interface__action__Commands_FeedbackMessage;

// Struct for a sequence of commands_action_interface__action__Commands_FeedbackMessage.
typedef struct commands_action_interface__action__Commands_FeedbackMessage__Sequence
{
  commands_action_interface__action__Commands_FeedbackMessage * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} commands_action_interface__action__Commands_FeedbackMessage__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // COMMANDS_ACTION_INTERFACE__ACTION__DETAIL__COMMANDS__STRUCT_H_
