
def main(j, args, params, tags, tasklet):
    import json

    domain = args.getTag('domain')
    name = args.getTag('name')
    instance = args.getTag('instance')
    aysid = args.getTag('aysid')

    ays = j.atyourservice.getServicefromSQL(serviceid=aysid, reload=False)

    out = ''
    if not ays or not ays[0]:
        out = "h3. Could not find service:%s %s (%s)" % (domain, name, instance)
        params.result = (out, args.doc)
        return params

    ays = ays[0]

    out += "h2. Service: %s\n" % ays.name

    # for i in info:
    fields = [('Domain', 'domain'), ('Name', 'name'), ('Instance', 'instance'), ('Installed', 'isInstalled'),
              ('Path', 'path'), ('Template Path', 'templatepath'), ('No Remote', 'noremote'),
              ('Command', 'cmd'), ('Log Path', 'logPath'), ('Priority', 'priority'), ('Latest', 'isLatest')]

    for representation, field in fields:
        out += '|*%s*|%s|\n' % (representation, ays.__getattribute__(field))

    if ays.parent:
        out += '|*Parent*|[parent|/AYS/Service?aysid=%s]|\n' % (ays.parent)
    template = j.atyourservice.getTemplatefromSQL(metapath=ays.templatepath)
    if template:
        out += '|*Template*|[%s template|/AYS/Template?domain=%s&name=%s&aysid=%s]|\n' % (template[0].name, template[0].domain, template[0].name, template[0].id)  


    dependencies = sorted(ays.dependencies, key=lambda x: x.order)
    if dependencies:
        out += "h3. Dependencies\n"
        for dep in dependencies:
            href = '/AYS/Service?domain=%s&name=%s&instance=%s&aysid=%s' % (dep.domain, dep.name, dep.instance, dep.id)
            out += "* [%s|%s]\n" % (dep.name, href)


    if ays.processes:
        out += "h3. Processes\n"
        count = 1
        for process in ays.processes:
            out += '* *Process %s*\n' % count
            processtable = ['** *%s*: %s\n' % (key, value) for key, value in process.__dict__.items() if key not in ('id', '_sa_instance_state')]
            out += ''.join(processtable)
            count += 1

    out += "h3. HRD\n"
    exports = list()
    for hrditem in ays.hrd:
        if hrditem.key.startswith('service.git.export'):
            exports.append(hrditem)
        else:
            out += '* %s: %s\n' % (hrditem.key, hrditem.value)
    if exports:
        out += "h3. Service Exports\n"
        out += "{{code:\n"
        for export in exports:
            vals = ['\t%s:%s' % (key, value) for key, value in json.loads(export.value).items()]
            out += "%s:\n%s" % (export.key, '\n'.join(vals))
        out += "}}\n"


    children = json.loads(ays.children)
    if children:
        out += "h3. Children\n"
        for cdomain, domainchildren in children.items():
            out += '* %s\n' % cdomain
            for child in domainchildren:
                childsql = j.atyourservice.getServicefromSQL(domain=cdomain, name=child)
                if childsql:
                    out += '** [%s|/AYS/Service?domain=%s&name=%s&aysid=%s]\n' % (child, cdomain, child, childsql[0].id)

    out += "h3. Files\n"
    for representation, path in (('Installed', ays.path), ('Logs', ays.logPath), ('Template', ays.templatepath)):
        if not path or not j.system.fs.exists(path):
            continue
        path = path.replace(j.dirs.baseDir, '$base')
        path = path.replace(j.dirs.codeDir, '$codedir')
        out += "h5. %s\n" % representation

        out += "{{explorer: ppath:%s height:200}}\n" % path

    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
