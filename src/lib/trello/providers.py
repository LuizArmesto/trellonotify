# -*- coding: utf-8 -*-

__all__ = ['ApiOne']

import requests

from urllib import urlencode

from lib.common import API_KEY

from .base import BaseModel

from .exceptions import ApiKeyError
from .exceptions import BadRequestError
from .exceptions import ExpiredTokenError
from .exceptions import InvalidTokenError
from .exceptions import NotFoundError
from .exceptions import UnauthorizedError

from .fields import NotEmptyField


class ApiOne(BaseModel):

    API_VERSION = '1'
    PROTOCOL = 'https'
    BASE_URL = '{protocol}://api.trello.com/{version}'

    HEADERS = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    api_key = NotEmptyField(is_local=True)
    oauth_token = NotEmptyField(is_local=True)

    def __init__(self, api_key=API_KEY, oauth_token=None,
            session=requests.session, proxies=None, *args, **kwargs):
        self.api_key = api_key
        self.oauth_token = oauth_token

        self.session = session(headers=self.HEADERS, proxies=proxies)
        self.proxies = proxies

        super(ApiOne, self).__init__(*args, **kwargs)

    @property
    def base_url(self):
        return self.BASE_URL.format(protocol=self.PROTOCOL,
                                    version=self.API_VERSION)

    def get_url(self, path, params={}):
        if not path.startswith('/'):
            path = '/{}'.format(path)
        return '{base}{path}?{params}'.format(base=self.base_url,
                                              path=path,
                                              params=urlencode(params))

    def request(self, method, path, body=None, **params):
        params.update({'key': self.api_key,
                       'token': self.oauth_token})

        if path.startswith('tokens') and not 'member' in path:
            # We don't want ExpiredTokenError when getting token info
            params.pop('token')

        url = self.get_url(path, params)
        print url
        response = self.session.request(method, url, data=body)
        content = response.content
        code = response.status_code

        if code == 400:
            if 'invalid token' in content:
                raise InvalidTokenError(content)
            else:
                raise BadRequestError(content)
        elif code == 401:
            if 'expired token' in content:
                raise ExpiredTokenError(content)
            elif 'invalid token' in content:
                raise InvalidTokenError(content)
            elif 'invalid key' in content:
                raise ApiKeyError(content)
            else:
                raise UnauthorizedError(content)
        elif code == 404:
            raise NotFoundError(content)

        return response

    def get(self, path, **params):
        return self.request('GET', path, **params)

    def post(self, path, body=None, **params):
        return self.request('POST', path, body, **params)

    def put(self, path, body=None, **params):
        return self.request('PUT', path, body, **params)

    def delete(self, path, body=None, **params):
        return self.request('DELETE', path, body, **params)

    def fetch(self, path='', method='GET', body=None, **params):
        for key, value in params.items():
            if isinstance(value, list):
                if value:
                    if len(value) > 1:
                        value = ','.join(value)
                    else:
                        value = value[0]
            params[key] = value
        response = self.request(method, path, body, **params)
        return response.content


class Cacheble(object):  # TODO
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('CacheMixIn was not implemented yet!')


class Local(object):  # TODO
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('LocalMixIn was not implemented yet!')
