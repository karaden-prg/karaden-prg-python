from __future__ import absolute_import, division, annotations, unicode_literals

from copy import copy

from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.model.error import Error
from karaden.model.karaden_object import KaradenObject
from karaden.param.bulk.bulk_message_params import BulkMessageParams


class BulkMessageCreateParams(BulkMessageParams):
    def __init__(self, bulk_file_id: str) -> None:
        self.bulk_file_id = bulk_file_id

    def to_data(self) -> dict:
        payload = {}
        payload["bulk_file_id"] = self.bulk_file_id
        return payload

    def to_path(self) -> str:
        return BulkMessageParams.CONTEXT_PATH

    def _validate_bulk_file_id(self):
        messages = []

        if self.bulk_file_id is None or self.bulk_file_id == "":
            messages.append("bulk_file_idは必須です。")
            messages.append("文字列（UUID）を入力してください。")

        return messages

    def validate(self):
        errors = KaradenObject()
        has_error = False

        messages = self._validate_bulk_file_id()
        if len(messages) > 0:
            errors.set_property("bulk_file_id", messages)
            has_error = True

        if has_error:
            error = Error()
            error.set_property("errors", errors)
            raise InvalidParamsException(error)

        return self

    @classmethod
    def new_builder(cls) -> BulkMessageCreateParamsBuilder:
        return BulkMessageCreateParamsBuilder()


class BulkMessageCreateParamsBuilder:
    def __init__(self) -> None:
        self.params = BulkMessageCreateParams("")

    def with_bulk_file_id(self, bulk_file_id: str) -> BulkMessageCreateParamsBuilder:
        self.params.bulk_file_id = bulk_file_id
        return self

    def build(self) -> BulkMessageCreateParams:
        return copy(self.params)
