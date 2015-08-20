
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if not clients:
        page = args.page
        page.addMessage('* no agentcontroller2client installed. Use "ays install agentcontroller2_client"')
        params.result = page
        return params

    instance = clients[0].instance
    acclient = j.clients.ac.getByInstance(instance)
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
