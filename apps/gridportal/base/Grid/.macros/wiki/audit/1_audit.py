def main(j, args, params, tags, tasklet):
    import yaml
    import ujson as json
    import datetime

    params.result = (args.doc, args.doc)
    id = args.getTag('id')
    client = j.clients.osis.getNamespace('system').audit

    if not id or not id.isalnum():
        args.doc.applyTemplate({})
        return params

    try:
        audit = client.get(id).dump()
    except:
        args.doc.applyTemplate({'id': None})
        return params
    
    for key in ('kwargs', 'args', 'result'):
        audit[key] = yaml.dump(json.loads(audit[key])).replace("!!python/unicode ", "")


    audit['time'] = datetime.datetime.fromtimestamp(audit['timestamp']).strftime('%m-%d %H:%M:%S') or 'N/A'
    audit['id'] = id
    args.doc.applyTemplate(audit)
    return params
