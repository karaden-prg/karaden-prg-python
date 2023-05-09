from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.exception.karaden_exception import KaradenException
from karaden.model.error_interface import ErrorInterface


class UnknownErrorException(KaradenException):
    def __init__(self, status_code: int, headers: dict, body: str, error: ErrorInterface = None):
        super().__init__(headers, body, error)
        self.status_code = status_code
