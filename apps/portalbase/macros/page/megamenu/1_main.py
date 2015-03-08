
def main(j, args, params, tags, tasklet):
    page = args.page
    params.result = page

    if not page._hasmenu:
        page.addMessage("**error: Cannot create page because menudropdown macro can only be used if beforehand a menu macro was used")
        return params

    keyword = args.tags.tagGet('marker', "$$$menuright")


    #todo what does this do? (4kds)
    if page.body.find(keyword) == -1:
        return params

    ddcode = """
<li class="dropdown">
  <a href="#" class="dropdown-toggle pull-right $$class" data-toggle="dropdown">$$name<b class="caret"></b></a>
  <ul class="dropdown-menu mega-menu">
       $$items
  </ul>
</li>
"""

    items = ""
    header = args.tags.tagGet("name", "Admin")
    klass = args.tags.tagGet("class", "")


    contents = j.core.hrd.get(content=args.cmdstr + '\n')
    columns = contents.getDictFromPrefix('column')

    for title, rows in columns.iteritems():
        if not isinstance(rows, dict):
            continue
        items += '<div class="mega-menu-column">'
        items += '<ul><li class="nav-header">%s</li>' % title
        for name, target in rows.iteritems():
            if name != "" and name[0] != "#":
                name = name.strip()
                line = "<li><a href=\"%s\">%s</a></li>" % (target, name)
                items += "%s\n" % line
        items += '</ul></li>'

    ddcode = ddcode.replace("$$items", items)
    ddcode = ddcode.replace("$$name", header)
    ddcode = ddcode.replace("$$class", klass)
    ddcode += '$$$menuright'

    page.body = page.body.replace(keyword, ddcode)

    return params


def match(j, args, params, tags, tasklet):
    return True
