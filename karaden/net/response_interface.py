from __future__ import absolute_import, division, annotations, unicode_literals

import abc
from karaden.exception.karaden_exception import KaradenException
from karaden.model.karaden_object import KaradenObject


class ResponseInterface(metaclass=abc.ABCMeta):
    @abc.abstractproperty
    def error(self) -> KaradenException:
        raise NotImplementedError()

    @abc.abstractproperty
    def object(self) -> KaradenObject:
        raise NotImplementedError()

    @abc.abstractproperty
    def is_error(self) -> bool:
        raise NotImplementedError()
