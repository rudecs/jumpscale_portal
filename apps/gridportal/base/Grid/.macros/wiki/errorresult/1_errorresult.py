def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    guid = args.getTag('ecoguid')

    out = "[*Error Condition Object Details*|error condition?id=%s]" % guid

    params.result = (out, doc)
    return params
    

def match(j, args, params, tags, tasklet):
    return True
