[actor] @dbtype:mem,fs
	"""
	API Actor api for managing cpu node creation and bootstraping
	"""    
	method:init @noauth
		"""
		return the init script for creating a new node
		"""
		result:str  #returns script for creating a new node

	method:create @noauth
		"""
		Create a new cpu node
		"""
		var:login str,,login to connect to the node
		var:passwd str,,password of the login given in argument
		var:pubkey str,,public ssh key of the cpunode
		var:hostname str,,hostname of the cpunode
		result:str  #returns the newly generated bootstrap script
