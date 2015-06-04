
def main(j, args, params, tags, tasklet):
    import json
    domain = args.getTag('domain') or ''
    name = args.getTag('sname') or ''
    instance = args.getTag('instance') or ''

    acc = j.clients.agentcontroller.getByInstance('main')
    result = acc.executeJumpscript('jumpscale', 'ays_list', nid=j.application.whoAmI.nid,
                                   gid=j.application.whoAmI.gid, role='master',
                                   args={'domain': domain, 'name': name, 'instance': instance})

    if result['state'] != 'OK':
        out = 'Could not find Service with domain "%s", name "%s" and instance "%s"' % (
            domain, name, instance)
        params.result = (out, args.doc)
        return params

    obj = json.loads(result['result'][0])
    
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
