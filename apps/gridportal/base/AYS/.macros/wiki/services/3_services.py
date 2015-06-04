
def main(j, args, params, tags, tasklet):
    import json
    params.merge(args)
    doc = params.doc

    domain = args.getTag('domain') or ''
    name = args.getTag('name') or ''
    # category = args.getTag('category')

    acc = j.clients.agentcontroller.getByInstance('main')
    result = acc.executeJumpscript('jumpscale', 'ays_list', nid=j.application.whoAmI.nid,
                                      gid=j.application.whoAmI.gid, role='master')

    if result['state'] != 'OK':
        params.result = ('An error has occured', doc)
        return params

    services = result['result']
    out = ['{{datatables_use}}']
    out.append('||Domain||Name||Instance||')

    for service in services.values():
        service = json.loads(service)
        out.append("|%(domain)s|[%(name)s|service?domain=%(domain)s&sname=%(name)s]|%(instance)s|" % service)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
