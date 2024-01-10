from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.request_options import RequestOptions, RequestOptionsBuilder


class TestHelper:
    api_base = 'http://localhost:4010'
    api_key = '123'
    api_version = '2023-12-01'
    tenant_id = '159bfd33-b9b7-f424-4755-c119b324591d'

    @classmethod
    def get_default_request_options_builder(cls) -> RequestOptionsBuilder:
        return (
            RequestOptions.new_builder()
            .with_api_base(cls.api_base)
            .with_api_key(cls.api_key)
            .with_api_version(cls.api_version)
            .with_tenant_id(cls.tenant_id)
        )
