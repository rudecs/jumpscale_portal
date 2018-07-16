def main(j, args, params, tags, tasklet):
    import json
    page = args.page
    data = {'action': args.getTag('id'),
            'action_class': args.getTag('class') or '',
            'deleterow': args.getTag('deleterow') or 'false',
            'label': args.getTag('label') or '',
            'tags': j.core.tags.getObject(args.cmdstr, None, True).getDict()
            }

    element = page.getActionHtml(**data)
    page.addMessage(element)
    page.addJS('/system/.files/js/action.js', header=False)
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
