from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.exception.karaden_exception import KaradenException
from karaden.model.error_interface import ErrorInterface


class InvalidParamsException(KaradenException):
    def __init__(self, error: ErrorInterface = None):
        super().__init__(None, None, error)
