def main(j, args, params, tags, tasklet):

    import JumpScale.grid.agentcontroller

    doc = args.doc
    nid = args.getTag('nid')
    node = j.core.portal.active.osis.get('system', 'node', int(nid))

    workerscl = j.clients.agentcontroller.getProxy(category="worker")
    jobs = workerscl.getQueuedJobs(queue=None, format='json', _agentid=nid)
    doc.applyTemplate({'name': node['name'], 'jobs': jobs})
    params.result = (doc, doc)

    return params

def match(j, args, params, tags, tasklet):
    return True
