

def main(j, args, params, tags, tasklet):
    import json
    params.merge(args)
    doc = params.doc

    domain = args.getTag('domain') or ''
    name = args.getTag('sname') or ''
    instance = args.getTag('instance') or ''
    action = args.getTag('action')

    acc = j.clients.agentcontroller.getByInstance('main')
    result = acc.executeJumpscript('jumpscale', 'ays_action', nid=j.application.whoAmI.nid,
                                   gid=j.application.whoAmI.gid, role='master',
                                   args={'domain': domain, 'sname': name, 'instance': instance, 'action': action})

    if result['state'] == 'ERROR':
        params.result = ('An error has occured', doc)
        return params

    params.result = ('Action has been successfully performed', doc)
    return params



def match(j, args, params, tags, tasklet):
    return True
