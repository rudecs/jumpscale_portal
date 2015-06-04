

def main(j, args, params, tags, tasklet):
    import json
    params.merge(args)
    doc = params.doc

    acc = j.clients.agentcontroller.getByInstance('main')
    result = acc.executeJumpscript('jumpscale', 'ays_status', nid=j.application.whoAmI.nid,
                                   gid=j.application.whoAmI.gid, role='master')

    if result['state'] == 'ERROR':
        params.result = ('An error has occured', doc)
        return params

    rcl = j.clients.redis.getByInstance('system')
    services = rcl.hgetall('ays:services:status')
    out = ['{{datatables_use}}']
    out.append('||Domain||Name||Instance||Priority||Status||Ports||')

    for service in services.values():
        service = json.loads(service)
        out.append("|%(domain)s|[%(name)s|service?domain=%(domain)s&sname=%(name)s]|%(instance)s|%(priority)s|%(status)s|%(ports)s|" % service)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
