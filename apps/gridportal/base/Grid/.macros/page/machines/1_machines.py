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

    def makeMac(row, field):
        return '<br/>'.join(row[field])

    def makeNode(row, field):
        return '[%s|/grid/grid node?id=%s&gid=%s]' % (row['nid'], row['nid'], row['gid'])


    fields = [
            {'name': 'Name',
             'id': 'name',
             'value': makeLink,
             'type': 'text'
            },
            {'name': 'Status',
             'id': 'state',
             'value': 'state'
            },
            {'name': 'Memory (KiB)',
             'id': 'mem',
             'value': 'mem',
             'type': 'int'
            },
            {'name': 'Mac Address',
             'id': 'netaddr',
             'value': makeMac,
             'sortable': False,
             'filterable': False,
            },
            {'name': 'Node',
             'id': 'nid',
             'value': makeNode,
            },
            {'name': 'CPU Cores',
             'id': 'cpucore',
             'value': 'cpucore',
             'type': 'int'
            },
    ]
    tableid = modifier.addTableFromModel('system', 'machine', fields, nativequery=filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
