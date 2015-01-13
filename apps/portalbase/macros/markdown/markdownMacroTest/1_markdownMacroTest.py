
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    params.result = ""

    output = """
# I'm a markdown output
"""

    if j.core.portal.active.isAdminFromCTX(params.requestContext):
        params.result = output

    params.result = (params.result, doc)
    return params

def match(j, args, params, tags, tasklet):
    return True
