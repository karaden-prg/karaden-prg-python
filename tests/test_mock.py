from __future__ import absolute_import, division, annotations, unicode_literals

from datetime import datetime
from tests.test_helper import TestHelper
from karaden.param.message_create_params import MessageCreateParams
from karaden.param.message_detail_params import MessageDetailParams
from karaden.param.message_list_params import MessageListParams
from karaden.param.message_cancel_params import MessageCancelParams
from karaden.model.message import Message


def test_一覧():
    dt = datetime.fromisoformat('2020-01-31T23:59:59+09:00')
    params = (
        MessageListParams
        .new_builder()
        .with_service_id(1)
        .with_status('done')
        .with_start_at(dt)
        .with_end_at(dt)
        .with_page(0)
        .with_per_page(100)
        .with_tag('string')
        .with_result('done')
        .with_sent_result('none')
        .with_to('09012345678')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    messages = Message.list(params, request_options)

    assert 'list' == messages.object
    assert messages.has_more
    data = messages.data
    assert 1 == len(data)
    message = data[0]
    assert '82bdf9de-a532-4bf5-86bc-c9a1366e5f4a' == message.id
    assert 'message' == message.object
    assert 1 == message.service_id
    assert 1 == message.billing_address_id
    assert '09012345678' == message.to
    assert '本文' == message.body
    tags = message.tags
    assert isinstance(tags, list)
    assert 1 == len(tags)
    assert 'string' == tags[0]
    assert message.is_shorten
    assert message.is_shorten_clicked
    assert 'done' == message.result
    assert 'done' == message.status
    assert 'none' == message.sent_result
    assert 'docomo' == message.carrier
    assert dt == message.scheduled_at
    assert dt == message.limited_at
    assert dt == message.sent_at
    assert dt == message.received_at
    assert dt == message.charged_at
    assert dt == message.created_at
    assert dt == message.updated_at


def test_作成():
    dt = datetime.fromisoformat('2020-01-31T23:59:59+09:00')
    params = (
        MessageCreateParams
        .new_builder()
        .with_service_id(1)
        .with_to('09012345678')
        .with_body('本文')
        .with_is_shorten(True)
        .with_limited_at(dt)
        .with_scheduled_at(dt)
        .with_tags(['タグ１', 'タグ２', 'タグ３'])
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    message = Message.create(params, request_options)

    assert '82bdf9de-a532-4bf5-86bc-c9a1366e5f4a' == message.id
    assert 'message' == message.object
    assert 1 == message.service_id
    assert 1 == message.billing_address_id
    assert '09012345678' == message.to
    assert '本文' == message.body
    tags = message.tags
    assert isinstance(tags, list)
    assert 1 == len(tags)
    assert 'string' == tags[0]
    assert message.is_shorten
    assert message.is_shorten_clicked
    assert 'done' == message.result
    assert 'done' == message.status
    assert 'none' == message.sent_result
    assert 'docomo' == message.carrier
    assert dt == message.scheduled_at
    assert dt == message.limited_at
    assert dt == message.sent_at
    assert dt == message.received_at
    assert dt == message.charged_at
    assert dt == message.created_at
    assert dt == message.updated_at


def test_詳細():
    dt = datetime.fromisoformat('2020-01-31T23:59:59+09:00')
    params = (
        MessageDetailParams
        .new_builder()
        .with_id('82bdf9de-a532-4bf5-86bc-c9a1366e5f4a')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    message = Message.detail(params, request_options)

    assert '82bdf9de-a532-4bf5-86bc-c9a1366e5f4a' == message.id
    assert 'message' == message.object
    assert 1 == message.service_id
    assert 1 == message.billing_address_id
    assert '09012345678' == message.to
    assert '本文' == message.body
    tags = message.tags
    assert isinstance(tags, list)
    assert 1 == len(tags)
    assert 'string' == tags[0]
    assert message.is_shorten
    assert message.is_shorten_clicked
    assert 'done' == message.result
    assert 'done' == message.status
    assert 'none' == message.sent_result
    assert 'docomo' == message.carrier
    assert dt == message.scheduled_at
    assert dt == message.limited_at
    assert dt == message.sent_at
    assert dt == message.received_at
    assert dt == message.charged_at
    assert dt == message.created_at
    assert dt == message.updated_at


def test_キャンセル():
    dt = datetime.fromisoformat('2020-01-31T23:59:59+09:00')
    params = (
        MessageCancelParams
        .new_builder()
        .with_id('82bdf9de-a532-4bf5-86bc-c9a1366e5f4a')
        .build()
    )
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    message = Message.cancel(params, request_options)

    assert '82bdf9de-a532-4bf5-86bc-c9a1366e5f4a' == message.id
    assert 'message' == message.object
    assert 1 == message.service_id
    assert 1 == message.billing_address_id
    assert '09012345678' == message.to
    assert '本文' == message.body
    tags = message.tags
    assert isinstance(tags, list)
    assert 1 == len(tags)
    assert 'string' == tags[0]
    assert message.is_shorten
    assert message.is_shorten_clicked
    assert 'done' == message.result
    assert 'done' == message.status
    assert 'none' == message.sent_result
    assert 'docomo' == message.carrier
    assert dt == message.scheduled_at
    assert dt == message.limited_at
    assert dt == message.sent_at
    assert dt == message.received_at
    assert dt == message.charged_at
    assert dt == message.created_at
    assert dt == message.updated_at
