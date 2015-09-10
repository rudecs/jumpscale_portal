def main(j, args, params, tags, tasklet):
    page = args.page
    action = args.requestContext.params.get('action')
    aysid = args.requestContext.params.get('aysid')


    installedagent = j.application.getAppHRDInstanceNames('agentcontroller2_client')
    if not installedagent:
        if not installedagent:
            page.addMessage('No agentcontroller2_client installed on node')
            params.result = page
            return params

    acc = j.clients.ac.getByInstance(installedagent[0])

    ays = j.atyourservice.getServicefromSQL(serviceid=aysid)

    if not ays:
        page.addMessage("h3. Could not find service installed on node")
        params.result = page
        return params
    ays = ays[0]

    parent = ''
    if ays.parent:
        parent = sql.session.query(AYSdb.Service).get(ays.parent)
        parent = '%s__%s__%s' % (parent.domain, parent.name, parent.instance)

    result = acc.execute(j.application.whoAmI.gid, j.application.whoAmI.nid, 'ays', [action, '-n', ays.name, '-d', ays.domain,
                '-i', ays.instance, '--parent', parent])

    page.addMessage('Action %s on service %s:%s:%s is triggered in job %s' % (action, ays.domain, ays.name, ays.instance, result.id))

    params.result = page
    return params

def match(j, args, params, tags, tasklet):
    return True
