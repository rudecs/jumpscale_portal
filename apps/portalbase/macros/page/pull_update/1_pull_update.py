import os

def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    space_name = args.cmdstr.strip()
    space = j.core.portal.active.getSpace(space_name)
    space_path = os.path.abspath(space.model.path)

    try:
        j.system.process.execute('cd %s;git pull' % space_path)
        page.addMessage('Pulled and Updated')
    except Exception, error:
        page.addMessage(error)

    return params


def match(j, args, params, tags, tasklet):
    return True