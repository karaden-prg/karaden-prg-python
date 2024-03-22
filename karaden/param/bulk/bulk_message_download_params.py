from __future__ import absolute_import, division, annotations, unicode_literals

import os
from copy import copy

from karaden.param.bulk.bulk_message_params import BulkMessageParams
from karaden.model.karaden_object import KaradenObject
from karaden.model.error import Error
from karaden.exception.invalid_params_exception import InvalidParamsException


class BulkMessageDownloadParams(BulkMessageParams):
    DEFAULT_MAX_RETRIES = 2
    MAX_MAX_RETRIES = 5
    MIN_MAX_RETRIES = 1
    DEFAULT_RETRY_INTERVAL = 20
    MAX_RETRY_INTERVAL = 60
    MIN_RETRY_INTERVAL = 10

    def __init__(self, id: str, directory_path: str, max_retries: int = DEFAULT_MAX_RETRIES, retry_interval: int = DEFAULT_RETRY_INTERVAL) -> None:
        self.id = id
        self.directory_path = directory_path
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def _validate_id(self):
        messages = []

        if self.id is None or self.id == '':
            messages.append('idは必須です')
            messages.append('文字列（UUID）を入力してください。')

        return messages

    def _validate_directory_path(self):
        messages = []

        if self.directory_path is None or self.directory_path == '':
            messages.append('directory_pathは必須です')
            messages.append('文字列を入力してください。')

        if not os.path.exists(self.directory_path):
            messages.append('指定されたディレクトリパスが存在しません。')

        if not os.path.isdir(self.directory_path):
            messages.append('指定されたパスはディレクトリではありません。')

        if not os.access(self.directory_path, os.R_OK):
            messages.append('指定されたディレクトリには読み取り権限がありません。')

        if not os.access(self.directory_path, os.W_OK):
            messages.append('指定されたディレクトリには書き込み権限がありません。')

        return messages

    def _validate_max_retries(self):
        messages = []

        if self.max_retries is None or not isinstance(self.max_retries, int) or self.max_retries < self.MIN_MAX_RETRIES:
            messages.append(f'max_retriesには{self.MIN_MAX_RETRIES}以上の整数を入力してください。')

        if self.max_retries is None or not isinstance(self.max_retries, int) or self.max_retries > self.MAX_MAX_RETRIES:
            messages.append(f'max_retriesには{self.MAX_MAX_RETRIES}以下の整数を入力してください。')


        return messages

    def _validate_retry_interval(self):
        messages = []

        if self.retry_interval is None or not isinstance(self.retry_interval, int) or self.retry_interval < self.MIN_RETRY_INTERVAL:
            messages.append(f'retry_intervalには{self.MIN_RETRY_INTERVAL}以上の整数を入力してください。')

        if self.retry_interval is None or not isinstance(self.retry_interval, int) or self.retry_interval > self.MAX_RETRY_INTERVAL:
            messages.append(f'retry_intervalには{self.MAX_RETRY_INTERVAL}以下の整数を入力してください。')

        return messages

    def validate(self):
        errors = KaradenObject()
        has_error = False

        messages = self._validate_id()
        if len(messages) > 0:
            errors.set_property('id', messages)
            has_error = True

        messages = self._validate_directory_path()
        if len(messages) > 0:
            errors.set_property('directory_path', messages)
            has_error = True

        messages = self._validate_max_retries()
        if len(messages) > 0:
            errors.set_property('max_retries', messages)
            has_error = True

        messages = self._validate_retry_interval()
        if len(messages) > 0:
            errors.set_property('retry_interval', messages)
            has_error = True

        if has_error:
            error = Error()
            error.set_property('errors', errors)
            raise InvalidParamsException(error)

        return self

    @classmethod
    def new_builder(cls) -> BulkMessageDownloadParams:
        return BulkMessageDownloadParamsBuilder()


class BulkMessageDownloadParamsBuilder:
    def __init__(self) -> None:
        self.params = BulkMessageDownloadParams('', '')

    def with_id(self, id: str) -> BulkMessageDownloadParams:
        self.params.id = id
        return self

    def with_directory_path(self, directory_path: str) -> BulkMessageDownloadParams:
        self.params.directory_path = directory_path
        return self

    def with_max_retries(self, max_retries: int) -> BulkMessageDownloadParams:
        self.params.max_retries = max_retries
        return self

    def with_retry_interval(self, retry_interval: int) -> BulkMessageDownloadParams:
        self.params.retry_interval = retry_interval
        return self

    def build(self) -> BulkMessageDownloadParams:
        return copy(self.params)
