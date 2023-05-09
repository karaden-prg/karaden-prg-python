from __future__ import absolute_import, division, annotations, unicode_literals

from copy import copy
from datetime import datetime
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.model.karaden_object import KaradenObject
from karaden.model.error import Error
from karaden.param.message_params import MessageParams


class MessageCreateParams(MessageParams):
    def __init__(self, service_id: int, to: str, body: str, tags: list = None, is_shorten: bool = None, scheduled_at: datetime = None, limited_at: datetime = None) -> None:
        self.service_id = service_id
        self.to = to
        self.body = body
        self.tags = tags
        self.is_shorten = is_shorten
        self.scheduled_at = scheduled_at
        self.limited_at = limited_at

    def to_data(self) -> dict:
        payload = {}
        payload['service_id'] = self.service_id
        payload['to'] = self.to
        payload['body'] = self.body
        if self.tags is not None:
            payload['tags[]'] = self.tags
        if self.is_shorten is not None:
            payload['is_shorten'] = 'true' if self.is_shorten else 'false'
        if self.scheduled_at is not None:
            payload['scheduled_at'] = self.scheduled_at.isoformat(timespec='seconds')
        if self.limited_at is not None:
            payload['limited_at'] = self.limited_at.isoformat(timespec='seconds')
        return payload

    def to_path(self) -> str:
        return MessageParams.CONTEXT_PATH

    def _validate_service_id(self):
        messages = []

        if self.service_id is None or self.service_id <= 0:
            messages.append('service_idは必須です。')
            messages.append('数字を入力してください。')

        return messages

    def _validate_to(self):
        messages = []

        if self.to is None or self.to == '':
            messages.append('toは必須です。')
            messages.append('文字列を入力してください。')

        return messages

    def _validate_body(self):
        messages = []

        if self.body is None or self.body == '':
            messages.append('bodyは必須です。')
            messages.append('文字列を入力してください。')

        return messages

    def validate(self):
        errors = KaradenObject()
        has_error = False

        messages = self._validate_service_id()
        if len(messages) > 0:
            errors.set_property('service_id', messages)
            has_error = True

        messages = self._validate_to()
        if len(messages) > 0:
            errors.set_property('to', messages)
            has_error = True

        messages = self._validate_body()
        if len(messages) > 0:
            errors.set_property('body', messages)
            has_error = True

        if has_error:
            error = Error()
            error.set_property('errors', errors)
            raise InvalidParamsException(error)

        return self

    @classmethod
    def new_builder(cls) -> MessageCreateParamsBuilder:
        return MessageCreateParamsBuilder()


class MessageCreateParamsBuilder:
    def __init__(self) -> None:
        self.params = MessageCreateParams(0, '', '', None, None)

    def with_service_id(self, service_id: int) -> MessageCreateParamsBuilder:
        self.params.service_id = service_id
        return self

    def with_to(self, to: str) -> MessageCreateParamsBuilder:
        self.params.to = to
        return self

    def with_body(self, body: str) -> MessageCreateParamsBuilder:
        self.params.body = body
        return self

    def with_tags(self, tags: list) -> MessageCreateParamsBuilder:
        self.params.tags = tags
        return self

    def with_is_shorten(self, is_shorten: bool) -> MessageCreateParamsBuilder:
        self.params.is_shorten = is_shorten
        return self

    def with_scheduled_at(self, scheduled_at: datetime) -> MessageCreateParamsBuilder:
        self.params.scheduled_at = scheduled_at
        return self

    def with_limited_at(self, limited_at: datetime) -> MessageCreateParamsBuilder:
        self.params.limited_at = limited_at
        return self

    def build(self) -> MessageCreateParams:
        return copy(self.params)
