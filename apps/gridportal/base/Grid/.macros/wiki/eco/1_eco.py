
def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    scl = j.clients.osis.getNamespace('system')
    try:
        obj = scl.eco.get(id).__dict__
    except:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params
    try:
        node = scl.node.get(obj['nid'])
        obj['nodename'] = node.name
    except:
        obj['nodename'] = 'N/A'
    grid = scl.grid.get(obj['gid'])
    if grid:
        obj['gridname'] = grid.name
    else:
        obj['gridname'] = 'Not Found'
    obj['epoch'] = "{{div: class=jstimestamp|data-ts=%s}}{{div}}" % obj['epoch']
    obj['lasttime'] = "{{div: class=jstimestamp|data-ts=%s}}{{div}}" % obj['lasttime']
    for attr in ['errormessage', 'errormessagePub']:
        obj[attr] = j.html.escape(obj[attr])
    for attr in ['jid']:
        obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj[attr] != 0 else 'N/A'
    obj['id'] = id
    obj['levelname'] = j.errorconditionhandler.getLevelName(obj['level'])

    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
