[actor] @dbtype:fs
	"""
    heathcheck
	"""
    method:run
		"""
	    Run full healtcheck
		"""
		var:nid int,,node id @optional
        result:bool


    method:refreshCommand
		"""
	    Refresh a single healthcheck
		"""
		var:nid int,,node id
		var:cmd str,,command to refresh
        result:str

    method:getOverallStatus @method:get,post
        """
        get the status of the system
        """
        result:json

    method:getStatusSummary @method:get,post
        """
        get the status summary for the nodes
        """
        result:json

    method:getDetailedStatus @method:get,post
        """
        get detailed status for a node
        """
        var:nid int,,id of node
        result:json
