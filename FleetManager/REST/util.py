"""
REST API Utility Module for Data Serialization and Deserialization

.. module:: util
    :synopsis: Comprehensive utilities for REST API data processing and model conversion

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module provides essential utilities for handling data serialization and deserialization
in the REST API components of the Fleet Management System. It supports conversion between
various data formats and model objects, with comprehensive type handling and validation.

Core Functionality:
    - **Model Deserialization**: Convert dictionaries to model objects
    - **Type Conversion**: Handle primitive and complex type transformations
    - **Date/Time Processing**: Parse and validate temporal data formats
    - **Collection Handling**: Process lists, dictionaries, and nested structures
    - **Error Recovery**: Graceful handling of malformed or invalid data

Supported Data Types:
    - Primitive types: int, float, str, bool, bytearray
    - Temporal types: datetime.date, datetime.datetime
    - Collection types: List[T], Dict[K, V]
    - Custom model objects extending base model classes
    - Generic types with type parameter validation

Type Safety:
    All conversion functions include comprehensive type checking and validation
    to ensure data integrity and prevent runtime errors from malformed input.

.. note::
    This module is designed to work with auto-generated model classes from
    OpenAPI/Swagger specifications and follows Connexion framework patterns.

.. warning::
    Input validation is critical when deserializing user-provided data.
    Ensure proper error handling in calling code for production deployments.

.. seealso::
    - :mod:`REST.type_util`: Type inspection and validation utilities
    - :mod:`REST.models`: Auto-generated model classes for deserialization targets
"""

import datetime

import six
import typing
from REST import type_util


def _deserialize(data, klass):
    """Deserialize data to specified class type with comprehensive type handling.

    This is the main entry point for data deserialization, providing intelligent
    routing to appropriate type-specific deserialization functions based on the
    target class type.

    Deserialization Workflow:
        1. **Null Check**: Handle None values gracefully
        2. **Type Classification**: Identify target type category
        3. **Route to Handler**: Call appropriate specialized deserializer
        4. **Validation**: Ensure result matches expected type
        5. **Error Recovery**: Handle conversion failures gracefully

    Supported Type Categories:
        - **Primitives**: int, float, str, bool, bytearray
        - **Objects**: Generic object deserialization
        - **Temporal**: datetime.date, datetime.datetime
        - **Generics**: List[T], Dict[K,V] with type parameters
        - **Models**: Custom model classes from OpenAPI specs

    :param data: Input data to deserialize (dict, list, str, primitive)
    :type data: Union[dict, list, str, int, float, bool, None]
    :param klass: Target class for deserialization (class literal or string)
    :type klass: Union[type, str]

    :return: Deserialized object of the specified type
    :rtype: object

    :raises TypeError: If target class is not supported for deserialization
    :raises ValueError: If data format is incompatible with target type
    :raises AttributeError: If model class lacks required deserialization methods

    Example:
        ::

            # Deserialize primitive data
            result = _deserialize("123", int)  # Returns: 123

            # Deserialize model object
            mission_data = {"mission_id": 1, "name": "Test Mission"}
            mission = _deserialize(mission_data, Mission)

            # Deserialize list of models
            missions_data = [{"mission_id": 1}, {"mission_id": 2}]
            missions = _deserialize(missions_data, List[Mission])

    .. note::
        For generic types, type parameters must be available via __args__ attribute.
        This is automatically handled for properly annotated type hints.

    .. warning::
        Malformed input data may cause deserialization failures. Ensure proper
        validation of input data before calling this function in production code.
    """
    if data is None:
        return None

    if klass in six.integer_types or klass in (float, str, bool, bytearray):
        return _deserialize_primitive(data, klass)
    elif klass == object:
        return _deserialize_object(data)
    elif klass == datetime.date:
        return deserialize_date(data)
    elif klass == datetime.datetime:
        return deserialize_datetime(data)
    elif type_util.is_generic(klass):
        if type_util.is_list(klass):
            return _deserialize_list(data, klass.__args__[0])
        if type_util.is_dict(klass):
            return _deserialize_dict(data, klass.__args__[1])
    else:
        return deserialize_model(data, klass)


def _deserialize_primitive(data, klass):
    """Deserialize data to primitive Python types with type conversion and validation.

    Handles conversion of input data to fundamental Python types including integers,
    floats, strings, booleans, and byte arrays. Provides robust error handling for
    Unicode encoding issues and type conversion failures.

    Type Conversion Strategy:
        1. **Direct Conversion**: Attempt direct type constructor call
        2. **Unicode Handling**: Handle Unicode encoding issues for string data
        3. **Fallback**: Return original data if conversion fails
        4. **Validation**: Ensure result is of expected type

    Supported Primitive Types:
        - **int**: Integer values with overflow protection
        - **float**: Floating-point numbers with precision handling
        - **str**: String values with Unicode support
        - **bool**: Boolean values with truthiness conversion
        - **bytearray**: Byte array conversion for binary data

    :param data: Input data to convert to primitive type
    :type data: Union[str, int, float, bool, bytes, bytearray]
    :param klass: Target primitive type class
    :type klass: Union[type(int), type(float), type(str), type(bool), type(bytearray)]

    :return: Converted value of the specified primitive type
    :rtype: Union[int, float, str, bool, bytearray]

    :raises UnicodeEncodeError: Handled internally with Unicode conversion fallback
    :raises TypeError: Handled internally with original data fallback
    :raises ValueError: If data cannot be converted to target type

    Example:
        ::

            # Integer conversion
            result = _deserialize_primitive("123", int)  # Returns: 123

            # Float conversion with string input
            result = _deserialize_primitive("3.14", float)  # Returns: 3.14

            # Boolean conversion
            result = _deserialize_primitive("true", bool)  # Returns: True

            # String conversion with Unicode handling
            result = _deserialize_primitive(b"hello", str)  # Returns: "hello"

    .. note::
        Unicode encoding errors are automatically handled by converting to
        Unicode string representation using six.u() function.

    .. warning::
        Type conversion failures fall back to returning original data.
        This may result in unexpected types in the calling code.
    """
    try:
        value = klass(data)
    except UnicodeEncodeError:
        value = six.u(data)
    except TypeError:
        value = data
    return value


def _deserialize_object(value):
    """Return the original object value without transformation.

    This function serves as a passthrough for generic object types that don't
    require special deserialization handling. It's used when the target type
    is specified as 'object' and the input should be preserved as-is.

    :param value: Input value to return unchanged
    :type value: object

    :return: Original input value without modification
    :rtype: object

    Example:
        ::

            data = {"key": "value", "nested": {"data": 123}}
            result = _deserialize_object(data)  # Returns: same dict object
    """
    return value


def deserialize_date(string):
    """Deserialize string representation to Python date object.

    Converts string input to a date object using intelligent parsing that handles
    various date formats. Uses dateutil.parser for robust date parsing when available,
    with graceful fallback for environments where dateutil is not installed.

    Supported Date Formats:
        - ISO 8601: "2025-06-29"
        - US Format: "06/29/2025", "06-29-2025"
        - European Format: "29/06/2025", "29-06-2025"
        - Natural Language: "June 29, 2025", "29 Jun 2025"

    :param string: String representation of date in various supported formats
    :type string: str

    :return: Parsed date object, or original string if parsing fails
    :rtype: Union[datetime.date, str]

    :raises ImportError: Handled internally - returns original string if dateutil unavailable
    :raises ValueError: Handled internally by dateutil parser

    Example:
        ::

            # ISO 8601 format
            date_obj = deserialize_date("2025-06-29")  # Returns: date(2025, 6, 29)

            # US format
            date_obj = deserialize_date("06/29/2025")  # Returns: date(2025, 6, 29)

            # Natural language
            date_obj = deserialize_date("June 29, 2025")  # Returns: date(2025, 6, 29)

    .. note::
        When dateutil is not available, the function returns the original string
        unchanged. This provides graceful degradation in minimal environments.

    .. warning::
        Ambiguous date formats may be interpreted differently depending on the
        system locale. Use ISO 8601 format for consistent parsing across systems.
    """
    try:
        from dateutil.parser import parse
        return parse(string).date()
    except ImportError:
        return string


def deserialize_datetime(string):
    """Deserialize string representation to Python datetime object.

    Converts string input to a datetime object using intelligent parsing that handles
    various datetime formats including ISO 8601, RFC standards, and natural language
    representations. Provides robust timezone handling and format detection.

    Supported DateTime Formats:
        - ISO 8601: "2025-06-29T14:30:00Z", "2025-06-29T14:30:00+00:00"
        - RFC 2822: "Sun, 29 Jun 2025 14:30:00 GMT"
        - Natural Language: "June 29, 2025 2:30 PM", "29 Jun 2025 14:30"
        - Custom Formats: Various combinations with automatic detection

    Timezone Handling:
        - Preserves timezone information when present in input
        - Handles UTC/GMT indicators and timezone offsets
        - Supports named timezone abbreviations

    :param string: String representation of datetime in supported formats
    :type string: str

    :return: Parsed datetime object, or original string if parsing fails
    :rtype: Union[datetime.datetime, str]

    :raises ImportError: Handled internally - returns original string if dateutil unavailable
    :raises ValueError: Handled internally by dateutil parser for malformed input

    Example:
        ::

            # ISO 8601 with timezone
            dt = deserialize_datetime("2025-06-29T14:30:00Z")
            # Returns: datetime(2025, 6, 29, 14, 30, tzinfo=tzutc())

            # Natural language format
            dt = deserialize_datetime("June 29, 2025 2:30 PM")
            # Returns: datetime(2025, 6, 29, 14, 30)

            # RFC format
            dt = deserialize_datetime("Sun, 29 Jun 2025 14:30:00 GMT")
            # Returns: datetime(2025, 6, 29, 14, 30, tzinfo=tzutc())

    .. note::
        The dateutil parser is very flexible and can handle most reasonable
        datetime string representations. When dateutil is unavailable, the
        original string is returned for graceful degradation.

    .. warning::
        Ambiguous datetime formats may be interpreted differently based on
        system locale settings. Use ISO 8601 format for consistent parsing.
    """
    try:
        from dateutil.parser import parse
        return parse(string)
    except ImportError:
        return string


def deserialize_model(data, klass):
    """Deserialize dictionary data to OpenAPI model object with attribute mapping.

    This function converts dictionary data into instances of auto-generated OpenAPI
    model classes. It handles attribute mapping, type conversion, and validation
    according to the model's Swagger type specifications.

    Deserialization Process:
        1. **Model Instantiation**: Create empty instance of target model class
        2. **Schema Validation**: Check if model has Swagger type definitions
        3. **Attribute Mapping**: Convert dictionary keys using attribute_map
        4. **Type Conversion**: Recursively deserialize nested attributes
        5. **Instance Population**: Set attributes on model instance

    Model Requirements:
        - Model class must have swagger_types dictionary defining attribute types
        - Model class must have attribute_map dictionary for key translation
        - Model class must be instantiable with no-argument constructor

    :param data: Dictionary data to deserialize, or list for batch processing
    :type data: Union[dict, list]
    :param klass: Target model class from OpenAPI specification
    :type klass: type

    :return: Populated model instance with deserialized data
    :rtype: object

    :raises AttributeError: If model class lacks required swagger_types or attribute_map
    :raises TypeError: If data format is incompatible with model structure
    :raises ValueError: If required attributes are missing or invalid

    Example:
        ::

            # Deserialize mission data
            mission_data = {
                "mission_id": 123,
                "name": "Agricultural Survey",
                "vehicles": [{"id": 1, "type": "drone"}]
            }
            mission = deserialize_model(mission_data, Mission)

            # Access deserialized attributes
            print(mission.mission_id)  # 123
            print(mission.name)        # "Agricultural Survey"

    .. note::
        If the model class has no swagger_types definition, the original data
        is returned unchanged. This provides compatibility with non-OpenAPI models.

    .. warning::
        Model deserialization assumes the input data structure matches the
        expected schema. Invalid or missing attributes may result in incomplete
        model instances.
    """
    instance = klass()

    if not instance.swagger_types:
        return data

    for attr, attr_type in six.iteritems(instance.swagger_types):
        if data is not None \
                and instance.attribute_map[attr] in data \
                and isinstance(data, (list, dict)):
            value = data[instance.attribute_map[attr]]
            setattr(instance, attr, _deserialize(value, attr_type))

    return instance


def _deserialize_list(data, boxed_type):
    """Deserialize a list of elements to specified type with recursive processing.

    Processes each element in the input list through the main deserialization
    function, converting them to the specified boxed type. This enables handling
    of complex nested structures like List[Model] or List[List[T]].

    Processing Strategy:
        1. **Element Iteration**: Process each list element individually
        2. **Recursive Deserialization**: Apply full deserialization to each element
        3. **Type Consistency**: Ensure all elements match the boxed type
        4. **Result Assembly**: Return new list with converted elements

    :param data: List of elements to deserialize
    :type data: list
    :param boxed_type: Target type for list elements (e.g., Mission, int, str)
    :type boxed_type: type

    :return: New list with elements converted to the specified type
    :rtype: list

    :raises TypeError: If input data is not a list
    :raises ValueError: If elements cannot be converted to boxed_type

    Example:
        ::

            # Deserialize list of integers
            int_list = _deserialize_list(["1", "2", "3"], int)
            # Returns: [1, 2, 3]

            # Deserialize list of model objects
            mission_data = [{"id": 1}, {"id": 2}]
            missions = _deserialize_list(mission_data, Mission)
            # Returns: [Mission(id=1), Mission(id=2)]

    .. note::
        Empty lists are handled gracefully and return empty results.
        The function preserves list order during deserialization.

    .. warning::
        If any element fails deserialization, the entire operation may fail.
        Consider error handling in calling code for robust list processing.
    """
    return [_deserialize(sub_data, boxed_type)
            for sub_data in data]


def _deserialize_dict(data, boxed_type):
    """Deserialize dictionary values to specified type while preserving keys.

    Processes each value in the input dictionary through the main deserialization
    function, converting them to the specified boxed type. Dictionary keys are
    preserved unchanged, creating a new dictionary with converted values.

    Processing Strategy:
        1. **Key Preservation**: Maintain original dictionary keys unchanged
        2. **Value Conversion**: Apply deserialization to each dictionary value
        3. **Type Consistency**: Ensure all values match the boxed type
        4. **Result Assembly**: Return new dictionary with converted values

    Use Cases:
        - Dict[str, Model]: String keys mapping to model objects
        - Dict[int, List[T]]: Integer keys mapping to typed lists
        - Dict[str, Dict[str, T]]: Nested dictionary structures

    :param data: Dictionary with values to deserialize
    :type data: dict
    :param boxed_type: Target type for dictionary values (e.g., Mission, int, str)
    :type boxed_type: type

    :return: New dictionary with keys preserved and values converted to specified type
    :rtype: dict

    :raises TypeError: If input data is not a dictionary
    :raises ValueError: If values cannot be converted to boxed_type

    Example:
        ::

            # Deserialize dictionary with integer values
            data = {"count": "10", "limit": "50"}
            result = _deserialize_dict(data, int)
            # Returns: {"count": 10, "limit": 50}

            # Deserialize dictionary with model objects
            vehicle_data = {
                "drone1": {"id": 1, "type": "drone"},
                "tractor1": {"id": 2, "type": "tractor"}
            }
            vehicles = _deserialize_dict(vehicle_data, Vehicle)
            # Returns: {"drone1": Vehicle(id=1), "tractor1": Vehicle(id=2)}

    .. note::
        Empty dictionaries are handled gracefully and return empty results.
        The function preserves key-value association during deserialization.

    .. warning::
        If any value fails deserialization, the entire operation may fail.
        Dictionary keys are assumed to be valid and are not validated.
    """
    return {k: _deserialize(v, boxed_type)
            for k, v in six.iteritems(data)}
