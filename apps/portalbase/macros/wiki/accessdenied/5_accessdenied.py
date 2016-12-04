

def main(j, args, params, tags, tasklet):
    session = args.requestContext.env['beaker.session']
    msg = "h4. Access Denied"
    if j.core.portal.active.isLoggedInFromCTX(args.requestContext):
        msg += " - [Logout|/system/login?user_logoff_=1]"
    else:
        loginurl = j.core.portal.active.force_oauth_url or '/system/login'
        msg += " - [Login|%s]" % loginurl
    autherror = session.get('autherror', '')
    if autherror:
        msg += "\n{color:red}%s{color}" % autherror

    params.result = (msg, args.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
