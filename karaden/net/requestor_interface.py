from __future__ import absolute_import, division, annotations, unicode_literals

import abc
from karaden.request_options import RequestOptions
from karaden.net.response_interface import ResponseInterface


class RequestorInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def send(self, method: str, path: str, params: dict, data: dict, request_options: RequestOptions = None) -> ResponseInterface:
        raise NotImplementedError()
