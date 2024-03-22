from __future__ import absolute_import, division, annotations, unicode_literals

import json
import pytest
from datetime import datetime, timezone, timedelta
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.bulk.bulk_message_list_message_params import BulkMessageListMessageParams


def test_正しいパスを生成できる():
    id= 'id'
    params = BulkMessageListMessageParams(id)

    assert '{}/{}/messages'.format(BulkMessageListMessageParams.CONTEXT_PATH, id) == params.to_path()


def test_idを入力できる():
    expected = 'id'
    params = (
        BulkMessageListMessageParams
        .new_builder()
        .with_id(expected)
        .build()
    )

    assert expected == params.id


@pytest.mark.parametrize(
    ('id'),
    [
        (None),
        (''),
    ]
)
def test_idがNoneや空文字はエラー(id):
    params = (
        BulkMessageListMessageParams.new_builder()
        .with_id(id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('id')
    assert isinstance(messages, list)