from JumpScale import j

class system_contentmanager(j.code.classGetBase()):
    """
    this actor manages all content on the wiki
    can e.g. notify wiki/appserver of updates of content
    """
    def __init__(self):
        pass
        
        self._te={}
        self.actorname="contentmanager"
        self.appname="system"
        #system_contentmanager_osis.__init__(self)


    def checkEvents(self, cursor, **kwargs):
        """
        Check for events
        param:cursor cursor to get from
        result dict
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method checkEvents")

    def getActors(self, **kwargs):
        """
        result list(str)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getActors")

    def getActorsWithPaths(self, **kwargs):
        """
        result list([name,path])
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getActorsWithPaths")

    def getSpaces(self, **kwargs):
        """
        result list(str)
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getSpaces")

    def getSpacesWithPaths(self, **kwargs):
        """
        result list([name,path])
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method getSpacesWithPaths")

    def modelobjectlist(self, namespace, category, key, **kwargs):
        """
        @todo describe what the goal is of this method
        param:namespace namespace of the model
        param:category category of the model
        param:key 
        result list
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method modelobjectlist")

    def modelobjectupdate(self, appname, actorname, key, **kwargs):
        """
        post args with ref_$id which refer to the key which is stored per actor in the cache
        param:appname 
        param:actorname 
        param:key 
        result html
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method modelobjectupdate")

    def notifyActorModification(self, id, **kwargs):
        """
        param:id id of actor which changed
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method notifyActorModification")

    def notifyActorNew(self, path, name, **kwargs):
        """
        param:path path of content which got changed
        param:name name of actor
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method notifyActorNew")

    def notifySpaceNew(self, path, name, **kwargs):
        """
        param:path path of content which got changed
        param:name name
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method notifySpaceNew")

    def prepareActorSpecs(self, app, actor, **kwargs):
        """
        compress specs for specific actor and targz in appropriate download location
        param:app name of app
        param:actor name of actor
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method prepareActorSpecs")

    def sendEvent(self, title, text, level, eventstreamid, **kwargs):
        """
        Send an event
        param:title title of the message
        param:text text of the message
        param:level level of the message
        param:eventstreamid stream id of the event
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method sendEvent")

    def wikisave(self, cachekey, text, **kwargs):
        """
        param:cachekey key to the doc
        param:text content of file to edit
        result bool
        """
        #put your code here to implement this method
        raise NotImplementedError ("not implemented method wikisave")
