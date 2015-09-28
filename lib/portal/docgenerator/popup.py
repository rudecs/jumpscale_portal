class Popup(object):
    def __init__(self, id, submit_url, header='', action_button='Confirm', form_layout='', reload_on_success=True, navigateback=False, clearForm=True):
        self.widgets = []
        self.id = id
        self.form_layout = form_layout
        self.header = header
        self.action_button = action_button
        self.submit_url = submit_url
        self.reload_on_success = reload_on_success
        self.navigateback = navigateback
        self.clearForm = clearForm

        import jinja2
        self.jinja = jinja2.Environment(variable_start_string="${", variable_end_string="}")

    def addText(self, label, name, required=False, type='text', value='', placeholder=''):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="${type}" value="${value}", class="form-control" name="${name}" {% if required %}required{% endif %} placeholder="${placeholder}">
              </div>
        ''')
        content = template.render(label=label, name=name, type=type, value=value, required=required, placeholder=placeholder)
        self.widgets.append(content)

    def addHiddenField(self, name, value):
        template = self.jinja.from_string('''
            <input type="hidden" class="form-control" name="${name}" value="${value}">
        ''')
        content = template.render(value=value, name=name)
        self.widgets.append(content)

    def addTextArea(self, label, name, required=False, placeholder=''):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <textarea class="form-control" name="${name}" {% if required %}required{% endif %} placeholder="${placeholder}">
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, placeholder=placeholder)
        self.widgets.append(content)

    def addNumber(self, label, name, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <input type="number" class="form-control" name="${name}" {% if required %}required{% endif %}>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required)
        self.widgets.append(content)

    def addDropdown(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height" for="${name}">${label}</label>
                <select class="form-control" name="${name}" {% if required %}required{% endif %}>
                    {% for title, value in options %}
                        <option value="${value}">${title}</option>
                    {% endfor %}
                </select>
              </div>
        ''')
        content = template.render(label=label, name=name, required=required, options=options)
        self.widgets.append(content)

    def addRadio(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value in options %}
                    <label>
                        <input type="radio" name="${name}" value="${value}" {% if required %}required{% endif %}>
                            ${title}
                        </input>
                    </label>
                {% endfor %}
              </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def addCheckboxes(self, label, name, options, required=False):
        template = self.jinja.from_string('''
            <div class="form-group">
                <label class="line-height">${label}</label>
                {% for title, value, checked in options %}
                    <label class="checkbox">
                      <input type="checkbox" {% if checked %}checked{% endif%} {% if required %}required{% endif %} name="${name}" value="${value}" />
                      ${title}
                    </label>
                {% endfor %}
            </div>
        ''')
        content = template.render(label=label, name=name, options=options, required=required)
        self.widgets.append(content)

    def write_html(self, page):
        template = self.jinja.from_string('''
            <form role="form" method="post" action="${submit_url}" class="popup_form">
            <div id="${id}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="${id}Label" aria-hidden="true">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>
                    <div id="${id}Label" class="modal-header-text">${header}</div>
                  </div>
                  <div class="modal-body modal-body-form">
                    <div class="modal-body modal-body-error alert alert-danger padding-all-small padding-left-large">
                      Error happened on the server
                    </div>
                    {% for widget in widgets %}${widget}{% endfor %}
                  </div>
                  <div class="modal-footer">
                    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                    <button class="btn btn-primary" data-loading-text="Loading...">${action_button}</button>
                  </div>
                </div>
            </div>
        </form>
        ''')

        content = template.render(id=self.id, header=self.header, action_button=self.action_button, form_layout=self.form_layout,
                                widgets=self.widgets, submit_url=self.submit_url)

        css = '.modal-body-error { display: none } .modal-header-text { font-weight: bold; font-size: 24.5px; line-height: 30px; }'
        if css not in page.head:
            page.addCSS(cssContent=css)

        jsLink = '/jslib/old/jquery.form/jquery.form.js'
        if jsLink not in page.head:
            page.addJS(jsLink)

        js = self.jinja.from_string('''$(function(){
            $('#${id}').parent().ajaxForm({
                clearForm: ${'true' if clearform else 'false' },
                beforeSubmit: function(formData, $form, options) {
                    this.popup = $form;
                    var extradata = $form.data('extradata');
                    if (extradata) {
                        for (var name in extradata) {
                            formData.push({'name': name, 'value': extradata[name]});
                        }
                    }
                    $form.find('.modal-footer > .btn-primary').button('loading');
                    $form.find("input,select,textarea").prop("disabled", true)
                },
                success: function(responseText, statusText, xhr) {
                    this.popup.find('.modal').modal('hide');
                    this.popup.find('.modal-body').hide();
                    this.popup.find('.modal-body-form').show();

                    //in case we reload we need to reset the form here
                    this.popup.find("input,select,textarea").prop("disabled", false)
                    this.popup.find('.modal-footer > .btn-primary').button('reset').show();
                    var extracallback = this.popup.data('extracallback');
                    if (extracallback) {
                        extracallback();
                    }
                    {% if navigateback %}
                    window.location = document.referrer;
                    {% elif reload %}
                    location.reload();
                    {% endif %}
                },
                error: function(response, statusText, xhr, $form) {
                    if (response) {
                        var responsetext = response.responseJSON || response.responseText;
                        this.popup.find('.modal-body-error').text(responsetext);
                    }
                    if (response && (response.status == 400 || response.status == 409)){
                        this.popup.find("input,select,textarea").prop("disabled", false)
                        this.popup.find('.modal-footer > .btn-primary').button('reset').show();
                    } else {
                        this.popup.find('.modal-body').hide();
                        this.popup.find('.modal-footer > .btn-primary').hide();
                    }
                    this.popup.find('.modal-body-error').show();
                }
            });
            $('#${id}').on('hidden.bs.modal', function () {
                $(this).find("input,select,textarea").prop("disabled", false)
                $(this).find('.modal-footer > .btn-primary').button('reset').show();
                $(this).find('.modal-body').hide();
                $(this).find('.modal-body-form').show();
            });
        });''')

        js = js.render(id=self.id, reload=self.reload_on_success, navigateback=self.navigateback, clearform=self.clearForm)

        if js not in page.head:
            page.addJS(jsContent=js)

        page.addMessage(content)
