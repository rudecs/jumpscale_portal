from JumpScale import j
import yaml

def main(j, args, params, tags, tasklet):
    scl = j.clients.osis.getNamespace('system')
    id = args.requestContext.params.get("id")
    if id:
        current = False
        version = scl.version.searchOne({'id': int(id)})
    else:
        current = True
        version = scl.version.searchOne({'status':'CURRENT'})
        if not version:
            version = scl.version.searchOne({'status':'ERROR'})

    if version:
        version['manifest'] = yaml.load(version['manifest'])

    history = scl.version.search({'status':{'$ne':'CURRENT'}}, size=0)[1:]
    result = {'current':current, 'version':version, 'history':history}
    args.doc.applyTemplate(result, False)
    params.result = (args.doc, args.doc) 
    return params

def match(j, args, params, tags, tasklet):
    return True
