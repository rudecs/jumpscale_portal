import json


def prettify(j, s):
    if isinstance(s, basestring):
        try:
            s = json.loads(s)
        except:
            pass

    return j.html.escape(json.dumps(s, indent=4, sort_keys=True))


def main(j, args, params, tags, tasklet):
    job_str = args.getTag('job')

    if not job_str:
        out = 'Missing job param "job"'
        params.result = (out, args.doc)
        return params

    job = json.loads(job_str.decode('base64'))

    job['args'] = prettify(j, job['args'])
    job['data'] = prettify(j, job['data'])

    jobid = job['id']

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if not clients:
        params.result = ('* Agent controller 2 is not available, are you missing the client?', params.doc)
        return params

    instance = clients[0].instance
    acclient = j.clients.ac.getByInstance(instance)
    job_ref = acclient.get_by_id(None, None, jobid)

    # Note we are retrieving the job results directly with the client, not from the passed job
    # object so when you can see changes in result state by refreshing the page.
    # the job object is maily passed for job data.
    if not job_ref:
        params.result = ('Job with jobid %s not found' % jobid, args.doc)
        return params

    jobresult = {
        'job': job
    }

    results = job_ref.noblock_get_result()

    for result in results:
        # reget the job result on, but linked with the correct agent to
        # retrieve the log messages.
        cmd = acclient.get_by_id(result['gid'], result['nid'], jobid)

        result['data'] = prettify(j, result['data'])
        result['msgs'] = cmd.get_msgs()
        result['msgs'].reverse()
        result['starttime'] = j.base.time.epoch2HRDateTime(result['starttime'])
        result['time'] = result['time'] / 1000

    jobresult['results'] = results
    args.doc.applyTemplate(jobresult)

    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
