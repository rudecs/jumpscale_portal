import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import ujson
import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    
    out = list()
    data = j.core.grid.healthchecker.fetchMonitoringOnAllNodes()
    lastchecked = 'N/A'
    out.append('Grid was last checked at: %s.' % lastchecked)

    nodeids = set()
    for nid, result in data.items():
        for categorydata in result.values():
            for dataitem in categorydata:
                if dataitem.get('state') == 'ERROR':
                    nodeids.add(nid)

    if nodeids:
        nodenames = [j.core.grid.healthchecker.getName(nodeid) for nodeid in list(nodeids)]
        out.append('{{html: <div><p class="alert alert-warning padding-vertical-none width-50"> Something on node(s) %s is not running.</p></div>}}' % ', '.join(nodenames))
    else:
        out.append('{{html: <div><p class="alert alert-success padding-vertical-none width-50">Everything seems to be OK.</p></div>}}')
    out.append('For more details, check [status overview.|/grid/Status Overview]')

    out = '\n'.join(out)

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
