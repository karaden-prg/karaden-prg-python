from __future__ import absolute_import, division, annotations, unicode_literals

import os
import re
import requests
import time

from karaden.exception.bulk_message_create_failed_exception import BulkMessageCreateFailedException
from karaden.exception.file_download_failed_exception import FileDownloadFailedException
from karaden.exception.file_not_found_exception import FileNotFoundException
from karaden.exception.bulk_message_show_retry_limit_exceed_exception import BulkMessageShowRetryLimitExceedException
from karaden.exception.bulk_message_list_message_retry_limit_exceed_exception import BulkMessageListMessageRetryLimitExceedException
from karaden.model.bulk_file import BulkFile
from karaden.model.bulk_message import BulkMessage
from karaden.param.bulk.bulk_message_create_params import BulkMessageCreateParams
from karaden.param.bulk.bulk_message_download_params import BulkMessageDownloadParams
from karaden.param.bulk.bulk_message_list_message_params import BulkMessageListMessageParams
from karaden.param.bulk.bulk_message_show_params import BulkMessageShowParams
from karaden.request_options import RequestOptions
from karaden.utility import Utility


class BulkMessageService:
    BUFFER_SIZE = 1024 * 1024
    REGEX_PATTERN = "filename=\"([^\"]+)\""

    @classmethod
    def create(cls, filename: str, request_options: RequestOptions = None) -> BulkMessage:
        if not os.path.isfile(filename):
            raise FileNotFoundException()

        bulk_file = BulkFile.create(request_options)

        Utility.put_signed_url(bulk_file.url, filename, 'text/csv', request_options)

        params = (
            BulkMessageCreateParams
            .new_builder()
            .with_bulk_file_id(bulk_file.id)
            .build()
        )
        return BulkMessage.create(params, request_options)

    @classmethod
    def download(cls, params: BulkMessageDownloadParams, request_options: RequestOptions = None) -> BulkMessage | bool:
        params.validate()
        show_params = (
            BulkMessageShowParams
            .new_builder()
            .with_id(params.id)
            .build()
        )
        if not BulkMessageService.check_bulk_message_status(params.max_retries, params.retry_interval, show_params, request_options):
            raise BulkMessageShowRetryLimitExceedException()

        result_params = (
            BulkMessageListMessageParams
            .new_builder()
            .with_id(params.id)
            .build()
        )
        download_url = BulkMessageService.get_download_url(params.max_retries, params.retry_interval, result_params, request_options)
        if download_url is None:
            raise BulkMessageListMessageRetryLimitExceedException()

        try:
            BulkMessageService.get_contents(download_url, os.path.normpath(os.path.abspath(params.directory_path)), request_options)
        except:
            raise FileDownloadFailedException()

        return True

    @staticmethod
    def get_contents(download_url: str, directory_path: str, request_options: RequestOptions = None):
        timeout = Utility.get_timeout(request_options)
        with requests.get(download_url, stream=True, timeout=timeout) as r:
            match = re.search(BulkMessageService.REGEX_PATTERN,  r.headers['content-disposition'])
            if match is None:
                raise FileDownloadFailedException()
            filename = os.path.join(directory_path, (match.group(1)))
            with open(filename, 'wb') as f:
                for chunk in r.iter_content(BulkMessageService.BUFFER_SIZE):
                    f.write(chunk)

    @staticmethod
    def check_bulk_message_status(retry_count: int, retry_interval: int, params: BulkMessageShowParams, request_options: RequestOptions = None) -> bool:
        for count in range(retry_count + 1):
            if count > 0:
                time.sleep(retry_interval)

            bulk_message = BulkMessage.show(params, request_options)
            if bulk_message.status == BulkMessage.STATUS_ERROR:
                raise BulkMessageCreateFailedException()

            if bulk_message.status == BulkMessage.STATUS_DONE:
                return True

        return False

    @staticmethod
    def get_download_url(retry_count: int, retry_interval: int, params: BulkMessageListMessageParams, request_options: RequestOptions = None) -> str | None:
        for count in range(retry_count + 1):
            if count > 0:
                time.sleep(retry_interval)

            result = BulkMessage.list_message(params, request_options)
            if result is not None:
                return result

        return None
