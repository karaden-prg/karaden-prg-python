from __future__ import absolute_import, division, annotations, unicode_literals

from typing import Any
from karaden.request_options import RequestOptions
from karaden.model.karaden_object_interface import KaradenObjectInterface


class KaradenObject(KaradenObjectInterface):
    OBJECT_NAME = 'default'

    def __init__(self, id=None, request_options: RequestOptions = None) -> None:
        self._properties = {}
        self._request_options = request_options

        self.set_property('id', id)

    @property
    def id(self) -> Any:
        return self.get_property('id')

    @property
    def object(self) -> str:
        return self.get_property('object')

    def get_property_keys(self) -> list:
        return list(self._properties.keys())

    def set_property(self, name: str, value):
        self._properties[name] = value

    def get_property(self, name: str) -> Any:
        return self._properties.get(name, None)
