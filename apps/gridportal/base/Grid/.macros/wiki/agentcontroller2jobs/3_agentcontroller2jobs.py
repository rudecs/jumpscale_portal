
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    instances = j.application.getAppHRDInstanceNames('agentcontroller2')
    if not instances:
        page = args.page
        page.addMessage('* no agentcontroller2client installed. Use "ays install agentcontroller2_client"')
        params.result = page
        return params

    hrd = j.application.getAppInstanceHRD('agentcontroller2', instance=instances[0], parent=None)
    redispasswd = hrd.get('instance.param.redis.password')

    acclient = j.clients.ac.get(password=redispasswd)
    jobs = acclient.get_jobs(count=100)

    out = list()
    out.append('||Grid ID||Node ID||Command||Role||Result||')

    for job in jobs:
        out.append("|%(gid)s|%(nid)s|%(cmd)s|%(role)s|[Result|/grid/agentcontroller2job?jobid=%(id)s]|" % job)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
