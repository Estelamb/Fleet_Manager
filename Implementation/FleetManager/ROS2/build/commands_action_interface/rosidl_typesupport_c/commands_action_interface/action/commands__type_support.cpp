// generated from rosidl_typesupport_c/resource/idl__type_support.cpp.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "commands_action_interface/action/detail/commands__struct.h"
#include "commands_action_interface/action/detail/commands__type_support.h"
#include "commands_action_interface/action/detail/commands__functions.h"
#include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/message_type_support_dispatch.h"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_c/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Goal_type_support_ids_t;

static const _Commands_Goal_type_support_ids_t _Commands_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_Goal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_Goal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_Goal_type_support_symbol_names_t _Commands_Goal_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_Goal)),
  }
};

typedef struct _Commands_Goal_type_support_data_t
{
  void * data[2];
} _Commands_Goal_type_support_data_t;

static _Commands_Goal_type_support_data_t _Commands_Goal_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_Goal_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_Goal_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_Goal_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_Goal_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_Goal_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Goal_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Goal__get_type_hash,
  &commands_action_interface__action__Commands_Goal__get_type_description,
  &commands_action_interface__action__Commands_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_Goal)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_Goal_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Result_type_support_ids_t;

static const _Commands_Result_type_support_ids_t _Commands_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_Result_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_Result_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_Result_type_support_symbol_names_t _Commands_Result_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_Result)),
  }
};

typedef struct _Commands_Result_type_support_data_t
{
  void * data[2];
} _Commands_Result_type_support_data_t;

static _Commands_Result_type_support_data_t _Commands_Result_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_Result_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_Result_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_Result_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_Result_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_Result_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Result_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Result__get_type_hash,
  &commands_action_interface__action__Commands_Result__get_type_description,
  &commands_action_interface__action__Commands_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_Result)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_Result_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Feedback_type_support_ids_t;

static const _Commands_Feedback_type_support_ids_t _Commands_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_Feedback_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_Feedback_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_Feedback_type_support_symbol_names_t _Commands_Feedback_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_Feedback)),
  }
};

typedef struct _Commands_Feedback_type_support_data_t
{
  void * data[2];
} _Commands_Feedback_type_support_data_t;

static _Commands_Feedback_type_support_data_t _Commands_Feedback_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_Feedback_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_Feedback_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_Feedback_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_Feedback_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_Feedback_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Feedback_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Feedback__get_type_hash,
  &commands_action_interface__action__Commands_Feedback__get_type_description,
  &commands_action_interface__action__Commands_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_Feedback)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Request_type_support_ids_t;

static const _Commands_SendGoal_Request_type_support_ids_t _Commands_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_SendGoal_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_SendGoal_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_SendGoal_Request_type_support_symbol_names_t _Commands_SendGoal_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_SendGoal_Request)),
  }
};

typedef struct _Commands_SendGoal_Request_type_support_data_t
{
  void * data[2];
} _Commands_SendGoal_Request_type_support_data_t;

static _Commands_SendGoal_Request_type_support_data_t _Commands_SendGoal_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_SendGoal_Request_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_SendGoal_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_SendGoal_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_SendGoal_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_SendGoal_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_SendGoal_Request)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Response_type_support_ids_t;

static const _Commands_SendGoal_Response_type_support_ids_t _Commands_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_SendGoal_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_SendGoal_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_SendGoal_Response_type_support_symbol_names_t _Commands_SendGoal_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_SendGoal_Response)),
  }
};

typedef struct _Commands_SendGoal_Response_type_support_data_t
{
  void * data[2];
} _Commands_SendGoal_Response_type_support_data_t;

static _Commands_SendGoal_Response_type_support_data_t _Commands_SendGoal_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_SendGoal_Response_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_SendGoal_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_SendGoal_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_SendGoal_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_SendGoal_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_SendGoal_Response)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Event_type_support_ids_t;

static const _Commands_SendGoal_Event_type_support_ids_t _Commands_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_SendGoal_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_SendGoal_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_SendGoal_Event_type_support_symbol_names_t _Commands_SendGoal_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_SendGoal_Event)),
  }
};

typedef struct _Commands_SendGoal_Event_type_support_data_t
{
  void * data[2];
} _Commands_SendGoal_Event_type_support_data_t;

static _Commands_SendGoal_Event_type_support_data_t _Commands_SendGoal_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_SendGoal_Event_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_SendGoal_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_SendGoal_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_SendGoal_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_SendGoal_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_SendGoal_Event)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
#include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
#include "service_msgs/msg/service_event_info.h"
#include "builtin_interfaces/msg/time.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _Commands_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_type_support_ids_t;

static const _Commands_SendGoal_type_support_ids_t _Commands_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_SendGoal_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_SendGoal_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_SendGoal_type_support_symbol_names_t _Commands_SendGoal_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_SendGoal)),
  }
};

typedef struct _Commands_SendGoal_type_support_data_t
{
  void * data[2];
} _Commands_SendGoal_type_support_data_t;

static _Commands_SendGoal_type_support_data_t _Commands_SendGoal_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_SendGoal_service_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_SendGoal_service_typesupport_ids.typesupport_identifier[0],
  &_Commands_SendGoal_service_typesupport_symbol_names.symbol_name[0],
  &_Commands_SendGoal_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Commands_SendGoal_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &Commands_SendGoal_Request_message_type_support_handle,
  &Commands_SendGoal_Response_message_type_support_handle,
  &Commands_SendGoal_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    commands_action_interface,
    action,
    Commands_SendGoal
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    commands_action_interface,
    action,
    Commands_SendGoal
  ),
  &commands_action_interface__action__Commands_SendGoal__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal__get_type_description,
  &commands_action_interface__action__Commands_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_SendGoal)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_SendGoal_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Request_type_support_ids_t;

static const _Commands_GetResult_Request_type_support_ids_t _Commands_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_GetResult_Request_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_GetResult_Request_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_GetResult_Request_type_support_symbol_names_t _Commands_GetResult_Request_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_GetResult_Request)),
  }
};

typedef struct _Commands_GetResult_Request_type_support_data_t
{
  void * data[2];
} _Commands_GetResult_Request_type_support_data_t;

static _Commands_GetResult_Request_type_support_data_t _Commands_GetResult_Request_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_GetResult_Request_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_GetResult_Request_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_GetResult_Request_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_GetResult_Request_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_GetResult_Request_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Request_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_GetResult_Request)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Response_type_support_ids_t;

static const _Commands_GetResult_Response_type_support_ids_t _Commands_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_GetResult_Response_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_GetResult_Response_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_GetResult_Response_type_support_symbol_names_t _Commands_GetResult_Response_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_GetResult_Response)),
  }
};

typedef struct _Commands_GetResult_Response_type_support_data_t
{
  void * data[2];
} _Commands_GetResult_Response_type_support_data_t;

static _Commands_GetResult_Response_type_support_data_t _Commands_GetResult_Response_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_GetResult_Response_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_GetResult_Response_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_GetResult_Response_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_GetResult_Response_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_GetResult_Response_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Response_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_GetResult_Response)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Event_type_support_ids_t;

static const _Commands_GetResult_Event_type_support_ids_t _Commands_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_GetResult_Event_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_GetResult_Event_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_GetResult_Event_type_support_symbol_names_t _Commands_GetResult_Event_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_GetResult_Event)),
  }
};

typedef struct _Commands_GetResult_Event_type_support_data_t
{
  void * data[2];
} _Commands_GetResult_Event_type_support_data_t;

static _Commands_GetResult_Event_type_support_data_t _Commands_GetResult_Event_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_GetResult_Event_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_GetResult_Event_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_GetResult_Event_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_GetResult_Event_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_GetResult_Event_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Event_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_GetResult_Event)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/service_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"
// already included above
// #include "service_msgs/msg/service_event_info.h"
// already included above
// #include "builtin_interfaces/msg/time.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{
typedef struct _Commands_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_type_support_ids_t;

static const _Commands_GetResult_type_support_ids_t _Commands_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_GetResult_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_GetResult_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_GetResult_type_support_symbol_names_t _Commands_GetResult_service_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_GetResult)),
  }
};

typedef struct _Commands_GetResult_type_support_data_t
{
  void * data[2];
} _Commands_GetResult_type_support_data_t;

static _Commands_GetResult_type_support_data_t _Commands_GetResult_service_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_GetResult_service_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_GetResult_service_typesupport_ids.typesupport_identifier[0],
  &_Commands_GetResult_service_typesupport_symbol_names.symbol_name[0],
  &_Commands_GetResult_service_typesupport_data.data[0],
};

static const rosidl_service_type_support_t Commands_GetResult_service_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_service_typesupport_map),
  rosidl_typesupport_c__get_service_typesupport_handle_function,
  &Commands_GetResult_Request_message_type_support_handle,
  &Commands_GetResult_Response_message_type_support_handle,
  &Commands_GetResult_Event_message_type_support_handle,
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_CREATE_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    commands_action_interface,
    action,
    Commands_GetResult
  ),
  ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_DESTROY_EVENT_MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c,
    commands_action_interface,
    action,
    Commands_GetResult
  ),
  &commands_action_interface__action__Commands_GetResult__get_type_hash,
  &commands_action_interface__action__Commands_GetResult__get_type_description,
  &commands_action_interface__action__Commands_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_GetResult)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_GetResult_service_type_support_handle;
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "rosidl_typesupport_c/identifier.h"
// already included above
// #include "rosidl_typesupport_c/message_type_support_dispatch.h"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_c/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_c
{

typedef struct _Commands_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_FeedbackMessage_type_support_ids_t;

static const _Commands_FeedbackMessage_type_support_ids_t _Commands_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_c",  // ::rosidl_typesupport_fastrtps_c::typesupport_identifier,
    "rosidl_typesupport_introspection_c",  // ::rosidl_typesupport_introspection_c::typesupport_identifier,
  }
};

typedef struct _Commands_FeedbackMessage_type_support_symbol_names_t
{
  const char * symbol_name[2];
} _Commands_FeedbackMessage_type_support_symbol_names_t;

#define STRINGIFY_(s) #s
#define STRINGIFY(s) STRINGIFY_(s)

static const _Commands_FeedbackMessage_type_support_symbol_names_t _Commands_FeedbackMessage_message_typesupport_symbol_names = {
  {
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_c, commands_action_interface, action, Commands_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_c, commands_action_interface, action, Commands_FeedbackMessage)),
  }
};

typedef struct _Commands_FeedbackMessage_type_support_data_t
{
  void * data[2];
} _Commands_FeedbackMessage_type_support_data_t;

static _Commands_FeedbackMessage_type_support_data_t _Commands_FeedbackMessage_message_typesupport_data = {
  {
    0,  // will store the shared library later
    0,  // will store the shared library later
  }
};

static const type_support_map_t _Commands_FeedbackMessage_message_typesupport_map = {
  2,
  "commands_action_interface",
  &_Commands_FeedbackMessage_message_typesupport_ids.typesupport_identifier[0],
  &_Commands_FeedbackMessage_message_typesupport_symbol_names.symbol_name[0],
  &_Commands_FeedbackMessage_message_typesupport_data.data[0],
};

static const rosidl_message_type_support_t Commands_FeedbackMessage_message_type_support_handle = {
  rosidl_typesupport_c__typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_FeedbackMessage_message_typesupport_map),
  rosidl_typesupport_c__get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_hash,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_description,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_c

}  // namespace action

}  // namespace commands_action_interface

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_c, commands_action_interface, action, Commands_FeedbackMessage)() {
  return &::commands_action_interface::action::rosidl_typesupport_c::Commands_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
}
#endif

#include "action_msgs/msg/goal_status_array.h"
#include "action_msgs/srv/cancel_goal.h"
#include "commands_action_interface/action/commands.h"
// already included above
// #include "commands_action_interface/action/detail/commands__type_support.h"

static rosidl_action_type_support_t _commands_action_interface__action__Commands__typesupport_c = {
  NULL, NULL, NULL, NULL, NULL,
  &commands_action_interface__action__Commands__get_type_hash,
  &commands_action_interface__action__Commands__get_type_description,
  &commands_action_interface__action__Commands__get_type_description_sources,
};

#ifdef __cplusplus
extern "C"
{
#endif

const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(
  rosidl_typesupport_c, commands_action_interface, action, Commands)()
{
  // Thread-safe by always writing the same values to the static struct
  _commands_action_interface__action__Commands__typesupport_c.goal_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, commands_action_interface, action, Commands_SendGoal)();
  _commands_action_interface__action__Commands__typesupport_c.result_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, commands_action_interface, action, Commands_GetResult)();
  _commands_action_interface__action__Commands__typesupport_c.cancel_service_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, srv, CancelGoal)();
  _commands_action_interface__action__Commands__typesupport_c.feedback_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, commands_action_interface, action, Commands_FeedbackMessage)();
  _commands_action_interface__action__Commands__typesupport_c.status_message_type_support =
    ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(
    rosidl_typesupport_c, action_msgs, msg, GoalStatusArray)();

  return &_commands_action_interface__action__Commands__typesupport_c;
}

#ifdef __cplusplus
}
#endif
