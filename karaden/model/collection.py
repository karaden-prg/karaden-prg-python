from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.model.karaden_object import KaradenObject


class Collection(KaradenObject):
    OBJECT_NAME = 'list'

    @property
    def data(self) -> list:
        return self.get_property('data')

    @property
    def has_more(self) -> bool:
        return self.get_property('has_more')
