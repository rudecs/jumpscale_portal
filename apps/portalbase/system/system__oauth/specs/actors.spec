[actor] @dbtype:fs
	"""
	An actor to perform actions for gitlab users
	"""    
    method:authenticate @noauth method:get
        """
        """
        var:type str,, [default to github] @tags: optional
        result:str
        
    method:authorize @noauth method:get
        """
        """
        result:str

    method:getOauthLogoutURl @noauth method:get
        """
        """
        result:str
