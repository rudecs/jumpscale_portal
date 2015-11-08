import JumpScale.grid.gridhealthchecker
import JumpScale.baselib.redis2
import ujson

def main(j, args, params, tags, tasklet):
    doc = args.doc

    dbdata = j.core.grid.healthchecker.checkDBs()
    out = list()
    results = dbdata.values()

    for noderesults in results:
        for category, data in sorted(noderesults.items()):
            out.append('h5. %s' % category)
            for dataitem in data:
                if isinstance(dataitem, dict):
                    status = j.core.grid.healthchecker.getWikiStatus(dataitem.get('state'))
                    out.append('|%s |%s |' % (dataitem.get('message', ''), status))
                else:
                    out.append(dataitem)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
