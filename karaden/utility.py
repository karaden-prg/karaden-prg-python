from __future__ import absolute_import, division, annotations, unicode_literals

from typing import Any, Tuple

import requests

from karaden.exception.file_upload_failed_exception import FileUploadFailedException
from karaden.request_options import RequestOptions


class Utility:
    DEFAULT_OBJECT_NAME: str
    object_types: dict
    DEFAULT_CONNECTION_TIMEOUT = 10.0
    DEFAULT_READ_TIMEOUT = 30.0

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

    @classmethod
    def put_signed_url(cls, singed_url: str, filename: str, content_type = 'application/octet-stream', request_options: RequestOptions = None) -> None:
        try:
            timeout = Utility.get_timeout(request_options)

            with open(filename, 'rb') as file:
                response = requests.put(singed_url, data=file, headers={'Content-Type': content_type}, timeout=timeout)

                if response.status_code != 200:
                    raise FileUploadFailedException()

        except FileUploadFailedException as e1:
            raise
        except Exception as e2:
            raise FileUploadFailedException() from e2

    @classmethod
    def get_timeout(cls, request_options: RequestOptions = None) -> Tuple[float, float]:
        connection_timeout = getattr(request_options, 'connection_timeout', Utility.DEFAULT_CONNECTION_TIMEOUT)
        read_timeout = getattr(request_options, 'read_timeout', Utility.DEFAULT_READ_TIMEOUT)
        return (connection_timeout, read_timeout)
