
def main(j, args, params, tags, tasklet):

    params.result = (args.doc, args.doc)
    params.merge(args)
    doc = params.doc
    # tags = params.tags

    jsid = args.getTag("id")
    if not jsid:
        doc.applyTemplate({})
        return params

    osis = j.clients.osis.getNamespace('system')
    try:
        obj = osis.jumpscript.get(int(jsid)).__dict__
        jumpscript = {}
        args = []

        for k, v in obj.iteritems():
            if k in ('args', 'roles'):
                if k == 'args':
                    args = v
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
        doc.applyTemplate({'jumpscript': jumpscript, 'source': obj['source'], 'name': obj['name'], 'args': args})
    except:
        doc.applyTemplate({})

    return params


def match(j, args, params, tags, tasklet):
    return True
