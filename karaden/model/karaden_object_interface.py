from __future__ import absolute_import, division, annotations, unicode_literals

import abc
from typing import Any


class KaradenObjectInterface(metaclass=abc.ABCMeta):
    @property
    @abc.abstractmethod
    def id(self) -> Any:
        raise NotImplementedError()

    @property
    @abc.abstractmethod
    def object(self) -> str:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_property_keys(self) -> list:
        raise NotImplementedError()

    @abc.abstractmethod
    def set_property(self, name: str, value):
        raise NotImplementedError()

    @abc.abstractmethod
    def get_property(self, name: str) -> Any:
        raise NotImplementedError()
