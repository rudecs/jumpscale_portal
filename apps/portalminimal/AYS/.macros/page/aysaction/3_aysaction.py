def main(j, args, params, tags, tasklet):
    page = args.page
    action = args.requestContext.params.get('action')
    aysid = args.requestContext.params.get('aysid')

    from JumpScale.baselib.atyourservice import AYSdb

    # TODO ---> get out of factory
    sql = j.db.sqlalchemy.get(sqlitepath=j.dirs.varDir+"/AYS.db", tomlpath=None, connectionstring='')

    ays = sql.session.query(AYSdb.Service).get(aysid)

    if not ays:
        page.addMessage("h3. Could not find service:%s %s (%s) installed on node:%s" % (domain, name, instance, nid))
        params.result = page
        return params

    parent = None
    if ays.parent:
        parent = sql.session.query(AYSdb.Service).get(ays.parent)
    service = j.atyourservice.get(domain=ays.domain, name=ays.name, instance=ays.instance, parent=parent)

    try:
        getattr(service, action)()
        state = 'success'
    except Exception, e:
        state = 'failure'

    page.addMessage('Action %s on service %s:%s:%s was a %s' % (action, ays.domain, ays.name, ays.instance, state))


    params.result = page
    return params

def match(j, args, params, tags, tasklet):
    return True
