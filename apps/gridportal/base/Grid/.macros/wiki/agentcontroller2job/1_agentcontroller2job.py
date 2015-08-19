import datetime
import json # pretty printer require native json

def main(j, args, params, tags, tasklet):    
    import urllib

    jobid = args.getTag('jobid')
    if not jobid:
        out = 'Missing jobresult jobid param "jobid"'
        params.result = (out, args.doc)
        return params

    instances = j.application.getAppHRDInstanceNames('agentcontroller2')
    if not instances:
        page = args.page
        page.addMessage('* no agentcontroller2client installed. Use "ays install agentcontroller2_client"')
        params.result = page
        return params

    hrd = j.application.getAppInstanceHRD('agentcontroller2', instance=instances[0], parent=None)
    redispasswd = hrd.get('instance.param.redis.password')

    acclient = j.clients.ac.get(password=redispasswd)
    jobresult = acclient.get_job(jobid)
 
    if not jobresult:
        params.result = ('jobresult with jobid %s not found' % jobid, args.doc)
        return params


    jobresult['nid'] = jobresult.get('nid', 0)
    jobresult['starttime'] = j.base.time.epoch2HRDateTime(jobresult['starttime'])
    jobresult['time'] = jobresult['time']/1000

    print jobresult
    args.doc.applyTemplate(jobresult)

    params.result = (args.doc, args.doc)
    return params


def match(j, args, params, tags, tasklet):
    return True
