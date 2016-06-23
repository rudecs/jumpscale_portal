from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):
    params.merge(args)

    name = params.tags.tagGet("spacename")

    out = "Space \"%s\" succesfully deleted." % name

    if name or name.find("$$") != -1:
        raise exceptions.BadRequest("BadRequest", "text/plain")

    try:
        space = j.core.portal.active.deleteSpace(name)

    except Exception as e:
        error = e
        out = "ERROR: could not reload the docs for space %s, please check event log." % params.tags.tagGet("spacename")
        eco = j.errorconditionhandler.parsePythonErrorObject(e)
        eco.process()
        print(eco)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
