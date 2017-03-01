[actor] @dbtype:osis
	"""
	audits handling
	"""
    method:listAudits
		"""
		list system audits.
		"""
		var:username str,,Username @optional
		var:responsetime int,,responseTime @optional
		var:restcall str,,REST endpoint @optional
		var:epoch int,,Epoch of the audit call timestamp @optional
		var:statuscode int,, status code returned @optional
		var:page int,, page number @optional
		var:size int,, page size @optional
		result:list of audits
