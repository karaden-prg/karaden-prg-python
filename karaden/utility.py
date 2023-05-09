from __future__ import absolute_import, division, annotations, unicode_literals

from typing import Any
from karaden.request_options import RequestOptions


class Utility:
    DEFAULT_OBJECT_NAME: str
    object_types: dict

    @classmethod
    def convert_to_karaden_object(cls, contents: dict, request_options: RequestOptions) -> Any:
        object_name = contents['object'] if 'object' in contents.keys() and contents['object'] in cls.object_types else cls.DEFAULT_OBJECT_NAME
        return cls.construct_from(cls.object_types[object_name], contents, request_options)

    @classmethod
    def construct_from(cls, object_type, contents: dict, request_options: RequestOptions) -> Any:
        obj = object_type(contents['id'] if 'id' in contents else None, request_options)
        for key in contents.keys():
            obj.set_property(key, cls.convert_to_object(contents[key], request_options))
        return obj

    @classmethod
    def convert_to_list(cls, contents: list, request_options: RequestOptions) -> list:
        array = []
        for value in contents:
            array.append(cls.convert_to_object(value, request_options))
        return array

    @classmethod
    def convert_to_object(cls, value, request_options: RequestOptions) -> list:
        if isinstance(value, list):
            value = cls.convert_to_list(value, request_options)
        elif isinstance(value, dict):
            value = cls.convert_to_karaden_object(value, request_options)
        return value
