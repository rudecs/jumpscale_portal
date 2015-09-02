def main(j, args, params, tags, tasklet):

    page = args.page
    attributes = "class='nav nav-list' style='-moz-column-count: 3; -webkit-column-count:3; column-count:3;'"

    refresh = j.tools.text.getBool(args.tags.tagGet('refresh', False))

    page.addLink(description='Reload templates', link='/AYS/templates?refresh=True')

    templateslist = j.atyourservice.getTemplatefromSQL(reload=refresh)

    if not templateslist and not refresh:
        templateslist = j.atyourservice.getTemplatefromSQL(reload=True)

    if not templateslist:
        page.addMessage('No templates to display.')
        params.result = page
        return params

    templates = dict()
    for ays in templateslist:
        templates.setdefault(ays.type, dict())
        templates[ays.type].setdefault(ays.domain, list())
        templates[ays.type][ays.domain].append(ays)
  
    for type in sorted(templates.keys()):
        page.addHeading(type, 2)
        for domain in sorted(templates[type].keys()):
            page.addHeading(domain, 3)
            for ays in sorted(templates[type][domain], key=lambda x: x.name.lower()):
                href = '/AYS/template?domain=%s&name=%s&aysid=%s' % (domain, ays.name, ays.id)
                page.addBullet("<a href='%s'></i> %s</a>" % (href, ays.name), attributes=attributes)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
