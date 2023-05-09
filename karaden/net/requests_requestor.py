from __future__ import absolute_import, division, annotations, unicode_literals

import sys
import platform
import json
import requests
from urllib.parse import urlparse
from karaden.config import Config
from karaden.request_options import RequestOptions
from karaden.net.requestor_interface import RequestorInterface
from karaden.net.requests_response import RequestsResponse
from karaden.net.response_interface import ResponseInterface


class RequestsRequestor(RequestorInterface):
    DEFAULT_USER_AGENT = 'Karaden/Python/'

    def send(self, method: str, path: str, params: dict, data: dict, request_options: RequestOptions = None) -> ResponseInterface:
        request_options = Config.as_request_options().merge(request_options)
        request_options.validate()

        url = '{}{}'.format(request_options.base_uri, path)

        headers = {
            'User-Agent': self.build_user_agent(request_options),
            'Karaden-Version': request_options.api_version,
            'Karaden-Client-User-Agent': self.build_client_user_agent(),
            'Authorization': 'Bearer {}'.format(request_options.api_key),
            'Accept-Encoding': 'gzip, deflate',
            'TE': 'chunked',
        }
        headers = dict(filter(lambda item: item[1] is not None, headers.items()))

        proxy = request_options.proxy
        proxies = None if proxy is None else {urlparse(proxy).scheme: proxy}

        timeout = (request_options.connection_timeout, request_options.read_timeout)

        response = requests.request(method, url, params=params, data=data, headers=headers, timeout=timeout, proxies=proxies)
        return RequestsResponse(response, request_options)

    def build_user_agent(self, request_options: RequestOptions) -> str:
        return request_options.user_agent if request_options.user_agent is None else self.DEFAULT_USER_AGENT

    def build_client_user_agent(self):
        return json.dumps({
            'bindings_version': Config.VERSION,
            'language': 'Python',
            'language_version': sys.version,
            'uname': platform.uname(),
        })
