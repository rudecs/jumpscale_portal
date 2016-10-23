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
        if not val:
            continue
        if tag == 'from' and val:
            filters['timeStart'] = {'$gte': j.base.time.getEpochAgo(val)}
        elif tag == 'to' and val:
            filters['timeStop'] = {'$lte': j.base.time.getEpochAgo(val)}
        elif tag == 'organization':
            filters['category'] = val
        elif tag == 'jsname':
            filters['cmd'] = val
        elif tag in ('nid', 'gid') and val:
            filters[tag] = int(val)
        elif tag == 'filter':
            filter = json.loads(val or 'null')
            filters.update(filter)
        elif val:
            filters[tag] = val

    modifier = j.html.getPageModifierGridDataTables(page)

    def makeLink(row, field):
        time = modifier.makeTime(row, field)
        return '[%s|/grid/job?id=%s]' % (time, row['guid'])

    def makeResult(row, field):
        result = row[field]
        try:
            result = json.loads(result)
        except:
            pass
        return j.html.escape(str(result))

    fields = [
        {'name': 'Create Time',
         'value': makeLink,
         'type': 'date',
         'id': 'timeCreate'},
        {'name': 'Start',
         'value': modifier.makeTimeOnly,
         'id': 'timeStart'},
        {'name': 'Stop',
         'value': modifier.makeTimeOnly,
         'id': 'timeStop'},
        {'name': 'Command',
         'value': 'cmd',
         'id': 'cmd'},
        {'name': 'Queue',
         'value': 'queue',
         'id': 'queue'},
        {'name': 'State',
         'value': 'state',
         'id': 'state'},
    ]
    tableid = modifier.addTableFromModel('system', 'job', fields, nativequery=filters)
    modifier.addSearchOptions('#%s' % tableid)
    modifier.addSorting('#%s' % tableid, 1, 'desc')

    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
