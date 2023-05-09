from __future__ import absolute_import, division, annotations, unicode_literals

import json

from typing import Tuple
from tests.test_helper import TestHelper
from karaden.model.message import Message
from karaden.param.message_create_params import MessageCreateParams
from karaden.param.message_detail_params import MessageDetailParams
from karaden.param.message_list_params import MessageListParams
from karaden.param.message_cancel_params import MessageCancelParams
from httpretty import HTTPretty, httprettified
from httpretty.core import HTTPrettyRequest


@httprettified(allow_net_connect=False)
def test_メッセージを作成できる():
    path = '/messages'
    params = (
        MessageCreateParams.new_builder()
        .with_service_id(1)
        .with_to('to')
        .with_body('body')
        .with_tags(['a', 'b'])
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)
    object = {'object': 'message'}

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert 'application/x-www-form-urlencoded' == request.headers.get_content_type()
        assert 'service_id=1&to=to&body=body&tags%5B%5D=a&tags%5B%5D=b' == request.body.decode('utf-8')

        return (200, headers, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.POST, mock_url, body=callback)

    output = Message.create(params, request_options)

    assert object['object'] == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_メッセージの詳細を取得できる():
    path = '/messages'
    params = (
        MessageDetailParams.new_builder()
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

    output = Message.detail(params, request_options)

    assert object['object'] == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_メッセージの一覧を取得できる():
    path = '/messages'
    params = (
        MessageListParams.new_builder()
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)
    object = {'object': 'list'}

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:

        return (200, {'Content-Type': 'application/json'}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    output = Message.list(params, request_options)

    assert object['object'] == output.get_property('object')


@httprettified(allow_net_connect=False)
def test_メッセージの送信をキャンセルできる():
    path = '/messages'
    params = (
        MessageCancelParams.new_builder()
        .with_id('id')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}/{}/cancel'.format(request_options.base_uri, path, params.id)
    object = {'object': 'message'}

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:

        return (200, {'Content-Type': 'application/json'}, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.POST, mock_url, body=callback)

    output = Message.cancel(params, request_options)

    assert object['object'] == output.get_property('object')


def test_service_idを出力できる():
    expected = 1
    message = Message()
    message.set_property('service_id', expected)
    assert expected == message.service_id


def test_billing_address_idを出力できる():
    expected = 1
    message = Message()
    message.set_property('service_id', expected)
    assert expected == message.service_id


def test_toを出力できる():
    expected = '1234567890'
    message = Message()
    message.set_property('to', expected)
    assert expected == message.to


def test_bodyを出力できる():
    expected = 'body'
    message = Message()
    message.set_property('body', expected)
    assert expected == message.body


def test_tagsを出力できる():
    expected = ['tag']
    message = Message()
    message.set_property('tags', expected)
    assert expected == message.tags


def test_statusを出力できる():
    expected = 'status'
    message = Message()
    message.set_property('status', expected)
    assert expected == message.status


def test_resultを出力できる():
    expected = 'result'
    message = Message()
    message.set_property('result', expected)
    assert expected == message.result


def test_sent_resultを出力できる():
    expected = 'sent_result'
    message = Message()
    message.set_property('sent_result', expected)
    assert expected == message.sent_result


def test_carrierを出力できる():
    expected = 'carrier'
    message = Message()
    message.set_property('carrier', expected)
    assert expected == message.carrier


def test_scheduled_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('scheduled_at', expected)
    assert expected == message.scheduled_at.isoformat(timespec='seconds')


def test_limited_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('limited_at', expected)
    assert expected == message.limited_at.isoformat(timespec='seconds')


def test_sent_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('sent_at', expected)
    assert expected == message.sent_at.isoformat(timespec='seconds')


def test_received_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('received_at', expected)
    assert expected == message.received_at.isoformat(timespec='seconds')


def test_charged_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('charged_at', expected)
    assert expected == message.charged_at.isoformat(timespec='seconds')


def test_created_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('created_at', expected)
    assert expected == message.created_at.isoformat(timespec='seconds')


def test_updated_atを出力できる():
    expected = '2022-12-09T00:00:00+09:00'
    message = Message()
    message.set_property('updated_at', expected)
    assert expected == message.updated_at.isoformat(timespec='seconds')
