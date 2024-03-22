from __future__ import absolute_import, division, annotations, unicode_literals


class BulkMessageParams:
    CONTEXT_PATH = '/messages/bulks'

    def validate(self) -> BulkMessageParams:
        return self
