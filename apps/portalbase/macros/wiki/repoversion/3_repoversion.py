
def main(j, args, params, tags, tasklet):
    account = args.getTag('account')
    provider = args.getTag('provider')
    repo = args.getTag('repo')
    acl = j.clients.agentcontroller.get()
    jsargs = {'account': account, 'repo': repo, 'provider': provider}
    jobresult = acl.executeJumpscript('jumpscale', 'repoversion', role='master', gid=j.application.whoAmI.gid, args=jsargs)
    result = jobresult['result']
    link = result['hex']
    if provider == 'github':
        link = '[{0}|https://github.com/{1}/{2}/commit/{0}]'.format(result['hex'], account, repo)
    wiki = "%s: %s (%s) {{ts: %s}}" % (result['version'][0], result['version'][1], link, result['timestamp'])

    params.result = (wiki, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
