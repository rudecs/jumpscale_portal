[actor] @dbtype:fs
	"""
	purge handling
	"""

    method:purge
        """
        Remove logs
        By default the logs en eco's older than than 1 week but this can be overriden
        """
        var:age str,, age of the records
        result: bool
