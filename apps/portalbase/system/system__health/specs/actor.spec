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

    method:getOverallStatus
        """
        get the status of the system
        """
        result:json

    method:getStatusSummary
        """
        get the status summary for the nodes
        """
        result:json

    method:getDetailedStatus
        """
        get detailed status for a node
        """
        var:nid int,,id of node
        result:json

