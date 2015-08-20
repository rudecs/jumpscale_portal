import datetime
import json # pretty printer require native json

def main(j, args, params, tags, tasklet):    
    import urllib

    jobid = args.getTag('jobid')
    if not jobid:
        out = 'Missing jobresult jobid param "jobid"'
        params.result = (out, args.doc)
        return params

    clients = j.atyourservice.findServices('jumpscale', 'agentcontroller2_client')
    if not clients:
        page = args.page
        page.addMessage('* no agentcontroller2client installed. Use "ays install agentcontroller2_client"')
        params.result = page
        return params

    instance = clients[0].instance
    acclient = j.clients.ac.getByInstance(instance)
    job = acclient.get_by_id(None, None, jobid)
 
    if not job:
        params.result = ('Job with jobid %s not found' % jobid, args.doc)
        return params

    jobresult = {'id': jobid}
    results = job.noblock_get_result()

    for result in results:
        cmd = acclient.get_by_id(result['gid'], result['nid'], jobid)
        result['msgs'] = cmd.get_msgs()
        result['msgs'].reverse()
        result['starttime'] = j.base.time.epoch2HRDateTime(result['starttime'])
        result['time'] = result['time']/1000

    jobresult['results'] = results
    args.doc.applyTemplate(jobresult)

    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
