import urllib
import requests
from JumpScale import j
from JumpScale.portal.portal import exceptions
from JumpScale.baselib.oauth.OauthInstance import AuthError
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
        cache.set(client.state, cache_data, ex=600)
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
        session = ctx.env['beaker.session']
        code = kwargs.get('code')
        cache_result = None

        def authfailure(msg):
            session['autherror'] = msg
            session.save()
            j.logger.log(msg)
            j.console.warning(msg)
            if cache_result:
                redirecturl = str(cache_result['redirect'])
            else:
                redirecturl = '/'
            raise exceptions.Redirect(redirecturl)

        if not code:
            return authfailure('Code is missing')

        state = kwargs.get('state')
        if not state:
            return authfailure('State is missing')

        cache = j.clients.redis.getByInstance('system')
        cache_result = cache.get(state)

        if not cache_result:
            return authfailure(' Invalid or expired state')

        cache_result = json.loads(cache_result)
        client = j.clients.oauth.get(instance=cache_result['type'])
        try:
            accesstoken = client.getAccessToken(code, state)
            userinfo = client.getUserInfo(accesstoken)
            session = ctx.env['beaker.session']
            if hasattr(client, "extra"):
                client.extra(session, accesstoken)
        except AuthError as e:
            return authfailure(str(e))
        except Exception as e:
            return authfailure('Failed to retreive user details')

        osis = j.clients.osis.getByInstance('main')
        user = j.clients.osis.getCategory(osis, "system", "user")

        if cache_result['type'] != 'oauth':
            if cache_result['type'].startswith('itsyouonline'):
                userid = '{}@itsyouonline'.format(userinfo.username)
            else:
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
            # update user info
            u = users[0]
            if cache_result['type'] != 'oauth':
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
