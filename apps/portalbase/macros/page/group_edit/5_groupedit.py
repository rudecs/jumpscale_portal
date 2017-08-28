from JumpScale.portal.docgenerator.popup import Popup
from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    groupguid = args.getTag('guid')
    if groupguid is None:
        raise exceptions.BadRequest("BadRequest", "text/plain")
    scl = j.clients.osis.getNamespace('system')
    group = None
    guidExists = scl.group.search({'id': groupguid})[1:]
    if guidExists:
        group = scl.group.get(groupguid)
    if not group:
        return params
    popup = Popup(id='group_edit', header='Change Group', clearForm=False, submit_url='/restmachine/system/usermanager/editGroup')

    options = list()
    popup.addText('Enter domain', 'domain', value=group.domain)
    popup.addText('Enter description', 'description', value=group.description)
    for user in scl.user.search({})[1:]:
        available = user['id'] in group.users
        options.append((user['id'], user['id'], available))
    popup.addCheckboxes('Select Users', 'users', options)
    popup.addHiddenField('name', group.id)
    popup.write_html(page)

    return params
