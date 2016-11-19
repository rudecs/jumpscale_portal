def main(j, args, params, tags, tasklet):
    import yaml
    import ujson as json
    import datetime

    params.result = (args.doc, args.doc)
    id = args.getTag('id')
    client = j.clients.osis.getNamespace('system').audit

    if not id:
        args.doc.applyTemplate({})
        return params

    try:
        audit = client.get(id).dump()
    except:
        args.doc.applyTemplate({'id': None})
        return params

    for key in ('kwargs', 'args', 'result'):
        obj = json.loads(audit[key])
        if key == 'result' and isinstance(obj, list) and len(obj) == 1:
            obj = obj[0]
            try:
                obj = json.loads(obj)
            except:
                pass
        audit[key] = yaml.safe_dump(obj, default_flow_style=False)

    audit['time'] = datetime.datetime.fromtimestamp(audit['timestamp']).strftime('%m-%d %H:%M:%S') or 'N/A'
    audit['id'] = id
    args.doc.applyTemplate(audit)
    return params
