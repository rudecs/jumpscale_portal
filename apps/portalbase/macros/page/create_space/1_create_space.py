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
<body id="markdown-portal">
{{ApplyFlatTheme}}
<header style="padding: 0;">
<nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">
<div class="header-container container">
<div class="navbar-header">
<button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#navbar-collapse-01">
<span class="sr-only">Toggle navigation</span>
</button>
<a class="navbar-brand" href="#">Portal/Jumpscale7</a>
</div>
<div class="navbar-collapse" id="navbar-collapse-01">
<ul id="menu-container" class="nav navbar-nav navbar-left">
{{adminmenu}}{{find}}
{{menu:
Documentation:/Help
}}
</ul>
</div><!-- /.navbar-collapse -->
</div>
</nav>
</header>
<div class="container">
<div class="col-md-2 navigation">
{{navigation}}
</div>
<div class="col-md-10" markdown="1">
{{breadcrumbs}}
{% block body %}{% endblock %}
</div>
</div>
<footer class="container">
</footer>
<script src="/jslib/flatui/js/flat-ui.min.js"></script>
</body>
</html>
'''

def errmsg(s):
    return '<div class="alert alert-danger" role="alert">%s</div>'%(s)

def main(j, args, params, tags, tasklet):
    import re
    params.result = page = args.page

    portal = j.core.portal.active
    contentdir = args.paramsExtra.get('contentdir')
    space_path = args.paramsExtra.get('space_path')
    space_type = args.paramsExtra.get('space_type')

    if contentdir and space_path:
        if not (j.dirs.baseDir in space_path or j.dirs.codeDir in space_path):
            page.addMessage(errmsg('***ERROR***: The space path is incorrect, please add full path.'))

        real_space_path = os.path.realpath(space_path)
        permitted_dirs = [j.dirs.baseDir, j.dirs.codeDir]
        if not any(not os.path.relpath(real_space_path, p).startswith('..') for p in permitted_dirs):
            page.addMessage(errmsg('***ERROR***: The space path should only be under {}' \
                .format(" or ".join(permitted_dirs))))
            return params

        if not re.search('^[/\w\d]+$', real_space_path):
            page.addMessage(errmsg('***ERROR***: The space path should not contain any special characters'))
            return params

        if os.path.exists(space_path):
            page.addMessage(errmsg('***ERROR***: The space path "{}" already exists'.format(space_path)))
            return params


        if not os.path.exists(contentdir):
            page.addMessage(errmsg('***ERROR***: The content dir "{}" does not exist'.format(contentdir)))
            return params

        for directory in os.listdir(contentdir):
            space_name = os.path.basename(space_path)
            if space_name == directory or\
               space_name == os.path.basename(os.readlink(os.path.join(contentdir, directory))):
                page.addMessage(
                    errmsg('***ERROR***: The space name "{0}" with contentdir "{1}" already exists'.format(space_name,
                                                                                                           contentdir)))
                return params

        portal.spacesloader = j.core.portalloader.getSpacesLoader()
        os.makedirs(os.path.join(space_path, '.space'))
        os.symlink(space_path, os.path.join(contentdir, os.path.basename(space_path)))

        with open(os.path.join(space_path, '.space', 'acl.cfg'), 'w') as f:
            f.write(acl_cfg)

        with open(os.path.join(space_path, '.space', 'main.cfg'), 'w') as f:
            f.write(main_cfg)

        if space_type == "md":
            spacename = j.system.fs.getBaseName(space_path).lower()
            with open(os.path.join(space_path, '.space', 'nav.md'), 'w') as f:
                f.write('Home:/{}/Home'.format(spacename))

            with open(os.path.join(space_path, '.space', 'default.md'), 'w') as f:
                f.write(default_wiki)

            with open(os.path.join(space_path, 'home.md'), 'w') as f:
                f.write('''{{% extends ".space/default.md" %}}{{% block body %}}\n##Welcome to the new space\nThis space lives in `{}`{{% endblock %}}'''.format(space_path))

        portal.spacesloader.scan(portal.contentdirs)
        if space_type == 'wiki':
            spacename = j.system.fs.getBaseName(space_path).lower()
            portal.spacesloader.id2object[spacename].createDefaults(space_path)

        page.addMessage('Created successfully. Click <a href="/{}/">here</a> to go to the new portal'.format(os.path.basename(space_path)))

    else:
        contentdirs = ''.join('<option value="{0}">{0}</option>'.format(d) for d in portal.contentdirs)

        page.addMessage('''
            <form class="form-horizontal" method="get" action="/system/createspace">
                <fieldset>
                    <div class="control-group">
                        <label class="control-label" for="space_path">Path to space</label>
                        <div class="controls">
                            <input name="space_path" type="text" placeholder="" class="input-xxlarge width-40" required="" value="/opt/code/github/jumpscale/www_<my_space>">
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
                    <div class="control-group margin-bottom-large">
                        <label class="control-label" for="space_type">Space type</label>
                        <div class="controls" name="space_type">
                            <select name="space_type" id="space_type" class="input-xxlarge width-40">
                                <option value="wiki">Portal Wiki</option>
                                <option value="md">Markdown</option>
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
