
def main(j, args, params, tags, tasklet):
    import json
    params.merge(args)
    doc = params.doc

    domain = args.getTag('domain') or ''
    name = args.getTag('name') or ''
    # category = args.getTag('category')

    acc = j.clients.agentcontroller.getByInstance('main')
    result = acc.executeJumpscript('jumpscale', 'templates_action', nid=j.application.whoAmI.nid,
                                      gid=j.application.whoAmI.gid, role='master')['result']

    if 'code' in result.keys():
        params.result = ('An error has occured', doc)
        return params

    templates = result
    out = ['{{datatables_use}}']
    out.append('||Domain||Name||Metadata Path||Instances||')

    for template in templates.values():
        template = json.loads(template)
        template['instances'] = ', '.join(template['instances']) if template['instances'] else 'Not Installed'
        out.append("|%(domain)s|[%(name)s|template?domain=%(domain)s&name=%(name)s]|%(metapath)s|%(instances)s|" % template)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
