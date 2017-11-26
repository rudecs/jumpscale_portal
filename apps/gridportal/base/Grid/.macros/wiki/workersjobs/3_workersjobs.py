def main(j, args, params, tags, tasklet):

    import JumpScale.grid.agentcontroller
    import gevent

    doc = args.doc
    params.result = (doc, doc)
    nid = args.getTag('nid')

    node_exists = j.core.portal.active.osis.exists('system', 'node', int(nid))
    if node_exists:
        node = j.core.portal.active.osis.get('system', 'node', int(nid))
        try:
            workerscl = j.clients.agentcontroller.getProxy(category="worker")
            with gevent.Timeout(5):
                jobs = workerscl.getQueuedJobs(queue=None, format='json', _agentid=nid)
            doc.applyTemplate({'name': node['name'], 'jobs': jobs})
        except gevent.Timeout:
            doc.applyTemplate({'name': node['name']})
    else:
        doc.applyTemplate({})
    return params




def match(j, args, params, tags, tasklet):
    return True
