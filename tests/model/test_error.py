from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.model.karaden_object import KaradenObject
from karaden.model.error import Error


def test_codeを出力できる():
    value = 'code'
    error = Error()
    error.set_property('code', value)
    assert value == error.code


def test_messageを出力できる():
    value = 'message'
    error = Error()
    error.set_property('message', value)
    assert value == error.message


def test_errorsを出力できる():
    value = KaradenObject()
    error = Error()
    error.set_property('errors', value)
    assert isinstance(error.errors, KaradenObject)
