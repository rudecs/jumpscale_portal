from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):
    params.merge(args)

    name = params.tags.tagGet("name")

    out = "space %s succesfully reloaded." % name
    if name.startswith("$$"):
        raise exceptions.BadRequest("BadRequest", "text/plain")

    try:
        space = j.core.portal.active.loadSpace(name, force=True)

    except Exception as e:
        error = e
        out = "ERROR: could not reload the docs for space %s, please check event log." % params.tags.tagGet("name")
        eco = j.errorconditionhandler.parsePythonErrorObject(e)
        eco.process()
        print(eco)

    params.result = (out, params.doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
