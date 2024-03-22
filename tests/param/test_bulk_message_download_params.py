from __future__ import absolute_import, division, annotations, unicode_literals

import os
import tempfile
import pytest
from datetime import datetime, timezone, timedelta
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.bulk.bulk_message_download_params import BulkMessageDownloadParams


def test_idを入力できる():
    expected = 'id'
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id(expected)
        .build()
    )

    assert expected == params.id


def test_directory_pathを入力できる():
    expected = 'path'
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_directory_path(expected)
        .build()
    )

    assert expected == params.directory_path


def test_max_retriesを入力できる():
    expected = 1
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_max_retries(expected)
        .build()
    )

    assert expected == params.max_retries


def test_retry_intervalを入力できる():
    expected = 1
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_retry_interval(expected)
        .build()
    )

    assert expected == params.retry_interval


@pytest.mark.parametrize(
    ('id'),
    [
        (None),
        (''),
    ]
)
def test_idがNoneや0以下はエラー(id):
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_id(id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('id')
    assert isinstance(messages, list)


def test_with_idが未使用の場合はエラー():
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('id')
    assert isinstance(messages, list)


def test_directory_pathが存在しない値の場合はエラー():
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_directory_path('invalid')
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('directory_path')
    assert isinstance(messages, list)


def test_directory_pathがファイルを指定している場合はエラー():
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_directory_path(tempfile.NamedTemporaryFile(suffix=".csv", delete=True).name)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('directory_path')
    assert isinstance(messages, list)


def test_指定されたdirectory_pathに読み取り権限がない場合はエラー(tmpdir):
    os.chmod(tmpdir, 0o377)
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_directory_path(tmpdir)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('directory_path')
    assert isinstance(messages, list)

    os.chmod(tmpdir, 0o777)


def test_指定されたdirectory_pathに書き込み権限がない場合はエラー(tmpdir):
    os.chmod(tmpdir, 0o577)
    params = (
        BulkMessageDownloadParams
        .new_builder()
        .with_directory_path(tmpdir)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('directory_path')
    assert isinstance(messages, list)

    os.chmod(tmpdir, 0o777)


@pytest.mark.parametrize(
    ('max_retries'),
    [
        (None),
        (0),
        (6),
        (-1),
        (1.1),
    ]
)
def test_max_retriesがNoneまたは0以下または6以上または小数値はエラー(max_retries):
    params = (
        BulkMessageDownloadParams.new_builder()
        .with_max_retries(max_retries)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('max_retries')
    assert isinstance(messages, list)


@pytest.mark.parametrize(
    ('retry_interval'),
    [
        (None),
        (9),
        (61),
        (-1),
        (10.1),
    ]
)
def test_retry_intervalがNoneまたは9以下または61以上または小数値はエラー(retry_interval):
    params = (
        BulkMessageDownloadParams.new_builder()
        .with_retry_interval(retry_interval)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('retry_interval')
    assert isinstance(messages, list)
