from __future__ import absolute_import, division, annotations, unicode_literals

import json
import pytest

from typing import Tuple
from httpretty import HTTPretty, httprettified
from httpretty.core import HTTPrettyRequest
from karaden.model.bulk_message import BulkMessage
from karaden.model.error import Error
from karaden.param.bulk.bulk_message_create_params import BulkMessageCreateParams
from karaden.param.bulk.bulk_message_list_message_params import BulkMessageListMessageParams
from karaden.param.bulk.bulk_message_show_params import BulkMessageShowParams
from tests.test_helper import TestHelper


@httprettified(allow_net_connect=False)
def test_一括送信メッセージを作成できる():
    path = '/messages/bulks'
    params = (
        BulkMessageCreateParams.new_builder()
        .with_bulk_file_id('c439f89c-1ea3-7073-7021-1f127a850437')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)
    object = {'object': 'bulk_message'}

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert 'application/x-www-form-urlencoded' == request.headers.get_content_type()
        assert 'bulk_file_id=c439f89c-1ea3-7073-7021-1f127a850437' == request.body.decode('utf-8')

        return (200, {'Content-Type': 'application/json'}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.POST, mock_url, body=callback)

    output = BulkMessage.create(params, request_options)

    assert object['object'] == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_メッセージの詳細を取得できる():
    path = '/messages/bulks'
    params = (
        BulkMessageShowParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}/{}'.format(request_options.base_uri, path, params.id)
    object = {'object': 'message'}

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:

        return (200, {'Content-Type': 'application/json'}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    output = BulkMessage.show(params, request_options)

    assert object['object'] == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_メッセージの結果を取得できる():
    path = '/messages/bulks'
    params = (
        BulkMessageListMessageParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}/{}/messages'.format(request_options.base_uri, path, params.id)
    object = {'object': 'bulk_message'}
    expect_url = 'http://example.com'

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:

        return (302, {'location': expect_url}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    output = BulkMessage.list_message(params, request_options)

    assert output == expect_url

@pytest.mark.parametrize(
    ('location'),
    [
        ('location'),
        ('LOCATION'),
    ]
)
@httprettified(allow_net_connect=False)
def test_Locationが大文字小文字関係なく一括送信メッセージの結果を取得できる(location):
    path = '/messages/bulks'
    params = (
        BulkMessageListMessageParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}/{}/messages'.format(request_options.base_uri, path, params.id)
    object = {'object': 'bulk_message'}
    expect_url = 'http://example.com'

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:

        return (302, {location: expect_url}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    output = BulkMessage.list_message(params, request_options)

    assert output == expect_url


def test_statusを出力できる():
    expected = 'status'
    message = BulkMessage()
    message.set_property('status', expected)
    assert expected == message.status


def test_errorを出力できる():
    expected = Error()
    message = BulkMessage()
    message.set_property('error', expected)
    assert expected == message.error


def test_受付エラーがない場合はerrorは出力されない():
    expected = None
    message = BulkMessage()
    message.set_property('error', expected)
    assert expected == message.error


def test_created_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = BulkMessage()
    message.set_property('created_at', expected)
    assert expected == message.created_at.isoformat(timespec='seconds')


def test_updated_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = BulkMessage()
    message.set_property('updated_at', expected)
    assert expected == message.updated_at.isoformat(timespec='seconds')
