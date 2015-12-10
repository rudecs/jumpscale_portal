import requests
import os


class ApiError(Exception):
    def __init__(self, response):
        super(ApiError, self).__init__('%s %s' % (response.status_code, response.reason))
        self._response = response

    @property
    def response(self):
        return self._response


class BaseResource(object):
    def __init__(self, session, url):
        self._session = session
        self._url = url

    def __getattr__(self, item):
        url = os.path.join(self._url, item)
        resource = BaseResource(self._session, url)
        setattr(self, item, resource)
        return resource

    def __call__(self, **kwargs):
        response = self._session.post(self._url, kwargs)

        if not response.ok:
            raise ApiError(response)

        if response.headers.get('content-type', 'text/html') == 'application/json':
            return response.json()

        return response.content


class Resource(BaseResource):
    def __init__(self, ip, port, secret, path):
        session = requests.Session()

        if secret is not None:
            session.cookies['beaker.session.id'] = secret

        scheme = "http" if port != 443 else "https"
        url = "%s://%s:%s/%s" % (scheme, ip, port, path.lstrip('/'))

        super(Resource, self).__init__(session, url)
