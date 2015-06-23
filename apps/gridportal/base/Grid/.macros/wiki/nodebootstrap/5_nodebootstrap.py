import datetime


def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    ctx = args.get('requestContext')
    host = ctx.env['HTTP_HOST']
    cookies = ctx.env['HTTP_COOKIE']
    res = j.codetools.regex.findAll('beaker.session.id=(\w+)', cookies)
    authKey = "unknown"
    if res > 0:
        authKey = res[0].split('=')[1]

    url = "http://%s/restmachine/system/cpunode/init?authkey=%s" % (host, authKey)
    out = """{{code: template:text nolinenr theme:neat
curl %s | bash
}}""" % url
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
