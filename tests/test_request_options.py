from __future__ import absolute_import, division, annotations, unicode_literals

import pytest
from tests.test_helper import TestHelper
from karaden.request_options import RequestOptions, RequestOptionsBuilder
from karaden.exception.invalid_request_options_exception import InvalidRequestOptionsException


def test_base_uriはapi_baseとtenant_idを半角スラッシュで結合した値():
    api_base = TestHelper.api_base
    tenant_id = TestHelper.tenant_id
    request_options = RequestOptions()
    request_options.api_base = api_base
    request_options.tenant_id = tenant_id

    assert request_options.base_uri == '{}/{}'.format(api_base, tenant_id)


def test_マージ元がnullならばマージ先を上書きしない():
    api_key = TestHelper.api_key
    request_options = (RequestOptions(), RequestOptions())

    request_options[0].api_key = api_key

    merged = request_options[0].merge(request_options[1])

    assert merged != request_options[0]
    assert api_key == merged.api_key


def test_マージ元がnullでなければマージ先を上書きする():
    api_key = ('a', 'b')
    request_options = (RequestOptions(), RequestOptions())

    request_options[0].api_key = api_key[0]
    request_options[1].api_key = api_key[1]

    merged = request_options[0].merge(request_options[1])

    assert merged != request_options[0]
    assert api_key[1] == merged.api_key


def test_api_versionを入力できる():
    expected = '2023-01-01'
    request_options = (
        RequestOptionsBuilder()
        .with_api_version(expected)
        .build()
    )

    assert expected == request_options.api_version


def test_api_baseを入力できる():
    expected = TestHelper.api_base
    request_options = (
        RequestOptionsBuilder()
        .with_api_base(expected)
        .build()
    )

    assert expected == request_options.api_base


def test_tenant_idを入力できる():
    expected = TestHelper.tenant_id
    request_options = (
        RequestOptionsBuilder()
        .with_tenant_id(expected)
        .build()
    )

    assert expected == request_options.tenant_id


def test_api_keyを入力できる():
    expected = TestHelper.api_key
    request_options = (
        RequestOptionsBuilder()
        .with_api_key(expected)
        .build()
    )

    assert expected == request_options.api_key


def test_user_agentを入力できる():
    expected = 'user_agent'
    request_options = (
        RequestOptionsBuilder()
        .with_user_agent(expected)
        .build()
    )

    assert expected == request_options.user_agent


def test_proxyを入力できる():
    expected = 'http://proxy'
    request_options = (
        RequestOptionsBuilder()
        .with_proxy(expected)
        .build()
    )

    assert expected == request_options.proxy


def test_connection_timeoutを入力できる():
    expected = 100
    request_options = (
        RequestOptionsBuilder()
        .with_connection_timeout(expected)
        .build()
    )

    assert expected == request_options.connection_timeout


def test_read_timeoutを入力できる():
    expected = 1000
    request_options = (
        RequestOptionsBuilder()
        .with_read_timeout(expected)
        .build()
    )

    assert expected == request_options.read_timeout


@pytest.mark.parametrize(
    ('value'),
    [
        (None),
        (''),
    ]
)
def test_api_keyがNoneや空文字はエラー(value):
    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_api_key(value)
        .build()
    )

    with pytest.raises(InvalidRequestOptionsException) as e:
        request_options.validate()

    messages = e.value.error.errors.get_property('api_key')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('value'),
    [
        (None),
        (''),
    ]
)
def test_api_versionがNoneや空文字はエラー(value):
    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_api_version(value)
        .build()
    )

    with pytest.raises(InvalidRequestOptionsException) as e:
        request_options.validate()

    messages = e.value.error.errors.get_property('api_version')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('value'),
    [
        (None),
        (''),
    ]
)
def test_api_baseがNoneや空文字はエラー(value):
    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_api_base(value)
        .build()
    )

    with pytest.raises(InvalidRequestOptionsException) as e:
        request_options.validate()

    messages = e.value.error.errors.get_property('api_base')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('value'),
    [
        (None),
        (''),
    ]
)
def test_tenant_idがNoneや空文字はエラー(value):
    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_tenant_id(value)
        .build()
    )

    with pytest.raises(InvalidRequestOptionsException) as e:
        request_options.validate()

    messages = e.value.error.errors.get_property('tenant_id')
    assert isinstance(messages, list)
