import json

class Popup(object):
    def __init__(self, id, submit_url, header='', action_button='Confirm', form_layout='', reload_on_success=True, navigateback=False, clearForm=True, showresponse=False):
        self.widgets = []
        self.id = id
        self.form_layout = form_layout
        self.header = header
        self.action_button = action_button
        self.submit_url = submit_url
        self.showresponse = showresponse
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


    def addMessage(self, message, type='info'):
        template = self.jinja.from_string('''
            <div class="alert alert-${type} padding-vertical-small" role="alert">
            ${message}
            </div>
        ''')
        content = template.render(type=type, message=message)
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
        <form role="form" method="post" action="${submit_url}" class="popup_form"
        {% for key, value in data.iteritems() -%}
            data-${key}="${value}"
        {%- endfor %}
        >
            <div id="${id}" class="modal fade" tabindex="-1" role="dialog" aria-labelledby="${id}Label" aria-hidden="true">
                <div class="modal-content">
                  <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-hidden="true">x</button>
                    <div id="${id}Label" class="modal-header-text">${header}</div>
                  </div>
                  <div class="modal-body-container">
                    <div class="modal-body modal-body-error alert alert-danger padding-all-small padding-left-large">
                        <pre>Error happened on the server</pre>
                    </div>
                    <div class="modal-body modal-body-message alert alert-success padding-all-small padding-left-large">
                    </div>
                    <div class="modal-body modal-body-form">
                    {% for widget in widgets %}${widget}{% endfor %}
                    </div>
                  </div>
                  <div class="modal-footer">
                    <button class="btn" data-dismiss="modal" aria-hidden="true">Close</button>
                    <button class="btn btn-primary" data-loading-text="Loading...">${action_button}</button>
                  </div>
                </div>
            </div>
        </form>
        ''')
        data = {'clearform': json.dumps(self.clearForm),
                'reload': json.dumps(self.reload_on_success),
                'showresponse': json.dumps(self.showresponse),
                'navigateback': json.dumps(self.navigateback)}
        content = template.render(id=self.id, header=self.header, action_button=self.action_button, form_layout=self.form_layout,
                                widgets=self.widgets, submit_url=self.submit_url, clearForm=self.clearForm, data=data)

        css = '.modal-header-text { font-weight: bold; font-size: 24.5px; line-height: 30px; }'
        if css not in page.head:
            page.addCSS(cssContent=css)

        jsLink = '/jslib/old/jquery.form/jquery.form.js'
        page.addJS(jsLink, header=False)

        js = self.jinja.from_string('''$(function(){
            $(".modal-body-error, .modal-body-message").hide();
            var resetForm = function($form) {
                $form.find('.modal-body').hide();
                $form.find('.modal-body-form').show();

                //in case we reload we need to reset the form here
                $form.find("input,select,textarea").prop("disabled", false)
                $form.find('.modal-footer > .btn-primary').button('reset').show();

            };
            $('.popup_form').ajaxForm({
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
                    var extracallback = this.popup.data('extracallback');
                    if (extracallback) {
                        extracallback();
                    }
                    if (this.popup.data('clearform') === true) {
                        this.popup.clearForm();
                    }
                    if (this.popup.data('showresponse') === true) {
                        resetForm(this.popup);
                        this.popup.find('.modal-footer > .btn-primary').hide();
                        this.popup.find('.modal-body-form').hide();
                        this.popup.find('.modal-body-message').show();
                        this.popup.find('.modal-body-message').text(responseText);
                        return;

                    } else {
                        this.popup.find('.modal').modal('hide');
                    }
                    if (this.popup.data('navigateback') === true) {
                        resetForm(this.popup);
                        window.location = document.referrer;
                    } else if (this.popup.data('reload') === true) {
                        resetForm(this.popup);
                        location.reload();
                    }
                },
                error: function(response, statusText, xhr, $form) {
                    if (response) {
                        var errortext = response.responseJSON || response.responseText;
                        try {
                            var eco = JSON.parse(errortext);
                            errortext = eco.backtrace || errortext;
                        } catch (e) {
                            // dont do anything just use errortext
                        }
                        this.popup.find('.modal-body-error > pre').text(errortext);
                    }
                    if (response && (response.status == 400 || response.status == 409)){
                        this.popup.find("input,select,textarea").prop("disabled", false)
                        this.popup.find('.modal-footer > .btn-primary').button('reset').show();
                    } else {
                        this.popup.find('.modal-body-form').hide();
                        this.popup.find('.modal-footer > .btn-primary').hide();
                    }
                    this.popup.find('.modal-body-error').show();
                }
            });
            $('.popup_form').on('hidden.bs.modal', function () {
                resetForm($(this));
            });
        });''')

        js = js.render()

        page.addJS(jsContent=js, header=False)

        page.addMessage(content)
