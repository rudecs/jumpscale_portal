import urllib
import requests

from JumpScale import j
from JumpScale.portal.portal import exceptions
try:
    import ujson as json
except:
    import json


class system_oauth(j.code.classGetBase()):
    """
    Oauth System actors
    """

    def authenticate(self, type='', **kwargs):
        cache = j.clients.redis.getByInstance('system')

        if j.core.portal.active.force_oauth_instance and not type:
            type = j.core.portal.active.force_oauth_instance

        if not type:
            type = 'github'

        ctx = kwargs['ctx']
        referer = ctx.env.get('HTTP_REFERER', '/')
        redirect = kwargs.get('redirect', referer)
        client = j.clients.oauth.get(instance=type)
        cache_data = json.dumps({'type': type, 'redirect': redirect})
        cache.set(client.state, cache_data, ex=180)
        ctx.start_response('302 Found', [('Location', client.url)])
        return 'OK'

    def getOauthLogoutURl(self, **kwargs):
        ctx = kwargs['ctx']
        redirecturi = ctx.env.get('HTTP_REFERER')
        if not redirecturi:
            redirecturi = 'http://%s' % ctx.env['HTTP_HOST']
        session = ctx.env['beaker.session']
        if session:
            oauth = session.get('oauth')
            session.delete()
            session.save()
            if oauth:
                back_uri = urllib.urlencode({'redirect_uri': redirecturi})
                location = str('%s?%s' % (oauth.get('logout_url'), back_uri))
                ctx.start_response('302 Found', [('Location', location)])
            else:
                ctx.start_response('302 Found', [('Location', redirecturi)])
        else:
            ctx.start_response('302 Found', [('Location', redirecturi)])
        return ''

    def authorize(self, **kwargs):
        ctx = kwargs['ctx']
        code = kwargs.get('code')
        if not code:
            raise exceptions.Forbidden('Not Authorized -- Code is missing')

        state = kwargs.get('state')
        if not state:
            return exceptions.Forbidden('Not Authorized -- State is missing')

        cache = j.clients.redis.getByInstance('system')
        cache_result = cache.get(state)

        if not cache_result:
            unauthorized_redirect_url = '%s?%s' % ('/restmachine/system/oauth/authenticate', urllib.urlencode({
                                                   'type': j.core.portal.active.force_oauth_instance or 'github'}))
            msg = 'Not Authorized -- Invalid or expired state'
            j.logger.log(msg)
            raise exceptions.Redirect(unauthorized_redirect_url)

        cache_result = json.loads(cache_result)
        client = j.clients.oauth.get(instance=cache_result['type'])
        accesstoken = client.getAccessToken(code, state)
        userinfo = client.getUserInfo(accesstoken)

        osis = j.clients.osis.getByInstance('main')
        user = j.clients.osis.getCategory(osis, "system", "user")

        if cache_result['type'] != 'oauth':
            userid = '{}@{}'.format(userinfo.username, cache_result['type'])
        else:
            userid = userinfo.username

        users = user.search({'id': userid})[1:]
        if not users:
            # register user
            u = user.new()
            u.id = userid
            u.groups = userinfo.groups
            u.emails = [userinfo.emailaddress]
            user.set(u)
        else:
            u = users[0]
            if userinfo.emailaddress not in u['emails']:
                raise exceptions.BadRequest(
                    'User with same name already exists')
            u['groups'] = userinfo.groups
            u['emails'] = [userinfo.emailaddress]
            user.set(u)

        session = ctx.env['beaker.session']
        session['user'] = userid
        session['email'] = userinfo.emailaddress
        session['oauth'] = {'authorized': True,
                            'type': str(cache_result['type']),
                            'logout_url': client.logout_url}
        session.save()

        raise exceptions.Redirect(str(cache_result['redirect']))
