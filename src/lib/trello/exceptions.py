# -*- coding: utf-8 -*-


class TrelloException(Exception):
    pass


class ApiKeyError(TrelloException):
    pass


class BadRequestError(TrelloException):
    pass


class TokenError(TrelloException):
    pass


class ExpiredTokenError(TokenError):
    pass


class InvalidTokenError(TokenError):
    pass


class NotFoundError(TrelloException):
    pass


class UnauthorizedError(TrelloException):
    pass
