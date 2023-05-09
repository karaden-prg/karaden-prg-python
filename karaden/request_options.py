from __future__ import absolute_import, division, annotations, unicode_literals

from copy import copy


class RequestOptions:
    errors: any
    error: any
    validation_exception: any

    def __init__(self) -> None:
        self.api_version = None
        self.api_key = None
        self.tenant_id = None
        self.user_agent = None
        self.proxy = None
        self.api_base = None
        self.connection_timeout = None
        self.read_timeout = None

    def merge(self, source: RequestOptions) -> RequestOptions:
        destination = RequestOptions()
        self.merge_value(destination, source, 'api_version')
        self.merge_value(destination, source, 'api_key')
        self.merge_value(destination, source, 'tenant_id')
        self.merge_value(destination, source, 'user_agent')
        self.merge_value(destination, source, 'proxy')
        self.merge_value(destination, source, 'api_base')
        self.merge_value(destination, source, 'connection_timeout')
        self.merge_value(destination, source, 'read_timeout')
        return destination

    def merge_value(self, destination: RequestOptions, source: RequestOptions, name: str) -> None:
        values = (getattr(self, name), None if source is None else getattr(source, name))
        setattr(destination, name, values[0] if values[1] is None else values[1])

    @property
    def base_uri(self) -> str:
        return '{0}/{1}'.format(self.api_base, self.tenant_id)

    @classmethod
    def new_builder(cls) -> RequestOptionsBuilder:
        return RequestOptionsBuilder()

    def _validate_api_version(self):
        messages = []

        if self.api_version is None or self.api_version == '':
            messages.append('api_versionは必須です。')
            messages.append('文字列を入力してください。')

        return messages

    def _validate_api_key(self):
        messages = []

        if self.api_key is None or self.api_key == '':
            messages.append('api_keyは必須です。')
            messages.append('文字列を入力してください。')

        return messages

    def _validate_api_base(self):
        messages = []

        if self.api_base is None or self.api_base == '':
            messages.append('api_baseは必須です。')
            messages.append('文字列を入力してください。')

        return messages

    def _validate_tenant_id(self):
        messages = []

        if self.tenant_id is None or self.tenant_id == '':
            messages.append('tenant_idは必須です。')
            messages.append('文字列（UUID）を入力してください。')

        return messages

    def validate(self) -> RequestOptions:
        errors = self.__class__.errors()
        has_error = False

        messages = self._validate_tenant_id()
        if len(messages) > 0:
            errors.set_property('tenant_id', messages)
            has_error = True

        messages = self._validate_api_version()
        if len(messages) > 0:
            errors.set_property('api_version', messages)
            has_error = True

        messages = self._validate_api_key()
        if len(messages) > 0:
            errors.set_property('api_key', messages)
            has_error = True

        messages = self._validate_api_base()
        if len(messages) > 0:
            errors.set_property('api_base', messages)
            has_error = True

        if has_error:
            error = self.__class__.error()
            error.set_property('errors', errors)
            raise self.__class__.validation_exception(error)

        return self

class RequestOptionsBuilder:
    def __init__(self) -> None:
        self.request_options = RequestOptions()

    def with_api_version(self, api_version: str) -> RequestOptionsBuilder:
        self.request_options.api_version = api_version
        return self

    def with_api_key(self, api_key: str) -> RequestOptionsBuilder:
        self.request_options.api_key = api_key
        return self

    def with_tenant_id(self, tenant_id: str) -> RequestOptionsBuilder:
        self.request_options.tenant_id = tenant_id
        return self

    def with_user_agent(self, user_agent: str) -> RequestOptionsBuilder:
        self.request_options.user_agent = user_agent
        return self

    def with_proxy(self, proxy: str) -> RequestOptionsBuilder:
        self.request_options.proxy = proxy
        return self

    def with_api_base(self, api_base: str) -> RequestOptionsBuilder:
        self.request_options.api_base = api_base
        return self

    def with_connection_timeout(self, connection_timeout: float) -> RequestOptionsBuilder:
        self.request_options.connection_timeout = connection_timeout
        return self

    def with_read_timeout(self, read_timeout: float) -> RequestOptionsBuilder:
        self.request_options.read_timeout = read_timeout
        return self

    def build(self) -> RequestOptions:
        return copy(self.request_options)
