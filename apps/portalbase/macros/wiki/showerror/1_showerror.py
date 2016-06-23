from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):
    
    error = args.getTag('error')
    out = """h4. error was:

    %s"""%(error) if error else ""
    args.doc.applyTemplate({"error":out})
    params.result = (args.doc, args.doc)
    return params
