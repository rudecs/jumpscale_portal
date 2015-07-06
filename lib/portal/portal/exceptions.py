import httplib
import json

codemapping = httplib.responses.copy()
codemapping[419] = 'Authentication Timeout'


class BaseError(BaseException):
    def __init__(self, code, headers, msg, status=None):
        self.code = code
        self.headers = headers
        self.msg = msg
        if status is None:
            status = codemapping.get(code, 'Unkonwn')
        self.status = status


class Error(BaseError):
    CODE = 500

    def __init__(self, msg):
        msg = json.dumps(msg)
        BaseError.__init__(self, self.CODE, [('Content-Type', 'application/json')], msg)


class BadRequest(Error):
    CODE = 400


class NotFound(Error):
    CODE = 404


class MethodNotAllowed(Error):
    CODE = 405


class Conflict(Error):
    CODE = 409


class PreconditionFailed(Error):
    CODE = 412


class ServiceUnavailable(Error):
    CODE = 503
