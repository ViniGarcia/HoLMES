class VibSummaryModels:
	VibVnfInstance = """ CREATE TABLE IF NOT EXISTS VnfInstance (
                     id integer PRIMARY KEY,
                     vnfId text NOT NULL,
                     vnfPlatform text NOT NULL,
                     vnfExtAgents text,
                     vnfAuth text,
                     UNIQUE (vnfId)
                    ); """

class VibVnfInstance:
	vnfId = None
	vnfPlatform = None
	vnfExtAgents = None			
	vnfAuth = None
	
	def __init__(self):
		pass

	def __init__(self, vnfId, vnfPlatform, vnfExtAgents, vnfAuth):
		self.vnfId = vnfId
		self.vnfPlatform = vnfPlatform
		self.vnfExtAgents = vnfExtAgents
		self.vnfAuth = vnfAuth

	def toSql(self):
		return ('''INSERT INTO VnfInstance(vnfId,vnfPlatform,vnfExtAgents,vnfAuth)
              	   VALUES(?,?,?,?)''', (self.vnfId, self.vnfPlatform, self.vnfExtAgents, self.vnfAuth))

	def toDictionary(self):
		return