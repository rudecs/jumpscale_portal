def main(j, args, params, tags, tasklet):
    username = args.getTag('username')
    if not username:
        out = 'Missing Username'
        params.result = (out, args.doc)
        return params

    user = j.apps.system.usermanager._getUser(username)
    if not user:
        out = 'Could not find Username: %s' % username
        params.result = (out, args.doc)
        return params

    args.doc.applyTemplate(user.dump())
    params.result = (args.doc, args.doc)
    return params
