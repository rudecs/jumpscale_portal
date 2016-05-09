import datetime

def main(j, args, params, tags, tasklet):
    params.result = (args.doc, args.doc)
    guid = args.getTag('id')
    if not guid:
        args.doc.applyTemplate({})
        return params

    logs = j.apps.system.gridmanager.getLogs(guid=guid)
    if not logs:
        args.doc.applyTemplate({})
        return params

    obj = logs[0]
    for attr in ['epoch']:
        obj[attr] = datetime.datetime.fromtimestamp(obj[attr]).strftime('%Y-%m-%d %H:%M:%S')
    obj['jid'] = '[%(jid)s|job?id=%(jid)s]|' % obj if obj['jid'] else 'N/A'

    args.doc.applyTemplate(obj)

    return params


def match(j, args, params, tags, tasklet):
    return True
