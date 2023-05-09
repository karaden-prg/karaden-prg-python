from __future__ import absolute_import, division, annotations, unicode_literals

import requests
import pytest
import time
from urllib.parse import urlparse, urlencode
from typing import Tuple
from httpretty import HTTPretty, httprettified
from httpretty.core import HTTPrettyRequest
from karaden.config import Config
from karaden.net.requests_requestor import RequestsRequestor
from tests.test_helper import TestHelper


@pytest.fixture
def setup() -> RequestsRequestor:
    requestor = RequestsRequestor()

    yield requestor


@httprettified(allow_net_connect=False)
def test_ベースURLとパスが結合される(setup):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert mock_url == url

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, None, None, request_options)


@pytest.mark.parametrize(
    ('method'),
    [
        ('POST'),
        ('GET'),
        ('PUT'),
        ('DELETE'),
        ('OPTIONS'),
        ('HEAD'),
    ]
)
@httprettified(allow_net_connect=False)
def test_メソッドがHTTPクライアントに伝わる(setup, method):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert request.method == method

        return (200, headers, '')

    HTTPretty.register_uri(method, mock_url, body=callback)

    requestor.send(method, path, None, None, request_options)


@httprettified(allow_net_connect=False)
def test_URLパラメータがHTTPクライアントに伝わる(setup):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)
    params = {
        "key1": "value1",
        "key2": "value2",
    }

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert '{}?{}'.format(mock_url, urlencode(params)) == url

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, params, None, request_options)


@httprettified(allow_net_connect=False)
def test_本文がHTTPクライアントに伝わる(setup):
    requestor = setup

    path = '/test'
    data = {
        'test': 'test',
    }
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert request.body.decode('utf-8') == 'test=test'

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.POST, mock_url, body=callback)

    requestor.send('POST', path, None, data, request_options)


@httprettified(allow_net_connect=False)
def test_リクエスト時に指定したリクエストオプションはコンストラクタのリクエストオプションを上書きする(setup):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert 'Bearer {}'.format(request_options.api_key) == request.headers['Authorization']

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, None, None, request_options)


@httprettified(allow_net_connect=False)
def test_APIキーに基づいてBearer認証ヘッダを出力する(setup):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert 'Bearer {}'.format(request_options.api_key) == request.headers['Authorization']

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, None, None, request_options)


@httprettified(allow_net_connect=False)
def test_APIバージョンを設定した場合はAPIバージョンヘッダを出力する(setup):
    requestor = setup

    api_version = 'test'
    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_api_version(api_version)
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert api_version == request.headers['Karaden-Version']

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, None, None, request_options)

@httprettified(allow_net_connect=False)
def test_APIバージョンを設定しない場合はデフォルトのAPIバージョンヘッダを出力する(setup):
    requestor = setup

    path = '/test'
    request_options = (
        TestHelper.get_default_request_options_builder()
        .build()
    )
    mock_url = '{}{}'.format(request_options.base_uri, path)

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        assert Config.DEFALUT_API_VERSION == request.headers['Karaden-Version']

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, mock_url, body=callback)

    requestor.send('GET', path, None, None, request_options)


@httprettified(allow_net_connect=False)
def test_proxyはrequestsのrequestが呼び出されるときに指定されていること(setup, mocker):
    requestor = setup

    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_proxy('http://proxy')
        .build()
    )

    def mocked_request(method, url, **kwargs):
        proxies = kwargs['proxies']
        (key, value) = list(proxies.items())[0]
        assert key == urlparse(request_options.proxy).scheme
        assert value == request_options.proxy

        class MockedResponse(requests.Response):
            def __init__(self) -> None:
                super().__init__()

        response = MockedResponse()
        response.status_code = 200
        response._content = ''.encode()

        return response

    mocker.patch('requests.request', side_effect=mocked_request)

    requestor.send('GET', '', None, None, request_options)


def test_connection_timeoutが設定されるとConnectTimeoutが発生すること(setup):
    requestor = setup

    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_api_base('http://10.255.255.1')
        .with_connection_timeout(0.5)
        .build()
    )

    with pytest.raises(requests.exceptions.ConnectTimeout):
        requestor.send('GET', '', None, None, request_options)


@httprettified(allow_net_connect=False)
def test_read_timeoutが設定されるとReadTimeoutが発生すること(setup):
    requestor = setup

    request_options = (
        TestHelper.get_default_request_options_builder()
        .with_read_timeout(0.5)
        .build()
    )

    def callback(
            request: HTTPrettyRequest,
            url: str,
            headers: dict) -> Tuple[int, dict, str]:
        time.sleep(1)

        return (200, headers, '')

    HTTPretty.register_uri(HTTPretty.GET, request_options.base_uri, body=callback)

    with pytest.raises(requests.exceptions.ReadTimeout):
        requestor.send('GET', '', None, None, request_options)
