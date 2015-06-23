import jinja2 
from collections import OrderedDict

def main(j, args, params, tags, tasklet):
    jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")
    hrd = j.application.instanceconfig
    params.merge(args)
    doc = params.doc

    macrostr = params.macrostr
    macrostr = macrostr.split('\n')

    navigationmenu = None
    adminmenu = None
    megamenu = OrderedDict()

    pages = macrostr[1:-1]

    if pages:
        pagedict = OrderedDict()
        megamenu['Pages'] = pagedict
        for page in pages:
            pagename, pagelink = page.split(':')
            pagedict[pagename] = pagelink

    if j.core.portal.active.authentication_method == 'gitlab':
        spaces = {}
        for s in j.core.portal.active.getUserSpacesObjects(params.requestContext):
            if s['namespace']['name']:
                spaces[s['name']] = "%s_%s" % (s['namespace']['name'], s['name'])
            else:
                spaces[s['name']] = "/%s" % s['name']
    else:
        spaces = {}
        for spaceid in j.core.portal.active.getUserSpaces(params.requestContext):
            space = j.core.portal.active.getSpace(spaceid, ignore_doc_processor=True)
            spaces[space.model.name] = "/%s" % spaceid

    if spaces:
        megamenu['Spaces'] = spaces
    megamenu.update(hrd.getDictFromPrefix('instance.navigationlinks'))
    template = jinja.from_string('''
{{megamenu: name:Navigation
{% for name, links in megamenu.iteritems() %}
column.${name} ={% for pagename, link in links.iteritems() %}
        ${pagename}:${link},

{%- endfor %}
{% endfor %}
}}
''')
    navigationmenu = template.render(megamenu=megamenu)
    if j.core.portal.active.isAdminFromCTX(params.requestContext):
        adminmenu = """
{{menudropdown: name:Administration
New Page:/system/create
Edit Page:/system/edit?space=$$space&page=$$page&$$querystr
Create Space:/system/createspace
--------------
Files:/system/files?space=$$space
Access:/system/OverviewAccess?space=$$space
Reload:javascript:$.ajax({'url': '/system/ReloadSpace?name=$$space'}).done(function(){location.reload()});void(0);
ReloadAll:javascript:reloadAll();void 0;
Pull latest changes & update:javascript:pullUpdate('$$space');void 0;
}}
"""

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
