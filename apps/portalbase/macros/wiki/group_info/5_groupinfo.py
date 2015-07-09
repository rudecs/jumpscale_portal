def main(j, args, params, tags, tasklet):
    guid = args.getTag('guid')
    if not guid:
        out = 'Missing GUID'
        params.result = (out, args.doc)
        return params

    group = j.apps.system.usermanager.modelGroup.get(guid)
    if not group:
        out = 'Could not find Group: %s' % guid
        params.result = (out, args.doc)
        return params

    args.doc.applyTemplate(group.dump())
    params.result = (args.doc, args.doc)
    return params
