
def main(j, args, params, tags, tasklet):
    domain = args.getTag('domain')
    name = args.getTag('name')
    instance = args.getTag('instance')
    nid = args.getTag('nid')

    actor = j.apps.actorsloader.getActor('system', 'servicemanager')

    if not nid:
        nid = j.application.whoAmI.nid

    jp = actor.getServices(nid=nid, domain=domain, pname=name, instance=instance)
    out = ''
    if not jp:
        out= "h3. Could not find service:%s %s (%s) installed on node:%s"%(domain,name,instance,nid)
        params.result = (out, args.doc)
        return params

    # if result == False:
    #     page.addHTML("<script>window.open('/AYS/AYS', '_self', '');</script>" )
    #     params.result = page
    #     return params
   
    jp = actor.getServiceInfo(nid=nid, domain=domain, pname=name, instance=instance)
    
    out += "h2. Service: %s\n"%jp['name']
    # for i in info:
    out += '|*Domain*|%s|*Installed*|%s|\n' % (jp['domain'], jp['isInstalled'])
    out += "|*instance*|%s|*Supported platforms*|%s|\n" % (jp['instance'], ', '.join([x for x in jp['supportedPlatforms']]))
    out += '|*Build Number*|%s|||' % jp['buildNr']

    out += 'h3. Description\n'
    descr = jp['description'].replace('$(jp.name)', jp['name'])
    descr = descr.replace('$(jp.instance)', jp['instance'])
    descr = descr.replace('$(jp.description)', '')
    out +=  descr + "\n"

    out+="h3. Dependencies\n"
    dependencies = sorted(jp['dependencies'], key=lambda x: x.name)
    for dep in dependencies:
        href = '/AYS/ServiceShow?nid=%s&domain=%s&name=%s&instance=%s' % (nid, dep.domain, dep.name, dep.instance)
        out+="* [%s|%s]\n" % (href, dep.name)

    jp['nid'] = nid
    out+="""
h3. Explorers

|[Service Code Editors|/AYS/ServiceCodeEditors?nid=%(nid)s&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Service Browser|/AYS/ServiceBrowser?nid=%(nid)s&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Service Files|/AYS/ServiceFiles?nid=%(nid)s&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
""" % jp

    out+="""
h3. Actions

|[Start|/AYS/ServiceAction?action=start&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Stop|/AYS/ServiceAction?action=stop&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Restart|/AYS/ServiceAction?action=restart&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Update|/AYS/ServiceAction?action=update&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Package|/AYS/ServiceAction?action=service&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
|[Upload|/AYS/ServiceAction?action=upload&domain=%(domain)s&name=%(name)s&instance=%(instance)s]|
""" % jp

    params.result = (out, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
