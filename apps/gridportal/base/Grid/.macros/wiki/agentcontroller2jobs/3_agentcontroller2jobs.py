import base64
import json


def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if clients:
        instance = clients[0].instance
        acclient = j.clients.ac.getByInstance(instance)
        jobs = acclient.get_cmds(count=100)
    else:
        jobs = []

    out = list()
    out.append('||Grid ID||Node ID||Command||Role||Fanout||Details||')

    line = '|{gid}|{nid}|{cmd}|{role}|{fanout}|[Details|/grid/agentcontroller2job?job={job}]|'
    for job in jobs:
        jobrow = line.format(job=job['id'], **job)
        out.append(jobrow)
    else:
        out.append("| | | | | | |")

    out = '\n'.join(out)
    params.result = (out, doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
