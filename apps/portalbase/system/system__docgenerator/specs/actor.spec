[actor] @dbtype:mem #tasklets
    method: prepareCatalog @method:get,post
        """
        Initializes the swagger entry point for listing the available APIs
        """
        result:dict

    #method:getDocForActor @method:get,post
    #    """
    #    Gets the json doc of the given actor
    #    """
    #    var:actorname str,,name of the actor to get documentation for
    #    result:dict 