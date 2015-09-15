def main(j, args, params, tags, tasklet):
    page = args.page
    action = args.requestContext.params.get('action', 'install')
    aysid = args.requestContext.params.get('aysid')
    instance = args.requestContext.params.get('instance', 'main')
    parent = args.requestContext.params.get('parent', '')

    installedagent = j.application.getAppHRDInstanceNames('agentcontroller2_client')
    if not installedagent:
        if not installedagent:
            page.addMessage('No agentcontroller2_client installed on node')
            params.result = page
            return params

    acc = j.clients.ac.getByInstance(installedagent[0])


    installargs = args.requestContext.params.copy()
    for param in ('name', 'rights', 'space', 'instance', 'action', 'path', 'aysid', 'parent'):
        installargs.pop(param)


    ays = j.atyourservice.getTemplatefromSQL(templateid=aysid)

    if not ays:
        page.addMessage("h3. Could not find template on node")
        params.result = page
        return params

    ays = ays[0]

    installargs = ['%s:%s' % (key, value) for key, value in installargs.items()]

    result = acc.execute(j.application.whoAmI.gid, j.application.whoAmI.nid, 'ays', ['install', '-n', ays.name, '-d', ays.domain,
                '-i', instance, '--data', ' '.join(installargs), '--parent', parent])

    page.addMessage('Service %s:%s:%s install job (%s) has started' % (ays.domain, ays.name, instance, result.id))


    params.result = page
    return params

def match(j, args, params, tags, tasklet):
    return True
