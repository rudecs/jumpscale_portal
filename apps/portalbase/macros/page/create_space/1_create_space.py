import os

acl_cfg = '''all:R
admin:*
guests:R
guest:R
'''

main_cfg = '''[main]
id = cloudscalers_operations
'''

default_wiki = '''
<html>
<head>
    <link rel="stylesheet" href="/jslib/bootstrap/css/bootstrap-3-3-1.min.css">
    <link rel="stylesheet" href="/jslib/old/bootstrap/css/bootstrap-responsive.css">
    <link rel="stylesheet" href="/jslib/flatui/css/flat-ui.css">
    <link rel="stylesheet" href="/jslib/new-ui/new-ui.css">
</head>
<body style="background: #ECF0F1;">
<header class="container" style="padding: 0;">
<div>
<nav class="navbar navbar-inverse navbar-embossed" role="navigation">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-01">
<span class="sr-only">Toggle navigation</span>
</button>
<a class="navbar-brand" href="#">Portal/Jumpscale7</a>
</div>
<div class="navbar-collapse" id="navbar-collapse-01">
<ul class="nav navbar-nav navbar-left" style="width: 80%;">
{{adminmenu}}{{find}}
{{menu:
Documentation:/Help
Incubaid:http://www.incubaid.com
}}
</ul>
</div><!-- /.navbar-collapse -->
</nav>
</div>
</header>
<div class="container" style="background: #fff;">
<div class="col-md-2 navigation">
{{navigation}}
</div>
<div class="col-md-10" markdown="1">
{% block body %}{% endblock %}
</div>
</div>
<footer class="container">
</footer>
<script src="/jslib/jquery/jquery-2.0.3.min.js"></script>
<script src="/jslib/flatui/js/flat-ui.min.js"></script>
</body>
</html>
'''

def main(j, args, params, tags, tasklet):
    params.result = page = args.page

    portal = j.core.portal.active
    contentdir = args.paramsExtra.get('contentdir')
    space_path = args.paramsExtra.get('space_path')

    if contentdir and space_path:
        if os.path.exists(space_path):
            page.addMessage('***ERROR***: The space path "{}" already exists'.format(space_path))
            return params

        if not os.path.exists(contentdir):
            page.addMessage('***ERROR***: The content dir "{}" does not exist'.format(contentdir))
            return params

        os.makedirs(os.path.join(space_path, '.space'))
        os.symlink(space_path, os.path.join(contentdir, os.path.basename(space_path)))

        with open(os.path.join(space_path, '.space', 'acl.cfg'), 'w') as f:
            f.write(acl_cfg)

        with open(os.path.join(space_path, '.space', 'main.cfg'), 'w') as f:
            f.write(main_cfg)

        with open(os.path.join(space_path, '.space', 'nav.md'), 'w') as f:
            f.write('Home:Home')

        with open(os.path.join(space_path, '.space', 'default.md'), 'w') as f:
            f.write(default_wiki)

        with open(os.path.join(space_path, 'home.md'), 'w') as f:
            f.write('''
{{% extends ".space/default.md" %}}{{% block body %}}
##Welcome to the new space 
This space lives in `{}`{{% endblock %}}
                '''.format(space_path))

        
        portal.spacesloader = j.core.portalloader.getSpacesLoader()
        portal.spacesloader.scan(portal.contentdirs)

        page.addMessage('Created successfully. Click <a href="/{}/">here</a> to go to the new portal'.format(os.path.basename(space_path)))

    else:
        contentdirs = ''.join('<option value="{0}">{0}</option>'.format(d) for d in portal.contentdirs)

        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/createspace">
                <fieldset>
                    <div class="control-group">
                        <label class="control-label" for="space_path">Path to space</label>
                        <div class="controls">
                            <input name="space_path" type="text" placeholder="" class="input-xxlarge width-40" required="" value="/opt/code/incubaid/www_<my_space>">
                        </div>
                    </div>

                    <div class="control-group margin-bottom-large">
                        <label class="control-label" for="contentdir">Content Directory</label>
                        <div class="controls" name="contentdir">
                            <select name="contentdir" id="contentdir" class="input-xxlarge width-40">
                            {0}
                            </select>
                        </div>
                    </div>

                    <div class="control-group">
                        <div class="controls">
                            <button class="btn btn-primary">Create</button>
                        </div>
                    </div>

                </fieldset>
            </form>'''.format(contentdirs))

    return params


def match(j, args, params, tags, tasklet):
    return True
