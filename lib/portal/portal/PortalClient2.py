import requests
import os


class ApiError(Exception):
    def __init__(self, response):
        super(ApiError, self).__init__('%s %s' % (response.status_code, response.reason))
        self._response = response

    @property
    def response(self):
        return self._response


class Resource(object):
    def __init__(self, ip, port, secret, path):
        self._ip = ip
        self._port = port
        self._secret = secret
        self._path = path

    def __getattr__(self, item):
        path = os.path.join(self._path, item)
        resource = Resource(self._ip, self._port, self._secret, path)
        setattr(self, item, resource)
        return resource

    @property
    def _url(self):
        scheme = "http" if self.port != 443 else "https"
        return "%s://%s:%s%s" % (scheme, self._ip, self._port, self._path)

    def __call__(self, **kwargs):
        kwargs['authkey'] = self._secret
        response = requests.post(self._url, kwargs)

        if not response.ok:
            raise ApiError(response)

        if response.headers.get('content-type', 'text/html') == 'application/json':
            return response.json()

        return response.content
