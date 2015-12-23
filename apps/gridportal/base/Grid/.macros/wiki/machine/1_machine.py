import datetime

def main(j, args, params, tags, tasklet):
    params.result = (args.doc, args.doc)
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing machine id param "id"'
        params.result = (out, args.doc)
        return params

    if not j.core.portal.active.osis.exists('system', 'machine', guid):
        args.doc.applyTemplate({})
        return params
    machine = j.core.portal.active.osis.get('system', 'machine', guid)
    node = j.core.portal.active.osis.get('system', 'node', machine['nid'])
    machine['nodename'] = node['name']
    if not j.core.portal.active.osis.exists('system', 'grid', machine['gid']):
        machine['gridname'] = str(machine['gid'])
    else:
        machine['gridname'] = j.core.portal.active.osis.get('system', 'grid', machine['gid'])['name']
    obj = machine
    for attr in ['roles', 'ipaddr']:
        obj[attr] = ', '.join([str(x) for x in obj[attr]]) 

    netaddr = obj['netaddr']
    netinfo = ''
    #for k, v in netaddr.iteritems():
    #    netinfo += 'mac address: %s, interface: %s, ip: %s<br>' % (k, v[0], v[1])
    #obj['netaddr'] = netinfo

    obj['lastcheck'] = datetime.datetime.fromtimestamp(obj['lastcheck']).strftime('%Y-%m-%d %H:%M:%S')
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
