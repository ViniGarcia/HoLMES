'''
GENERAL INFORMATION: This file contains several classes that defines the
					 data model to communicate with the VIB through the
					 VIB Manager.
NOTE:				 The classes contain two "to" standard methods ("toSql"/
					 "toDictionary") and two "from" standard methods. 
					 "toSql" returns the query to insert the class into the
					 VIB, and "fromSql" rebuild the class from data returned
					 by the VIB.  
					 "toDictionary" returns the dictionary containing the 
					 dictionary representation of all the classes objects,
					 while "fromDictionary" recreates the class from the 
					 dictionary representation.
'''

#######################################################################################################
#######################################################################################################

'''
CLASS: VibSummaryModels
AUTHOR: Vinicius Fulber-Garcia
CREATION: 30 Oct. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; VibAuthInstance update)
DESCRIPTION: This class represents the table creation rou-
			 tines of all the tables of the VIB. Once a
			 table is updated in its respective class, the
			 creation routine must be updated here too.
'''
class VibSummaryModels:
	VibVnfInstance = """ CREATE TABLE IF NOT EXISTS VnfInstance (
                     vnfId text PRIMARY KEY,
                     vnfPlatform text NOT NULL,
                     vnfExtAgents text,
                     vnfAuth boolean
                    ); """

	VibAuthInstance = """ CREATE TABLE IF NOT EXISTS AuthInstance (
                     userId text PRIMARY KEY,
                     vnfId text NOT NULL,
                     authData text NOT NULL,
                     authResource text,
                     FOREIGN KEY (vnfId)
       					REFERENCES VnfInstance (vnfId)
                    ); """

'''
CLASS: VibVnfInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 30 Oct. 2020
L. UPDATE: 02 Nov. 2020 (Fulber-Garcia; Class methods creation)
DESCRIPTION: This class represents the VnfInstance table of the
			 VIB. Note that modifications on this class, parti-
			 culary in the attributes, must be updated in the
			 VibSummaryModels too.
'''
class VibVnfInstance:
	vnfId = None
	vnfPlatform = None
	vnfExtAgents = None			
	vnfAuth = None
	
	def __init__(self, vnfId, vnfPlatform, vnfExtAgents, vnfAuth):
		self.vnfId = vnfId
		self.vnfPlatform = vnfPlatform
		self.vnfExtAgents = vnfExtAgents
		self.vnfAuth = vnfAuth

	def fromSql(self, sqlData):
		self.vnfId = sqlData[0]
		self.vnfPlatform = sqlData[1]
		self.vnfExtAgents = sqlData[2]
		self.vnfAuth = boolean(sqlData[3])

	def fromDictionary(self, dictData):
		self.vnfId = dictData["vnfId"]
		self.vnfPlatform = dictData["vnfPlatform"]
		self.vnfExtAgents = dictData["vnfExtAgents"]
		self.vnfAuth = dictData["vnfAuth"]

	def toSql(self):
		return ('''INSERT INTO VnfInstance(vnfId,vnfPlatform,vnfExtAgents,vnfAuth)
              	   VALUES(?,?,?,?)''', (self.vnfId, self.vnfPlatform, self.vnfExtAgents, self.vnfAuth))

	def toDictionary(self):
		return {"vnfId":self.vnfId, "vnfPlatform":self.vnfPlatform, "vnfExtAgents":self.vnfExtAgents, "vnfAuth":self.vnfAuth}

'''
CLASS: VibAuthInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the AuthInstance table of the
			 VIB. Note that modifications on this class, parti-
			 culary in the attributes, must be updated in the
			 VibSummaryModels too.
'''
class VibAuthInstance:
	userId = None
	vnfId = None
	authData = None
	authResource = None

	def __init__(self, userId, vnfId, authData):
		self.userId = userId
		self.vnfId = vnfId
		self.authData = authData

	def __init__(self, userId, vnfId, authData, authResource):
		self.userId = userId
		self.vnfId = vnfId
		self.authData = authData
		self.authResource = authResource

	def fromSql(self, sqlData):
		self.userId = sqlData[0]
		self.vnfId = sqlData[1]
		self.authData = sqlData[2]
		self.authResource = sqlData[3]

	def fromDictionary(self, dictData):
		self.userId = dictData["userId"]
		self.vnfId = dictData["vnfId"]
		self.authData = dictData["authData"]
		if "authResource" in self.dictData:
			self.authResource = dictData["authResource"]

	def toSql(self):
		return ('''INSERT INTO AuthInstance(userId,vnfId,authData,authResource)
              	   VALUES(?,?,?,?)''', (self.userId, self.vnfId, self.authData, self.authResource))

	def toDictionary(self):
		return {"userId":self.userId, "vnfId":self.vnfId, "authData":self.authData, "authResource":self.authResource}