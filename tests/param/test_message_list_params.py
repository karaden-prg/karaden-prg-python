from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.param.message_list_params import MessageListParams
from datetime import datetime


def test_正しいパスを生成できる():
    params = MessageListParams()

    assert MessageListParams.CONTEXT_PATH == params.to_path()


def test_service_idを送信データにできる():
    expected = 1
    params = MessageListParams(service_id=expected)

    data = params.to_params()
    assert expected == data['service_id']


def test_toを送信データにできる():
    expected = 'to'
    params = MessageListParams(to=expected)

    data = params.to_params()
    assert expected == data['to']


def test_statusを送信データにできる():
    expected = 'status'
    params = MessageListParams(status=expected)

    data = params.to_params()
    assert expected == data['status']


def test_resultを送信データにできる():
    expected = 'result'
    params = MessageListParams(result=expected)

    data = params.to_params()
    assert expected == data['result']


def test_sent_resultを送信データにできる():
    expected = 'sent_result'
    params = MessageListParams(sent_result=expected)

    data = params.to_params()
    assert expected == data['sent_result']


def test_tagを送信データにできる():
    expected = 'tag'
    params = MessageListParams(tag=expected)

    data = params.to_params()
    assert expected == data['tag']


def test_start_atを送信データにできる():
    expected = datetime.now()
    params = MessageListParams(start_at=expected)

    data = params.to_params()
    assert expected == data['start_at']


def test_end_atを送信データにできる():
    expected = datetime.now()
    params = MessageListParams(end_at=expected)

    data = params.to_params()
    assert expected == data['end_at']

def test_pageを送信データにできる():
    expected = 1
    params = MessageListParams(page=expected)

    data = params.to_params()
    assert expected == data['page']

def test_per_pageを送信データにできる():
    expected = 1
    params = MessageListParams(per_page=expected)

    data = params.to_params()
    assert expected == data['per_page']

def test_service_idを入力できる():
    expected = 1
    params = (
        MessageListParams
        .new_builder()
        .with_service_id(expected)
        .build()
    )

    assert expected == params.service_id


def test_toを入力できる():
    expected = 'to'
    params = (
        MessageListParams
        .new_builder()
        .with_to(expected)
        .build()
    )

    assert expected == params.to


def test_statusを入力できる():
    expected = 'status'
    params = (
        MessageListParams
        .new_builder()
        .with_status(expected)
        .build()
    )

    assert expected == params.status


def test_resultを入力できる():
    expected = 'result'
    params = (
        MessageListParams
        .new_builder()
        .with_result(expected)
        .build()
    )

    assert expected == params.result


def test_sent_resultを入力できる():
    expected = 'sent_result'
    params = (
        MessageListParams
        .new_builder()
        .with_sent_result(expected)
        .build()
    )

    assert expected == params.sent_result


def test_tagを入力できる():
    expected = 'tag'
    params = (
        MessageListParams
        .new_builder()
        .with_tag(expected)
        .build()
    )

    assert expected == params.tag


def test_start_atを入力できる():
    expected = datetime.now()
    params = (
        MessageListParams
        .new_builder()
        .with_start_at(expected)
        .build()
    )

    assert expected == params.start_at


def test_end_atを入力できる():
    expected = datetime.now()
    params = (
        MessageListParams
        .new_builder()
        .with_end_at(expected)
        .build()
    )

    assert expected == params.end_at

def test_pageを入力できる():
    expected = 1
    params = (
        MessageListParams
        .new_builder()
        .with_page(expected)
        .build()
    )

    assert expected == params.page

def test_per_pageを入力できる():
    expected = 1
    params = (
        MessageListParams
        .new_builder()
        .with_per_page(expected)
        .build()
    )

    assert expected == params.per_page