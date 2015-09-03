
def main(j, args, params, tags, tasklet):
    domain = args.getTag('domain')
    name = args.getTag('name')
    instance = args.getTag('instance')
    aysid = args.getTag('aysid')

    ays = j.atyourservice.getServicefromSQL(serviceid=aysid, reload=False)

    out = ''
    if not ays:
        out = "h3. Could not find service:%s %s (%s)" % (domain, name, instance)
        params.result = (out, args.doc)
        return params

    ays = ays[0]

    out += "h2. Service: %s\n" % ays.name

    # for i in info:
    fields = [('Domain', 'domain'), ('Name', 'name'), ('Instance', 'instance'), ('Installed', 'isInstalled'),
              ('Path', 'path'), ('Template Path', 'templatepath'), ('Parent', 'parent'), ('No Remote', 'noremote'),
              ('Command', 'cmd'), ('Log Path', 'logPath'), ('Priority', 'priority'), ('Latest', 'isLatest')]

    for representation, field in fields:
        out += '|*%s*|%s|\n' % (representation, ays.__getattribute__(field))
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
    for hrditem in ays.hrd:
        out += '* %s: %s\n' % (hrditem.key, hrditem.value)


    out += """
\n
h3. Files\n
|[Service Code Editors|/AYS/AYSCodeEditors?logpath=%(logPath)s&templatepath=%(templatepath)s&installedpath=%(path)s&domain=%(domain)s&servicename=%(name)s&instance=%(instance)s]|
""" % ays.__dict__

    if ays.isInstalled:
        out += """
    h3. Actions

    |[Start|/AYS/ServiceAction?action=start&aysid=%(id)s]|
    |[Stop|/AYS/ServiceAction?action=stop&aysid=%(id)s]|
    |[Restart|/AYS/ServiceAction?action=restart&aysid=%(id)s]|
    |[Update|/AYS/ServiceAction?action=update&aysid=%(id)s]|
    """ % {'id': aysid}

    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
