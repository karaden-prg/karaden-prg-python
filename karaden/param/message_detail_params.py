from __future__ import absolute_import, division, annotations, unicode_literals

from copy import copy
from karaden.param.message_params import MessageParams
from karaden.model.karaden_object import KaradenObject
from karaden.model.error import Error
from karaden.exception.invalid_params_exception import InvalidParamsException


class MessageDetailParams(MessageParams):
    def __init__(self, id: str) -> None:
        self.id = id

    def to_path(self) -> str:
        return '{}/{}'.format(MessageParams.CONTEXT_PATH, self.id)

    def _validate_id(self):
        messages = []

        if self.id is None or self.id == '':
            messages.append('idは必須です。')
            messages.append('文字列（UUID）を入力してください。')

        return messages

    def validate(self):
        errors = KaradenObject()
        has_error = False

        messages = self._validate_id()
        if len(messages) > 0:
            errors.set_property('id', messages)
            has_error = True

        if has_error:
            error = Error()
            error.set_property('errors', errors)
            raise InvalidParamsException(error)

        return self

    @classmethod
    def new_builder(cls) -> MessageDetailParamsBuilder:
        return MessageDetailParamsBuilder()


class MessageDetailParamsBuilder:
    def __init__(self) -> None:
        self.params = MessageDetailParams('')

    def with_id(self, id: str) -> MessageDetailParamsBuilder:
        self.params.id = id
        return self

    def build(self) -> MessageDetailParams:
        return copy(self.params)
