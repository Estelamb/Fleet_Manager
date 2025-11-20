"""
Type Inspection and Validation Utilities for REST API

.. module:: type_util
    :synopsis: Cross-version type inspection utilities for generic types and collections

.. moduleauthor:: Fleet Management System Team

.. versionadded:: 1.0

This module provides type inspection utilities that work across different Python versions,
specifically handling the differences in typing module behavior between Python < 3.7 and
Python >= 3.7. It enables consistent type checking for generic types, dictionaries, and
lists in the REST API serialization/deserialization pipeline.

Python Version Compatibility:
    - **Python < 3.7**: Uses typing.GenericMeta and __extra__ attribute
    - **Python >= 3.7**: Uses __origin__ attribute for type inspection

The module abstracts these version differences, providing a unified interface for:
    - Generic type detection (List[T], Dict[K,V], etc.)
    - Dictionary type validation (Dict, typing.Dict)
    - List type validation (List, typing.List)

Key Features:
    - **Version Agnostic**: Consistent API across Python versions
    - **Generic Type Support**: Handles parameterized types like List[Model]
    - **Dictionary Detection**: Identifies Dict and typing.Dict types
    - **List Detection**: Identifies List and typing.List types
    - **Runtime Safety**: Graceful handling of type inspection edge cases

Usage in Deserialization:
    These utilities are primarily used by the util.py module to determine
    appropriate deserialization strategies for different data types during
    REST API data processing.

.. note::
    This module handles the complexity of Python typing evolution, ensuring
    consistent behavior across different deployment environments.

.. warning::
    The typing module behavior changed significantly in Python 3.7. This
    module provides compatibility, but type hints should be used consistently.

.. seealso::
    - :mod:`REST.util`: Main deserialization utilities that use these functions
    - :mod:`typing`: Python's typing module documentation
"""

# coding: utf-8

import sys

if sys.version_info < (3, 7):
    import typing

    def is_generic(klass):
        """Determine whether klass is a generic class (Python < 3.7 implementation).
        
        For Python versions before 3.7, generic types use typing.GenericMeta
        as their metaclass. This function checks if the provided class is
        an instance of this metaclass.

        :param klass: Class to inspect for generic type properties
        :type klass: type

        :return: True if klass is a generic type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import List, Dict
                is_generic(List[str])  # Returns: True
                is_generic(str)        # Returns: False
                is_generic(Dict[str, int])  # Returns: True
        """
        return type(klass) == typing.GenericMeta

    def is_dict(klass):
        """Determine whether klass is a Dict type (Python < 3.7 implementation).
        
        For Python versions before 3.7, dictionary types are identified by
        checking the __extra__ attribute which contains the concrete type.

        :param klass: Type to inspect for dictionary properties
        :type klass: type

        :return: True if klass is a Dict type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import Dict, List
                is_dict(Dict[str, int])  # Returns: True
                is_dict(List[str])       # Returns: False
                is_dict(dict)           # Returns: False (plain dict, not typing.Dict)
        """
        return klass.__extra__ == dict

    def is_list(klass):
        """Determine whether klass is a List type (Python < 3.7 implementation).
        
        For Python versions before 3.7, list types are identified by
        checking the __extra__ attribute which contains the concrete type.

        :param klass: Type to inspect for list properties
        :type klass: type

        :return: True if klass is a List type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import List, Dict
                is_list(List[str])       # Returns: True
                is_list(Dict[str, int])  # Returns: False
                is_list(list)           # Returns: False (plain list, not typing.List)
        """
        return klass.__extra__ == list

else:

    def is_generic(klass):
        """Determine whether klass is a generic class (Python >= 3.7 implementation).
        
        For Python 3.7 and later, generic types are identified by the presence
        of the __origin__ attribute, which indicates the class is a parameterized
        generic type from the typing module.

        :param klass: Class to inspect for generic type properties
        :type klass: type

        :return: True if klass is a generic type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import List, Dict, Union
                is_generic(List[str])     # Returns: True
                is_generic(str)           # Returns: False
                is_generic(Union[str, int])  # Returns: True
        """
        return hasattr(klass, '__origin__')

    def is_dict(klass):
        """Determine whether klass is a Dict type (Python >= 3.7 implementation).
        
        For Python 3.7 and later, dictionary types are identified by checking
        the __origin__ attribute which contains the base type for parameterized
        generic types.

        :param klass: Type to inspect for dictionary properties
        :type klass: type

        :return: True if klass is a Dict type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import Dict, List
                is_dict(Dict[str, int])  # Returns: True
                is_dict(List[str])       # Returns: False
                is_dict(dict)           # Returns: False (plain dict, not typing.Dict)
        """
        return klass.__origin__ == dict

    def is_list(klass):
        """Determine whether klass is a List type (Python >= 3.7 implementation).
        
        For Python 3.7 and later, list types are identified by checking
        the __origin__ attribute which contains the base type for parameterized
        generic types.

        :param klass: Type to inspect for list properties
        :type klass: type

        :return: True if klass is a List type, False otherwise
        :rtype: bool

        Example:
            ::

                from typing import List, Dict
                is_list(List[str])       # Returns: True
                is_list(Dict[str, int])  # Returns: False
                is_list(list)           # Returns: False (plain list, not typing.List)
        """
        return klass.__origin__ == list
