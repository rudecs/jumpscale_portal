[actor] @dbtype:fs
    """
    get async task info
    """

    method:get
        """
        Get taks info return 204 withouth content when task is still busy
        Return 404 if task does not exist or expired (tasks will be kept 5minutes after they finished)

        Return 200
        status, methodresult
        """
        var:taskguid str,,task to get info for
        result: str


    method:kill
        """
        Kill task
        """
        var:taskguid str,,task to get info for
        result: bool
