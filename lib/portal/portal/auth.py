from JumpScale import j
from JumpScale.portal.portal import exceptions
import ujson as json
from functools import partial
import time
import types

clients = dict()


def getClient(namespace):
    if namespace not in clients:
        client = j.clients.osis.getNamespace(namespace, j.core.portal.active.osis)
        clients[namespace] = client
    return clients[namespace]


def get_result(result):
    try:
        if not isinstance(result, types.GeneratorType):
            return json.dumps(result)
        else:
            return json.dumps('Result of type generator')
    except:
        return json.dumps('binary data')


class AuditMiddleWare(object):
    def __init__(self, app):
        self.app = app
        self.client = getClient('system')

    def write_audit(self, env, result=None, responsetime=None, statuscode=None):
        audit = self.client.audit.new()
        audit.user = env['beaker.session'].get('user', 'Unknown')
        audit.call = env['PATH_INFO']
        audit.tags = env['tags']
        audit.args = json.dumps([])  # we dont want to log self
        ctx = env.get('JS_CTX')
        kwargs = ctx.params.copy() if ctx else {}
        auditkwargs = kwargs.copy()
        auditkwargs.pop('ctx', None)
        if ctx.env['is_stream']:
            audit.kwargs = json.dumps({})
        else:
            audit.kwargs = get_result(auditkwargs)
        audit.result = get_result(result)
        audit.responsetime = responsetime
        audit.statuscode = statuscode
        key, _, _ = self.client.audit.set(audit)
        env['JS_AUDITKEY'] = key

    def __call__(self, env, start_response):
        statinfo = {'status': 200}
        def my_response(status, headers, exc_info=None):
            statinfo['status'] = int(status.split(" ", 1)[0])
            return start_response(status, headers, exc_info)

        start = time.time()
        env['tags'] = ""
        env['write_audit'] = partial(self.write_audit, env)
        result = self.app(env, my_response)
        responsetime = time.time() - start
        if 'JS_AUDITKEY' in env:
            tags = env.get('tags', '')
            self.client.audit.updateSearch({'guid': env['JS_AUDITKEY']}, {
                '$set': {
                    'tags': tags,
                    'result': get_result(result),
                    'responsetime': responsetime,
                    'statuscode': statinfo['status']
                }
            })
        elif statinfo['status'] >= 400:
            self.write_audit(env, result, responsetime, statinfo['status'])
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
                ctx.env['tags'] = self.tags_str
            user = ctx.env['beaker.session']['user']
            if self.groups:
                userobj = j.core.portal.active.auth.getUserInfo(user)
                groups = set()
                if userobj:
                    groups = set(userobj.groups)
                if not groups.intersection(self.groups):
                    raise exceptions.Forbidden('User %s has no access. If you would like to gain access please contact your adminstrator' % user)

            if self.audit:
                ctx.env['write_audit']()
            return func(*args, **kwargs)
        return wrapper
