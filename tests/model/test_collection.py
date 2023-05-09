from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.model.collection import Collection


def test_dataを出力できる():
    expected = []
    collection = Collection()
    collection.set_property('data', expected)
    assert isinstance(collection.data, list)


def test_has_moreを出力できる():
    expected = True
    collection = Collection()
    collection.set_property('has_more', expected)
    assert collection.has_more
