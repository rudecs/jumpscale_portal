[actor] @dbtype:fs
    """
    """
    method:userget
        """
        get a user
        """
        var:name str,,name of user @tags validator:username

    method:editUser
        """
        set Groups for a user
        """
        var:username str,,name of user @tags validator:username
        var:groups list,,list of groups this user belongs to @optional
        var:password str,,password for user @optional @tags validator:password
        var:emails list,,list of email addresses
        var:domain str,,Domain of user @optional

    method:delete
        """
        Delete a user
        """
        var:username str,, name of the user @tags validator:username

    method:create
        """
        create a user
        """
        var:username str,,name of user @tags validator:username
        var:password str,,password optional when provider is set
        var:groups list,,list of groups this user belongs to @optional
        var:emails list,,list of email addresses
        var:domain str,,domain of user @optional
        var:provider str,None,provider for this user @optional
        result:str, username created when provider is given this will be <username@provider>

    method:authenticate @noauth
        """
        authenticate and return False if not successfull
        otherwise return secret for api
        """
        var:name str,,name @tags validator:username
        var:secret str,,md5 or passwd
        #var:refresh bool,False,if True will recreate a new key otherwise will use last key created @optional
        result:str #is key to be used to e.g use the rest interface

    method:userexists
        """
        """
        var:name str,,name @tags validator:username
        result:bool


    method:createGroup
        """
        create a group
        """
        var:name str,,name of group @tags validator:groupname
        var:domain str,,domain of group
        var:description str,,description of group
        result:bool    #True if successful, False otherwise

    method:editGroup
        """
        edit a group
        """
        var:name str,,name of group @tags validator:groupname
        var:domain str,,domain of group
        var:description str,,description of group
        var:users str,,list or comma seperate string of users @optional
        result:bool    #True if successful, False otherwise

    method:deleteGroup
        """
        delete a group
        """
        var:id str,,id/name of group @tags validator:groupname
        result:bool    #True if successful, False otherwise

    method:usergroupsget
        """
        return list of groups in which user is member of
        """
        var:user str,,name of user @tags validator:username
        result:list(str)

    method:whoami @noauth
        """
        return username
        """
        result:str
