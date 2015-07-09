def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    ctx = args.get('requestContext')
    host = ctx.env['HTTP_HOST']
    scheme = ctx.env.get('HTTP_X_FORWARDED_PROTO', 'http')
    authKey = ctx.env['beaker.session'].id

    url = "%s://%s/restmachine/system/cpunode/init?authkey=%s" % (scheme, host, authKey)
    out = """{{code: template:text nolinenr theme:neat
curl -L %s | bash
}}""" % url
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
