def main(j, args, params, tags, tasklet):
    page = args.page
    modifier = j.html.getPageModifierGridDataTables(page)

    filters = dict()
    for tag, val in args.tags.tags.iteritems():
        val = args.getTag(tag)
        if tag == 'from' and val:
            filters['epoch'] = {'$gte': j.base.time.getEpochAgo(val)}
        elif tag == 'to' and val:
            filters['epoch'] = {'$lte': j.base.time.getEpochAgo(val)}
        elif tag in ('gid', 'nid') and val:
            filters[tag] = int(val)
        elif val:
            filters[tag] = val

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        return '[%s|log?id=%s]' % (time, row['guid'])

    def cleanUp(row, field):
        return j.html.escape(row[field])

    nidstr = '[%(nid)s|/grid/grid node?id=%(nid)s&gid=%(gid)s]'
    fields = [
        {'id': 'epoch',
         'name': 'Start Time',
         'value': makeTime,
         'type': 'date'},
        {'id': 'appname',
         'name': 'App Name',
         'value': 'appname'},
        {'id': 'category',
         'name': 'Category',
         'value': 'category'},
        {'id': 'message',
         'name': 'Message',
         'value': 'message'},
        {'id': 'level',
         'name': 'Level',
         'type': 'int',
         'value': 'level'},
        {'id': 'nid',
         'name': 'Node ID',
         'value': nidstr},
    ]
    tableid = modifier.addTableFromModel('system', 'log', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
