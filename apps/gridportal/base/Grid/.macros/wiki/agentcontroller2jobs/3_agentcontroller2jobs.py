import base64
import json


def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if not clients:
        params.result = ('* Agent controller 2 is not available, are you missing the client?', doc)
        return params

    instance = clients[0].instance
    acclient = j.clients.ac.getByInstance(instance)
    jobs = acclient.get_jobs(count=100)

    out = list()
    out.append('||Grid ID||Node ID||Command||Role||Fanout||Details||')

    line = '|{gid}|{nid}|{cmd}|{role}|{fanout}|[Details|/grid/agentcontroller2job?job={job}]|'
    for job in jobs:
        jobrow = line.format(
            job=base64.b64encode(json.dumps(job)).strip(),
            **job
        )

        out.append(jobrow)

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
