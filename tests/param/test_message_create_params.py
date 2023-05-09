from __future__ import absolute_import, division, annotations, unicode_literals

import json
import pytest
from datetime import datetime, timezone, timedelta
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.message_create_params import MessageCreateParams


def test_正しいパスを生成できる():
    params = MessageCreateParams(1, 'to', 'body')

    assert MessageCreateParams.CONTEXT_PATH == params.to_path()


def test_service_idを送信データにできる():
    expected = 1
    params = MessageCreateParams(expected, 'to', 'body')

    data = params.to_data()
    assert expected == data['service_id']


def test_toを送信データにできる():
    expected = 'to'
    params = MessageCreateParams(1, expected, 'body')

    data = params.to_data()
    assert expected == data['to']


def test_bodyを送信データにできる():
    expected = 'body'
    params = MessageCreateParams(1, 'to', expected)

    data = params.to_data()
    assert expected == data['body']


def test_tagsを送信データにできる():
    expected = ['tag']
    params = MessageCreateParams(1, 'to', 'body', expected)

    data = params.to_data()
    assert json.dumps(expected) == json.dumps(data['tags[]'])


def test_scheduled_atを送信データにできる():
    expected = datetime.now(timezone(timedelta(hours=9)))
    params = MessageCreateParams(1, 'to', 'body', scheduled_at=expected)

    data = params.to_data()
    assert expected.isoformat(timespec='seconds') == data['scheduled_at']


def test_limited_atを送信データにできる():
    expected = datetime.now(timezone(timedelta(hours=9)))
    params = MessageCreateParams(1, 'to', 'body', limited_at=expected)

    data = params.to_data()
    assert expected.isoformat(timespec='seconds') == data['limited_at']

def test_is_shortenがTrueの場合は送信データは文字列のtrueになる():
    param = True
    expected = 'true'
    params = MessageCreateParams(1, 'to', 'body', is_shorten=param)

    data = params.to_data()
    assert expected == data['is_shorten']

def test_is_shortenがFalseの場合は送信データは文字列のfalseになる():
    param = False
    expected = 'false'
    params = MessageCreateParams(1, 'to', 'body', is_shorten=param)

    data = params.to_data()
    assert expected == data['is_shorten']

def test_is_shortenが指定なしの場合は送信データにis_shortenはない():
    expected = None
    params = MessageCreateParams(1, 'to', 'body')

    data = params.to_data()
    assert 'is_shorten' not in data.keys();

def test_service_idを入力できる():
    expected = 'service_id'
    params = (
        MessageCreateParams
        .new_builder()
        .with_service_id(expected)
        .build()
    )

    assert expected == params.service_id


def test_toを入力できる():
    expected = 'to'
    params = (
        MessageCreateParams
        .new_builder()
        .with_to(expected)
        .build()
    )

    assert expected == params.to


def test_bodyを入力できる():
    expected = 'body'
    params = (
        MessageCreateParams
        .new_builder()
        .with_body(expected)
        .build()
    )

    assert expected == params.body


def test_tagsを入力できる():
    expected = ['tag']
    params = (
        MessageCreateParams
        .new_builder()
        .with_tags(expected)
        .build()
    )

    assert json.dumps(expected) == json.dumps(params.tags)


def test_scheduled_atを入力できる():
    expected = datetime.now()
    params = (
        MessageCreateParams
        .new_builder()
        .with_scheduled_at(expected)
        .build()
    )

    assert expected == params.scheduled_at


def test_limited_atを入力できる():
    expected = datetime.now()
    params = (
        MessageCreateParams
        .new_builder()
        .with_limited_at(expected)
        .build()
    )

    assert expected == params.limited_at


@pytest.mark.parametrize(
    ('service_id'),
    [
        (None),
        (0),
        (-1),
    ]
)
def test_service_idがNoneや0以下はエラー(service_id):
    params = (
        MessageCreateParams.new_builder()
        .with_service_id(service_id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('service_id')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('to'),
    [
        (None),
        (''),
    ]
)
def test_toがNoneや空文字はエラー(to):
    params = (
        MessageCreateParams.new_builder()
        .with_to(to)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('to')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('body'),
    [
        (None),
        (''),
    ]
)
def test_bodyがNoneや空文字はエラー(body):
    params = (
        MessageCreateParams.new_builder()
        .with_body(body)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('body')
    assert isinstance(messages, list)
