[actor] @dbtype:fs
    """
    Agent Controller
    """

    method:listActiveSessions @method:get,post
        """
        Lists all active sessions.
        """
        result:list(str)
    method:listSessions @method:get,post
        """
        Lists all sessions.
        """
        result:list(str)
    method:executeJumpscript
        """
        Execute a jumpscript
        """
        var:organization str,,
        var:name str,,
        var:nid int,None, @optional
        var:role str,None, @optional
        var:args dict,, @optional
        var:all bool,False, @optional
        var:timeout int,600, @optional
        var:wait bool,True, @optional
        var:queue str,, @optional
        var:gid int,None,
        var:errorreport bool,True, @optional
    method:loadJumpscripts @method:get,post
        """
        Load available jumpscripts
        """
        var:path str,"jumpscripts", @optional
