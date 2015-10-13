import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import ujson

def main(j, args, params, tags, tasklet):
    doc = args.doc

    status = None
    out = list()
    rediscl = j.clients.redis.getByInstance('system', gevent=True)


    if rediscl.hexists('healthcheck:monitoring', 'lastcheck'):
        lastchecked = j.basetype.float.fromString(rediscl.hget('healthcheck:monitoring', 'lastcheck'))
        lastchecked = '{{span: class=jstimestamp|data-ts=%s}}{{span}}' % lastchecked
    else:
        lastchecked = 'N/A'
    out.append('Grid was last checked at: %s.' % lastchecked)

    out.append('||Grid ID||Node ID||Node Name||JSAgent Status||Details||')
    data = rediscl.hget('healthcheck:monitoring', 'results')
    data = ujson.loads(data) if data else dict()
    rows = list()

    errors = dict()
    for nid, result in data.items():
        for category, categorydata in result.items():
            for dataitem in categorydata:
                if dataitem.get('state') != 'OK':
                    errors.setdefault(nid, set())
                    errors[nid].add(category)

    if len(data) > 0:
        for nid, checks in data.iteritems():
            level = 0
            if nid in errors:
                level = -1
                categories = errors.get(nid, [])
                runningstring = '{color:orange}*DEGRADED** (issues in %s){color}' % ', '.join(categories)
            else:
                level = 0
                runningstring = '{color:green}*RUNNING*{color}'
            status = checks.get('Processmanager', [{'state': 'UNKOWN'}])[0]
            if status and status['state'] != 'OK':
                level = -2
                runningstring = '{color:red}*HALTED*{color}'
            gid = j.core.grid.healthchecker.getGID(nid)
            link = '[Details|nodestatus?nid=%s&gid=%s]' % (nid, gid) 
            row = {'level': level, 'gid': gid, 'nid': nid}
            row['message'] = '|%s|[%s|grid node?id=%s&gid=%s]|%s|%s|%s|' % (gid, nid, nid, gid, j.core.grid.healthchecker.getName(nid), runningstring, link)
            rows.append(row)

    def sorter(row1, row2):
        for sortkey in ('level', 'gid', 'nid'):
            if row1[sortkey] != row2[sortkey] or sortkey == 'nid':
                return cmp(row1[sortkey], row2[sortkey] )

    out.extend([x['message'] for x in sorted(rows, cmp=sorter)])
    params.result = ('\n'.join(out), doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
