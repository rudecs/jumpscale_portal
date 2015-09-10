
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

    asks = [{line.split('=')[0].strip():line.split('=')[1].strip()} for line in ays.instancehrd.splitlines() if line.strip() and not line.startswith('#') and '@ASK' in line]
    askparams = '\n' if asks else ''
    for ask in asks:
        for key, value in ask.items():
            tags = j.core.tags.getObject(value)
            askparams += '   - name: %s\n' % key
            descr = '%s' % (tags.tagGet('descr', ''))
            askparams += '     default: "%s"\n' % tags.tagGet('default', '')
            askparams += '     label: "%s"\n' % (descr or key)
            askparams += '     type: text\n'



    out += """
{{actions:
- display: Install
  action: /AYS/TemplateAction?action=install
  input:
   - instance
   - name: parent
     type: text
     label: parent (should be in the format domain__name__instance)%s
  data: 
    aysid: %s
}}
    """ % (askparams, aysid)

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

    if ays.metapath or not j.system.fs.exists(ays.metapath):
        out += "h3. Files\n"
        path = ays.metapath.replace(j.dirs.baseDir, '$base')
        path = path.replace(j.dirs.codeDir, '$codedir')
        out += "h5. MetaPath\n"
        out += "{{explorer: ppath:%s height:200}}\n" % path

    params.result = (out, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
