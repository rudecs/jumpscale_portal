
def main(j, args, params, tags, tasklet):
    id = args.getTag('id')
    if not id:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    oscl = j.clients.osis.getByInstance('main')
    ecocl = j.clients.osis.getCategory(oscl, 'system', 'eco')
    try:
        obj = ecocl.get(id).__dict__
    except:
        params.result = (args.doc, args.doc)
        args.doc.applyTemplate({})
        return params

    obj['epoch'] = "{{div: class=jstimestamp|data-ts=%s}}{{div}}" % obj['epoch']
    obj['lasttime'] = "{{div: class=jstimestamp data-ts=%s}}{{div}}" % obj['lasttime']
    for attr in ['errormessage', 'errormessagePub']:
        obj[attr] = j.html.escape(obj[attr])
    for attr in ['jid']:
        obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj[attr] != 0 else 'N/A'
    obj['id'] = id

    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
