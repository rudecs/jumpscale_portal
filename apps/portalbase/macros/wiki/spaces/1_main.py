
def main(j, args, params, tags, tasklet):
    """
    {{spaces}}
    """
    params.merge(args)

    doc = params.doc

    out = "{{datatables_use}}\n"
    
    bullets = params.tags.labelExists("bullets")
    table = params.tags.labelExists("table")
    filterbyuser = params.tags.labelExists("filterbyuser")
    isgitlab = j.core.portal.active.authentication_method == 'gitlab'
    addSpinner = isgitlab
    
    spaces = j.core.portal.active.getUserSpaces(params.requestContext)
    if isgitlab:
        gitlabnonclonedspaces = [s[s.index('portal_'):] for s in j.core.portal.active.getNonClonedGitlabSpaces(params.requestContext)]
    spaces.sort()
    excludes=[]
    if params.tags.tagExists("exclude"):
        excludes=params.tags.tagGet("exclude").split(",")
        excludes=[item.strip().lower() for item in excludes]
    
    for item in spaces:
        item = item.lower()
        if  item not in excludes:
            anchor = item.strip("/")
            if isgitlab:
                idx = item.find('_')
                anchor = item
                item = item[idx+1:]
                spacename = item[:idx]
            if table:
                out += "|[%s|/%s]|" % (item, anchor)
            else:
                if item[0] != "_" and item.strip() != "" and item.find("space_system")==-1:
                    if bullets:
                        out += "* [%s|/%s]" % (item, anchor)
                    else:
                        out += "[%s|/%s]" % (item, anchor)

            if addSpinner:
                if item.startswith("portal_"):
                    classname = "loadspace"
                    if item in gitlabnonclonedspaces:
                        classname+= " new-repo"
                    out += '{{div:class=%s}}|' % classname
                else:
                    out += '{{div}}|'
            out += '\n'

    if addSpinner:
        out += '{{html:<script src="/jslib/spin.min.js"></script>}}'
        out += '{{html:<script src="/jslib/gitlab/loadUserSpacesAsyncronously.js"></script>}}'
        
            
    params.result = (out, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True