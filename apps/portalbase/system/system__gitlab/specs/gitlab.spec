[actor] @dbtype:fs
	"""
	An actor to perform actions for gitlab users
	"""    
    method:updateUserSpaces
		"""		
        Update gitlab user spaces
		"""
		var:username str,,User name [Must be valid gitlab user]
		result:int

    method:checkUpdateUserSpaceJob
        """
        Check Update gitlab user spaces job status
        """
        var:jobid str,, Update JOB ID
        result:str
