def main(j, args, params, tags, tasklet):

    page = args.page

    logpath = args.requestContext.params.get('logpath')
    templatepath = args.requestContext.params.get('templatepath')
    installedpath = args.requestContext.params.get('installedpath')
    metapath = args.requestContext.params.get('metapath')
    domain = args.requestContext.params.get('domain')
    name = args.requestContext.params.get('servicename')
    instance = args.requestContext.params.get('instance')

    instancestr =  ':%s' % instance if instance else ''
    page.addHeading("Code editors for %s:%s%s" % (domain, name, instancestr), 2)

    for representation, path in (('Installed', installedpath), ('Logs', logpath), ('Template', templatepath), ('Metadata', metapath)):
        if not path or not j.system.fs.exists(path):
            continue
        page.addHeading("%s" % representation, 3)
        page.addExplorer(path, readonly=True, tree=True, height=300)

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
