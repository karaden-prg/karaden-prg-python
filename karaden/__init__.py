from __future__ import absolute_import, division, annotations, unicode_literals

__author__ = 'cpaas-dev-admin-om'
__email__ = 'cpaas-dev-admin-om@nttcoms.com'
__version__ = '1.1.0'

from karaden.config import Config
from karaden.request_options import RequestOptions
from karaden.model.karaden_object import KaradenObject
from karaden.model.message import Message
from karaden.model.error import Error
from karaden.model.collection import Collection
from karaden.exception.bad_request_exception import BadRequestException
from karaden.exception.forbidden_exception import ForbiddenException
from karaden.exception.not_found_exception import NotFoundException
from karaden.exception.too_many_requests_exception import TooManyRequestsException
from karaden.exception.unauthorized_exception import UnauthorizedException
from karaden.exception.unprocessable_entity_exception import UnprocessableEntityException
from karaden.exception.invalid_request_options_exception import InvalidRequestOptionsException
from karaden.net.requests_requestor import RequestsRequestor
from karaden.net.requests_response import RequestsResponse
from karaden.utility import Utility


Config.api_base = Config.DEFAULT_API_BASE
Config.api_version = Config.DEFALUT_API_VERSION

Utility.DEFAULT_OBJECT_NAME = Message.OBJECT_NAME
Utility.object_types = {
    KaradenObject.OBJECT_NAME: KaradenObject,
    Collection.OBJECT_NAME: Collection,
    Message.OBJECT_NAME: Message,
    Error.OBJECT_NAME: Error,
}

Message.requestor = RequestsRequestor()

RequestsResponse.errors = {
    BadRequestException.STATUS_CODE: BadRequestException,
    UnauthorizedException.STATUS_CODE: UnauthorizedException,
    ForbiddenException.STATUS_CODE: ForbiddenException,
    NotFoundException.STATUS_CODE: NotFoundException,
    UnprocessableEntityException.STATUS_CODE: UnprocessableEntityException,
    TooManyRequestsException.STATUS_CODE: TooManyRequestsException,
}

RequestOptions.errors = KaradenObject
RequestOptions.error = Error
RequestOptions.validation_exception = InvalidRequestOptionsException
