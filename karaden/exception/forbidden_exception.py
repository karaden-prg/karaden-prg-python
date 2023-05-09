from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.exception.karaden_exception import KaradenException


class ForbiddenException(KaradenException):
    STATUS_CODE = 403
