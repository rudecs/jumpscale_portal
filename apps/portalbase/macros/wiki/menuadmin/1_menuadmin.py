
def main(j, args, params, tags, tasklet):
    params.merge(args)
    doc = params.doc
    username = j.core.portal.active.getUserFromCTX(params.requestContext)

    macrostr = params.macrostr
    macrostr = macrostr.split('\n')

    navigationmenu = None
    adminmenu = None

    pages = macrostr[1:-1]

    pagesstr = ''
    pages = pagesstr + ',\n        '.join(pages) if pages else ''

    if pages:
        pages += ',\n'

    if j.core.portal.active.authentication_method == 'gitlab':
        spaces = {}
        for s in j.core.portal.active.getUserSpacesObjects(params.requestContext):
            if s['namespace']['name']:
                spaces[s['name']] = "%s_%s" % (s['namespace']['name'], s['name'])
            else:
                spaces[s['name']] = s['name']
    else:
        spaces = {}
        for space in j.core.portal.active.getUserSpaces(params.requestContext):
            name = j.core.portal.active.getSpace(space, ignore_doc_processor=True).model.id
            spaces[name] = space
    spacestxt=""
    for name, space in spaces.iteritems():
        if not name.startswith('_'):
            spacestxt += "%s:/%s,\n        " % (name, space.lower().strip("/"))

    if pages or spacestxt:
        navigationmenu = '''
{{megamenu: name:Navigation
column.Spaces =
        %s

column.Pages =
        %s

}}
    ''' % (spacestxt, pages)
       

    if j.core.portal.active.isAdminFromCTX(params.requestContext):
        adminmenu = """
{{menudropdown: name:%s
New Page:/system/create
Edit Page:/system/edit?space=$$space&page=$$page$$querystr
Create Space:/system/createspace
--------------
Files:/system/files?space=$$space
Access:/system/OverviewAccess?space=$$space
Reload:javascript:$.ajax({'url': '/system/ReloadSpace?name=$$space'}).done(function(){location.reload()});void(0);
ReloadAll:javascript:reloadAll();void 0;
Pull latest changes & update:javascript:pullUpdate('$$space');void 0;
}}
""" % (username)




#was inside
#ShowLogs:/system/ShowSpaceAccessLog?space=$$space
#ResetLogs:/system/ResetAccessLog?space=$$space
#Spaces:/system/Spaces
#Pages:/system/Pages?space=$$space

    result = ''
    for menu in [navigationmenu, adminmenu]:
        if menu:
            result += menu

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
