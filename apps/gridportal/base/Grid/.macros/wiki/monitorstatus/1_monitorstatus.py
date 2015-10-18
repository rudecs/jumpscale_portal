import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.units
import JumpScale.baselib.redis
import ujson

def main(j, args, params, tags, tasklet):
    doc = args.doc
    import time
    now = time.time()
    nid = args.getTag('nid')
    nidint = int(nid)

    out = list()

    results = j.core.grid.healthchecker.fetchMonitoringOnNode(nidint)

    noderesults = results.get(nidint, dict())
    for category, data in sorted(noderesults.items()):
        out.append('h5. %s' % category)
        for dataitem in data:
            if isinstance(dataitem, dict):
                status = j.core.grid.healthchecker.getWikiStatus(dataitem.get('state'))
                lastchecked = dataitem.get('lastchecked', '')
                if lastchecked:
                    lastchecked = '%s ago' % j.base.time.getSecondsInHR(now - lastchecked)
                out.append('|%s |%s |%s |' % (dataitem.get('message', ''), lastchecked, status))
            else:
                out.append(dataitem)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True


