from JumpScale import j
from JumpScale.portal.portal import exceptions
import ujson as json
import time
import types

clients = dict()


def getClient(namespace):
    if namespace not in clients:
        client = j.clients.osis.getNamespace(namespace, j.core.portal.active.osis)
        clients[namespace] = client
    return clients[namespace]


def doAudit(user, path, kwargs, responsetime, statuscode, result,  tags):
    client = getClient('system')
    audit = client.audit.new()
    audit.user = user
    audit.call = path
    audit.statuscode = statuscode
    audit.tags = tags
    audit.args = json.dumps([])  # we dont want to log self
    auditkwargs = kwargs.copy()
    auditkwargs.pop('ctx', None)
    audit.kwargs = json.dumps(auditkwargs)
    try:
        if not isinstance(result, types.GeneratorType):
            audit.result = json.dumps(result)
        else:
            audit.result = json.dumps('Result of type generator')
    except:
        audit.result = json.dumps('binary data')

    audit.responsetime = responsetime
    client.audit.set(audit)


class AuditMiddleWare(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, env, start_response):
        statinfo = {'status': 200}
        def my_response(status, headers, exc_info=None):
            statinfo['status'] = int(status.split(" ", 1)[0])
            return start_response(status, headers, exc_info)

        start = time.time()
        env['beaker.session']['tags'] = ""
        result = self.app(env, my_response)
        responsetime = time.time() - start
        audit = env.get('JS_AUDIT')
        if audit or statinfo['status'] >= 400:
            ctx = env.get('JS_CTX')
            tags = env['beaker.session'].get('tags', '')
            user = env['beaker.session'].get('user', 'Unknown')
            kwargs = ctx.params.copy() if ctx else {}
            if j.core.portal.active.authentication_method:
                doAudit(user, env['PATH_INFO'], kwargs, responsetime, statinfo['status'], result, tags)
        return result

class auth(object):

    def __init__(self, groups=None, audit=True, **kwargs):
        if isinstance(groups, str):
            groups = [groups]
        if groups is None:
            groups = list()
        self.groups = set(groups)
        self.audit = audit
        self.tags = kwargs

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            self.tags_str = ' '.join(["%s:%s" % (k, kwargs[v]) for k, v in self.tags.iteritems()])

            if 'ctx' not in kwargs:
                # call is not performed over rest let it pass
                return func(*args, **kwargs)

            ctx = kwargs['ctx']
            if self.tags:
                ctx.env['beaker.session']['tags'] = self.tags_str
            user = ctx.env['beaker.session']['user']
            if self.groups:
                userobj = j.core.portal.active.auth.getUserInfo(user)
                groups = set()
                if userobj:
                    groups = set(userobj.groups)
                if not groups.intersection(self.groups):
                    raise exceptions.Forbidden('User %s has no access. If you would like to gain access please contact your adminstrator' % user)

            ctx.env['JS_AUDIT'] = self.audit
            return func(*args, **kwargs)
        return wrapper
