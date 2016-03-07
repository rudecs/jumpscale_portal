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
    title = args.getTag('title', 'Action')
    gridbinding = args.getTag('gridbinding', '').split()
    content = "\n".join(macrostr.split("\n")[1:-1])

    if not content:
        return _showexample()

    actionoptions = []
    actions = yaml.load(content)
    if actions == content:
        return _showexample()

    if not isinstance(actions, list):
      actions = [actions]

    for actiondata in actions:
        actionurl = actiondata['action']
        display = actiondata['display']
        inputs = actiondata.get('input', '')
        navigateback = actiondata.get('navigateback', False)
        reload = actiondata.get('reload', True)
        clearForm = actiondata.get('clearform', True)
        hide = actiondata.get('hide', False)
        data = actiondata.get('data', {})
        showresponse = actiondata.get('showresponse', False)
        hideon = actiondata.get('hideon', [])
        if hideon:
            hideon_input = actiondata.get('hideonInput', '')
            if hideon_input in hideon:
                continue

        action = "$('%s').modal('show');"

        if actionurl.startswith("#"):
            actionoptions.append((display, action % actionurl))
            continue
        else:
            actionid = "action-%s" % display.replace(' ', '')
            if not hide:
                actionoptions.append((display, action % ('#' + actionid)))

        popup = Popup(id=actionid, header="Confirm Action %s" % display, submit_url=actionurl,
                      navigateback=navigateback, reload_on_success=reload,
                      showresponse=showresponse, clearForm=clearForm, gridbinding=gridbinding)
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
                        elif var['type'] == 'checkboxes':
                            popup.addCheckboxes(label, name, options)
                        elif var['type'] == 'radio':
                            popup.addRadio(label, name, options)
                    elif var['type'] in ('text', 'password', 'number'):
                        label = var['label']
                        name = var['name']
                        default = var.get('default', '')
                        popup.addText(label, name, type=var['type'], value=default)
                    elif var['type'] == 'hidden':
                        popup.addHiddenField(var['name'], var['value'])
                    elif var['type'] == 'message':
                        popup.addMessage(var['message'], var['messagetype'])

        for name, value in data.items():
            popup.addHiddenField(name, value)

        popup.write_html(page)

    if len(actionoptions) >= 1:
        actionsid = None
        if gridbinding:
            actionsid = "actions_%s" % gridbinding[0]
            jscontent = """
    $(document).on('init.dt', function(e, settings) {
        var actionid = '#actions_' + settings.sTableId;
        var action = $(actionid);
        if (action) {
            action.css('margin', '10px');
            var container = '#' + settings.sTableId + '_length';
            $(container).append(action);
            var tableid = '#' + settings.sTableId;
            var table = $(tableid);
            if (table.dataTable().fnSettings().oInit.select) {
                var link = $('<a href="#">Select All</a>');
                var selected = false;
                link.click(function (e) {
                    e.preventDefault();
                    var rows = table.DataTable().rows();
                    if (!selected) {
                        rows.select();
                        $(this).text('Clear Selection');
                    } else {
                        rows.deselect();
                        $(this).text('Select All');
                    }
                    selected = !selected;
                });
                $(container).append(link);
            }
        }
    });
"""
            page.addDocumentReadyJSfunction(jscontent)
        page.addBootstrapCombo(title, actionoptions, actionsid)
    params.result = page

    return params


def match(j, args, params, tags, tasklet):
    return True
