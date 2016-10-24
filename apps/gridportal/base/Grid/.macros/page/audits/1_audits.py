import datetime

def main(j, args, params, tags, tasklet):
    try:
        import ujson as json
    except:
        import json

    page = args.page

    filters = dict()
    fieldids = ['timestamp', 'user', 'call', 'statuscode']
    for tag, val in args.tags.tags.iteritems():
        if tag in fieldids:
            val = args.getTag(tag)
            filters[tag] = val

    modifier = j.html.getPageModifierGridDataTables(page)

    def makeTime(row, field):
        time = modifier.makeTime(row, field)
        link = "[%s|audit?id=%s]" % (time, row['guid'])
        return link

    fields = [
        {'name': 'Time',
         'type': 'date',
         'id': 'timestamp',
         'value': makeTime},
        {'name': 'User',
         'id': 'user',
         'value': 'user'},
        {'name': 'Call',
         'id': 'call',
         'value': 'call'},
        {'name': 'Status Code',
         'id': 'statuscode',
         'type': 'int',
         'value': 'statuscode'},
    ]
    tableid = modifier.addTableFromModel('system', 'audit', fields, filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
