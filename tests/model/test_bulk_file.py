from __future__ import absolute_import, division, annotations, unicode_literals

import json

from typing import Tuple
from httpretty import HTTPretty, httprettified
from httpretty.core import HTTPrettyRequest
from karaden.model.bulk_file import BulkFile

from tests.test_helper import TestHelper


@httprettified(allow_net_connect=False)
def test_一括送信用CSVのアップロード先URLを発行できる():
    path = "/messages/bulks/files"
    request_options = TestHelper.get_default_request_options_builder().build()
    mock_url = "{}{}".format(request_options.base_uri, path)
    object = {"object": "bulk_file"}

    def callback(
        request: HTTPrettyRequest, url: str, headers: dict
    ) -> Tuple[int, dict, str]:
        return (200, headers, json.dumps(object))

    HTTPretty.register_uri(HTTPretty.POST, mock_url, body=callback)

    output = BulkFile.create(request_options)

    assert object["object"] == output.get_property("object")


def test_urlを出力できる():
    expected = "https://example.com/"
    bulk_file = BulkFile()
    bulk_file.set_property("url", expected)
    assert expected == bulk_file.url


def test_created_atを出力できる():
    expected = "2022-12-09T00:00:00+09:00"
    bulk_file = BulkFile()
    bulk_file.set_property("created_at", expected)
    assert expected == bulk_file.created_at.isoformat(timespec="seconds")


def test_expires_atを出力できる():
    expected = "2022-12-09T00:00:00+09:00"
    bulk_file = BulkFile()
    bulk_file.set_property("expires_at", expected)
    assert expected == bulk_file.expires_at.isoformat(timespec="seconds")
