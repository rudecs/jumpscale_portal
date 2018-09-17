def main(j, args, params, tags, tasklet):

    page = args.page
    params.extend(args)
    if "." in args.doc.name:
        if args.doc.name.split('.')[1] == "md":
            page.removeCSS('bootstrap.css')
            page.removeCSS('bootstrap-responsive.css')
    else:
        page.addBootstrap()

    page._hasmenu = True
    page.login = True

    menu = args.cmdstr

    noguest = args.tags.labelExists('no-guest')

    if args.tags.labelExists("nopadding"):
        page.padding = False

    if args.tags.tagExists("classtags"):
        classtags = args.tags.tagGet("classtags")
    else:
        classtags = "navbar navbar-inverse navbar-fixed-top"

    if "." in args.doc.name:
        if args.doc.name.split('.')[1] == "md":
            T = """{items}{login}{username}{findmenu}
"""
    else:
        T = """
    <div class="{classtags}"  {hide-menu}>
        <div class="navbar-inner">
            <div class="container">
                <a class="btn btn-navbar" data-toggle="collapse" data-target=".nav-collapse">
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                </a>
                {brand}
                <div class="nav-collapse collapse">
                   <ul class="nav pull-left">
                   $$$menuleft
                   {items}
                   $$$searchbox
                   $$$menuright
                   </ul>
                   {login}
                   {username}
                   {findmenu}
                </div>
            </div>
        </div>
    </div>

"""
    T = T.replace("{classtags}", classtags)
    if page.logo != "":
        # will be logo
        T = T.replace(
            "{brand}", "<a class=\"brand\" href=\"/home\"><img style=\"margin-top: -5px; max-width: 120px; max-height: 120px;\" src=\"%s\" alt=\"home\" title=\"home\"></a>" % page.logo)
    elif page.projectname != "":
        T = T.replace("{brand}", "<a class=\"brand\" href=\"/%s\">%s</a>" % (args.doc.getSpaceName(), page.projectname))
    else:
        T = T.replace("{brand}", "")

    L = """
<ul class="nav navbar pull-right">
    <li>
        %s
    </li>
</ul>"""

    loggedin = j.core.portal.active.isLoggedInFromCTX(params.requestContext)

    if loggedin:
        username = params.requestContext.env['beaker.session']['user']
        username = L % '<a href="#"> %s </a>' % username
        T = T.replace("{username}", username)
    else:
        T = T.replace("{username}", "")

    if page.login:
        if loggedin:
            loginorlogout = """
        <a href="javascript:;" onclick="nextElementSibling.submit();">Logout</a>
    <form action="#" method="post" class="hide">
        <input type="hidden" name="user_logoff_" value="1"/>
    </form>
                """
        else:
            if not j.core.portal.active.force_oauth_instance:
                loginorlogout = """
            <a href="javascript:;" onclick="nextElementSibling.submit();">Login</a>
        <form action="#" method="post" class="hide">
            <input type="hidden" name="user_login_" value="guest"/>
        </form>
                    """
            else:
                loginorlogout = '<a href="{}">Login</a>'.format(j.core.portal.active.force_oauth_url)

        T = T.replace("{login}", L % loginorlogout)
    else:
        T = T.replace("{login}", "")

    if page.hasfindmenu:
        if "." in args.doc.name:
            if args.doc.name.split('.')[1] == "md":
                L = """<form id="search-form" class="navbar-form navbar-right padding-right-none" action="/system/find?page={name}&space={space}" method="post" role="search">
<div class="form-group">
<div class="input-group">
<input class="form-control search-query" id="navbarInput-01" type="search" placeholder="Search">
</div>
</div>
</form>"""
        else:
            L = """
<form name="input" action="/system/find?page={name}&space={space}" method="post" class="navbar-search pull-right">
<input name="text" type="text" class="search-query" placeholder="Search">
</form>"""
        T = T.replace("{findmenu}", L)
    else:
        T = T.replace("{findmenu}", "")

    T = T.replace("{name}", args.doc.pagename)
    T = T.replace("{space}", args.doc.getSpaceName())

    items = ""
    for line in menu.split("\n"):
        line = line.strip()
        if line != "" and line[0] != "#":
            # print line
            if line.find(":") != -1:
                if 'target=_blank' not in line:
                    name, target = line.split(":", 1)
                    line2 = "<li><a href=\"%s\">%s</a></li>" % (target, name)
                else:
                    line = line.replace(':target=_blank', '')
                    name, target = line.split(":", 1)
                    line2 = "<li><a href=\"%s\" target=\"_blank\">%s</a></li>" % (target, name)
            elif line.startswith('$$$'):
                line2 = line
            else:
                name = line
                target = "/%s/%s" % (args.doc.getSpaceName(), line)
                line2 = "<li><a href=\"%s\">%s</a></li>" % (target, name)
            items += "%s\n" % line2
    T = T.replace("{items}", items)
    user = j.core.portal.active.getUserFromCTX(args.requestContext)
    if user == "guest" and noguest:
        T = T.replace("{hide-menu}", "style=\"display:none;\"")
    else:
        T = T.replace("{hide-menu}", "")

    page.addHTMLBody(T)
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
