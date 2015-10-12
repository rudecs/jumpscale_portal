import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.units
import JumpScale.baselib.redis
import ujson

def main(j, args, params, tags, tasklet):
    doc = args.doc
    nid = args.getTag('nid')
    nidstr = str(nid)
    rediscl = j.clients.redis.getByInstance('system')

    out = list()

    results = rediscl.hget('healthcheck:monitoring', 'results')
    results = ujson.loads(results)

    noderesults = results.get(nidstr, dict())
    for category, data in noderesults.items():
        out.append('h5. %s' % category)
        for dataitem in data:
            if isinstance(dataitem, dict):
                status = j.core.grid.healthchecker.getWikiStatus(dataitem.get('state'))
                out.append('|%s|%s|' % (dataitem.get('message', ' '), status))
            else:
                out.append(dataitem)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True


