from itertools import count

def main(j, args, params, tags, tasklet):
    page = args.page
    hrd = j.application.instanceconfig

    menulinks = hrd.getDictFromPrefix('instance.navigationlinks')
    if not menulinks:
        menulinks = {'Portal': j.core.portal.active.getSpaceLinks(args.requestContext)}
    hrdListHTML = j.core.portal.active.templates.render('system/hamburgermenu/structure.html', menulinks=menulinks)
    script = j.core.portal.active.templates.render('system/hamburgermenu/script.js', hrdListHTML=hrdListHTML).replace('\n', '')
    style = j.core.portal.active.templates.render('system/hamburgermenu/style.css')

    page.addCSS('/jslib/bootstrap/css/off-canvas/jasny-bootstrap.css')
    page.addCSS(cssContent=style)
    page.addMessage('''<script type="text/javascript">%s</script>''' % script)
    page.addMessage('''
        <script src="/jslib/bootstrap/js/off-canvas/jasny-bootstrap.js" type="text/javascript"></script>
    ''')
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
