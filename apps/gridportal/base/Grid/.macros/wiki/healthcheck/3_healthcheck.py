import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import ujson
import datetime
import time

def main(j, args, params, tags, tasklet):
    doc = args.doc
    
    out = list()
    data = j.core.grid.healthchecker.fetchMonitoringOnAllNodes()
    errors, oldestdate = j.core.grid.healthchecker.getErrorsAndCheckTime(data)

    out.append('Grid was last checked at: {{ts:%s}}' % oldestdate)

    if errors:
        nodenames = [j.core.grid.healthchecker.getName(nodeid) for nodeid in errors]
        out.append('{{html: <div><p class="alert alert-warning padding-vertical-none width-50"> Something on node(s) %s is not running.</p></div>}}' % ', '.join(nodenames))
    else:
        out.append('{{html: <div><p class="alert alert-success padding-vertical-none width-50">Everything is OK.</p></div>}}')
    out.append('For more details, check [status overview.|/grid/Status Overview]')

    out = '\n'.join(out)

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
