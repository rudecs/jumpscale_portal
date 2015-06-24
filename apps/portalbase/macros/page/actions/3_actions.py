def main(j, args, params, tags, tasklet):
    page = args.page
    from JumpScale.portal.docgenerator.popup import Popup
    import yaml

    def _showexample():
        page.addMessage("""Actions must be in yaml form.
eg:
- display: Start
  action: /restmachine/cloudbroker/machine/start
  input:
  - reason
  - spacename
  - name: accesstype
    type: dropdown
    label: ACL
    values:
     - label: Admin
       value: ARCXDU
     - label: Write
       value: RCX
     - label: Read
       value: R

  data:
   machineId: $$id
   accountName: $$accountname

- display: Stop
  action: /restmachine/cloudbroker/machine/stop?machineId=$$id&reason=ops&accountName=$$accountname&spaceName=$$spacename
}}
""")
        params.result = page
        return params

    macrostr = args.macrostr.strip()
    content = "\n".join(macrostr.split("\n")[1:-1])

    if not content:
        return _showexample()

    actionoptions = [('Choose Action', '#')]
    actions = yaml.load(content)
    if actions == content:
        return _showexample()

    for actiondata in actions:
        actionurl = actiondata['action']
        display = actiondata['display']
        inputs = actiondata.get('input', '')
        data = actiondata.get('data', {})
        if actionurl.startswith("#"):
            actionoptions.append((display, actionurl[1:]))
            continue
        else:
            actionid = "action-%s" % display.replace(' ', '')
            actionoptions.append((display, actionid))

        popup = Popup(id=actionid, header="Confirm Action %s" % display, submit_url=actionurl)
        if inputs:
            for var in inputs:
                if isinstance(var, basestring):
                    popup.addText(var, var)
                else:
                    if var['type'] in ('dropdown', 'radio'):
                        label = var['label']
                        name = var['name']
                        options = list()
                        for value in var['values']:
                            options.append((value['label'], value['value']))
                        if var['type'] == 'dropdown':
                            popup.addDropdown(label, name, options)
                        elif var['type'] == 'radio':
                            popup.addRadio(label, name, options)
                    elif var['type'] in ('text', 'password'):
                        label = var['label']
                        name = var['name']
                        password = var['type'] == 'password'
                        popup.addText(label, name, type=var['type'])

        for name, value in data.items():
            popup.addHiddenField(name, value)

        popup.write_html(page)

    id = page.addComboBox(actionoptions)
    page.addJS(None, """
        $(document).ready(function() {
            $("#%(id)s").change(function () {
                 var actionid = $("#%(id)s").val();
                 if (actionid != '#'){
                    $('#'+actionid).modal('show');
                 }
            });
            $(".popup_form > .modal").on('hidden.bs.modal', function() {
                $("#%(id)s").val('#');
            });
        });
        """ % ({'id':id}))
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
