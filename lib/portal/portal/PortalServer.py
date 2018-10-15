import urlparse
import collections
import types
import pprint
import os
import sys
import requests
import gevent
import time
import urllib
import cgi
import json
import mimeparse
import mimetypes
import inspect

from beaker.middleware import SessionMiddleware
from .MacroExecutor import MacroExecutorPage, MacroExecutorWiki, MacroExecutorPreprocess, MacroexecutorMarkDown
from .RequestContext import RequestContext
from .PortalRest import PortalRest
from .OsisBeaker import OsisBeaker
from .MinimalBeaker import MinimalBeaker
from . import exceptions
from .auth import AuditMiddleWare

from JumpScale.portal.portalloaders.SpaceWatcher import SpaceWatcher
from JumpScale.portal.html import multipart

from JumpScale import j
from gevent.pywsgi import WSGIServer
from PortalAuthenticatorGitlab import PortalAuthenticatorGitlab
from PortalAuthenticatorMinimal import PortalAuthenticatorMinimal
from PortalAuthenticatorOSIS import PortalAuthenticatorOSIS
from PortalTemplate import PortalTemplate


BLOCK_SIZE = 4096

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_JS = 'application/javascript'
CONTENT_TYPE_YAML = 'application/yaml'
CONTENT_TYPE_PLAIN = 'text/plain'
CONTENT_TYPE_HTML = 'text/html'
CONTENT_TYPE_PNG = 'image/png'


def exhaustgenerator(func):
    def wrapper(self, env, start_response):
        try:
            result = func(self, env, start_response)
        except exceptions.BaseError as e:
            start_response("%s %s" % (e.code, e.status), e.headers)
            return [e.msg]
        if isinstance(result, basestring):
            return [j.tools.text.toStr(result)]
        elif isinstance(result, collections.Iterable):
            def exhaust():
                for value in result:
                    yield value
            return exhaust()
        elif not result:
            return ['']
        else:
            return result
    return wrapper


class PortalServer:

    # INIT
    def __init__(self):

        self.cfg = j.application.instanceconfig

        self.contentdirs = list()
        self.libpath = j.html.getHtmllibDir()
        self.started = False
        self.epoch = time.time()
        self.force_oauth_instance = self.cfg.get('force_oauth_instance', "")
        if self.force_oauth_instance:
            self.force_oauth_url = '%s?%s' % ('/restmachine/system/oauth/authenticate',
                                              urllib.urlencode({'type': self.force_oauth_instance}))
        else:
            self.force_oauth_url = None

        j.core.portal.active = self

        self.watchedspaces = []
        self.pageKey2doc = {}
        self.routes = {}
        self.proxies = {}

        self.authentication_method = self.cfg.get("authentication_method")
        secure = urlparse.urlparse(self.cfg['url']).scheme == 'https'
        session_opts = {
            'session.cookie_expires': False,
            'session.httponly': True,
            'session.secure': secure,
            'session.data_dir': '%s' % j.system.fs.joinPaths(j.dirs.varDir, "beakercache")
        }

        if not self.authentication_method:
            minimalsession = {
                'session.type': 'MinimalBeaker',
                'session.namespace_class': MinimalBeaker,
                'session.namespace_args': {'client': None}
            }
            session_opts.update(minimalsession)
            self.auth = PortalAuthenticatorMinimal()
        else:
            if self.authentication_method == 'gitlab':
                self.auth = PortalAuthenticatorGitlab(instance=self.gitlabinstance)
            else:
                self.osis = j.clients.osis.getByInstance(self.cfg.get('connections', {}).get('osis', 'main'))
                osissession = {
                    'session.type': 'OsisBeaker',
                    'session.namespace_class': OsisBeaker,
                    'session.namespace_args': {'client': self.osis}
                }
                session_opts.update(osissession)
                self.auth = PortalAuthenticatorOSIS(self.osis)

        self.loadConfig()

        macroPathsPreprocessor = ["macros/preprocess"]
        macroPathsWiki = ["macros/wiki"]
        macroPathsPage = ["macros/page"]
        macroPathsMarkDown = ["macros/markdown"]

        self.macroexecutorPreprocessor = MacroExecutorPreprocess(macroPathsPreprocessor)
        self.macroexecutorPage = MacroExecutorPage(macroPathsPage)
        self.macroexecutorMarkDown = MacroexecutorMarkDown(macroPathsMarkDown)
        self.macroexecutorWiki = MacroExecutorWiki(macroPathsWiki)
        templatedirs = [j.system.fs.joinPaths(self.portaldir, 'templates'),
                        j.system.fs.joinPaths(self.appdir, 'templates')]
        self.templates = PortalTemplate(templatedirs)
        self.bootstrap()

        self._router = SessionMiddleware(AuditMiddleWare(self.router), session_opts)
        self._webserver = WSGIServer((self.listenip, self.port), self._router)

        self.confluence2htmlconvertor = j.tools.docgenerator.getConfluence2htmlConvertor()
        self.activejobs = list()
        self.jobids2greenlets = dict()

        self.schedule1min = {}
        self.schedule15min = {}
        self.schedule60min = {}

        self.rediscache = j.clients.redis.getByInstance('system')
        self.redisprod = j.clients.redis.getByInstance('system')

        self.jslibroot = j.system.fs.joinPaths(j.dirs.baseDir, "apps", "portals", "jslib")

        #  Load local spaces
        self.rest = PortalRest(self)
        self.spacesloader = j.core.portalloader.getSpacesLoader()
        self.loadSpaces()

    def loadConfig(self):

        def replaceVar(txt):
            # txt = txt.replace("$base", j.dirs.baseDir).replace("\\", "/")
            txt = txt.replace("$appdir", j.system.fs.getcwd()).replace("\\", "/")
            txt = txt.replace("$vardir", j.dirs.varDir).replace("\\", "/")
            txt = txt.replace("$htmllibdir", j.html.getHtmllibDir()).replace("\\", "/")
            txt = txt.replace("\\", "/")
            return txt

        # INIT FILE
        self.portaldir = j.system.fs.getcwd()

        self.appdir = replaceVar(self.cfg.get("appdir", self.portaldir))
        self.appdir = self.appdir.replace("$base", j.dirs.baseDir)

        self.getContentDirs()  # contentdirs need to be loaded before we go to other dir of base server
        j.system.fs.changeDir(self.appdir)

        self.listenip = self.cfg.get('listenip', '0.0.0.0')
        self.port = int(self.cfg.get("port", 82))
        self.addr = self.cfg.get("pubipaddr", '127.0.0.1')
        self.secret = self.cfg.get("secret")
        self.admingroups = self.cfg.get("admingroups", "").split(",")

        self.filesroot = replaceVar(self.cfg.get("filesroot"))
        j.system.fs.createDir(self.filesroot)
        self.defaultspace = self.cfg.get('defaultspace', 'welcome')
        self.defaultpage = self.cfg.get('defaultpage', '')

        self.gitlabinstance = self.cfg.get('connections', {}).get('gitlab', 'main')

        self.logdir = j.system.fs.joinPaths(j.dirs.logDir, "portal", str(self.port))
        j.system.fs.createDir(self.logdir)

        self.getContentDirs()

        # load proxies
        for proxy in self.cfg.get('proxies'):
            self.proxies[proxy['path']] = proxy

    def reset(self):
        self.routes = {}
        self.loadConfig()
        self.bootstrap()
        j.core.codegenerator.resetMemNonSystem()
        j.core.specparser.resetMemNonSystem()
        # self.actorsloader.scan(path=self.contentdirs,reset=True) #do we need to load them all
        self.bucketsloader = j.core.portalloader.getBucketsLoader()
        self.loadSpaces()

    def bootstrap(self):
        self.actors = {}  # key is the applicationName_actorname (lowercase)
        self.actorsloader = j.core.portalloader.getActorsLoader()
        self.app_actor_dict = {}
        self.taskletengines = {}
        self.actorsloader.reset()
        # self.actorsloader._generateLoadActor("system", "contentmanager", actorpath="%s/apps/portalbase/system/system__contentmanager/"%j.dirs.baseDir)
        # self.actorsloader._generateLoadActor("system", "master", actorpath="system/system__master/")
        # self.actorsloader._generateLoadActor("system", "usermanager", actorpath="system/system__usermanager/")
        self.actorsloader.scan(self.contentdirs)

        if self.authentication_method:
            self.actorsloader.getActor("system", "contentmanager")
            self.actorsloader.getActor("system", "usermanager")

    def deleteSpace(self, spacename):
        self.loadSpaces()
        spacename = spacename.lower()
        if spacename in self.spacesloader.spaces:
            space = self.spacesloader.spaces.pop(spacename)
            space.deleteOnDisk()
        else:
            raise RuntimeError("Could not find space %s to delete" % spacename)

    def loadSpaces(self):

        self.bucketsloader = j.core.portalloader.getBucketsLoader()
        self.spacesloader = j.core.portalloader.getSpacesLoader()
        self.bucketsloader.scan(self.contentdirs)

        self.spacesloader.scan(self.contentdirs)

        if self.authentication_method:
            if "system" not in self.spacesloader.spaces:
                raise RuntimeError("could not find system space")

    def getContentDirs(self):
        """
        walk over known content dirs & execute loader on it
        """
        contentdirs = self.cfg.get('contentdirs', '') or ''

        def append(path):
            path = j.system.fs.pathNormalize(path)
            if path not in self.contentdirs:
                self.contentdirs.append(path)

        paths = contentdirs.split(",")

        # add own base path
        self.basepath = j.system.fs.joinPaths(self.portaldir, "base")
        j.system.fs.createDir(self.basepath)
        append(self.basepath)

        paths.append(self.basepath)
        paths = list(set(paths))
        for path in paths:
            path = path.strip()
            if path == "" or path[0] == "#":
                continue
            path = path.replace("\\", "/")
            if path.find(":") == -1:
                if path not in self.watchedspaces:
                    SpaceWatcher(path)
            append(path)

        # add base path of parent portal
        if self.authentication_method:
            appdir = self.appdir
            append(j.system.fs.joinPaths(appdir, "wiki"))
            append(j.system.fs.joinPaths(appdir, "system"))

    def unloadActorFromRoutes(self, appname, actorname):
        for key in list(self.routes.keys()):
            appn, actorn, remaining = key.split("_", 2)
            # print appn+" "+appname+" "+actorn+" "+actorname
            if appn == appname and actorn == actorname:
                self.routes.pop(key)

# USER RIGHTS

    def getAccessibleLocalSpacesForGitlabUser(self, gitlabspaces):
        """
        Return Local Spaces (Non Gitlab Spaces) with guest permissions set to READ or higher
        """
        spaces = {}
        localspaces = [x.model.id.lower() for x in self.spacesloader.spaces.values() if x not in gitlabspaces]
        for space in localspaces:
            rights = ''
            spaceobject = self.spacesloader.spaces.get(space)
            for groupuser in ["guest", "guests"]:
                if groupuser in spaceobject.model.acl:
                    r = spaceobject.model.acl[groupuser]
                    if r == "*":
                        rights = "rwa"
                    else:
                        rights = r
            if 'r' in rights or '*' in rights:
                spaces[space] = rights
        return spaces

    def getUserSpaces(self, ctx):
        if not hasattr(ctx, 'env') or "user" not in ctx.env['beaker.session']:
            return []
        username = ctx.env['beaker.session']["user"]
        spaces = self.auth.getUserSpaces(username, spaceloader=self.spacesloader)

        # In case of gitlab, we want to get the local osis spaces tha user has access to
        if self.authentication_method == 'gitlab':
            spaces += self.getAccessibleLocalSpacesForGitlabUser(spaces).keys()

        else:
            result = []
            for s in spaces:
                rights = self.getUserSpaceRights(ctx, s)
                if 'r' in rights[1] or '*' in rights:
                    result.append(s)
            spaces = result
        return list(set(spaces))

    def getUserSpacesObjects(self, ctx):
        """
        Only used in gitlab
        """
        if hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            username = ctx.env['beaker.session']["user"]
            if self.authentication_method == 'gitlab':
                gitlabobjects = self.auth.getUserSpacesObjects(username)
                keys = [x['name'] for x in gitlabobjects]
                for name in self.getAccessibleLocalSpacesForGitlabUser(keys):
                    if username in name and name.replace("%s_" % username, '') in keys:
                        continue
                    gitlabobjects.append({'name': name, 'namespace': {'name': ''}})
                return gitlabobjects

    def getSpaceLinks(self, ctx):
        if self.authentication_method == 'gitlab':
            spaces = {}
            for s in self.getUserSpacesObjects(ctx):
                if s['namespace']['name']:
                    spaces[s['name']] = "%s_%s" % (s['namespace']['name'], s['name'])
                else:
                    spaces[s['name']] = "/%s" % s['name']
        else:
            spaces = {}
            for spaceid in self.getUserSpaces(ctx):
                space = self.getSpace(spaceid, ignore_doc_processor=True)
                if space.model.hidden:
                    continue
                spaces[space.model.name] = "/%s" % spaceid
        return spaces

    def getNonClonedGitlabSpaces(self, ctx):
        """
        Return Gitlab spaces that are not (YET) cloned into local filesystem
        This is helpful to identify non-existing spaces, so that system can disable
        access to them until cloning is finished.

        @param ctx: Context
        """
        if not self.authentication_method == 'gitlab':
            raise RuntimeError("This function only works with gitlab authentication")

        if not hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            return []
        username = ctx.env['beaker.session']["user"]

        clonedspaces = set([s.model.id[s.model.id.index('portal_'):]
                            for s in self.spacesloader.spaces.values() if 'portal_' in s.model.id])
        gitlabspaces = set([s[s.index('portal_'):]
                            for s in self.auth.getUserSpaces(username, spaceloader=self.spacesloader)])
        return gitlabspaces.difference(clonedspaces)

    def getUserSpaceRights(self, ctx, space):
        spaceobject = self.spacesloader.spaces.get(space)

        if hasattr(ctx, 'env') and "user" in ctx.env['beaker.session']:
            username = ctx.env['beaker.session']["user"]
        else:
            return "", ""

        if self.isAdminFromCTX(ctx):
            return username, 'rwa'

        if self.authentication_method == 'gitlab':
            gitlabspaces = self.auth.getUserSpaces(username, spaceloader=self.spacesloader)
            localspaceswithguestaccess = self.getAccessibleLocalSpacesForGitlabUser(gitlabspaces)
            if space in localspaceswithguestaccess:
                return username, localspaceswithguestaccess[space]

        username, rights = self.auth.getUserSpaceRights(username, space, spaceobject=spaceobject)

        return username, rights

    def getUserFromCTX(self, ctx):
        user = ctx.env["beaker.session"].get('user')
        return user or "guest"

    def getGroupsFromCTX(self, ctx):
        user = self.getUserFromCTX(ctx)
        if user:
            groups = self.auth.getGroups(user)
            return [str(item.lower()) for item in groups]
        else:
            return []

    def isAdminFromCTX(self, ctx):
        usergroups = set(self.getGroupsFromCTX(ctx))
        admingroups = set(self.admingroups)
        return bool(admingroups.intersection(usergroups))

    def isLoggedInFromCTX(self, ctx):
        user = self.getUserFromCTX(ctx)
        if user != "" and user != "guest":
            return True
        return False

# process pages, get docs
    def getpage(self):
        page = j.tools.docgenerator.pageNewHTML("index.html", htmllibPath="/jslib")
        return page

    def sendpage(self, page, start_response):
        contenttype = "text/html"
        start_response('200 OK', [('Content-Type', contenttype), ])
        return [page.getContent()]

    def getDoc(self, space, name, ctx, params={}):
        session = ctx.env['beaker.session']
        loggedin = session.get('user', '') not in ['guest', '']
        standard_pages = ["login", "error", "accessdenied", "pagenotfound"]
        spacedocgen = None

        print("GETDOC:%s" % space)
        space = space.lower()
        name = name.lower()

        if not space:
            space = self.defaultspace
            name = self.defaultpage

        if space not in self.spacesloader.spaces:
            if space == "system":
                raise RuntimeError("wiki has not loaded system space, cannot continue")
            ctx.params["error"] = cgi.escape("Could not find space %s\n" % space)
            print("could not find space %s" % space)
            if self.defaultspace and self.defaultspace in self.spacesloader.spaces:
                space = self.defaultspace
            else:
                space = 'system'
            name = "pagenotfound"
        else:
            spaceObject = self.spacesloader.getLoaderFromId(space)
            spacedocgen = spaceObject.docprocessor

            if name in spacedocgen.name2doc:
                pass
            elif name in standard_pages:  # One of the standard pages not found in that space, fall back to system space
                space = "system"
                spacedocgen = None
            elif name == "":
                if space in spacedocgen.name2doc:
                    name = space
                elif "home" in spacedocgen.name2doc:
                    name = 'home'
                else:
                    ctx.params["path"] = cgi.escape("space:%s pagename:%s" % (space, name))
                    name = "pagenotfound"
                    spacedocgen = None
            else:
                ctx.params["path"] = cgi.escape("space:%s pagename:%s" % (space, name))
                name = "pagenotfound"
                spacedocgen = None

        username, right = self.getUserSpaceRights(ctx, space)

        if name in standard_pages:
            if "r" not in right:
                right = "r" + right

        if "r" not in right:
            if loggedin:
                name = "accessdenied"
            elif self.force_oauth_instance:
                name = "accessdenied"
            else:
                name = "login"
            if not spaceObject.docprocessor.docExists(name):
                space = 'system'
                spacedocgen = None

        ctx.params["rights"] = right
        print("# space:%s name:%s user:%s right:%s" % (space, name, username, right))

        params['space'] = space
        params['name'] = name

        if not spacedocgen:
            doc, params = self.getDoc(space, name, ctx, params)
        else:
            doc = spacedocgen.name2doc[name]


        doc = doc.copy()
        doc.loadFromDisk()
        headers = [('Content-Type', 'text/html')]
        if name == "pagenotfound":
            ctx.start_response("404 Not found", headers)
        elif name == 'accessdenied':
            ctx.start_response("403 Not authorized", headers)
        else:
            ctx.start_response('200 OK', headers)

        return doc, params

    def returnDoc(self, ctx, space, docname, extraParams={}):
        doc, params = self.getDoc(space, docname, ctx, params=ctx.params)

        if doc.dirty or "reload" in ctx.params:
            doc.loadFromDisk()
            doc.preprocess()

        ctx.params.update(extraParams)

        # doc.applyParams(ctx.params)
        return doc.getHtmlBody(paramsExtra=extraParams, ctx=ctx)

    def processor_page(self, environ, start_response, wwwroot, path, prefix="", webprefix="", index=False, includedocs=False, ctx=None, space=None):
        def indexignore(item):
            ext = item.split(".")[-1].lower()
            if ext in ["pyc", "pyo", "bak"]:
                return True
            if item[0] == "_":
                return True
            if item[0] == ".":
                return True
            return False

        def formatContent(contenttype, path, template, start_response):
            content = j.system.fs.fileGetContents(path)
            page = self.getpage()
            page.addCodeBlock(content, template, edit=True)
            start_response('200 OK', [('Content-Type', contenttype), ])
            return [str(page).encode('utf-8')]

        def processHtml(contenttype, path, start_response, ctx, space):
            content = j.system.fs.fileGetContents(path)
            r = r"\[\[.*\]\]"  # @todo does not seem right to me
            for match in j.codetools.regex.yieldRegexMatches(r, content):
                docname = match.founditem.replace("[", "").replace("]", "")
                doc, params = self.getDoc(space, docname, ctx, params=ctx.params)

                if doc.name == 'pagenotfound':
                    content = content.replace(match.founditem, "*****CONTENT '%s' NOT FOUND******" % docname)
                else:
                    content2, doc = doc.executeMacrosDynamicWiki(paramsExtra={}, ctx=ctx)

                    page = self.confluence2htmlconvertor.convert(
                        content2, doc=doc, requestContext=ctx, page=self.getpage(), paramsExtra=ctx.params)
                    replace_obj = {
                        "space", space,
                        "page", doc.original_name,
                        "path", doc.path,
                        "querystr", ctx.env['QUERY_STRING'],
                        "$menuright", ""
                    }
                    page.body = j.tools.docpreprocessor.replace_params(page.body, replace_obj)

                    content = content.replace(match.founditem, page.body)

            start_response('200 OK', [('Content-Type', "text/html"), ])
            return [content.encode('utf-8')]

        def removePrefixes(path):
            path = path.replace("\\", "/")
            path = path.replace("//", "/")
            path = path.replace("//", "/")
            while len(path) > 0 and path[0] == "/":
                path = path[1:]
            while path.find(webprefix + "/") == 0:
                path = path[len(webprefix) + 1:]
            while path.find(prefix + "/") == 0:
                path = path[len(prefix) + 1:]
            return path

        def send_file(file_path, size):
            # print "sendfile:%s" % path
            f = open(file_path, "rb")
            block = f.read(BLOCK_SIZE * 10)
            BLOCK_SIZE2 = 0
            # print "%s %s" % (file_path,size)
            while BLOCK_SIZE2 < size:
                BLOCK_SIZE2 += len(block)
                # print BLOCK_SIZE2
                # print len(block)
                yield block
                block = f.read(BLOCK_SIZE)
            # print "endfile"

        wwwroot = wwwroot.replace("\\", "/").strip()

        path = removePrefixes(path)

        # print "wwwroot:%s" % wwwroot
        if not wwwroot.replace("/", "") == "":
            pathfull = wwwroot + "/" + path

        else:
            pathfull = path

        contenttype = "text/html"
        content = ""
        headers = list()
        ext = path.split(".")[-1].lower()
        contenttype = mimetypes.guess_type(pathfull)[0]

        if path == "favicon.ico":
            pathfull = "wiki/System/favicon.ico"
        else:
            if not os.path.abspath(pathfull).startswith(os.path.abspath(wwwroot)):
                raise exceptions.NotFound('Not found')

        if not j.system.fs.isFile(pathfull):
            if j.system.fs.isFile(pathfull + '.gz') and 'gzip' in environ.get('HTTP_ACCEPT_ENCODING'):
                pathfull += ".gz"
                headers.append(('Vary', 'Accept-Encoding'))
                headers.append(('Content-Encoding', 'gzip'))
            else:
                print("error")
                headers = [('Content-Type', contenttype), ]
                start_response("404 Not found", headers)
                return [("path %s not found" % path).encode('utf-8')]

        size = os.path.getsize(pathfull)

        if ext == "html":
            return processHtml(contenttype, pathfull, start_response, ctx, space)
        elif ext == "wiki":
            contenttype = "text/html"
            # return formatWikiContent(pathfull,start_response)
            return formatContent(contenttype, pathfull, "python", start_response)
        elif ext == "py":
            contenttype = "text/html"
            return formatContent(contenttype, pathfull, "python", start_response)
        elif ext == "spec":
            contenttype = "text/html"
            return formatContent(contenttype, pathfull, "python", start_response)

        # print contenttype

        status = '200 OK'

        headers.append(('Content-Type', contenttype))
        headers.append(("Content-length", str(size)))
        headers.append(("Cache-Control", 'public,max-age=3600'))

        start_response(status, headers)

        if content != "":
            return [content.encode('utf-8')]
        else:
            return send_file(pathfull, size)

    def process_elfinder(self, path, ctx):
        if not self.isAdminFromCTX(ctx):
            raise exceptions.NotFound('Not Found')

        from JumpScale.portal.html import elFinder
        db = j.db.keyvaluestore.getMemoryStore('elfinder')
        try:
            rootpath = db.cacheGet(path)
        except:
            raise exceptions.NotFound('Not Found')

        options = {'root': rootpath, 'dotFiles': True}
        con = elFinder.connector(options)
        params = ctx.params.copy()

        if params.get('init') == '1':
            params.pop('target', None)
        if 'target' in params:
            if j.system.fs.exists(params['target']):
                raise exceptions.NotFound('Not Found')
        status, header, response = con.run(params)
        status = '%s' % status
        headers = [(k, v) for k, v in header.items()]
        ctx.start_response(status, headers)
        if 'download' not in params:
            response = j.db.serializers.getSerializerType('j').dumps(response)
        else:
            response = response.get('content')
        return [response]

    def process_proxy(self, ctx, proxy):
        if not self.isAdminFromCTX(ctx):
            self.raiseError(ctx, httpcode='403 Forbidden')
            return 'Only admin can access that'
            return
        path = ctx.env['PATH_INFO']
        method = ctx.env['REQUEST_METHOD']
        query = ctx.env['QUERY_STRING']
        headers = {}
        for name, value in ctx.env.iteritems():
            if name.startswith('HTTP_'):
                headers[name[5:].replace('_', '-').title()] = value
        for key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
            if key in ctx.env:
                headers[key.replace('_', '-').title()] = ctx.env[key]
        desturl = proxy['dest'] + path[len(proxy['path']):]
        if query:
            desturl += "?%s" % query
        headers.pop('Connection', None)
        data = ctx.env['wsgi.input'].read()
        req = requests.Request(method, desturl, data=data, headers=headers).prepare()
        session = requests.Session()
        resp = session.send(req, stream=True, allow_redirects=False)
        resp.headers.pop("transfer-encoding", None)
        ctx.start_response('%s %s' % (resp.status_code, resp.reason), headers=resp.headers.items())
        rawdata = resp.raw.read()
        return rawdata

    def path2spacePagename(self, path):

        pagename = ""
        if path.find("?") != -1:
            path = path.split("?")[0]
        while len(path) > 0 and path[-1] == "/":
            path = path[:-1]
        if path.find("/") == -1:
            space = path.strip()
        else:
            splitted = path.split("/")
            space = splitted[0].lower()
            pagename = splitted[-1].lower()
        if not space:
            space = self.defaultspace

        return space, pagename

    # #################### FORMATTING + logs/raiseerror
    def log(self, ctx, user, path, space="", pagename=""):
        path2 = j.system.fs.joinPaths(self.logdir, "user_%s.log" % user)

        epoch = j.base.time.getTimeEpoch() + 3600 * 6
        hrtime = j.base.time.epoch2HRDateTime(epoch)

        if False and self.geoIP is not None:  # @todo fix geoip, also make sure nginx forwards the right info
            ee = self.geoIP.record_by_addr(ctx.env["REMOTE_ADDR"])
            loc = "%s_%s_%s" % (ee["area_code"], ee["city"], ee["region_name"])
        else:
            loc = ""

        msg = "%s|%s|%s|%s|%s|%s|%s\n" % (hrtime, ctx.env["REMOTE_ADDR"], epoch, space, pagename, path, loc)
        j.system.fs.writeFile(path2, msg, True)

        if space != "":
            msg = "%s|%s|%s|%s|%s|%s|%s\n" % (hrtime, ctx.env["REMOTE_ADDR"], epoch, user, pagename, path, loc)
            pathSpace = j.system.fs.joinPaths(self.logdir, "space_%s.log" % space)
            j.system.fs.writeFile(pathSpace, msg, True)

    def raiseError(self, ctx, msg="", msginfo="", errorObject=None, httpcode="500 Internal Server Error"):
        """
        """
        if not ctx.checkFormat():
            # error in format
            eco = j.errorconditionhandler.getErrorConditionObject()
            eco.errormessage = "only format supported = human or json, format is put with param &format=..."
            eco.type = "INPUT"
            print("WRONG FORMAT")
        else:
            if errorObject is not None:
                eco = errorObject
            else:
                eco = j.errorconditionhandler.getErrorConditionObject()

        method = ctx.env["PATH_INFO"]
        remoteAddress = ctx.env["REMOTE_ADDR"]
        queryString = ctx.env["QUERY_STRING"]

        eco.caller = remoteAddress
        if msg != "":
            eco.errormessage += "\n" + msg
        if msginfo != "":
            eco.errormessage += "\msginfo was:\n%s" % msginfo
        if queryString != "":
            eco.errormessage += "\nquerystr was:%s" % queryString
        if method != "":
            eco.errormessage += "\nmethod was:%s" % method

        eco.process()

        if ctx.fformat == "human" or ctx.fformat == "text":
            if msginfo is not None and msginfo != "":
                msg += "\n<br>%s" % msginfo
            else:
                msg += "\n%s" % eco
                msg = self._text2html(msg)

        else:
            # is json
            # result=[]
            # result["error"]=eco.obj2dict()
            def todict(obj):
                data = {}
                for key, value in obj.__dict__.items():
                    try:
                        data[key] = todict(value)
                    except AttributeError:
                        data[key] = value
                return data
            eco.tb = ""
            eco.frames = []
            msg = j.db.serializers.getSerializerType('j').dumps(todict(eco))

        ctx.start_response(httpcode, [('Content-Type', 'text/html')])

        j.console.echo("***ERROR***:%s : method %s from ip %s with params %s" % (
            eco, method, remoteAddress, queryString), 2)
        if j.application.debug:
            return msg
        else:
            msg = 'Your service request could not be fulfilled correctly, please contact support and mention "eco-{}-{}".'
            return msg.format(j.application.whoAmI.gid, eco.guid)

    def _text2html(self, text):
        text = text.replace("\n", "<br>")
        # text=text.replace(" ","&nbsp; ")
        return text

    def _text2htmlSerializer(self, content):
        return self._text2html(pprint.pformat(content))

    def _resultjsonSerializer(self, content):
        return j.db.serializers.getSerializerType('j').dumps({"result": content})

    def _resultyamlSerializer(self, content):
        return j.code.object2yaml({"result": content})

    def getMimeType(self, contenttype, format_types, result=None):
        supported_types = ["text/plain", "text/html", "application/yaml", "application/json"]
        CONTENT_TYPES = {
            "text/plain": str,
            "text/html": self._text2htmlSerializer,
            "application/yaml": self._resultyamlSerializer,
            "application/json": j.db.serializers.getSerializerType('j').dumps
        }

        if not contenttype:
            serializer = format_types["text"]["serializer"]
            return CONTENT_TYPE_HTML, serializer
        elif isinstance(result, types.GeneratorType):
            return 'application/octet-stream', lambda x: x
        else:
            mimeType = mimeparse.best_match(supported_types, contenttype)
            serializer = CONTENT_TYPES[mimeType]
            return mimeType, serializer

    def reformatOutput(self, ctx, result, restreturn=False):
        FFORMAT_TYPES = {
            "text": {"content_type": CONTENT_TYPE_HTML, "serializer": self._text2htmlSerializer},
            "html": {"content_type": CONTENT_TYPE_HTML, "serializer": self._text2htmlSerializer},
            "raw": {"content_type": CONTENT_TYPE_PLAIN, "serializer": str},
            "jsonraw": {"content_type": CONTENT_TYPE_JSON, "serializer": j.db.serializers.getSerializerType('j').dumps},
            "json": {"content_type": CONTENT_TYPE_JSON, "serializer": self._resultjsonSerializer},
            "yaml": {"content_type": CONTENT_TYPE_YAML, "serializer": self._resultyamlSerializer}
        }

        if '_jsonp' in ctx.params:
            result = {'httpStatus': ctx.httpStatus, 'httpMessage': ctx.httpMessage, 'body': result}
            return CONTENT_TYPE_JS, "%s(%s);" % (ctx.params['_jsonp'], j.db.serializers.getSerializerType('j').dumps(result))

        if ctx._response_started:
            return None, result

        fformat = ctx.fformat

        if '_png' in ctx.params:
            return CONTENT_TYPE_PNG, result

        if "CONTENT_TYPE" not in ctx.env:
            if ctx.env['PATH_INFO'].startswith('/restmachine'):
                ctx.env['CONTENT_TYPE'] = CONTENT_TYPE_JSON
            else:
                ctx.env['CONTENT_TYPE'] = CONTENT_TYPE_PLAIN
                
        if ctx.env['CONTENT_TYPE'].find("form-") != -1:
            ctx.env['CONTENT_TYPE'] = CONTENT_TYPE_PLAIN
        # normally HTTP_ACCEPT defines the return type we should rewrite this
        if fformat:
            # extra format paramter overrides http_accept header
            return FFORMAT_TYPES[fformat]['content_type'], FFORMAT_TYPES[fformat]['serializer'](result)
        else:
            if 'HTTP_ACCEPT' in ctx.env:
                returntype = ctx.env['HTTP_ACCEPT']
            else:
                returntype = ctx.env['CONTENT_TYPE']
            content_type, serializer = self.getMimeType(returntype, FFORMAT_TYPES, result)
            return content_type, serializer(result)

# router

    def startSession(self, ctx, path):
        session = ctx.env['beaker.session']
        if 'user_login_' in ctx.params and ctx.params.get('user_login_') == 'guest' and self.force_oauth_instance:
            raise exceptions.Redirect(self.force_oauth_url)

        # Already logged in user can't access login page again
        if 'user_logoff_' not in ctx.params and path.endswith('system/login') and 'user' in session and session['user'] != 'guest':
            ctx.start_response('204', [])
            return False, []

        if "authkey" in ctx.params:
            # user is authenticated by a special key
            key = ctx.params["authkey"]

            # check if authkey is a session
            newsession = session.get_by_id(key)
            if newsession:
                session = newsession
                ctx.env['beaker.session'] = session
            elif key == self.secret:
                session['user'] = 'admin'
                session.save()
            else:
                username = self.auth.getUserFromKey(key)
                if username != "guest":
                    session['user'] = username
                    session.save()
                else:
                    raise exceptions.AuthenticationTimeout('key not valid or expired')

        # validate JWT token
        if 'HTTP_AUTHORIZATION' in ctx.env:
            authorization = ctx.env['HTTP_AUTHORIZATION']
            type, _, token = authorization.partition(' ')
            if type.lower() == 'bearer':
                import jose.jwt
                payload = json.loads(jose.jwt.get_unverified_claims(token))
                issuer = payload.get('iss', 'main')
                payload['iss'] = issuer
                for instance in j.core.config.list('jwt_client'):
                    jwtcfg = j.core.config.get('jwt_client', instance)
                    secret = jwtcfg.get('secret')
                    algo = jwtcfg.get('algo')
                    try:
                        jose.jwt.decode(token, secret, algorithms=[algo])
                    except (jose.JWTError, jose.JWSError):
                        raise exceptions.Unauthorized(str(self.returnDoc(ctx, "system", "accessdenied",
                                                                         extraParams={"path": path})), 'text/html')
                    break
                else:
                    raise exceptions.Unauthorized(str(self.returnDoc(ctx, "system", "accessdenied",
                                                                     extraParams={"path": path})), 'text/html')

                session['user'] = '{username}@{iss}'.format(**payload)
                session['jwt'] = token
                session.save()
            elif type.lower() == 'authkey':
                if token == self.secret:
                    session['user'] = 'admin'
                    session.save()

        if "user_logoff_" in ctx.params and "user_login_" not in ctx.params:
            if session.get('user', '') not in ['guest', '']:
                # If user session is oauth session and logout url is provided, redirect user to that URL
                # after deleting session which will invalidate the oauth server session
                # then redirects user back to where he was in portal
                oauth = session.get('oauth')
                oauth_logout_url = ''
                if oauth:
                    oauth_logout_url = oauth.get('logout_url')
                session.delete()
                session = ctx.env['beaker.get_session']()
                ctx.env['beaker.session'] = session
                session['user'] = 'guest'
                session.save()

                if oauth_logout_url:
                    backurl = urlparse.urljoin(ctx.env['HTTP_REFERER'], ctx.env['PATH_INFO'])
                    ctx.start_response('302 Found', [('Location', '%s?%s' % (
                        str(oauth_logout_url), str(urllib.urlencode({'redirect_uri': backurl}))))])
                    return False, session
            session['user'] = 'guest'
            session.save()
            return True, session

        if "user_login_" in ctx.params:
            # user has filled in his login details, this is response on posted info
            name = ctx.params['user_login_']
            if 'passwd' not in ctx.params:
                secret = ""
            else:
                secret = ctx.params['passwd']
            if self.auth.authenticate(name, secret):
                session['user'] = name
                if "querystr" in session:
                    ctx.env['QUERY_STRING'] = session['querystr']
                else:
                    ctx.env['QUERY_STRING'] = ""

                session['auth_method'] = self.authentication_method

                session.save()
                # user is loging in from login page redirect him to home
                if path.endswith('system/login'):
                    status = '302'
                    headers = [
                        ('Location', "/"),
                    ]
                    ctx.start_response(status, headers)
                    return False, [""]
            else:
                session['user'] = ""
                session["querystr"] = ""
                session.save()
                return False, [str(self.returnDoc(ctx, "system", "login", extraParams={"path": path}))]

        if "user" not in session or session["user"] == "":
            session['user'] = "guest"
            session.save()

        if "querystr" in session:
            session["querystr"] = ""
            session.save()

        return True, session

    def _getParamsFromEnv(self, env, ctx, escape=True):

        params = urlparse.parse_qs(env["QUERY_STRING"], 1)
        if escape:
            for k, v_list in params.items():
                escaped_vals = []
                for v in v_list:
                    escaped_vals.append(j.html.escape(v))

                params[k] = escaped_vals

        def simpleParams(params):
            # HTTP parameters can be repeated multiple times, i.e. in case of using <select multiple>
            # Example: a=1&b=2&a=3
            #
            # urlparse.parse_qs returns a dictionary of names & list of values. Then it's simplified
            # for lists with only a single element, e.g.
            #
            #   {'a': ['1', '3'], 'b': ['2']}
            #
            # simplified to be
            #
            #   {'a': ['1', '3'], 'b': '2'}
            return dict(((k, v) if len(v) > 1 else (k, v[0])) for k, v in list(params.items()))

        def hasSupportedContentType(contenttype, supportedcontenttypes):
            for supportedcontenttype in supportedcontenttypes:
                if contenttype.find(supportedcontenttype) != -1:
                    return True

        params = simpleParams(params)

        contentype = env.get('CONTENT_TYPE', '')
        pragma = env.get('HTTP_PRAGMA', '')
        env['is_stream'] = False
        if 'stream' not in pragma and env["REQUEST_METHOD"] in ("POST", "PUT") and hasSupportedContentType(contentype, ('application/json', 'www-form-urlencoded', 'multipart/form-data', '')):
            if contentype.find("application/json") != -1:
                postData = env["wsgi.input"].read()
                if postData.strip() == "":
                    return params
                postParams = j.db.serializers.getSerializerType('j').loads(postData)
                if postParams:
                    params.update(postParams)
                return params
            elif contentype.find("www-form-urlencoded") != -1:
                postData = env["wsgi.input"].read()
                if postData.strip() == "":
                    return params
                params.update(dict(urlparse.parse_qs(postData, 1)))
                return simpleParams(params)
            elif contentype.find("multipart/form-data") != -1 and env.get('HTTP_TRANSFER_ENCODING') != 'chunked':
                env['is_stream'] = True
                forms, files = multipart.parse_form_data(ctx.env)
                params.update(forms)
                for key, value in files.items():
                    params.setdefault(key, dict())[value.filename] = value.file
            elif env.get('HTTP_TRANSFER_ENCODING') == 'chunked':
                env['is_stream'] = True
                from JumpScale.portal.html.multipart2.multipart import parse_options_header
                content_type, parameters = parse_options_header(env.get('CONTENT_TYPE'))
                boundary = parameters.get(b'boundary')
                inp = env.get('wsgi.input')
                params.update({'FILES': {'data': inp, 'boundary': boundary}})
        return params

    @property
    def requestContext(self):
        currentframe = None
        currentframe = inspect.currentframe()
        backframe = currentframe.f_back
        while backframe is not None:
            for vars in (backframe.f_locals, backframe.f_globals):
                ctx = vars.get('ctx')
                if isinstance(ctx, RequestContext):
                    return ctx
                ctx = vars.get('kwargs', {}).get('ctx')
                if isinstance(ctx, RequestContext):
                    return ctx

            backframe = backframe.f_back

    @exhaustgenerator
    def router(self, environ, start_response):
        path = environ["PATH_INFO"].lstrip("/")
        print("path:%s" % path)
        pathparts = path.split('/')
        if pathparts[0] == 'wiki':
            pathparts = pathparts[1:]

        if path.find("favicon.ico") != -1:
            return self.processor_page(environ, start_response, self.filesroot, "favicon.ico", prefix="")

        ctx = RequestContext(application="", actor="", method="",
                             env=environ, start_response=start_response,
                             path=path, params={}, server=self)

        for proxypath, proxy in self.proxies.iteritems():
            if path.startswith(proxypath.lstrip('/')):
                return self.process_proxy(ctx, proxy)

        if path.startswith('restmachine'):
            ctx.params = self._getParamsFromEnv(environ, ctx, False)
        else:
            ctx.params = self._getParamsFromEnv(environ, ctx, True)
        ctx.env['JS_CTX'] = ctx

        if path.find("jslib/") == 0:
            path = path[6:]
            user = "None"
            # self.log(ctx, user, path)
            return self.processor_page(environ, start_response, self.jslibroot, path, prefix="jslib/")

        if path.find("images/") == 0:
            try:
                space, image = pathparts[1:3]
            except ValueError:
                # not a valid path
                return self.returnDoc(ctx, 'system', 'pagenotfound', {'path': path})

            spaceObject = self.getSpace(space)
            image = image.lower()

            if image in spaceObject.docprocessor.images:
                path2 = spaceObject.docprocessor.images[image]

                return self.processor_page(environ, start_response, j.system.fs.getDirName(path2), j.system.fs.getBaseName(path2), prefix="images")
            return self.returnDoc(ctx, 'system', 'pagenotfound', {'path': path})

        if path.find("files/specs/") == 0:
            path = path[6:]
            user = "None"
            self.log(ctx, user, path)
            return self.processor_page(environ, start_response, self.filesroot, path, prefix="files/")

        if path.find(".files") != -1:
            user = "None"
            self.log(ctx, user, path)
            space = pathparts[0].lower()
            if space == '.files':
                space = self.defaultspace
                path = "/".join(pathparts[1:])
            else:
                path = "/".join(pathparts[2:])
            sploader = self.spacesloader.getSpaceFromId(space)
            filesroot = j.system.fs.joinPaths(sploader.model.path, ".files")
            return self.processor_page(environ, start_response, filesroot, path, prefix="")

        if path.find(".static") != -1:
            user = "None"
            self.log(ctx, user, path)
            space, pagename = self.path2spacePagename(path)
            space = pathparts[0].lower()
            path = "/".join(pathparts[2:])
            sploader = self.spacesloader.getSpaceFromId(space)
            filesroot = j.system.fs.joinPaths(sploader.model.path, ".static")

            return self.processor_page(environ, start_response, filesroot, path, prefix="", includedocs=True, ctx=ctx, space=space)

        # user is logged in now
        is_session, session = self.startSession(ctx, path)
        if not is_session:
            return session
        user = session['user']
        match = pathparts[0]
        path = ""
        if len(pathparts) > 1:
            path = "/".join(pathparts[1:])

        if match == "restmachine":
            return self.rest.processor_rest(environ, start_response, path, ctx=ctx)

        elif match == "elfinder":
            return self.process_elfinder(path, ctx)

        elif match == "restextmachine":
            if not self.authentication_method:
                try:
                    j.clients.osis.getByInstance(self.cfg.get('osis.connection', 'main'))
                except Exception as e:
                    self.raiseError(ctx, msg="You have a minimal portal with no OSIS configured",
                                    msginfo="", errorObject=None, httpcode="500 Internal Server Error")
            return self.rest.processor_restext(environ, start_response, path, ctx=ctx)

        elif match == "ping":
            status = '200 OK'
            headers = [
                ('Content-Type', "text/html"),
            ]
            start_response(status, headers)
            return ["pong"]

        elif match == "files":
            self.log(ctx, user, path)
            return self.processor_page(environ, start_response, self.filesroot, path, prefix="files")

        elif match == "specs":
            return self.processor_page(environ, start_response, "specs", path, prefix="specs")

        elif match == "appservercode":
            return self.processor_page(environ, start_response, "code", path, prefix="code", webprefix="appservercode")

        elif match == "lib":
            # print self.libpath
            return self.processor_page(environ, start_response, self.libpath, path, prefix="lib")

        elif match == 'render':
            return self.render(environ, start_response)

        else:
            path = '/'.join(pathparts)
            ctx.params["path"] = '/'.join(pathparts)
            space, pagename = self.path2spacePagename(path)
            self.log(ctx, user, path, space, pagename)
            pagestring = str(self.returnDoc(ctx, space, pagename, {}))
            return [pagestring]

    def render(self, environ, start_response):
        path = environ["PATH_INFO"].lstrip("/")
        query_string = environ["QUERY_STRING"].lstrip("/")
        params = cgi.parse_qs(query_string)
        content = params.get('content', [''])[0]
        space = params.get('render_space', None)
        if space:
            space = space[0]
        else:
            start_response('200 OK', [('Content-Type', "text/html")])
            return 'Parameter "space" not supplied'

        doc = params.get('render_doc', None)
        if doc:
            doc = doc[0]
        else:
            start_response('200 OK', [('Content-Type', "text/html")])
            return 'Parameter "doc" not supplied'

        ctx = RequestContext(application=self, actor="", method="",
                             env=environ, start_response=start_response,
                             path=path, params=None, server=self)
        ctx.params = self._getParamsFromEnv(environ, ctx)

        doc, _ = self.getDoc(space, doc, ctx)

        doc = doc.copy()
        doc.source = content
        doc.loadFromSource()
        doc.preprocess()

        content, doc = doc.executeMacrosDynamicWiki(ctx=ctx)

        page = self.confluence2htmlconvertor.convert(
            content, doc=doc, requestContext=ctx, page=self.getpage(), paramsExtra=ctx.params)

        replace_obj = {
            "space", space,
            "page", doc.original_name,
            "path", doc.path,
            "querystr", ctx.env['QUERY_STRING'],
            "$menuright", ""
        }
        page.body = j.tools.docpreprocessor.replace_params(page.body, replace_obj)

        if "todestruct" in doc.__dict__:
            doc.destructed = True

        start_response('200 OK', [('Content-Type', "text/html")])
        return str(page)

    def addRoute(self, function, appname, actor, method, params, description="", auth=True, returnformat=None, httpmethod='POST'):
        """
        @param function is the function which will be called as follows: function(webserver,path,params):
            function can also be a string, then only the string will be returned
            if str=='taskletengine' will directly call the taskletengine e.g. for std method calls from actors
        @appname e.g. system is 1e part of url which is routed http://localhost/appname/actor/method/
        @actor e.g. system is 2nd part of url which is routed http://localhost/appname/actor/method/
        @method e.g. "test" is part of url which is routed e.g. http://localhost/appname/actor/method/
        @auth is for authentication if false then there will be no auth key checked

        example function called

            def test(self,webserver,path,params):
                return 'hello world!!'

            or without the self in the functioncall (when no class method)

            what you return is being send to the browser

        example call: http://localhost:9999/test?key=1234&color=dd&name=dd

        """

        appname = appname.replace("_", ".")
        actor = actor.replace("_", ".")
        method = method.replace("_", ".")
        self.app_actor_dict["%s_%s" % (appname, actor)] = 1

        methoddict = {'get': 'GET', 'set': 'PUT', 'new': 'POST', 'delete': 'DELETE',
                      'post': 'POST',
                      'find': 'GET', 'list': 'GET', 'datatables': 'GET', 'create': 'POST'}
        route = {'func': function, 'params': params, 'description': description,
                 'auth': auth, 'returnformat': returnformat}
        self.routes["%s_%s_%s_%s" % (methoddict.get(httpmethod, 'POST'), appname, actor, method)] = route

# SCHEDULING

    def _timer(self):
        """
        will remember time every 0.5 sec
        """
        lfmid = 0
        while True:
            self.epoch = int(time.time())
            if lfmid < self.epoch - 200:
                lfmid = self.epoch
                self.fiveMinuteId = j.base.time.get5MinuteId(self.epoch)
                self.hourId = j.base.time.getHourId(self.epoch)
                self.dayId = j.base.time.getDayId(self.epoch)
            gevent.sleep(0.5)

    def _minRepeat(self):
        while True:
            gevent.sleep(5)
            for key in self.schedule1min.keys():
                item, args, kwargs = self.schedule1min[key]
                item(*args, **kwargs)

    def _15minRepeat(self):
        while True:
            gevent.sleep(60 * 15)
            for key in self.schedule15min.keys():
                item, args, kwargs = self.schedule15min[key]
                item(*args, **kwargs)

    def _60minRepeat(self):
        while True:
            gevent.sleep(60 * 60)
            for key in self.schedule60min.keys():
                item, args, kwargs = self.schedule60min[key]
                item(*args, **kwargs)

    def getNow(self):
        return self.epoch

    def addSchedule1MinPeriod(self, name, method, *args, **kwargs):
        self.schedule1min[name] = (method, args, kwargs)

    def addSchedule15MinPeriod(self, name, method, *args, **kwargs):
        self.schedule15min[name] = (method, args, kwargs)

    def addSchedule60MinPeriod(self, name, method, *args, **kwargs):
        self.schedule60min[name] = (method, args, kwargs)

# START-STOP / get spaces/actors/buckets / addgreenlet

    def start(self):
        """
        Start the web server, serving the `routes`. When no `routes` dict is passed, serve a single 'test' route.

        This method will block until an exception stops the server.

        @param routes: routes to serve, will be merged with the already added routes
        @type routes: dict(string, list(callable, dict(string, string), dict(string, string)))
        """

        TIMER = gevent.greenlet.Greenlet(self._timer)
        TIMER.start()

        S1 = gevent.greenlet.Greenlet(self._minRepeat)
        S1.start()

        S2 = gevent.greenlet.Greenlet(self._15minRepeat)
        S2.start()

        S3 = gevent.greenlet.Greenlet(self._60minRepeat)
        S3.start()

        j.console.echo("webserver started on port %s" % self.port)
        self._webserver.serve_forever()

    def stop(self):
        self._webserver.stop()

    def getSpaces(self):
        return list(self.spacesloader.id2object.keys())

    def getBuckets(self):
        return list(self.bucketsloader.id2object.keys())

    def getActors(self):
        return list(self.actorsloader.id2object.keys())

    def getSpace(self, name, ignore_doc_processor=False):

        name = name.lower()
        if name not in self.spacesloader.spaces:
            raise RuntimeError("Could not find space %s" % name)
        space = self.spacesloader.spaces[name]
        return space

    def getBucket(self, name):
        if name not in self.bucketsloader.buckets:
            raise RuntimeError("Could not find bucket %s" % name)
        bucket = self.bucketsloader.buckets(name)
        return bucket

    def addGreenlet(self, appName, greenlet):
        """
        """
        greenletObject = greenlet()
        if greenletObject.method == "":
            raise RuntimeError("greenlet class needs to have a method")
        if greenletObject.actor == "":
            raise RuntimeError("greenlet class needs to have a actor")

        greenletObject.server = self
        self.addRoute(function=greenletObject.wscall,
                      appname=appName,
                      actor=greenletObject.actor,
                      method=greenletObject.method,
                      paramvalidation=greenletObject.paramvalidation,
                      paramdescription=greenletObject.paramdescription,
                      paramoptional=greenletObject.paramoptional,
                      description=greenletObject.description, auth=greenletObject.auth)

    def restartInProcess(self, app):
        import fcntl
        args = sys.argv[:]
        args.insert(0, sys.executable)
        apppath = j.system.fs.joinPaths(j.dirs.appDir, app)
        max_fd = 1024
        for fd in range(3, max_fd):
            try:
                flags = fcntl.fcntl(fd, fcntl.F_GETFD)
            except IOError:
                continue
            fcntl.fcntl(fd, fcntl.F_SETFD, flags | fcntl.FD_CLOEXEC)
        os.chdir(apppath)
        os.execv(sys.executable, args)

    def __str__(self):
        out = ""
        for key, val in self.__dict__.items():
            if key[0] != "_" and key not in ["routes"]:
                out += "%-35s :  %s\n" % (key, val)
        routes = ",".join(list(self.routes.keys()))
        out += "%-35s :  %s\n" % ("routes", routes)
        items = out.split("\n")
        items.sort()
        out = "portalserver:" + "\n".join(items)
        return out

    __repr__ = __str__
