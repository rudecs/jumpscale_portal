
def main(j, args, params, tags, tasklet):
    account = args.getTag('account')
    provider = args.getTag('provider')
    repo = args.getTag('repo')
    acl = j.clients.agentcontroller.get()
    jsargs = {'account': account, 'repo': repo, 'provider': provider}
    jobresult = acl.executeJumpscript('jumpscale', 'repoversion', role='master', gid=j.application.whoAmI.gid, args=jsargs)
    wiki = jobresult['result'][1]

    params.result = (wiki, args.doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
