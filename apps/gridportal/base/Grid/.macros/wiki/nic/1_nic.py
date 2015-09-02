import datetime

def main(j, args, params, tags, tasklet):
    guid = args.getTag('id')
    if not guid:
        out = 'Missing NIC guid param "guid"'
        params.result = (out, args.doc)
        return params

    nic = j.core.portal.active.osis.get('system', 'nic', guid)
    if not nic:
        params.result = ('NIC with guid %s not found' % guid, args.doc)
        return params

    nic['lastcheck'] = datetime.datetime.fromtimestamp(nic['lastcheck']).strftime('%Y-%m-%d %H:%M:%S')
    nic['ipaddr'] = ', '.join([str(x) for x in nic['ipaddr']])

    args.doc.applyTemplate(nic)
    params.result = (args.doc, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
