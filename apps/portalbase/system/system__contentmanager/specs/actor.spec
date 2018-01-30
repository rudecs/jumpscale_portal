[actor] @dbtype:mem #tasklets
	"""
	this actor manages all content on the wiki
	can e.g. notify wiki/appserver of updates of content
	"""

    method:getSpaces @method:get,post
		"""
		"""
        result:list(str)

    method:getSpacesWithPaths @method:get,post
		"""
		"""
        result:list([name,path])


    method:getActorsWithPaths @method:get,post
        """
        """
        result:list([name,path])

    method:getActors @method:get,post
		"""
		"""
        result:list(str)

    method:notifySpaceNew @method:get,post
		"""
		"""
		var:path str,,path of content which got changed
		var:name str,,name
		result:bool

    method:notifyActorNew @method:get,post
		"""
		"""
		var:path str,,path of content which got changed
		var:name str,,name of actor
		result:bool

    method:notifyActorModification @method:get,post
		"""
		"""
		var:id str,,id of actor which changed
        result:bool

    method:prepareActorSpecs
		"""
		compress specs for specific actor and targz in appropriate download location
		"""
		var:app str,,name of app
		var:actor str,,name of actor
		result:bool

    method:wikisave @noauth
		"""
		"""
		var:cachekey str,,key to the doc
		var:text str,,content of file to edit
        result:bool

    method:modelobjectlist @noauth returnformat:jsonraw method:get
        """
        @todo describe what the goal is of this method
        """
        var:namespace str,, namespace of the model
        var:category str,, category of the model
        var:key str,,
        result:list

    method:modelobjectupdate @noauth returnformat:html
        """
        post args with ref_$id which refer to the key which is stored per actor in the cache
        """
        var:appname str,,
        var:actorname str,,
        var:key str,,
        result:html

    method:checkEvents @method:get
        """
        Check for events
        """
        var:cursor int,,cursor to get from
        result:dict
