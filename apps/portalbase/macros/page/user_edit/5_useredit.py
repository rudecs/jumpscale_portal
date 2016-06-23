from JumpScale.portal.docgenerator.popup import Popup
from JumpScale.portal.portal import exceptions

def main(j, args, params, tags, tasklet):

    params.result = page = args.page
    userguid = args.getTag('guid')
    if not userguid:
        raise exceptions.BadRequest("BadRequest", "text/plain")
    scl = j.clients.osis.getNamespace('system')
    user = scl.user.get(userguid)

    popup = Popup(id='user_edit', header='Update User',
                  submit_url='/restmachine/system/usermanager/editUser', clearForm=False)

    options = list()
    popup.addText('Enter Email Address', 'emails', value=', '.join(user.emails),
                  placeholder='If left empty, email address will not be changed')
    popup.addHiddenField('domain', user.domain)
    popup.addText('Enter Password', 'password', type='password',
                  placeholder='If left empty, password will not be changed')
    for group in scl.group.search({})[1:]:
        available = group['id'] in user.groups
        options.append((group['id'], group['id'], available))

    popup.addCheckboxes('Select Groups', 'groups', options)
    popup.addHiddenField('username', user.id)
    popup.write_html(page)

    return params
