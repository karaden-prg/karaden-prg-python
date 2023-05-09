from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.exception.karaden_exception import KaradenException


class UnexpectedValueException(KaradenException):
    def __init__(self, status_code: int, headers: dict, body: str):
        super().__init__(headers, body)
        self.status_code = status_code
