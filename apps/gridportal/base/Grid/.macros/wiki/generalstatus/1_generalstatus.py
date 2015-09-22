import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis
import ujson

def main(j, args, params, tags, tasklet):
    doc = args.doc
    nid = args.getTag('nid')
    nidstr = str(nid)
    rediscl = j.clients.redis.getByInstance('system')

    out = list()

    out.append('||Name||Status||Comments||')

    rstatus = rediscl.hget('healthcheck:monitoring', 'results')
    errors = rediscl.hget('healthcheck:monitoring', 'errors')
    rstatus = ujson.loads(rstatus).get(nid, {}) if rstatus else dict()
    errors = ujson.loads(errors).get(nid, {}) if errors else dict()

    for category, data in rstatus.items():
        # state = j.core.grid.healthchecker.getWikiStatus(data.get('state', 'UNKNOWN'))
        out.append('|%s|successful|%s|' % (category, str(data)))

    for category, data in errors.items():
        # state = j.core.grid.healthchecker.getWikiStatus(data.get('state', 'UNKNOWN'))
        out.append('|%s|error|%s|' % (category, data))
    out = '\n'.join(out)

    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True


