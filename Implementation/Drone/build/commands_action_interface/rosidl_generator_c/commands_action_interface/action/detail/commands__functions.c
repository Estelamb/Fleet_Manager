// generated from rosidl_generator_c/resource/idl__functions.c.em
// with input from commands_action_interface:action/Commands.idl
// generated code does not contain a copyright notice
#include "commands_action_interface/action/detail/commands__functions.h"

#include <assert.h>
#include <stdbool.h>
#include <stdlib.h>
#include <string.h>

#include "rcutils/allocator.h"


// Include directives for member types
// Member `commands_list`
#include "rosidl_runtime_c/string_functions.h"

bool
commands_action_interface__action__Commands_Goal__init(commands_action_interface__action__Commands_Goal * msg)
{
  if (!msg) {
    return false;
  }
  // commands_list
  if (!rosidl_runtime_c__String__Sequence__init(&msg->commands_list, 0)) {
    commands_action_interface__action__Commands_Goal__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_Goal__fini(commands_action_interface__action__Commands_Goal * msg)
{
  if (!msg) {
    return;
  }
  // commands_list
  rosidl_runtime_c__String__Sequence__fini(&msg->commands_list);
}

bool
commands_action_interface__action__Commands_Goal__are_equal(const commands_action_interface__action__Commands_Goal * lhs, const commands_action_interface__action__Commands_Goal * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // commands_list
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->commands_list), &(rhs->commands_list)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_Goal__copy(
  const commands_action_interface__action__Commands_Goal * input,
  commands_action_interface__action__Commands_Goal * output)
{
  if (!input || !output) {
    return false;
  }
  // commands_list
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->commands_list), &(output->commands_list)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_Goal *
commands_action_interface__action__Commands_Goal__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Goal * msg = (commands_action_interface__action__Commands_Goal *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Goal), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_Goal));
  bool success = commands_action_interface__action__Commands_Goal__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_Goal__destroy(commands_action_interface__action__Commands_Goal * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_Goal__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_Goal__Sequence__init(commands_action_interface__action__Commands_Goal__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Goal * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_Goal *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_Goal), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_Goal__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_Goal__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_Goal__Sequence__fini(commands_action_interface__action__Commands_Goal__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_Goal__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_Goal__Sequence *
commands_action_interface__action__Commands_Goal__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Goal__Sequence * array = (commands_action_interface__action__Commands_Goal__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Goal__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_Goal__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_Goal__Sequence__destroy(commands_action_interface__action__Commands_Goal__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_Goal__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_Goal__Sequence__are_equal(const commands_action_interface__action__Commands_Goal__Sequence * lhs, const commands_action_interface__action__Commands_Goal__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_Goal__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_Goal__Sequence__copy(
  const commands_action_interface__action__Commands_Goal__Sequence * input,
  commands_action_interface__action__Commands_Goal__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_Goal);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_Goal * data =
      (commands_action_interface__action__Commands_Goal *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_Goal__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_Goal__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_Goal__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `plan_result`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
commands_action_interface__action__Commands_Result__init(commands_action_interface__action__Commands_Result * msg)
{
  if (!msg) {
    return false;
  }
  // plan_result
  if (!rosidl_runtime_c__String__Sequence__init(&msg->plan_result, 0)) {
    commands_action_interface__action__Commands_Result__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_Result__fini(commands_action_interface__action__Commands_Result * msg)
{
  if (!msg) {
    return;
  }
  // plan_result
  rosidl_runtime_c__String__Sequence__fini(&msg->plan_result);
}

bool
commands_action_interface__action__Commands_Result__are_equal(const commands_action_interface__action__Commands_Result * lhs, const commands_action_interface__action__Commands_Result * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // plan_result
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->plan_result), &(rhs->plan_result)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_Result__copy(
  const commands_action_interface__action__Commands_Result * input,
  commands_action_interface__action__Commands_Result * output)
{
  if (!input || !output) {
    return false;
  }
  // plan_result
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->plan_result), &(output->plan_result)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_Result *
commands_action_interface__action__Commands_Result__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Result * msg = (commands_action_interface__action__Commands_Result *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Result), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_Result));
  bool success = commands_action_interface__action__Commands_Result__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_Result__destroy(commands_action_interface__action__Commands_Result * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_Result__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_Result__Sequence__init(commands_action_interface__action__Commands_Result__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Result * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_Result *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_Result), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_Result__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_Result__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_Result__Sequence__fini(commands_action_interface__action__Commands_Result__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_Result__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_Result__Sequence *
commands_action_interface__action__Commands_Result__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Result__Sequence * array = (commands_action_interface__action__Commands_Result__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Result__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_Result__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_Result__Sequence__destroy(commands_action_interface__action__Commands_Result__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_Result__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_Result__Sequence__are_equal(const commands_action_interface__action__Commands_Result__Sequence * lhs, const commands_action_interface__action__Commands_Result__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_Result__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_Result__Sequence__copy(
  const commands_action_interface__action__Commands_Result__Sequence * input,
  commands_action_interface__action__Commands_Result__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_Result);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_Result * data =
      (commands_action_interface__action__Commands_Result *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_Result__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_Result__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_Result__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `command_status`
// already included above
// #include "rosidl_runtime_c/string_functions.h"

bool
commands_action_interface__action__Commands_Feedback__init(commands_action_interface__action__Commands_Feedback * msg)
{
  if (!msg) {
    return false;
  }
  // command_status
  if (!rosidl_runtime_c__String__Sequence__init(&msg->command_status, 0)) {
    commands_action_interface__action__Commands_Feedback__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_Feedback__fini(commands_action_interface__action__Commands_Feedback * msg)
{
  if (!msg) {
    return;
  }
  // command_status
  rosidl_runtime_c__String__Sequence__fini(&msg->command_status);
}

bool
commands_action_interface__action__Commands_Feedback__are_equal(const commands_action_interface__action__Commands_Feedback * lhs, const commands_action_interface__action__Commands_Feedback * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // command_status
  if (!rosidl_runtime_c__String__Sequence__are_equal(
      &(lhs->command_status), &(rhs->command_status)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_Feedback__copy(
  const commands_action_interface__action__Commands_Feedback * input,
  commands_action_interface__action__Commands_Feedback * output)
{
  if (!input || !output) {
    return false;
  }
  // command_status
  if (!rosidl_runtime_c__String__Sequence__copy(
      &(input->command_status), &(output->command_status)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_Feedback *
commands_action_interface__action__Commands_Feedback__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Feedback * msg = (commands_action_interface__action__Commands_Feedback *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Feedback), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_Feedback));
  bool success = commands_action_interface__action__Commands_Feedback__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_Feedback__destroy(commands_action_interface__action__Commands_Feedback * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_Feedback__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_Feedback__Sequence__init(commands_action_interface__action__Commands_Feedback__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Feedback * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_Feedback *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_Feedback), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_Feedback__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_Feedback__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_Feedback__Sequence__fini(commands_action_interface__action__Commands_Feedback__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_Feedback__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_Feedback__Sequence *
commands_action_interface__action__Commands_Feedback__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_Feedback__Sequence * array = (commands_action_interface__action__Commands_Feedback__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_Feedback__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_Feedback__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_Feedback__Sequence__destroy(commands_action_interface__action__Commands_Feedback__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_Feedback__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_Feedback__Sequence__are_equal(const commands_action_interface__action__Commands_Feedback__Sequence * lhs, const commands_action_interface__action__Commands_Feedback__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_Feedback__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_Feedback__Sequence__copy(
  const commands_action_interface__action__Commands_Feedback__Sequence * input,
  commands_action_interface__action__Commands_Feedback__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_Feedback);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_Feedback * data =
      (commands_action_interface__action__Commands_Feedback *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_Feedback__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_Feedback__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_Feedback__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
#include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `goal`
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"

bool
commands_action_interface__action__Commands_SendGoal_Request__init(commands_action_interface__action__Commands_SendGoal_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    commands_action_interface__action__Commands_SendGoal_Request__fini(msg);
    return false;
  }
  // goal
  if (!commands_action_interface__action__Commands_Goal__init(&msg->goal)) {
    commands_action_interface__action__Commands_SendGoal_Request__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Request__fini(commands_action_interface__action__Commands_SendGoal_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // goal
  commands_action_interface__action__Commands_Goal__fini(&msg->goal);
}

bool
commands_action_interface__action__Commands_SendGoal_Request__are_equal(const commands_action_interface__action__Commands_SendGoal_Request * lhs, const commands_action_interface__action__Commands_SendGoal_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // goal
  if (!commands_action_interface__action__Commands_Goal__are_equal(
      &(lhs->goal), &(rhs->goal)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Request__copy(
  const commands_action_interface__action__Commands_SendGoal_Request * input,
  commands_action_interface__action__Commands_SendGoal_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // goal
  if (!commands_action_interface__action__Commands_Goal__copy(
      &(input->goal), &(output->goal)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_SendGoal_Request *
commands_action_interface__action__Commands_SendGoal_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Request * msg = (commands_action_interface__action__Commands_SendGoal_Request *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_SendGoal_Request));
  bool success = commands_action_interface__action__Commands_SendGoal_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_SendGoal_Request__destroy(commands_action_interface__action__Commands_SendGoal_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_SendGoal_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_SendGoal_Request__Sequence__init(commands_action_interface__action__Commands_SendGoal_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Request * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_SendGoal_Request *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_SendGoal_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_SendGoal_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_SendGoal_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Request__Sequence__fini(commands_action_interface__action__Commands_SendGoal_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_SendGoal_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_SendGoal_Request__Sequence *
commands_action_interface__action__Commands_SendGoal_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Request__Sequence * array = (commands_action_interface__action__Commands_SendGoal_Request__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_SendGoal_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_SendGoal_Request__Sequence__destroy(commands_action_interface__action__Commands_SendGoal_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_SendGoal_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_SendGoal_Request__Sequence__are_equal(const commands_action_interface__action__Commands_SendGoal_Request__Sequence * lhs, const commands_action_interface__action__Commands_SendGoal_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Request__Sequence__copy(
  const commands_action_interface__action__Commands_SendGoal_Request__Sequence * input,
  commands_action_interface__action__Commands_SendGoal_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_SendGoal_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_SendGoal_Request * data =
      (commands_action_interface__action__Commands_SendGoal_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_SendGoal_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_SendGoal_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `stamp`
#include "builtin_interfaces/msg/detail/time__functions.h"

bool
commands_action_interface__action__Commands_SendGoal_Response__init(commands_action_interface__action__Commands_SendGoal_Response * msg)
{
  if (!msg) {
    return false;
  }
  // accepted
  // stamp
  if (!builtin_interfaces__msg__Time__init(&msg->stamp)) {
    commands_action_interface__action__Commands_SendGoal_Response__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Response__fini(commands_action_interface__action__Commands_SendGoal_Response * msg)
{
  if (!msg) {
    return;
  }
  // accepted
  // stamp
  builtin_interfaces__msg__Time__fini(&msg->stamp);
}

bool
commands_action_interface__action__Commands_SendGoal_Response__are_equal(const commands_action_interface__action__Commands_SendGoal_Response * lhs, const commands_action_interface__action__Commands_SendGoal_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // accepted
  if (lhs->accepted != rhs->accepted) {
    return false;
  }
  // stamp
  if (!builtin_interfaces__msg__Time__are_equal(
      &(lhs->stamp), &(rhs->stamp)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Response__copy(
  const commands_action_interface__action__Commands_SendGoal_Response * input,
  commands_action_interface__action__Commands_SendGoal_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // accepted
  output->accepted = input->accepted;
  // stamp
  if (!builtin_interfaces__msg__Time__copy(
      &(input->stamp), &(output->stamp)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_SendGoal_Response *
commands_action_interface__action__Commands_SendGoal_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Response * msg = (commands_action_interface__action__Commands_SendGoal_Response *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_SendGoal_Response));
  bool success = commands_action_interface__action__Commands_SendGoal_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_SendGoal_Response__destroy(commands_action_interface__action__Commands_SendGoal_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_SendGoal_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_SendGoal_Response__Sequence__init(commands_action_interface__action__Commands_SendGoal_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Response * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_SendGoal_Response *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_SendGoal_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_SendGoal_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_SendGoal_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Response__Sequence__fini(commands_action_interface__action__Commands_SendGoal_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_SendGoal_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_SendGoal_Response__Sequence *
commands_action_interface__action__Commands_SendGoal_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Response__Sequence * array = (commands_action_interface__action__Commands_SendGoal_Response__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_SendGoal_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_SendGoal_Response__Sequence__destroy(commands_action_interface__action__Commands_SendGoal_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_SendGoal_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_SendGoal_Response__Sequence__are_equal(const commands_action_interface__action__Commands_SendGoal_Response__Sequence * lhs, const commands_action_interface__action__Commands_SendGoal_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Response__Sequence__copy(
  const commands_action_interface__action__Commands_SendGoal_Response__Sequence * input,
  commands_action_interface__action__Commands_SendGoal_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_SendGoal_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_SendGoal_Response * data =
      (commands_action_interface__action__Commands_SendGoal_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_SendGoal_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_SendGoal_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
#include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"

bool
commands_action_interface__action__Commands_SendGoal_Event__init(commands_action_interface__action__Commands_SendGoal_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    commands_action_interface__action__Commands_SendGoal_Event__fini(msg);
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_SendGoal_Request__Sequence__init(&msg->request, 0)) {
    commands_action_interface__action__Commands_SendGoal_Event__fini(msg);
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_SendGoal_Response__Sequence__init(&msg->response, 0)) {
    commands_action_interface__action__Commands_SendGoal_Event__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Event__fini(commands_action_interface__action__Commands_SendGoal_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  commands_action_interface__action__Commands_SendGoal_Request__Sequence__fini(&msg->request);
  // response
  commands_action_interface__action__Commands_SendGoal_Response__Sequence__fini(&msg->response);
}

bool
commands_action_interface__action__Commands_SendGoal_Event__are_equal(const commands_action_interface__action__Commands_SendGoal_Event * lhs, const commands_action_interface__action__Commands_SendGoal_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_SendGoal_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_SendGoal_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Event__copy(
  const commands_action_interface__action__Commands_SendGoal_Event * input,
  commands_action_interface__action__Commands_SendGoal_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_SendGoal_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_SendGoal_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_SendGoal_Event *
commands_action_interface__action__Commands_SendGoal_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Event * msg = (commands_action_interface__action__Commands_SendGoal_Event *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_SendGoal_Event));
  bool success = commands_action_interface__action__Commands_SendGoal_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_SendGoal_Event__destroy(commands_action_interface__action__Commands_SendGoal_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_SendGoal_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_SendGoal_Event__Sequence__init(commands_action_interface__action__Commands_SendGoal_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Event * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_SendGoal_Event *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_SendGoal_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_SendGoal_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_SendGoal_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_SendGoal_Event__Sequence__fini(commands_action_interface__action__Commands_SendGoal_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_SendGoal_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_SendGoal_Event__Sequence *
commands_action_interface__action__Commands_SendGoal_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_SendGoal_Event__Sequence * array = (commands_action_interface__action__Commands_SendGoal_Event__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_SendGoal_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_SendGoal_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_SendGoal_Event__Sequence__destroy(commands_action_interface__action__Commands_SendGoal_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_SendGoal_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_SendGoal_Event__Sequence__are_equal(const commands_action_interface__action__Commands_SendGoal_Event__Sequence * lhs, const commands_action_interface__action__Commands_SendGoal_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_SendGoal_Event__Sequence__copy(
  const commands_action_interface__action__Commands_SendGoal_Event__Sequence * input,
  commands_action_interface__action__Commands_SendGoal_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_SendGoal_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_SendGoal_Event * data =
      (commands_action_interface__action__Commands_SendGoal_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_SendGoal_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_SendGoal_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_SendGoal_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"

bool
commands_action_interface__action__Commands_GetResult_Request__init(commands_action_interface__action__Commands_GetResult_Request * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    commands_action_interface__action__Commands_GetResult_Request__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Request__fini(commands_action_interface__action__Commands_GetResult_Request * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
}

bool
commands_action_interface__action__Commands_GetResult_Request__are_equal(const commands_action_interface__action__Commands_GetResult_Request * lhs, const commands_action_interface__action__Commands_GetResult_Request * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Request__copy(
  const commands_action_interface__action__Commands_GetResult_Request * input,
  commands_action_interface__action__Commands_GetResult_Request * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_GetResult_Request *
commands_action_interface__action__Commands_GetResult_Request__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Request * msg = (commands_action_interface__action__Commands_GetResult_Request *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Request), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_GetResult_Request));
  bool success = commands_action_interface__action__Commands_GetResult_Request__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_GetResult_Request__destroy(commands_action_interface__action__Commands_GetResult_Request * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_GetResult_Request__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_GetResult_Request__Sequence__init(commands_action_interface__action__Commands_GetResult_Request__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Request * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_GetResult_Request *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_GetResult_Request), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_GetResult_Request__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_GetResult_Request__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Request__Sequence__fini(commands_action_interface__action__Commands_GetResult_Request__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_GetResult_Request__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_GetResult_Request__Sequence *
commands_action_interface__action__Commands_GetResult_Request__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Request__Sequence * array = (commands_action_interface__action__Commands_GetResult_Request__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Request__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_GetResult_Request__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_GetResult_Request__Sequence__destroy(commands_action_interface__action__Commands_GetResult_Request__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_GetResult_Request__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_GetResult_Request__Sequence__are_equal(const commands_action_interface__action__Commands_GetResult_Request__Sequence * lhs, const commands_action_interface__action__Commands_GetResult_Request__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Request__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Request__Sequence__copy(
  const commands_action_interface__action__Commands_GetResult_Request__Sequence * input,
  commands_action_interface__action__Commands_GetResult_Request__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_GetResult_Request);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_GetResult_Request * data =
      (commands_action_interface__action__Commands_GetResult_Request *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_GetResult_Request__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_GetResult_Request__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Request__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `result`
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"

bool
commands_action_interface__action__Commands_GetResult_Response__init(commands_action_interface__action__Commands_GetResult_Response * msg)
{
  if (!msg) {
    return false;
  }
  // status
  // result
  if (!commands_action_interface__action__Commands_Result__init(&msg->result)) {
    commands_action_interface__action__Commands_GetResult_Response__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Response__fini(commands_action_interface__action__Commands_GetResult_Response * msg)
{
  if (!msg) {
    return;
  }
  // status
  // result
  commands_action_interface__action__Commands_Result__fini(&msg->result);
}

bool
commands_action_interface__action__Commands_GetResult_Response__are_equal(const commands_action_interface__action__Commands_GetResult_Response * lhs, const commands_action_interface__action__Commands_GetResult_Response * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // status
  if (lhs->status != rhs->status) {
    return false;
  }
  // result
  if (!commands_action_interface__action__Commands_Result__are_equal(
      &(lhs->result), &(rhs->result)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Response__copy(
  const commands_action_interface__action__Commands_GetResult_Response * input,
  commands_action_interface__action__Commands_GetResult_Response * output)
{
  if (!input || !output) {
    return false;
  }
  // status
  output->status = input->status;
  // result
  if (!commands_action_interface__action__Commands_Result__copy(
      &(input->result), &(output->result)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_GetResult_Response *
commands_action_interface__action__Commands_GetResult_Response__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Response * msg = (commands_action_interface__action__Commands_GetResult_Response *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Response), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_GetResult_Response));
  bool success = commands_action_interface__action__Commands_GetResult_Response__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_GetResult_Response__destroy(commands_action_interface__action__Commands_GetResult_Response * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_GetResult_Response__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_GetResult_Response__Sequence__init(commands_action_interface__action__Commands_GetResult_Response__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Response * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_GetResult_Response *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_GetResult_Response), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_GetResult_Response__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_GetResult_Response__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Response__Sequence__fini(commands_action_interface__action__Commands_GetResult_Response__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_GetResult_Response__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_GetResult_Response__Sequence *
commands_action_interface__action__Commands_GetResult_Response__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Response__Sequence * array = (commands_action_interface__action__Commands_GetResult_Response__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Response__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_GetResult_Response__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_GetResult_Response__Sequence__destroy(commands_action_interface__action__Commands_GetResult_Response__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_GetResult_Response__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_GetResult_Response__Sequence__are_equal(const commands_action_interface__action__Commands_GetResult_Response__Sequence * lhs, const commands_action_interface__action__Commands_GetResult_Response__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Response__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Response__Sequence__copy(
  const commands_action_interface__action__Commands_GetResult_Response__Sequence * input,
  commands_action_interface__action__Commands_GetResult_Response__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_GetResult_Response);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_GetResult_Response * data =
      (commands_action_interface__action__Commands_GetResult_Response *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_GetResult_Response__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_GetResult_Response__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Response__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `info`
// already included above
// #include "service_msgs/msg/detail/service_event_info__functions.h"
// Member `request`
// Member `response`
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"

bool
commands_action_interface__action__Commands_GetResult_Event__init(commands_action_interface__action__Commands_GetResult_Event * msg)
{
  if (!msg) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__init(&msg->info)) {
    commands_action_interface__action__Commands_GetResult_Event__fini(msg);
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_GetResult_Request__Sequence__init(&msg->request, 0)) {
    commands_action_interface__action__Commands_GetResult_Event__fini(msg);
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_GetResult_Response__Sequence__init(&msg->response, 0)) {
    commands_action_interface__action__Commands_GetResult_Event__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Event__fini(commands_action_interface__action__Commands_GetResult_Event * msg)
{
  if (!msg) {
    return;
  }
  // info
  service_msgs__msg__ServiceEventInfo__fini(&msg->info);
  // request
  commands_action_interface__action__Commands_GetResult_Request__Sequence__fini(&msg->request);
  // response
  commands_action_interface__action__Commands_GetResult_Response__Sequence__fini(&msg->response);
}

bool
commands_action_interface__action__Commands_GetResult_Event__are_equal(const commands_action_interface__action__Commands_GetResult_Event * lhs, const commands_action_interface__action__Commands_GetResult_Event * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__are_equal(
      &(lhs->info), &(rhs->info)))
  {
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_GetResult_Request__Sequence__are_equal(
      &(lhs->request), &(rhs->request)))
  {
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_GetResult_Response__Sequence__are_equal(
      &(lhs->response), &(rhs->response)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Event__copy(
  const commands_action_interface__action__Commands_GetResult_Event * input,
  commands_action_interface__action__Commands_GetResult_Event * output)
{
  if (!input || !output) {
    return false;
  }
  // info
  if (!service_msgs__msg__ServiceEventInfo__copy(
      &(input->info), &(output->info)))
  {
    return false;
  }
  // request
  if (!commands_action_interface__action__Commands_GetResult_Request__Sequence__copy(
      &(input->request), &(output->request)))
  {
    return false;
  }
  // response
  if (!commands_action_interface__action__Commands_GetResult_Response__Sequence__copy(
      &(input->response), &(output->response)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_GetResult_Event *
commands_action_interface__action__Commands_GetResult_Event__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Event * msg = (commands_action_interface__action__Commands_GetResult_Event *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Event), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_GetResult_Event));
  bool success = commands_action_interface__action__Commands_GetResult_Event__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_GetResult_Event__destroy(commands_action_interface__action__Commands_GetResult_Event * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_GetResult_Event__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_GetResult_Event__Sequence__init(commands_action_interface__action__Commands_GetResult_Event__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Event * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_GetResult_Event *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_GetResult_Event), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_GetResult_Event__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_GetResult_Event__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_GetResult_Event__Sequence__fini(commands_action_interface__action__Commands_GetResult_Event__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_GetResult_Event__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_GetResult_Event__Sequence *
commands_action_interface__action__Commands_GetResult_Event__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_GetResult_Event__Sequence * array = (commands_action_interface__action__Commands_GetResult_Event__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_GetResult_Event__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_GetResult_Event__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_GetResult_Event__Sequence__destroy(commands_action_interface__action__Commands_GetResult_Event__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_GetResult_Event__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_GetResult_Event__Sequence__are_equal(const commands_action_interface__action__Commands_GetResult_Event__Sequence * lhs, const commands_action_interface__action__Commands_GetResult_Event__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Event__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_GetResult_Event__Sequence__copy(
  const commands_action_interface__action__Commands_GetResult_Event__Sequence * input,
  commands_action_interface__action__Commands_GetResult_Event__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_GetResult_Event);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_GetResult_Event * data =
      (commands_action_interface__action__Commands_GetResult_Event *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_GetResult_Event__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_GetResult_Event__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_GetResult_Event__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}


// Include directives for member types
// Member `goal_id`
// already included above
// #include "unique_identifier_msgs/msg/detail/uuid__functions.h"
// Member `feedback`
// already included above
// #include "commands_action_interface/action/detail/commands__functions.h"

bool
commands_action_interface__action__Commands_FeedbackMessage__init(commands_action_interface__action__Commands_FeedbackMessage * msg)
{
  if (!msg) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__init(&msg->goal_id)) {
    commands_action_interface__action__Commands_FeedbackMessage__fini(msg);
    return false;
  }
  // feedback
  if (!commands_action_interface__action__Commands_Feedback__init(&msg->feedback)) {
    commands_action_interface__action__Commands_FeedbackMessage__fini(msg);
    return false;
  }
  return true;
}

void
commands_action_interface__action__Commands_FeedbackMessage__fini(commands_action_interface__action__Commands_FeedbackMessage * msg)
{
  if (!msg) {
    return;
  }
  // goal_id
  unique_identifier_msgs__msg__UUID__fini(&msg->goal_id);
  // feedback
  commands_action_interface__action__Commands_Feedback__fini(&msg->feedback);
}

bool
commands_action_interface__action__Commands_FeedbackMessage__are_equal(const commands_action_interface__action__Commands_FeedbackMessage * lhs, const commands_action_interface__action__Commands_FeedbackMessage * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__are_equal(
      &(lhs->goal_id), &(rhs->goal_id)))
  {
    return false;
  }
  // feedback
  if (!commands_action_interface__action__Commands_Feedback__are_equal(
      &(lhs->feedback), &(rhs->feedback)))
  {
    return false;
  }
  return true;
}

bool
commands_action_interface__action__Commands_FeedbackMessage__copy(
  const commands_action_interface__action__Commands_FeedbackMessage * input,
  commands_action_interface__action__Commands_FeedbackMessage * output)
{
  if (!input || !output) {
    return false;
  }
  // goal_id
  if (!unique_identifier_msgs__msg__UUID__copy(
      &(input->goal_id), &(output->goal_id)))
  {
    return false;
  }
  // feedback
  if (!commands_action_interface__action__Commands_Feedback__copy(
      &(input->feedback), &(output->feedback)))
  {
    return false;
  }
  return true;
}

commands_action_interface__action__Commands_FeedbackMessage *
commands_action_interface__action__Commands_FeedbackMessage__create(void)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_FeedbackMessage * msg = (commands_action_interface__action__Commands_FeedbackMessage *)allocator.allocate(sizeof(commands_action_interface__action__Commands_FeedbackMessage), allocator.state);
  if (!msg) {
    return NULL;
  }
  memset(msg, 0, sizeof(commands_action_interface__action__Commands_FeedbackMessage));
  bool success = commands_action_interface__action__Commands_FeedbackMessage__init(msg);
  if (!success) {
    allocator.deallocate(msg, allocator.state);
    return NULL;
  }
  return msg;
}

void
commands_action_interface__action__Commands_FeedbackMessage__destroy(commands_action_interface__action__Commands_FeedbackMessage * msg)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (msg) {
    commands_action_interface__action__Commands_FeedbackMessage__fini(msg);
  }
  allocator.deallocate(msg, allocator.state);
}


bool
commands_action_interface__action__Commands_FeedbackMessage__Sequence__init(commands_action_interface__action__Commands_FeedbackMessage__Sequence * array, size_t size)
{
  if (!array) {
    return false;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_FeedbackMessage * data = NULL;

  if (size) {
    data = (commands_action_interface__action__Commands_FeedbackMessage *)allocator.zero_allocate(size, sizeof(commands_action_interface__action__Commands_FeedbackMessage), allocator.state);
    if (!data) {
      return false;
    }
    // initialize all array elements
    size_t i;
    for (i = 0; i < size; ++i) {
      bool success = commands_action_interface__action__Commands_FeedbackMessage__init(&data[i]);
      if (!success) {
        break;
      }
    }
    if (i < size) {
      // if initialization failed finalize the already initialized array elements
      for (; i > 0; --i) {
        commands_action_interface__action__Commands_FeedbackMessage__fini(&data[i - 1]);
      }
      allocator.deallocate(data, allocator.state);
      return false;
    }
  }
  array->data = data;
  array->size = size;
  array->capacity = size;
  return true;
}

void
commands_action_interface__action__Commands_FeedbackMessage__Sequence__fini(commands_action_interface__action__Commands_FeedbackMessage__Sequence * array)
{
  if (!array) {
    return;
  }
  rcutils_allocator_t allocator = rcutils_get_default_allocator();

  if (array->data) {
    // ensure that data and capacity values are consistent
    assert(array->capacity > 0);
    // finalize all array elements
    for (size_t i = 0; i < array->capacity; ++i) {
      commands_action_interface__action__Commands_FeedbackMessage__fini(&array->data[i]);
    }
    allocator.deallocate(array->data, allocator.state);
    array->data = NULL;
    array->size = 0;
    array->capacity = 0;
  } else {
    // ensure that data, size, and capacity values are consistent
    assert(0 == array->size);
    assert(0 == array->capacity);
  }
}

commands_action_interface__action__Commands_FeedbackMessage__Sequence *
commands_action_interface__action__Commands_FeedbackMessage__Sequence__create(size_t size)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  commands_action_interface__action__Commands_FeedbackMessage__Sequence * array = (commands_action_interface__action__Commands_FeedbackMessage__Sequence *)allocator.allocate(sizeof(commands_action_interface__action__Commands_FeedbackMessage__Sequence), allocator.state);
  if (!array) {
    return NULL;
  }
  bool success = commands_action_interface__action__Commands_FeedbackMessage__Sequence__init(array, size);
  if (!success) {
    allocator.deallocate(array, allocator.state);
    return NULL;
  }
  return array;
}

void
commands_action_interface__action__Commands_FeedbackMessage__Sequence__destroy(commands_action_interface__action__Commands_FeedbackMessage__Sequence * array)
{
  rcutils_allocator_t allocator = rcutils_get_default_allocator();
  if (array) {
    commands_action_interface__action__Commands_FeedbackMessage__Sequence__fini(array);
  }
  allocator.deallocate(array, allocator.state);
}

bool
commands_action_interface__action__Commands_FeedbackMessage__Sequence__are_equal(const commands_action_interface__action__Commands_FeedbackMessage__Sequence * lhs, const commands_action_interface__action__Commands_FeedbackMessage__Sequence * rhs)
{
  if (!lhs || !rhs) {
    return false;
  }
  if (lhs->size != rhs->size) {
    return false;
  }
  for (size_t i = 0; i < lhs->size; ++i) {
    if (!commands_action_interface__action__Commands_FeedbackMessage__are_equal(&(lhs->data[i]), &(rhs->data[i]))) {
      return false;
    }
  }
  return true;
}

bool
commands_action_interface__action__Commands_FeedbackMessage__Sequence__copy(
  const commands_action_interface__action__Commands_FeedbackMessage__Sequence * input,
  commands_action_interface__action__Commands_FeedbackMessage__Sequence * output)
{
  if (!input || !output) {
    return false;
  }
  if (output->capacity < input->size) {
    const size_t allocation_size =
      input->size * sizeof(commands_action_interface__action__Commands_FeedbackMessage);
    rcutils_allocator_t allocator = rcutils_get_default_allocator();
    commands_action_interface__action__Commands_FeedbackMessage * data =
      (commands_action_interface__action__Commands_FeedbackMessage *)allocator.reallocate(
      output->data, allocation_size, allocator.state);
    if (!data) {
      return false;
    }
    // If reallocation succeeded, memory may or may not have been moved
    // to fulfill the allocation request, invalidating output->data.
    output->data = data;
    for (size_t i = output->capacity; i < input->size; ++i) {
      if (!commands_action_interface__action__Commands_FeedbackMessage__init(&output->data[i])) {
        // If initialization of any new item fails, roll back
        // all previously initialized items. Existing items
        // in output are to be left unmodified.
        for (; i-- > output->capacity; ) {
          commands_action_interface__action__Commands_FeedbackMessage__fini(&output->data[i]);
        }
        return false;
      }
    }
    output->capacity = input->size;
  }
  output->size = input->size;
  for (size_t i = 0; i < input->size; ++i) {
    if (!commands_action_interface__action__Commands_FeedbackMessage__copy(
        &(input->data[i]), &(output->data[i])))
    {
      return false;
    }
  }
  return true;
}
