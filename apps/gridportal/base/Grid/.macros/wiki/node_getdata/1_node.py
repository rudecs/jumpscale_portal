
try:
    import ujson as json
except:
    import json
def main(j, args, params, tags, tasklet):

    params.result = (args.doc, args.doc)
    #macro puts obj info as params on doc, when show used as label, shows the content of the obj in nicely structured code block
    nid = args.getTag('id')
    gid = args.getTag('gid')
    if not nid or not gid:
        args.doc.applyTemplate({})
        return params
    gid = int(gid)
    osis = j.core.portal.active.osis

    node = None
    if osis.exists('system', 'node', '%s_%s' % (gid, nid)):
        node = osis.get('system', 'node', '%s_%s' % (gid, nid))
    grid = {'name': 'N/A'}
    if osis.exists('system', 'grid', gid):
        grid = osis.get('system', 'grid', gid)
    if not node:
        args.doc.applyTemplate({})
        return params

    #obj is a dict
    node["ipaddr"]=", ".join(node["ipaddr"])
    node["roles"]=", ".join(node["roles"])

    r=""
    for netitem in node["netaddr"]:
        dev = netitem['name']
        ip = netitem['ip']
        mac = netitem['mac']
        r+="|%-15s | %-20s | %s| \n"%(dev,mac,ip)

    node["netaddr"]=r
    node['gridname'] = grid['name']
    node['nodename'] = node['name']

    args.doc.applyTemplate(node)
    return params


def match(j, args, params, tags, tasklet):
    return True


