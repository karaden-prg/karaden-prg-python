from __future__ import absolute_import, division, annotations, unicode_literals

from copy import copy
from datetime import datetime
from karaden.param.message_params import MessageParams


class MessageListParams(MessageParams):
    def __init__(self, service_id: int = None, to: str = None, status: str = None, result: str = None, sent_result: str = None, tag: str = None, start_at: datetime = None, end_at: datetime = None, page: int = None, per_page: int = None) -> None:
        self.service_id = service_id
        self.to = to
        self.status = status
        self.result = result
        self.sent_result = sent_result
        self.tag = tag
        self.start_at = start_at
        self.end_at = end_at
        self.page = page
        self.per_page = per_page

    def to_params(self) -> dict:
        payload = {}
        if self.service_id is not None:
            payload['service_id'] = self.service_id
        if self.to is not None:
            payload['to'] = self.to
        if self.status is not None:
            payload['status'] = self.status
        if self.result is not None:
            payload['result'] = self.result
        if self.sent_result is not None:
            payload['sent_result'] = self.sent_result
        if self.tag is not None:
            payload['tag'] = self.tag
        if self.start_at is not None:
            payload['start_at'] = self.start_at
        if self.end_at is not None:
            payload['end_at'] = self.end_at
        if self.page is not None:
            payload['page'] = self.page
        if self.per_page is not None:
            payload['per_page'] = self.per_page
        return payload

    def to_path(self) -> str:
        return MessageParams.CONTEXT_PATH

    @classmethod
    def new_builder(cls) -> MessageListParamsBuilder:
        return MessageListParamsBuilder()


class MessageListParamsBuilder:
    def __init__(self) -> None:
        self.params = MessageListParams()

    def with_service_id(self, service_id: int) -> MessageListParamsBuilder:
        self.params.service_id = service_id
        return self

    def with_to(self, to: str) -> MessageListParamsBuilder:
        self.params.to = to
        return self

    def with_status(self, status: str) -> MessageListParamsBuilder:
        self.params.status = status
        return self

    def with_result(self, result: str) -> MessageListParamsBuilder:
        self.params.result = result
        return self

    def with_sent_result(self, sent_result: str) -> MessageListParamsBuilder:
        self.params.sent_result = sent_result
        return self

    def with_tag(self, tag: str) -> MessageListParamsBuilder:
        self.params.tag = tag
        return self

    def with_start_at(self, start_at: datetime) -> MessageListParamsBuilder:
        self.params.start_at = start_at
        return self

    def with_end_at(self, end_at: datetime) -> MessageListParamsBuilder:
        self.params.end_at = end_at
        return self

    def with_page(self, page: int) -> MessageListParamsBuilder:
        self.params.page = page
        return self

    def with_per_page(self, per_page: int) -> MessageListParamsBuilder:
        self.params.per_page = per_page
        return self

    def build(self) -> MessageListParams:
        return copy(self.params)
