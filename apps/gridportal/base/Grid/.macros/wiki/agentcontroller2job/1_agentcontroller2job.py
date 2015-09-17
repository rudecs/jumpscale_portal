import json


def prettify(j, s):
    if isinstance(s, basestring):
        try:
            s = json.loads(s)
        except:
            pass

    return j.html.escape(json.dumps(s, indent=4, sort_keys=True))


def main(j, args, params, tags, tasklet):
    job = args.getTag('job')

    if not job:
        out = 'Missing job param "job"'
        params.result = (out, args.doc)
        return params

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if not clients:
        params.result = ('* Agent controller 2 is not available, are you missing the client?', doc)
        return params

    instance = clients[0].instance
    acclient = j.clients.ac.getByInstance(instance)

    cmdjobs = acclient.get_cmd_jobs(job)
    for nodeinfo, jobinfo in cmdjobs.iteritems():
        jobinfo.jsonargs = json.dumps(jobinfo.args.dump(), indent=True)
    firstjob = cmdjobs.values()[0]

    args.doc.applyTemplate({'cmdjobs': cmdjobs, 'firstjob': firstjob})

    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
