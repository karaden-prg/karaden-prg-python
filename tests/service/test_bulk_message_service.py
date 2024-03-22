from __future__ import absolute_import, division, annotations, unicode_literals

import json
import os
import tempfile
import uuid
from collections import namedtuple

import pytest
from httpretty import HTTPretty, httprettified
from karaden.exception.bulk_message_create_failed_exception import BulkMessageCreateFailedException
from karaden.exception.bulk_message_list_message_retry_limit_exceed_exception import BulkMessageListMessageRetryLimitExceedException
from karaden.exception.bulk_message_show_retry_limit_exceed_exception import BulkMessageShowRetryLimitExceedException
from karaden.exception.file_download_failed_exception import FileDownloadFailedException
from karaden.exception.file_not_found_exception import FileNotFoundException

from karaden.param.bulk.bulk_message_download_params import BulkMessageDownloadParams
from karaden.param.bulk.bulk_message_list_message_params import BulkMessageListMessageParams
from karaden.param.bulk.bulk_message_show_params import BulkMessageShowParams
from karaden.service.bulk_message_service import BulkMessageService
from tests.test_helper import TestHelper


@pytest.fixture(scope="module")
def setUp():
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    signed_url = 'https://example.com'
    bulk_file_path = "/messages/bulks/files"
    bulk_file_url = "{}{}".format(request_options.base_uri, bulk_file_path)
    bulk_file_response = {
        "id": "741121d7-3f7e-ed85-9fac-28d87835528e",
        "object": "bulk_file",
        "url": signed_url,
        "created_at": "2023-12-01T15:00:00.0Z",
        "expires_at": "2023-12-01T15:00:00.0Z",
    }
    bulk_message_path = "/messages/bulks"
    bulk_message_url = "{}{}".format(request_options.base_uri, bulk_message_path)
    bulk_message_response = {
        "id": "ef931182-80ff-611c-c878-871a08bb5a6a",
        "object": "bulk_message",
        "status": "processing",
        "created_at": "2023-12-01T15:00:00.0Z",
        "updated_at": "2023-12-01T15:00:00.0Z",
    }

    dict = {
        "signed_url": signed_url,
        "bulk_file_url": bulk_file_url,
        "bulk_file_response": bulk_file_response,
        "bulk_message_url": bulk_message_url,
        "bulk_message_response": bulk_message_response,
    }

    return namedtuple('Class', dict.keys())(*dict.values())


@httprettified(allow_net_connect=False)
def test_bulkMessageオブジェクトが返る(setUp):
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )

    HTTPretty.register_uri(HTTPretty.PUT, setUp.signed_url)
    HTTPretty.register_uri(HTTPretty.POST, setUp.bulk_file_url, json.dumps(setUp.bulk_file_response))
    HTTPretty.register_uri(HTTPretty.POST, setUp.bulk_message_url, json.dumps(setUp.bulk_message_response))
    output = BulkMessageService.create(filename, request_options)

    assert 'bulk_message' == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_ファイルが存在しない場合はエラー(setUp):
    filename = "test.csv"

    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )

    HTTPretty.register_uri(HTTPretty.PUT, setUp.signed_url)
    HTTPretty.register_uri(HTTPretty.POST, setUp.bulk_file_url, json.dumps(setUp.bulk_file_response))
    HTTPretty.register_uri(HTTPretty.POST, setUp.bulk_message_url, json.dumps(setUp.bulk_message_response))

    with pytest.raises(FileNotFoundException):
        BulkMessageService.create(filename, request_options)


@httprettified(allow_net_connect=False)
def test_ファイルがダウンロードできる(tmpdir, monkeypatch):
    monkeypatch.setattr('time.sleep', lambda x: None)
    path = '/messages/bulks'
    show_params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    list_params = (
        BulkMessageListMessageParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    filename = 'file.csv'
    file_content = 'file content'
    bulk_message_response = {
        'id': 'ef931182-80ff-611c-c878-871a08bb5a6a',
        'object': 'bulk_message',
        'status': 'done',
        'created_at': '2023-12-01T15:00:00.0Z',
        'updated_at': '2023-12-01T15:00:00.0Z',
    }
    mock_show_url = '{}{}/{}'.format(request_options.base_uri, path, show_params.id)
    mock_list_url = '{}{}/{}/messages'.format(request_options.base_uri, path, list_params.id)
    mock_location_url = 'http://example.com/' + str(uuid.uuid1())

    HTTPretty.register_uri(HTTPretty.GET, mock_show_url, body=json.dumps(bulk_message_response))
    HTTPretty.register_uri(HTTPretty.GET, mock_list_url, status=302, location=mock_location_url)
    content_disposition = "attachment;filename=\"" + filename + "\";filename*=UTF-8''" + filename
    HTTPretty.register_uri(HTTPretty.GET, mock_location_url, body=file_content, status=200, content_disposition=content_disposition)
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id('id')
        .with_directory_path(tmpdir)
        .with_max_retries(1)
        .with_retry_interval(10)
        .build()
    )
    BulkMessageService.download(params, request_options)
    file_path = os.path.join(tmpdir, filename)
    with open(file_path, mode='r') as f:
        result = f.read()

    assert os.path.exists(file_path)
    assert result == file_content


@httprettified(allow_net_connect=False)
def test_bulk_messageのstatusがdone以外でリトライ回数を超過した場合はエラー(tmpdir, monkeypatch):
    monkeypatch.setattr('time.sleep', lambda x: None)
    path = '/messages/bulks'
    show_params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    bulk_message_response = {
        'id': 'ef931182-80ff-611c-c878-871a08bb5a6a',
        'object': 'bulk_message',
        'status': 'processing',
        'created_at': '2023-12-01T15:00:00.0Z',
        'updated_at': '2023-12-01T15:00:00.0Z',
    }
    mock_show_url = '{}{}/{}'.format(request_options.base_uri, path, show_params.id)

    HTTPretty.register_uri(HTTPretty.GET, mock_show_url, body=json.dumps(bulk_message_response))
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id('id')
        .with_directory_path(tmpdir)
        .with_max_retries(1)
        .with_retry_interval(10)
        .build()
    )
    with pytest.raises(BulkMessageShowRetryLimitExceedException):
        BulkMessageService.download(params, request_options)


@httprettified(allow_net_connect=False)
def test_結果取得APIが202を返しリトライ回数を超過した場合はエラー(tmpdir, monkeypatch):
    monkeypatch.setattr('time.sleep', lambda x: None)
    path = '/messages/bulks'
    show_params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    list_params = (
        BulkMessageListMessageParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    bulk_message_response = {
        'id': 'ef931182-80ff-611c-c878-871a08bb5a6a',
        'object': 'bulk_message',
        'status': 'done',
        'created_at': '2023-12-01T15:00:00.0Z',
        'updated_at': '2023-12-01T15:00:00.0Z',
    }
    mock_show_url = '{}{}/{}'.format(request_options.base_uri, path, show_params.id)
    mock_list_url = '{}{}/{}/messages'.format(request_options.base_uri, path, list_params.id)

    HTTPretty.register_uri(HTTPretty.GET, mock_show_url, body=json.dumps(bulk_message_response))
    HTTPretty.register_uri(HTTPretty.GET, mock_list_url, status=202)
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id('id')
        .with_directory_path(tmpdir)
        .with_max_retries(1)
        .with_retry_interval(10)
        .build()
    )
    with pytest.raises(BulkMessageListMessageRetryLimitExceedException):
        BulkMessageService.download(params, request_options)


@httprettified(allow_net_connect=False)
def test_bulk_messageのstatusがerrorはエラー(tmpdir, monkeypatch):
    monkeypatch.setattr('time.sleep', lambda x: None)
    path = '/messages/bulks'
    show_params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    bulk_message_response = {
        'id': 'ef931182-80ff-611c-c878-871a08bb5a6a',
        'object': 'bulk_message',
        'status': 'error',
        'created_at': '2023-12-01T15:00:00.0Z',
        'updated_at': '2023-12-01T15:00:00.0Z',
    }
    mock_show_url = '{}{}/{}'.format(request_options.base_uri, path, show_params.id)

    HTTPretty.register_uri(HTTPretty.GET, mock_show_url, body=json.dumps(bulk_message_response))
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id('id')
        .with_directory_path(tmpdir)
        .with_max_retries(1)
        .with_retry_interval(10)
        .build()
    )
    with pytest.raises(BulkMessageCreateFailedException):
        BulkMessageService.download(params, request_options)


@httprettified(allow_net_connect=False)
def test_ファイルダウンロード処理にエラーが発生した場合は例外が飛ぶ(tmpdir, monkeypatch):
    monkeypatch.setattr('time.sleep', lambda x: None)
    path = '/messages/bulks'
    show_params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    list_params = (
        BulkMessageListMessageParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    bulk_message_response = {
        'id': 'ef931182-80ff-611c-c878-871a08bb5a6a',
        'object': 'bulk_message',
        'status': 'done',
        'created_at': '2023-12-01T15:00:00.0Z',
        'updated_at': '2023-12-01T15:00:00.0Z',
    }
    mock_show_url = '{}{}/{}'.format(request_options.base_uri, path, show_params.id)
    mock_list_url = '{}{}/{}/messages'.format(request_options.base_uri, path, list_params.id)
    mock_location_url = ''

    HTTPretty.register_uri(HTTPretty.GET, mock_show_url, body=json.dumps(bulk_message_response))
    HTTPretty.register_uri(HTTPretty.GET, mock_list_url, status=302, location=mock_location_url)
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id('id')
        .with_directory_path(tmpdir)
        .with_max_retries(1)
        .with_retry_interval(10)
        .build()
    )
    with pytest.raises(FileDownloadFailedException):
        BulkMessageService.download(params, request_options)
