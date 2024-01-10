from __future__ import absolute_import, division, annotations, unicode_literals

from datetime import datetime
from karaden.request_options import RequestOptions
from karaden.model.requestable import Requestable
from karaden.model.collection import Collection
from karaden.param.message_create_params import MessageCreateParams
from karaden.param.message_detail_params import MessageDetailParams
from karaden.param.message_list_params import MessageListParams
from karaden.param.message_cancel_params import MessageCancelParams


class Message(Requestable):
    OBJECT_NAME = 'message'

    @property
    def service_id(self) -> str:
        return self.get_property('service_id')

    @property
    def billing_address_id(self) -> str:
        return self.get_property('billing_address_id')

    @property
    def to(self) -> str:
        return self.get_property('to')

    @property
    def body(self) -> str:
        return self.get_property('body')

    @property
    def tags(self) -> list:
        return self.get_property('tags')

    @property
    def is_shorten(self) -> bool:
        return self.get_property('is_shorten')
    
    @property
    def is_shorten_clicked(self) -> bool | None:
        return self.get_property('is_shorten_clicked')

    @property
    def status(self) -> list:
        return self.get_property('status')

    @property
    def result(self) -> list:
        return self.get_property('result')

    @property
    def sent_result(self) -> list:
        return self.get_property('sent_result')

    @property
    def carrier(self) -> list:
        return self.get_property('carrier')

    @property
    def scheduled_at(self) -> datetime:
        scheduled_at = self.get_property('scheduled_at')
        return datetime.fromisoformat(scheduled_at)

    @property
    def limited_at(self) -> datetime:
        limited_at = self.get_property('limited_at')
        return datetime.fromisoformat(limited_at)

    @property
    def sent_at(self) -> datetime:
        sent_at = self.get_property('sent_at')
        return datetime.fromisoformat(sent_at)

    @property
    def received_at(self) -> datetime:
        received_at = self.get_property('received_at')
        return datetime.fromisoformat(received_at)

    @property
    def charged_at(self) -> datetime:
        charged_at = self.get_property('charged_at')
        return datetime.fromisoformat(charged_at)

    @property
    def created_at(self) -> datetime:
        created_at = self.get_property('created_at')
        return datetime.fromisoformat(created_at)

    @property
    def updated_at(self) -> datetime:
        updated_at = self.get_property('updated_at')
        return datetime.fromisoformat(updated_at)

    @classmethod
    def create(cls, params: MessageCreateParams, request_options: RequestOptions = None) -> Message:
        params.validate()
        return cls.request('POST', params.to_path(), data=params.to_data(), request_options=request_options)

    @classmethod
    def detail(cls, params: MessageDetailParams, request_options: RequestOptions = None) -> Message:
        params.validate()
        return cls.request('GET', params.to_path(), request_options=request_options)

    @classmethod
    def list(cls, params: MessageListParams, request_options: RequestOptions = None) -> Collection:
        params.validate()
        return cls.request('GET', params.to_path(), params.to_params(), request_options=request_options)

    @classmethod
    def cancel(cls, params: MessageCancelParams, request_options: RequestOptions = None) -> Message:
        params.validate()
        return cls.request('POST', params.to_path(), request_options=request_options)
