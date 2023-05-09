from __future__ import absolute_import, division, annotations, unicode_literals

import pytest

from karaden.model.karaden_object import KaradenObject


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
def test_プロパティに入出力できる(value):
    key = 'test'
    obj = KaradenObject()
    obj.set_property(key, value)
    assert value == obj.get_property(key)


def test_プロパティのキーを列挙できる():
    expected = ['test1', 'test2']
    obj = KaradenObject()
    for value in expected:
        obj.set_property(value, value)

    keys = obj.get_property_keys()
    assert isinstance(keys, list)
    for value in expected:
        assert value in keys


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
def test_idを入出力できる(value):
    obj = KaradenObject()
    obj.set_property('id', value)
    assert value == obj.id


def test_objectを入出力できる():
    expected = 'test'
    obj = KaradenObject()
    obj.set_property('object', expected)
    assert expected == obj.object
