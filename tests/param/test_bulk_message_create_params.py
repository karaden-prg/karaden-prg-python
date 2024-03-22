from __future__ import absolute_import, division, annotations, unicode_literals

import pytest

from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.bulk.bulk_message_create_params import BulkMessageCreateParams


def test_正しいパスを生成できる():
    bulk_file_id = '72fe94ec-9c7d-9634-8226-e3136bd6cf7a'
    params = BulkMessageCreateParams(bulk_file_id)

    assert BulkMessageCreateParams.CONTEXT_PATH == params.to_path()


def test_bulk_file_idを入力できる():
    expected = '72fe94ec-9c7d-9634-8226-e3136bd6cf7a'
    params = (
        BulkMessageCreateParams
        .new_builder()
        .with_bulk_file_id(expected)
        .build()
    )

    assert expected == params.bulk_file_id


@pytest.mark.parametrize(
    ('bulk_file_id'),
    [
        (None),
        (''),
    ]
)
def test_bulk_file_idがNoneや空文字はエラー(bulk_file_id):
    params = (
        BulkMessageCreateParams.new_builder()
        .with_bulk_file_id(bulk_file_id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('bulk_file_id')
    assert isinstance(messages, list)
