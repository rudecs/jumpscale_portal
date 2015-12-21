
def main(j, args, params, tags, tasklet):
    page = args.page
    state = j.core.grid.healthchecker.fetchState()
    iconclass = {'OK': 'health-success',
                 'WARNING': 'health-warning',
                 'ERROR': 'health-danger',
                 }
    klass = iconclass.get(state, iconclass['WARNING'])
    page.body = page.body.replace('$$$menuleft', "<li><a href='/grid/Status Overview'>"
                                                 "<div title='Health Status' class='circle-dot glyphicon %s'>"
                                                 "</div></a></li>" % (klass))
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
