
def main(j, args, params, tags, tasklet):

    import urlparse
    import urllib
    # import urllib.request, urllib.error
    

    querystr = args.requestContext.env['QUERY_STRING']
    querytuples = urlparse.parse_qsl(querystr)
    for item in querytuples[:]:
        if item[0] in ['space', 'page']:
            querytuples.remove(item)
    querystr = urllib.urlencode(querytuples)

    page = args.page
    page.addCSS('/jslib/bootstrap/css/bootstrapmarkdown/bootstrap-markdown.min.css')
    page.addCSS(cssContent='''
        .md-editor.md-fullscreen-mode .md-input, .md-editor.md-fullscreen-mode .md-preview{ 
            font-size: 15px!important; 
        }
        .form-btn{
            padding: 2px 40px !important;
            margin-right: 15px;
        }
    ''')
    
    page_name = ''

    import re
    page_match = re.search(r"page\s*:\s*([^:}]*)", args.macrostr)
    if page_match:
        page_name = page_match.group(1)

    args = args.tags.getValues(app="", actor="", path="", bucket="", page="", space="")

    if page_name == "" and args["path"] == "":
        page.addMessage("ERROR: path needs to be defined in: %s" % params.cmdstr)
        params.result = page
        return params

    if args["app"] != "" and args["actor"] != "":
        # look for path for bucket
        aloader = j.core.portal.active.actorsloader.getActorLoaderFromId("%s__%s" % (args["app"].lower(), args["actor"].lower()))
        path = j.system.fs.joinPaths(aloader.model.path, args["path"])
    elif args["space"] != "":
        # look for path for bucket
        space = j.core.portal.active.getSpace(args["space"])
        if page_name != "":
            space = j.core.portal.active.getSpace(args["space"])
            doc = space.docprocessor.docGet(page_name)
            path = doc.path
            args["edit"] = True
        else:
            path = j.system.fs.joinPaths(space.model.path, args["path"])
    elif args["bucket"] != "":
        # look for path for bucket
        bucket = j.core.portal.active.getBucket(args["bucket"])
        path = j.system.fs.joinPaths(bucket.model.path, args["path"])
    else:
        page.addMessage("ERROR: could not find file as defined in: %s" % params.cmdstr)
        params.result = page
        return params
    if not j.system.fs.exists(path):
        page.addMessage('Supplied path "%s" does not exist.' % args['path'])
        params.result = page
        return params
    
    spaceName = doc.getSpaceName()
    content = j.system.fs.fileGetContents(path)
    content = content.replace("'", "\\'").replace('"', '\\"').replace("\n", "\\n").replace('{{','\\\{\\\{')
    guid = j.base.idgenerator.generateGUID()
    contents = {'path': doc.path, 'querystr': '', 'page': page_name, 'space': spaceName}
    j.apps.system.contentmanager.dbmem.cacheSet(guid, contents, 60)
    page.addJS('/jslib/bootstrap/js/bootstrapmarkdown/bootstrap-markdown.js')
    page.addMessage('''
        <form name="editFileForm" method="post" action="/restmachine/system/contentmanager/wikisave?cachekey={guid}">
            <textarea id="markdownEditor" name="text" data-provide="markdown" cols='60' rows='8'></textarea>
            <div style="text-align: center; margin: 30px 0;">
                <input type="submit" class="btn btn-lg btn-primary form-btn" value="Save">
                <input type="submit" href="../{spaceName}/{pageName}" class="btn btn-lg form-btn" value="Cancel">
            </div>
        </form>
        <script>
            jQuery("#markdownEditor").val("{content}");
            jQuery("#markdownEditor").markdown({{hiddenButtons:'cmdPreview', autofocus:false, savable:false, height: 700}});
        </script>
    '''.format(content=content, guid=guid, pageName=page_name, spaceName=spaceName))
    params.result = page
    return params


def match(j, args, params, tags, tasklet):
    return True
