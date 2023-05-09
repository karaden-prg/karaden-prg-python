from __future__ import absolute_import, division, annotations, unicode_literals

import json
import pytest

from karaden.request_options import RequestOptions
from karaden.model.karaden_object import KaradenObject
from karaden.model.message import Message
from karaden.utility import Utility


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
