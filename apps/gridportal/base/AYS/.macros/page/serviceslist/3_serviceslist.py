def main(j, args, params, tags, tasklet):

    page = args.page
    attributes = "class='nav nav-list' style='-moz-column-count: 3; -webkit-column-count:3; column-count:3;'"

    domain = args.tags.tagGet('domain', '')
    nid = args.tags.tagGet('nid', j.application.whoAmI.nid)

    from JumpScale.baselib.atyourservice import AYSdb

    #TODO ---> get out of factory
    sql = j.db.sqlalchemy.get(sqlitepath=j.dirs.varDir+"/AYS.db",tomlpath=None,connectionstring='')

    serviceslist = sql.session.query(AYSdb.Service).all()

    if not serviceslist:
        j.atyourservice.loadServicesInSQL()
        serviceslist = sql.session.query(AYSdb.Service).all()

    if not serviceslist:
        page.addMessage('No services to display.')
        params.result = page
        return params

    services = dict()
    for ays in serviceslist:
        if ays.domain not in services:
            services[ays.domain] = list()
        services[ays.domain].append(ays)
  
    for domain in sorted(services.keys()):
        page.addHeading(domain, 2)
        for ays in sorted(services[domain], key=lambda x: x.name.lower()):
            href = '/AYS/service?domain=%s&name=%s&instance=%s&aysid=%s' % (domain, ays.name, ays.instance, ays.id)
            icon = 'icon-ok' if ays.isInstalled else 'icon-remove'
            page.addBullet("<a href='%s'><i class='%s'></i> %s</a>" % (href, icon, ays.name), attributes=attributes)

        

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
