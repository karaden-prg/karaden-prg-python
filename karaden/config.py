from __future__ import absolute_import, division, annotations, unicode_literals

from karaden.request_options import RequestOptions


class Config:
    VERSION = '1.1.0'
    DEFAULT_API_BASE = 'https://prg.karaden.jp/api'
    DEFALUT_API_VERSION = '2023-12-01'

    api_version: str = None
    api_key: str = None
    tenant_id: str = None
    user_agent: str = None
    api_base: str = None
    connection_timeout = None
    read_timeout = None
    proxy: str = None

    @classmethod
    def as_request_options(cls) -> RequestOptions:
        return (
            RequestOptions.new_builder()
            .with_api_version(cls.api_version)
            .with_api_key(cls.api_key)
            .with_tenant_id(cls.tenant_id)
            .with_user_agent(cls.user_agent)
            .with_api_base(cls.api_base)
            .with_connection_timeout(cls.connection_timeout)
            .with_read_timeout(cls.read_timeout)
            .with_proxy(cls.proxy)
            .build()
        )
