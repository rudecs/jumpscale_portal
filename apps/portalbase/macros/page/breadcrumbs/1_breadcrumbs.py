import re

def main(j, args, params, tags, tasklet):
    page = args.page
    doc = args.doc
    page.addCSS('/jslib/old/breadcrumbs/breadcrumbs.css')

    data = "<ul class='breadcrumb'>%s</ul>"
    breadcrumbs = [(doc.original_name, doc.title)]
    space = j.core.portal.active.getSpace(doc.getSpaceName())
    while doc.parent:
        doc = space.docprocessor.name2doc.get(doc.parent)
        if not doc:
            break
        breadcrumbs.insert(0, (doc.original_name, doc.title))

    innerdata = ""
    breadcrumbs.insert(0, ('/%s' % space.model.id, space.model.name))
    for link, title in breadcrumbs[:-1]:
        innerdata += "<li><a href='%s'>%s</a><span style='opacity: 0.5; margin-right: 8px; margin-left: 2px;' class='icon-chevron-right'></span></li>" % (link, title)
    innerdata += "<li class='active'>%s</li>" % breadcrumbs[-1][1]

    page.addMessage(data % innerdata)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
