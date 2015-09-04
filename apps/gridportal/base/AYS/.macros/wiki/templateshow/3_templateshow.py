
def main(j, args, params, tags, tasklet):
    domain = args.getTag('domain')
    name = args.getTag('name')
    aysid = args.getTag('aysid')

    ays = j.atyourservice.getTemplatefromSQL(templateid=aysid, reload=False)

    out = ''
    if not ays:
        out = "h3. Could not find template:%s %s" % (domain, name)
        params.result = (out, args.doc)
        return params

    ays = ays[0]

    out += "h2. Template: %s\n" % ays.name

    fields = [('Domain', 'domain'), ('Name', 'name'), ('Metadata', 'metapath')]

    for representation, field in fields:
        out += '|*%s*|%s|\n' % (representation, ays.__getattribute__(field))

    instances = ays.instances
    if instances:
        out += "h3. Installed Instances\n"
        for instance in instances:
            service = j.atyourservice.getServicefromSQL(domain=ays.domain, name=ays.name, instance=instance.instance)
            if service:
                href = '/AYS/Service?domain=%s&name=%s&instance=%s&aysid=%s' % (ays.domain, ays.name, instance.instance, service[0].id)
            else:
                # TODO find closest match?
                href = instance
            out += "* [%s|%s]\n" % (instance.instance, href)

    dependencies = sorted(ays.dependencies, key=lambda x: x.name)
    if dependencies:
        out += "h3. Dependencies\n"
        for dep in dependencies:
            href = '/AYS/Template?domain=%s&name=%s&aysid=%s' % (dep.domain, dep.name, dep.id)
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
|[Template Code Editors|/AYS/AYSCodeEditors?metapath=%(metapath)s&domain=%(domain)s&servicename=%(name)s]|
""" % ays.__dict__

    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
