import datetime

def main(j, args, params, tags, tasklet):
    try:
        import ujson as json
    except:
        import json

    page = args.page

    filters = dict()
    for tag, val in args.tags.tags.iteritems():
        val = args.getTag(tag)
        if not val or val.startswith('$'):
            continue
        elif tag in ('nid', 'gid') and val:
            filters[tag] = int(val)
        elif val:
            filters[tag] = val

    modifier = j.html.getPageModifierGridDataTables(page)

    def makeLink(row, field):
        return '[%s|/grid/virtual machine?guid=%s]' % (row['name'], row['guid'])

    def makeResult(row, field):
        result = row[field]
        try:
            result = json.loads(result)
        except:
            pass
        return j.html.escape(str(result))

    def makeMac(row, field):
        return '<br/>'.join(row[field])

    def makeNode(row, field):
        return '[%s|/grid/grid node?id=%s&gid=%s]' % (row['nid'], row['nid'], row['gid'])


    fieldnames = ['Name', 'Status', 'Active', 'Memory', 'MAC Address', 'Node', 'CPU Cores']
    fieldvalues = [makeLink, "state", "active", "mem", makeMac, makeNode, "cpucore"]
    fieldids = ["name", "state", "active", "mem", "netaddr", "nid", "cpucore"]
    tableid = modifier.addTableForModel('system', 'machine', fieldids, fieldnames, fieldvalues, nativequery=filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
