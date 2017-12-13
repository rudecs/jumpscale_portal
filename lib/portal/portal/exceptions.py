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
        try:
            eco = json.loads(msg)
            msg = eco['backtrace']
        except:
            pass
        super(BaseError, self).__init__("%s: %s %s" % (code, status, msg))

class Error(BaseError):
    CODE = 500

    def __init__(self, msg, content_type='application/json'):
        if content_type == 'application/json':
            msg = json.dumps(msg)
        BaseError.__init__(self, self.CODE, [('Content-Type', content_type)], msg)


class Redirect(BaseError):
    def __init__(self, location):
        headers = [('Location', location)]
        BaseError.__init__(self, 302, headers, "")


class Accepted(Error):
    CODE = 202


class BadRequest(Error):
    CODE = 400


class Unauthorized(Error):
    CODE = 401


class Forbidden(Error):
    CODE = 403


class NotFound(Error):
    CODE = 404

class Gone(Error):
    CODE = 410

class MethodNotAllowed(Error):
    CODE = 405


class Conflict(Error):
    CODE = 409


class PreconditionFailed(Error):
    CODE = 412


class NotImplemented(Error):
    CODE = 501


class ServiceUnavailable(Error):
    CODE = 503
