from __future__ import absolute_import, division, annotations, unicode_literals

import json
import tempfile
import pytest

from karaden.exception.file_upload_failed_exception import FileUploadFailedException
from karaden.request_options import RequestOptions
from karaden.model.karaden_object import KaradenObject
from karaden.model.message import Message
from karaden.utility import Utility
from httpretty import HTTPretty, httprettified
from httpretty.core import HTTPrettyRequest


def test_objectのフィールドが存在しない場合はKaradenObjectが返る():
    contents = json.loads('{"test": "test"}')
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)


def test_objectのフィールドが存在してObjectTypesのマッピングが存在する場合はオブジェクトが返る():
    contents = json.loads('{"object": "message"}')
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, Message)


def objectのフィールドが存在してObjectTypesのマッピングに存在しない場合はKaradenObjectが返る():
    contents = json.loads('{"object": "test"}')
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)


@pytest.mark.parametrize(
    ('value'),
    [
        ('string'),
        (''),
        (123),
        (0),
        (True),
        (False),
        (None),
    ]
)
def test_プリミティブな値はデシリアライズしても変わらない(value):
    contents = json.loads(json.dumps({"test": value}))
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)
    assert obj.get_property("test") == value


@pytest.mark.parametrize(
    ('value'),
    [
        ('string'),
        (''),
        (123),
        (0),
        (True),
        (False),
        (None),
    ]
)
def test_プリミティブな値の配列の要素はデシリアライズしても変わらない(value):
    contents = json.loads(json.dumps({'test': [value]}))
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)
    assert isinstance(obj.get_property('test'), list)
    assert value == obj.get_property('test')[0]


def test_配列の配列もサポートする():
    value = "test"
    contents = json.loads(json.dumps({'test': [[value]]}))
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)
    assert isinstance(obj.get_property('test'), list)
    assert 1 == len(obj.get_property('test'))
    assert isinstance(obj.get_property('test')[0], list)
    assert 1 == len(obj.get_property('test')[0])
    assert value == obj.get_property('test')[0][0]


def test_配列のオブジェクトもサポートする():
    value = "test"
    contents = json.loads(json.dumps({'test': [{'test': value}]}))
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)
    assert isinstance(obj.get_property('test'), list)
    assert 1 == len(obj.get_property('test'))
    assert isinstance(obj.get_property('test')[0], KaradenObject)
    assert value == obj.get_property('test')[0].get_property('test')


@pytest.mark.parametrize(
    ('item', 'cls'),
    [
        ({}, KaradenObject),
        ({'object': None}, KaradenObject),
        ({'object': 'test'}, KaradenObject),
        ({'object': 'message'}, Message),
    ]
)
def test_オブジェクトの配列の要素はデシリアライズするとKaradenObjectに変換される(item, cls):
    item['test'] = 'test'
    contents = json.loads(json.dumps({'test': [item]}))
    request_options = RequestOptions()

    obj = Utility.convert_to_karaden_object(contents, request_options)

    assert isinstance(obj, KaradenObject)
    assert isinstance(obj.get_property('test'), list)
    assert isinstance(obj.get_property('test')[0], cls)
    assert item['test'] == obj.get_property('test')[0].get_property('test')


@httprettified(allow_net_connect=False)
def test_指定のURLにfileパスのファイルをPUTメソッドでリクエストする():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    signed_url = 'https://example.com/'

    def callback(
        request: HTTPrettyRequest,
        url: str,
        headers: dict):
        assert 'PUT' == request.method
        assert signed_url == request.url
        assert 'application/octet-stream' == request.headers.get_content_type()

        return (200, '', '')

    HTTPretty.register_uri(HTTPretty.PUT, signed_url, body=callback)

    Utility.put_signed_url(signed_url, filename)


@httprettified(allow_net_connect=False)
def test_レスポンスコードが200以外だとFileUploadFailedExceptionが発生する():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    signed_url = 'https://example.com/'

    def callback(
        request: HTTPrettyRequest,
        url: str,
        headers: dict):
        assert 'PUT' == request.method
        assert signed_url == request.url

        return (403, '', '')

    HTTPretty.register_uri(HTTPretty.PUT, signed_url, body=callback)

    with pytest.raises(FileUploadFailedException):
        Utility.put_signed_url(signed_url, filename)


@httprettified(allow_net_connect=False)
def test_例外が発生するとFileUploadFailedExceptionをリスローする():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    signed_url = 'https://example.com/'

    def callback(
        request: HTTPrettyRequest,
        url: str,
        headers: dict):
        raise Exception()

    HTTPretty.register_uri(HTTPretty.PUT, signed_url, body=callback)

    with pytest.raises(FileUploadFailedException):
        Utility.put_signed_url(signed_url, filename)


@httprettified(allow_net_connect=False)
def test_ContentTypeを指定できる():
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        filename = temp_file.name

    signed_url = 'https://example.com/'
    content_type = 'text/csv'

    def callback(
        request: HTTPrettyRequest,
        url: str,
        headers: dict):
        assert 'PUT' == request.method
        assert signed_url == request.url
        assert content_type == request.headers.get_content_type()

        return (200, '', '')

    HTTPretty.register_uri(HTTPretty.PUT, signed_url, body=callback)

    Utility.put_signed_url(signed_url, filename, content_type)
    