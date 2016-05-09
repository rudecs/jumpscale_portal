
def main(j, args, params, tags, tasklet):

    params.result = (args.doc, args.doc)
    params.merge(args)
    doc = params.doc
    # tags = params.tags

    actor=j.apps.actorsloader.getActor("system","gridmanager")

    organization = args.getTag("organization")
    name = args.getTag("jsname")

    for k,v in {'organization':organization, 'name':name}.iteritems():
        if not v:
            doc.applyTemplate({})
            return params

    try:
        obj = actor.getJumpscript(organization=organization, name=name)
        jumpscript = {}

        for k,v in obj.iteritems():
            if k in ('args', 'roles'):
                v = ' ,'.join(v)
            if k == 'source':
                continue
            if "_" == k[0]:
                continue 
            vstr = j.tools.text.toStr(v)
            if isinstance(v, list):
                vstr.replace("[", "\[")
                vstr.replace("]", "\]")
            jumpscript[k.capitalize()] = vstr.replace('\n', '') if vstr else vstr
        doc.applyTemplate({'jumpscript': jumpscript, 'source': obj['source'], 'name': name})

    except:
        doc.applyTemplate({})


    return params


def match(j, args, params, tags, tasklet):
    return True
