from __future__ import absolute_import, division, annotations, unicode_literals

import pytest
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.bulk.bulk_message_show_params import BulkMessageShowParams


def test_正しいパスを生成できる():
    id = 'id'
    params = BulkMessageShowParams(id)

    assert '{}/{}'.format(BulkMessageShowParams.CONTEXT_PATH, id) == params.to_path()


def test_idを入力できる():
    expected = 'id'
    params = (
        BulkMessageShowParams
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
        BulkMessageShowParams.new_builder()
        .with_id(id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('id')
    assert isinstance(messages, list)
    assert "idは必須です。" in messages
    assert "文字列（UUID）を入力してください。" in messages
