from JumpScale import j

class ActorsInfo():

    def getActorMethodCall(self, appname, actor, method, http_method='GET'):
        """
        used for during error show links to methods in browser
        """
        url = "/rest/%s/%s/%s?" % (appname, actor, method)

        try:
            m = j.core.portal.active.routes["%s_%s_%s_%s" % (http_method, appname, actor, method)]
        except:
            return ''

        auth = m['auth']
        if auth:
            params = ["authkey"]
        else:
            params = []
        params.extend(list(m['params'].keys()))

        for param in params:
            url += "%s=&" % param
        url += "format=text"
        if url[-1] == "&":
            url = url[:-1]
        if url[-1] == "?":
            url = url[:-1]
        # url="<a href=\"%s\">%s</a> " % (url,url)
        return url

    def getActorInfoPage(self, appname, actorname, methodname, page=None, http_method='GET'):
        """
        used for during error show info about 1 actor
        """
        if page == None:
            page = j.core.portal.active.getpage()
        if appname == "" or actorname == "" or methodname == "":
            txt = "getActorInfo need 3 params: appname, actorname, methoname, got: %s, %s,%s" % (appname, actorname, methodname)
            page.addMessage(txt)
            return page
        if page == None:
            page = j.core.portal.active.getpage()
        page.addHeading("%s.%s.%s" % (appname, actorname, methodname), 5)

        url = self.getActorMethodCall(appname, actorname, methodname, http_method=http_method)

        routekey="%s_%s_%s_%s" % (http_method, appname, actorname, methodname)
        # to ensure that the actor is loaded
        actorsloader = j.core.portal.active.actorsloader
        actorsloader.existsActor(appname, actorname)

        routeData = j.core.portal.active.routes[routekey]
        # routedata: function,paramvalidation,paramdescription,paramoptional,description

        description = routeData['description']
        if description.strip() != "":
            page.addMessage(description)
        # param info
        params = routeData['params']
        # optional = routeData[3]
        page.addLink("%s" % (methodname), url)
        if len(list(params.keys())) > 0:
            page.addBullet("Params:\n", 1)
            for key, param in params.items():
                descr = param.get('description', '').strip()
                page.addBullet("- %s : %s \n" % (key, descr), 2)

        return page

    def getActorsInfoPage(self, appname="", actor="", page=None, extraParams={}):
        actorsloader = j.core.portal.active.actorsloader
        if appname != "" and actor != "":
            result = actorsloader.existsActor(appname, actor)
            if result == False:
                # actor was not there
                page = j.core.portal.active.getpage()
                page.addHeading("Could not find actor %s %s." % (appname, actor), 4)
                return page

        if page == None:
            page = j.core.portal.active.getpage()
        if appname == "":
            page.addHeading("Applications in appserver.", 4)
            appnames = {}

            for appname, actorname in actorsloader.getAppActors():  # [item.split("_", 1) for  item in self.app_actor_dict.keys()]:
                appnames[appname] = 1
            appnames = sorted(appnames.keys())
            for appname in appnames:
                link = page.getLink("%s" % (appname), self.getActorInfoUrl(appname, ""))
                page.addBullet(link)
            return page

        if actor == "":
            page.addHeading("Actors for application %s" % (appname), 4)
            actornames = []
            for appname2, actorname2 in actorsloader.getAppActors():  # [item.split("_", 1) for  item in self.app_actor_dict.keys()]:
                if appname2 == appname:
                    actornames.append(actorname2)
            actornames.sort()

            for actorname in actornames:
                link = page.getLink("%s" % (actorname), self.getActorInfoUrl(appname, actorname))
                page.addBullet(link)
            return page

        keys = sorted(j.core.portal.active.routes.keys())
        page.addHeading("list", 2)
        for item in keys:
            http_method, app2, actor2, method = item.split("_")
            if app2 == appname and actor2 == actor:
                url = self.getActorMethodCall(appname, actor, method, http_method=http_method)
                link = page.getLink(item, url)
                page.addBullet(link)

        page.addHeading("details", 2)
        for item in keys:
            http_method, app2, actor2, method = item.split("_")
            if app2 == appname and actor2 == actor:
                page = self.getActorInfoPage(appname, actor, method, page=page, http_method=http_method)
        return page


    def getActorInfoUrl(self, appname, actor):
        """
        used for during error show links to actor in browser
        """
        if actor == "":
            url = "/rest/%s/" % (appname)
        else:
            url = "/rest/%s/%s/" % (appname, actor)
        return url