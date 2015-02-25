
def main(j, args, params, tags, tasklet):
    """
    {{spaces}} or {{spaces:'filterbyuser'}}
    """
    params.merge(args)

    doc = params.doc

    out = "{{datatables_use}}\n"
    
    bullets = params.tags.labelExists("bullets")
    table = params.tags.labelExists("table")
    filterbyuser = params.tags.labelExists("filterbyuser")
    addSpinner = False
    
    if filterbyuser:
        if j.core.portal.active.authentication_method == 'gitlab':
            addSpinner = True
        spaces = j.core.portal.active.getUserSpaces(params.requestContext)
    else:
        spaces = [ x.model.id.lower() for x in list(j.core.portal.active.spacesloader.spaces.values()) ]
    spaces.sort()

    if params.tags.tagExists("exclude"):
        excludes=params.tags.tagGet("exclude").split(",")
        excludes=[item.strip().lower() for item in excludes]
    else:
        excludes=[]    
    
    for item in spaces:
        if item.lower() not in excludes:
            
            if table:
                if j.core.portal.active.authentication_method == 'gitlab':
                    spacesobjects = {x['name']:x['namespace']['name'] for x in j.core.portal.active.getUserSpacesObjects(params.requestContext)}
                    gitlabspacename = spacesobjects.get(item, '')
                    spacename = "%s_%s" % (gitlabspacename, item.lower().strip("/"))
                    out += "|[%s|/%s]|" % (item, spacename)
                else:
                    out += "|[%s|/%s]|" % (item, item.lower().strip("/"))
            else:
                if item[0] != "_" and item.strip() != "" and item.find("space_system")==-1:
                    if bullets:
                        out += "* [%s|/%s]" % (item, item.lower().strip("/"))
                    else:
                        out += "[%s|/%s]" % (item, item.lower().strip("/"))
            
            if addSpinner:
                out += '{{div:class=loadspace}}|'
            out += '\n'

    if addSpinner:
        out += '{{html:<script src="/jslib/spin.min.js"></script>}}'
        out += '{{html:<script src="/jslib/gitlab/loadUserSpacesAsyncronously.js"></script>}}'
        
            
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True