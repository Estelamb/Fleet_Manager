// generated from rosidl_typesupport_cpp/resource/idl__type_support.cpp.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice

#include "cstddef"
#include "rosidl_runtime_c/message_type_support_struct.h"
#include "commands_action_interface/action/detail/commands__functions.h"
#include "commands_action_interface/action/detail/commands__struct.hpp"
#include "rosidl_typesupport_cpp/identifier.hpp"
#include "rosidl_typesupport_cpp/message_type_support.hpp"
#include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
#include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_Goal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Goal_type_support_ids_t;

static const _Commands_Goal_type_support_ids_t _Commands_Goal_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_Goal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_Goal)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Goal_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Goal__get_type_hash,
  &commands_action_interface__action__Commands_Goal__get_type_description,
  &commands_action_interface__action__Commands_Goal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_Goal>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_Goal_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_Goal)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_Goal>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_Result_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Result_type_support_ids_t;

static const _Commands_Result_type_support_ids_t _Commands_Result_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_Result)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_Result)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Result_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Result__get_type_hash,
  &commands_action_interface__action__Commands_Result__get_type_description,
  &commands_action_interface__action__Commands_Result__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_Result>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_Result_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_Result)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_Result>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_Feedback_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_Feedback_type_support_ids_t;

static const _Commands_Feedback_type_support_ids_t _Commands_Feedback_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_Feedback)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_Feedback)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_Feedback_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_Feedback__get_type_hash,
  &commands_action_interface__action__Commands_Feedback__get_type_description,
  &commands_action_interface__action__Commands_Feedback__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_Feedback>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_Feedback_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_Feedback)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_Feedback>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_SendGoal_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Request_type_support_ids_t;

static const _Commands_SendGoal_Request_type_support_ids_t _Commands_SendGoal_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_SendGoal_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_SendGoal_Request)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Request>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_SendGoal_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_SendGoal_Request)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_SendGoal_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Response_type_support_ids_t;

static const _Commands_SendGoal_Response_type_support_ids_t _Commands_SendGoal_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_SendGoal_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_SendGoal_Response)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Response>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_SendGoal_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_SendGoal_Response)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_SendGoal_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_Event_type_support_ids_t;

static const _Commands_SendGoal_Event_type_support_ids_t _Commands_SendGoal_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_SendGoal_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_SendGoal_Event)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_description,
  &commands_action_interface__action__Commands_SendGoal_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Event>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_SendGoal_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_SendGoal_Event)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
#include "rosidl_runtime_c/service_type_support_struct.h"
#include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
#include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_SendGoal_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_SendGoal_type_support_ids_t;

static const _Commands_SendGoal_type_support_ids_t _Commands_SendGoal_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_SendGoal)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_SendGoal)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_SendGoal_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_SendGoal_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<commands_action_interface::action::Commands_SendGoal>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<commands_action_interface::action::Commands_SendGoal>,
  &commands_action_interface__action__Commands_SendGoal__get_type_hash,
  &commands_action_interface__action__Commands_SendGoal__get_type_description,
  &commands_action_interface__action__Commands_SendGoal__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<commands_action_interface::action::Commands_SendGoal>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_SendGoal_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_SendGoal)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<commands_action_interface::action::Commands_SendGoal>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_GetResult_Request_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Request_type_support_ids_t;

static const _Commands_GetResult_Request_type_support_ids_t _Commands_GetResult_Request_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_GetResult_Request)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_GetResult_Request)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Request_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Request__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Request>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_GetResult_Request_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_GetResult_Request)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Request>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_GetResult_Response_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Response_type_support_ids_t;

static const _Commands_GetResult_Response_type_support_ids_t _Commands_GetResult_Response_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_GetResult_Response)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_GetResult_Response)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Response_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Response__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Response>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_GetResult_Response_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_GetResult_Response)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Response>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_GetResult_Event_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_Event_type_support_ids_t;

static const _Commands_GetResult_Event_type_support_ids_t _Commands_GetResult_Event_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_GetResult_Event)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_GetResult_Event)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_Event_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_hash,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_description,
  &commands_action_interface__action__Commands_GetResult_Event__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Event>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_GetResult_Event_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_GetResult_Event)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Event>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/service_type_support_struct.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_GetResult_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_GetResult_type_support_ids_t;

static const _Commands_GetResult_type_support_ids_t _Commands_GetResult_service_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_GetResult)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_GetResult)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_GetResult_service_typesupport_map),
  ::rosidl_typesupport_cpp::get_service_typesupport_handle_function,
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Request>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Response>(),
  ::rosidl_typesupport_cpp::get_message_type_support_handle<commands_action_interface::action::Commands_GetResult_Event>(),
  &::rosidl_typesupport_cpp::service_create_event_message<commands_action_interface::action::Commands_GetResult>,
  &::rosidl_typesupport_cpp::service_destroy_event_message<commands_action_interface::action::Commands_GetResult>,
  &commands_action_interface__action__Commands_GetResult__get_type_hash,
  &commands_action_interface__action__Commands_GetResult__get_type_description,
  &commands_action_interface__action__Commands_GetResult__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
get_service_type_support_handle<commands_action_interface::action::Commands_GetResult>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_GetResult_service_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_service_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__SERVICE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_GetResult)() {
  return ::rosidl_typesupport_cpp::get_service_type_support_handle<commands_action_interface::action::Commands_GetResult>();
}

#ifdef __cplusplus
}
#endif

// already included above
// #include "cstddef"
// already included above
// #include "rosidl_runtime_c/message_type_support_struct.h"
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/identifier.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_c/type_support_map.h"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support_dispatch.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
// already included above
// #include "rosidl_typesupport_interface/macros.h"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

typedef struct _Commands_FeedbackMessage_type_support_ids_t
{
  const char * typesupport_identifier[2];
} _Commands_FeedbackMessage_type_support_ids_t;

static const _Commands_FeedbackMessage_type_support_ids_t _Commands_FeedbackMessage_message_typesupport_ids = {
  {
    "rosidl_typesupport_fastrtps_cpp",  // ::rosidl_typesupport_fastrtps_cpp::typesupport_identifier,
    "rosidl_typesupport_introspection_cpp",  // ::rosidl_typesupport_introspection_cpp::typesupport_identifier,
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
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_fastrtps_cpp, commands_action_interface, action, Commands_FeedbackMessage)),
    STRINGIFY(ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_introspection_cpp, commands_action_interface, action, Commands_FeedbackMessage)),
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
  ::rosidl_typesupport_cpp::typesupport_identifier,
  reinterpret_cast<const type_support_map_t *>(&_Commands_FeedbackMessage_message_typesupport_map),
  ::rosidl_typesupport_cpp::get_message_typesupport_handle_function,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_hash,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_description,
  &commands_action_interface__action__Commands_FeedbackMessage__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
get_message_type_support_handle<commands_action_interface::action::Commands_FeedbackMessage>()
{
  return &::commands_action_interface::action::rosidl_typesupport_cpp::Commands_FeedbackMessage_message_type_support_handle;
}

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_message_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__MESSAGE_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands_FeedbackMessage)() {
  return get_message_type_support_handle<commands_action_interface::action::Commands_FeedbackMessage>();
}

#ifdef __cplusplus
}
#endif
}  // namespace rosidl_typesupport_cpp

#include "action_msgs/msg/goal_status_array.hpp"
#include "action_msgs/srv/cancel_goal.hpp"
// already included above
// #include "commands_action_interface/action/detail/commands__struct.hpp"
// already included above
// #include "rosidl_typesupport_cpp/visibility_control.h"
#include "rosidl_runtime_c/action_type_support_struct.h"
#include "rosidl_typesupport_cpp/action_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/message_type_support.hpp"
// already included above
// #include "rosidl_typesupport_cpp/service_type_support.hpp"

namespace commands_action_interface
{

namespace action
{

namespace rosidl_typesupport_cpp
{

static rosidl_action_type_support_t Commands_action_type_support_handle = {
  NULL, NULL, NULL, NULL, NULL,
  &commands_action_interface__action__Commands__get_type_hash,
  &commands_action_interface__action__Commands__get_type_description,
  &commands_action_interface__action__Commands__get_type_description_sources,
};

}  // namespace rosidl_typesupport_cpp

}  // namespace action

}  // namespace commands_action_interface

namespace rosidl_typesupport_cpp
{

template<>
ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
get_action_type_support_handle<commands_action_interface::action::Commands>()
{
  using ::commands_action_interface::action::rosidl_typesupport_cpp::Commands_action_type_support_handle;
  // Thread-safe by always writing the same values to the static struct
  Commands_action_type_support_handle.goal_service_type_support = get_service_type_support_handle<::commands_action_interface::action::Commands::Impl::SendGoalService>();
  Commands_action_type_support_handle.result_service_type_support = get_service_type_support_handle<::commands_action_interface::action::Commands::Impl::GetResultService>();
  Commands_action_type_support_handle.cancel_service_type_support = get_service_type_support_handle<::commands_action_interface::action::Commands::Impl::CancelGoalService>();
  Commands_action_type_support_handle.feedback_message_type_support = get_message_type_support_handle<::commands_action_interface::action::Commands::Impl::FeedbackMessage>();
  Commands_action_type_support_handle.status_message_type_support = get_message_type_support_handle<::commands_action_interface::action::Commands::Impl::GoalStatusMessage>();
  return &Commands_action_type_support_handle;
}

}  // namespace rosidl_typesupport_cpp

#ifdef __cplusplus
extern "C"
{
#endif

ROSIDL_TYPESUPPORT_CPP_PUBLIC
const rosidl_action_type_support_t *
ROSIDL_TYPESUPPORT_INTERFACE__ACTION_SYMBOL_NAME(rosidl_typesupport_cpp, commands_action_interface, action, Commands)() {
  return ::rosidl_typesupport_cpp::get_action_type_support_handle<commands_action_interface::action::Commands>();
}

#ifdef __cplusplus
}
#endif
