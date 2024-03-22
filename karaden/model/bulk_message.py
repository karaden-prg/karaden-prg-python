from __future__ import absolute_import, division, annotations, unicode_literals

from datetime import datetime
from http import HTTPStatus
from karaden.request_options import RequestOptions
from karaden.model.error import Error
from karaden.model.requestable import Requestable
from karaden.param.bulk.bulk_message_create_params import BulkMessageCreateParams
from karaden.param.bulk.bulk_message_show_params import BulkMessageShowParams
from karaden.param.bulk.bulk_message_list_message_params import BulkMessageListMessageParams


class BulkMessage(Requestable):
    OBJECT_NAME = 'bulk_message'
    STATUS_DONE = 'done'
    STATUS_WAITING = 'waiting'
    STATUS_PROCESSING = 'processing'
    STATUS_ERROR = 'error'

    @property
    def status(self) -> str:
        return self.get_property('status')

    @property
    def error(self)  -> Error | None:
        return self.get_property('error')

    @property
    def created_at(self) -> datetime:
        created_at = self.get_property('created_at')
        return datetime.fromisoformat(created_at)

    @property
    def updated_at(self) -> datetime:
        updated_at = self.get_property('updated_at')
        return datetime.fromisoformat(updated_at)

    @classmethod
    def create(cls, params: BulkMessageCreateParams, request_options: RequestOptions = None) -> BulkMessage:
        params.validate()
        return cls.request('POST', params.to_path(), data=params.to_data(), request_options=request_options)

    @classmethod
    def show(cls, params: BulkMessageShowParams, request_options: RequestOptions = None) -> BulkMessage:
        params.validate()
        return cls.request('GET', params.to_path(), request_options=request_options)

    @classmethod
    def list_message(cls, params: BulkMessageListMessageParams, request_options: RequestOptions = None) -> str | None:
        params.validate()
        response =  cls.request_and_return_response_interface('GET', params.to_path(), request_options=request_options)
        return response.headers['Location'] if response.status_code == HTTPStatus.FOUND else None
