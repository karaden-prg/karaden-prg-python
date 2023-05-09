from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.net.requestor_interface import RequestorInterface
from karaden.request_options import RequestOptions
from karaden.model.karaden_object import KaradenObject


class Requestable(KaradenObject):
    requestor: RequestorInterface = None

    @classmethod
    def request(cls, method: str, path: str, params: dict = None, data: dict = None, request_options: RequestOptions = None) -> KaradenObject:
        response = cls.requestor.send(method, path, params, data, request_options)
        if response.is_error:
            raise response.error
        return response.object
