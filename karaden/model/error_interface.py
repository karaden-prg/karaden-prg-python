from __future__ import absolute_import, division, annotations, unicode_literals

import abc
from karaden.model.karaden_object_interface import KaradenObjectInterface


class ErrorInterface(metaclass=abc.ABCMeta):
    @property
    @abc.abstractclassmethod
    def code(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractclassmethod
    def message(self) -> str:
        raise NotImplementedError()

    @property
    @abc.abstractclassmethod
    def errors(self) -> KaradenObjectInterface:
        raise NotImplementedError()
