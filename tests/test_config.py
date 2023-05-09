from __future__ import absolute_import, division, annotations, unicode_literals

import pytest
from tests.test_helper import TestHelper
from karaden.config import Config


@pytest.fixture
def setup():
    yield

    Config.api_base = Config.DEFAULT_API_BASE
    Config.api_key = None
    Config.api_version = Config.DEFALUT_API_VERSION
    Config.tenant_id = None
    Config.user_agent = None
    Config.proxy = None
    Config.connection_timeout = None
    Config.read_timeout = None


def test_入力したapi_versionが取得したRequestOptionsに入力されること(setup):
    expected = '2023-01-01'
    Config.api_version = expected
    request_options = Config.as_request_options()

    assert expected == request_options.api_version


def test_入力したapi_baseが取得したRequestOptionsに入力されること(setup):
    expected = TestHelper.api_base
    Config.api_base = expected
    request_options = Config.as_request_options()

    assert expected == request_options.api_base


def test_入力したtenant_idが取得したRequestOptionsに入力されること(setup):
    expected = TestHelper.tenant_id
    Config.tenant_id = expected
    request_options = Config.as_request_options()

    assert expected == request_options.tenant_id


def test_入力したapi_keyが取得したRequestOptionsに入力されること(setup):
    expected = TestHelper.api_key
    Config.api_key = expected
    request_options = Config.as_request_options()

    assert expected == request_options.api_key


def test_入力したuser_agentが取得したRequestOptionsに入力されること(setup):
    expected = 'user_agent'
    Config.user_agent = expected
    request_options = Config.as_request_options()

    assert expected == request_options.user_agent


def test_入力したproxyが取得したRequestOptionsに入力されること(setup):
    expected = 'http://proxy'
    Config.proxy = expected
    request_options = Config.as_request_options()

    assert expected == request_options.proxy


def test_入力したconnection_timeoutが取得したRequestOptionsに入力されること(setup):
    expected = 100
    Config.connection_timeout = expected
    request_options = Config.as_request_options()

    assert expected == request_options.connection_timeout


def test_入力したread_timeoutが取得したRequestOptionsに入力されること(setup):
    expected = 100
    Config.read_timeout = expected
    request_options = Config.as_request_options()

    assert expected == request_options.read_timeout
