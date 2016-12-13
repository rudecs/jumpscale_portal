def main(j, args, params, tags, tasklet):
    import copy
    page = args.page
    hrd = j.application.instanceconfig

    menulinks = copy.deepcopy(hrd.getListFromPrefix('instance.navigationlinks'))
    if not menulinks:
        spacelinks = j.core.portal.active.getSpaceLinks(args.requestContext)
        menulinks = []
        for name, url in spacelinks.iteritems():
            menulinks.append({'name': name, 'url': url, 'theme': 'light', 'external': 'false'})
    else:
        for section in menulinks:
            if 'children' in section:
                children = hrd.getDict(section['children'])
                section['children'] = []
                for key, value in children.iteritems():
                    section['children'].append({'url': value, 'name': key})

    groups = j.core.portal.active.getGroupsFromCTX(args.requestContext)
    for portal in menulinks[:]:
        scope = portal.get('scope')
        if scope and scope not in groups:
            menulinks.remove(portal)
            continue
        if 'children' not in portal:
            portal['children'] = list()
        external = portal.get('external', 'false').lower()
        portal['external'] = external
        if external == 'false':
            spacename = j.system.fs.getBaseName(portal['url']).lower()
            if spacename in j.core.portal.active.spacesloader.spaces:
                space = j.core.portal.active.spacesloader.spaces[spacename]
                docprocessor = space.docprocessor
                doc = docprocessor.name2doc.get('home')
                if not doc:
                    doc = docprocessor.name2doc.get(spacename)
                if not doc:
                    continue
                if doc.navigation:
                    navigation = doc.navigation.strip()
                    for line in navigation.splitlines():
                        line = line.strip()
                        if line.startswith('#'):
                            continue
                        try:
                            name, link = line.split(':', 1)
                        except:
                            continue
                        portal['children'].append({'url': link, 'name': name})

    params.result = page

    script = j.core.portal.active.templates.render('system/hamburgermenu/script.js')
    page.addJS(jsContent=script, header=False)
    style = j.core.portal.active.templates.render('system/hamburgermenu/style.css')
    page.addCSS(cssContent=style)

    if not menulinks or len(menulinks) == 1 and not menulinks[0]['children']:
        return params

    hrdListHTML = j.core.portal.active.templates.render('system/hamburgermenu/structure.html', menulinks=menulinks)
    page.addMessage('''<script id="portalsHamburgerStructure" type="text/x-jQuery-tmpl">%s</script>''' % hrdListHTML)

    return params


def match(j, args, params, tags, tasklet):
    return True
