def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    scl = j.clients.osis.getNamespace('system')
    if not guid:
        args.doc.applyTemplate({})
        params.result = (args.doc, args.doc)
        return params
    obj = next(iter(scl.group.search({'id': guid})[1:]), dict())
    args.doc.applyTemplate(obj)
    params.result = (args.doc, args.doc)
    return params
