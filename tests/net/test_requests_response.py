from __future__ import absolute_import, division, annotations, unicode_literals

import json
import requests
import pytest
from karaden.request_options import RequestOptions
from karaden.exception.unexpected_value_exception import UnexpectedValueException
from karaden.exception.unknown_error_exception import UnknownErrorException
from karaden.net.requests_response import RequestsResponse
from karaden.model.karaden_object import KaradenObject


def test_正常系のステータスコードで本文がJSONであればオブジェクトが返る():
    tmp = requests.Response()
    tmp._content = json.dumps({'test': 'test'}).encode()
    tmp.status_code = 200
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error is False
    assert isinstance(response.object, KaradenObject)


@pytest.mark.parametrize(
    ('status_code'),
    [
        (200),
        (300),
        (400),
        (500),
    ]
)
def test_ステータスコードによらず本文がJSONでなければUnexpectedValueException(status_code: int):
    tmp = requests.Response()
    tmp._content = ''.encode()
    tmp.status_code = status_code
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error is True
    assert isinstance(response.error, UnexpectedValueException)
    assert status_code == response.error.status_code


def test_エラー系のステータスコードで本文にobjectのプロパティがなければerror以外はUnexpectedValueException():
    tmp = requests.Response()
    tmp._content = json.dumps({'test': 'test'}).encode()
    tmp.status_code = 400
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error
    assert isinstance(response.error, UnexpectedValueException)
    assert tmp.status_code == response.error.status_code


@pytest.mark.parametrize(
    ('item'),
    [
        ('message'),
        ('test'),
        (123),
        (''),
        (None),
    ]
)
def test_エラー系のステータスコードで本文にobjectのプロパティの値がerror以外はUnexpectedValueExceptio(item):
    tmp = requests.Response()
    tmp._content = json.dumps({'object': item}).encode()
    tmp.status_code = 400
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error
    assert isinstance(response.error, UnexpectedValueException)
    assert tmp.status_code == response.error.status_code


@pytest.mark.parametrize(
    ('status_code'),
    filter(lambda x: x not in RequestsResponse.errors, list(range(100, 200)) + list(range(400, 500)) + list(range(500, 600)))
)
def test_エラー系のステータスコードで特殊例外以外はUnknownErrorException(status_code):
    tmp = requests.Response()
    tmp._content = json.dumps({'object': 'error', 'test': 'test'}).encode()
    tmp.status_code = status_code
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error
    assert isinstance(response.error, UnknownErrorException)
    assert tmp.status_code == response.error.status_code


@pytest.mark.parametrize(
    ('cls'),
    RequestsResponse.errors.values()
)
def test_特殊例外のステータスコード(cls):
    tmp = requests.Response()
    tmp._content = json.dumps({'object': 'error', 'test': 'test'}).encode()
    tmp.status_code = cls.STATUS_CODE
    tmp.headers = {}
    tmp.encoding = 'utf-8'
    request_options = RequestOptions()

    response = RequestsResponse(tmp, request_options)
    assert response.is_error
    assert isinstance(response.error, cls)
