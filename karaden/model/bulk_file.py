from __future__ import absolute_import, division, annotations, unicode_literals

from datetime import datetime

from karaden.model.requestable import Requestable
from karaden.param.bulk.bulk_message_params import BulkMessageParams
from karaden.request_options import RequestOptions


class BulkFile(Requestable):
    OBJECT_NAME = 'bulk_file'

    @property
    def url(self) -> str:
        return self.get_property('url')

    @property
    def created_at(self) -> datetime:
        created_at = self.get_property('created_at')
        return datetime.fromisoformat(created_at)

    @property
    def expires_at(self) -> datetime:
        expires_at = self.get_property('expires_at')
        return datetime.fromisoformat(expires_at)

    @classmethod
    def create(cls, request_options: RequestOptions = None) -> BulkFile:
        path = '{}/files'.format(BulkMessageParams.CONTEXT_PATH)
        return cls.request('POST', path, request_options=request_options)
