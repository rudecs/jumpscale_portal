def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    ctx = args.get('requestContext')
    host = ctx.env['HTTP_HOST']
    authKey = ctx.env['beaker.session'].id

    url = "https://%s/restmachine/system/cpunode/init?authkey=%s" % (host, authKey)
    out = """{{code: template:text nolinenr theme:neat
curl -L %s | bash
}}""" % url
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
