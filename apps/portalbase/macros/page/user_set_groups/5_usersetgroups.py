from JumpScale.portal.docgenerator.popup import Popup

def main(j, args, params, tags, tasklet):
    params.result = page = args.page
    username = args.getTag('userid')
    user = j.apps.system.usermanager._getUser(username)
    if not user:
        return params

    scl = j.clients.osis.getNamespace('system')
    popup = Popup(id='user_set_groups', header='Change User Groups', submit_url='/restmachine/system/usermanager/setGroups')

    options = list()
    for group in scl.group.search({})[1:]:
        available = group['id'] in user.groups
        options.append((group['id'], group['id'], available))

    popup.addCheckboxes('Select Groups', 'groups', options)
    popup.addHiddenField('username', username)
    popup.write_html(page)

    return params
