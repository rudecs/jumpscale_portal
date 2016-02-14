def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    params.result = (args.doc, args.doc)
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    if not j.apps.system.usermanager.modelUser.exists(guid):
        args.doc.applyTemplate({})
        return params

    user = j.apps.system.usermanager.modelUser.get(guid)
    obj = user.dump()
    obj['breadcrumbname'] = obj['id']
    args.doc.applyTemplate(obj)
    return params
