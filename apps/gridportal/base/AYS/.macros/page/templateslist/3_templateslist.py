def main(j, args, params, tags, tasklet):

    page = args.page
    attributes = "class='nav nav-list' style='-moz-column-count: 3; -webkit-column-count:3; column-count:3;'"

    domain = args.tags.tagGet('domain', '')

    from JumpScale.baselib.atyourservice import AYSdb

    # TODO ---> get out of factory
    sql = j.db.sqlalchemy.get(sqlitepath=j.dirs.varDir+"/AYS.db", tomlpath=None, connectionstring='')

    templateslist = sql.session.query(AYSdb.Template).all()

    if not templateslist:
        j.atyourservice.loadServicesInSQL()
        templateslist = sql.session.query(AYSdb.Template).all()

    if not templateslist:
        page.addMessage('No templates to display.')
        params.result = page
        return params

    templates = dict()
    for ays in templateslist:
        if ays.domain not in templates:
            templates[ays.domain] = list()
        templates[ays.domain].append(ays)

    for domain in sorted(templates.keys()):
        page.addHeading(domain, 2)
        for temp in sorted(templates[domain], key=lambda x: x.name.lower()):
            href = '/AYS/Template?domain=%s&name=%s&aysid=%s' % (domain, temp.name, temp.id)
            page.addBullet("<a href='%s'>%s</a>" % (href, temp.name), attributes=attributes)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
