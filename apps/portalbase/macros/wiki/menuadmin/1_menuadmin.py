
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc

    macrostr = params.macrostr
    macrostr = macrostr.split('\n')
    pages = macrostr[1:-1]

    pagesstr = ''
    pages = pagesstr + '\n'.join(pages).strip() if pages else ''
    if pages:
        pages = '--------------\n%s' % pages

    if j.core.portal.active.authentication_method == 'gitlab':
        spaces = {s['name']: "%s_%s" % (s['namespace']['name'], s['name']) for s in j.core.portal.active.getUserSpacesObjects(params.requestContext)}
    else:
        spaces = {}
        for space in j.core.portal.active.getUserSpaces(params.requestContext):
            name = j.core.portal.active.getSpace(space, ignore_doc_processor=True).model.id
            spaces[name] = space
    spacestxt=""
    for name, space in spaces.iteritems():
        if not name.startswith('_'):
            spacestxt += "%s:/%s\n" % (name, space.lower().strip("/"))
    if j.core.portal.active.isLoggedInFromCTX(params.requestContext):
        loginorlogout = "Logout: /system/login?user_logoff_=1" 
    else:
        loginorlogout = "Login: /system/login"    
        
    
    if spacestxt:
        spacestxt = '--------------\n%s' % spacestxt

    adminmenu = """
{{menudropdown: name:Navigation
New Page:/system/create
Edit Page:/system/edit?space=$$space&page=$$page$$querystr
Create Space:/system/createspace
%s
%s
--------------
Files:/system/files?space=$$space
Access:/system/OverviewAccess?space=$$space
Reload:javascript:$.ajax({'url': '/system/ReloadSpace?name=$$space'}).done(function(){location.reload()});void(0);
ReloadAll:javascript:reloadAll();void 0;
Pull latest changes & update:javascript:pullUpdate('$$space');void 0;
""" % (loginorlogout, pages)

    readonlymenu = """
{{menudropdown: name:Navigation
%s
%s
""" % (loginorlogout, pages)




#was inside
#ShowLogs:/system/ShowSpaceAccessLog?space=$$space
#ResetLogs:/system/ResetAccessLog?space=$$space
#Spaces:/system/Spaces
#Pages:/system/Pages?space=$$space

    result = ''
    if j.core.portal.active.isAdminFromCTX(params.requestContext):
        result = adminmenu
    else:
        result = readonlymenu

    result +=spacestxt
    result+='}}'

    result+='''
    {{htmlhead:
    <script type="text/javascript" src="/jslib/old/adminmenu/adminmenu.js"></script>
    }}
    '''

    params.result = result

    params.result = (params.result, doc)

    return params


def match(j, args, params, tags, tasklet):
    return True
