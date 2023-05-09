from __future__ import absolute_import, division, annotations, unicode_literals

import pytest
from karaden.exception.invalid_params_exception import InvalidParamsException
from karaden.param.message_detail_params import MessageDetailParams


def test_正しいパスを生成できる():
    id = 'id'
    params = MessageDetailParams(id)

    assert '{}/{}'.format(MessageDetailParams.CONTEXT_PATH, id) == params.to_path()


def test_idを入力できる():
    expected = 'id'
    params = (
        MessageDetailParams
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
        MessageDetailParams.new_builder()
        .with_id(id)
        .build()
    )
    with pytest.raises(InvalidParamsException) as e:
        params.validate()

    messages = e.value.error.errors.get_property('id')
    assert isinstance(messages, list)
