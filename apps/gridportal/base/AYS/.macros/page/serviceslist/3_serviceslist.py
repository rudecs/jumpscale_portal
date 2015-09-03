def main(j, args, params, tags, tasklet):

    page = args.page
    attributes = "class='nav nav-list' style='-moz-column-count: 3; -webkit-column-count:3; column-count:3;'"

    refresh = j.tools.text.getBool(args.tags.tagGet('refresh', False))

    page.addLink(description='Reload services', link='/AYS/services?refresh=True')

    serviceslist = j.atyourservice.getServicefromSQL(reload=refresh)

    if not serviceslist and not refresh:
        serviceslist = j.atyourservice.getServicefromSQL(reload=True)

    if not serviceslist:
        page.addMessage('No services to display.')
        params.result = page
        return params

    services = dict()
    for ays in serviceslist:
        services.setdefault(ays.type, dict())
        services[ays.type].setdefault(ays.domain, list())
        services[ays.type][ays.domain].append(ays)
  
    for type in sorted(services.keys()):
        page.addHeading(type, 2)
        for domain in sorted(services[type].keys()):
            page.addHeading(domain, 3)
            for ays in sorted(services[type][domain], key=lambda x: x.name.lower()):
                href = '/AYS/service?domain=%s&name=%s&instance=%s&aysid=%s' % (domain, ays.name, ays.instance, ays.id)
                icon = 'icon-ok' if ays.isInstalled else 'icon-remove'
                page.addBullet("<a href='%s'><i class='%s'></i> %s</a>" % (href, icon, ays.name), attributes=attributes)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
