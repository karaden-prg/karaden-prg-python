from __future__ import absolute_import, division, annotations, unicode_literals


class MessageParams:
    CONTEXT_PATH = '/messages'

    def validate(self) -> MessageParams:
        return self
