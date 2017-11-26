
def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.iteritems():
        if tag in ('gid', ) and val and not val.startswith("$$"):
            filters['gid'] = int(val)
    if args.getTag('roles'):
        filters['roles'] = args.getTag('roles')

    namelink = '[%(name)s|/grid/Grid Node?id=%(id)s&gid=%(gid)s]'
    fields = [
            {'name': 'Grid ID',
             'id': 'gid',
             'value': 'gid',
            },
            {'name': 'Name',
             'id': 'name',
             'value': namelink,
            },
            {'name': 'Grid Node ID',
             'id': 'id',
             'value': 'id',
            },
            {'name': 'IP Address',
             'id': 'ipaddr',
             'value': 'ipaddr',
             'type': 'text',
            },
            {'name': 'Roles',
             'id': 'roles',
             'type': 'text',
             'value': 'roles',
            },
    ]
    tableid = modifier.addTableFromModel('system', 'node', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)

    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
