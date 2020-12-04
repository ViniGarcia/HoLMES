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
import AsModels

import json

'''
CLASS: VibSummaryModels
AUTHOR: Vinicius Fulber-Garcia
CREATION: 30 Oct. 2020
L. UPDATE: 04 Dez. 2020 (Fulber-Garcia; Included VibMaInstance)
DESCRIPTION: This class represents the table creation rou-
			 tines of all the tables of the VIB. Once a
			 table is updated in its respective class, the
			 creation routine must be updated here too.
'''
class VibSummaryModels:
	VibCredentialInstance = """ CREATE TABLE IF NOT EXISTS CredentialInstance (
                     userId text NOT NULL,
                     vnfId text NOT NULL,
                     authData text NOT NULL,
                     authResource text,
                     FOREIGN KEY (vnfId)
       					REFERENCES VnfInstance (vnfId)
       				 PRIMARY KEY (userId, vnfId)
                    ); """

	VibSubscriptionInstance = """ CREATE TABLE IF NOT EXISTS SubscriptionInstance (
                     visId text PRIMARY KEY,
                     visFilter text,
                     visCallback text NOT NULL,
                     visLinks text NOT NULL
                    ); """

	VibMaInstance = """ CREATE TABLE IF NOT EXISTS MaInstance (
                     maId text PRIMARY KEY,
                     maSource text NOT NULL
                    ); """

	VibPlatformInstance = """ CREATE TABLE IF NOT EXISTS PlatformInstance (
                     	 platformId text PRIMARY KEY,
                     	 platformDriver text NOT NULL
                    	); """

	VibVnfInstance = """ CREATE TABLE IF NOT EXISTS VnfInstance (
                     vnfId text PRIMARY KEY,
                     vnfAddress text NOT NULL,
                     vnfPlatform text NOT NULL,
                     vnfExtAgents text,
                     vnfAuth boolean,
                     FOREIGN KEY (vnfPlatform)
       					REFERENCES PlatformInstance (platformId)
                    ); """

	VibVnfmInstance = """ CREATE TABLE IF NOT EXISTS VnfmInstance (
                     	 vnfmId text PRIMARY KEY,
                     	 vnfmDriver text NOT NULL
                    	); """

'''
CLASS: VibCredentialInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 01 Dez. 2020 (Fulber-Garcia; Class name changed)
DESCRIPTION: This class represents the AuthInstance table of the
			 VIB. Note that modifications on this class, parti-
			 culary in the attributes, must be updated in the
			 VibSummaryModels too.
'''
class VibCredentialInstance:
	userId = None
	vnfId = None
	authData = None
	authResource = None

	def __init__(self):
		return

	def fromData(self, userId, vnfId, authData, authResource):
		self.userId = userId
		self.vnfId = vnfId
		self.authData = authData
		self.authResource = authResource
		return self

	def fromSql(self, sqlData):
		self.userId = sqlData[0]
		self.vnfId = sqlData[1]
		self.authData = sqlData[2]
		self.authResource = sqlData[3]
		return self

	def fromDictionary(self, dictData):
		self.userId = dictData["userId"]
		self.vnfId = dictData["vnfId"]
		self.authData = dictData["authData"]
		if "authResource" in self.dictData:
			self.authResource = dictData["authResource"]
		return self

	def toSql(self):
		return ('''INSERT INTO CredentialInstance(userId,vnfId,authData,authResource)
              	   VALUES(?,?,?,?)''', (self.userId, self.vnfId, self.authData, self.authResource))

	def toDictionary(self):
		return {"userId":self.userId, "vnfId":self.vnfId, "authData":self.authData, "authResource":self.authResource}

'''
CLASS: VibSubscriptionInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 06 Nov. 2020
L. UPDATE: 03 Dez. 2020 (Fulber-Garcia; Validate method implementation)
DESCRIPTION: This class represents the VnfIndicatorSubscription 
			 table of the VIB. Note that modifications on this
			 class, particulary in the attributes, must be upda-
			 ted in the VibSummaryModels too.
ERROR CODES: -1 -> Invalid data type
			 -2 -> Missing mandatory information
'''
class VibSubscriptionInstance:
	visId = None
	visFilter = None
	visCallback = None
	visLinks = None

	def __init__(self):
		return

	def validate(self):

		if type(self.visId) != str:
			return ("0", -1)
		if self.visFilter != None and type(self.visFilter) != AsModels.VnfIndicatorSubscription:
			return ("1", -1)
		if type(self.visCallback) != str:
			return ("2", -1)
		if type(self.visLinks) != dict:
			return ("3", -1)
		if not "self" in self.visLinks:
			return ("3", -2)
		if type(self.visLinks["self"]) != str:
			return ("3.self", -1)

		return ("4", 0)

	def fromData(self, visId, visFilter, visCallback, visLinks):
		self.visId = visId
		self.visFilter = visFilter
		self.visCallback = visCallback
		self.visLinks = visLinks
		return self

	def fromSql(self, sqlData):
		self.visId = sqlData[0]
		if sqlData[1] != None:
			self.visFilter = AsModels.VnfIndicatorNotificationsFilter().fromDictionary(json.loads(sqlData[1]))
		else:
			self.visFilter = sqlData[1]
		self.visCallback = sqlData[2]
		self.visLinks = json.loads(sqlData[3])
		return self

	def fromDictionary(self, dictData):
		self.visId = dictData["visId"]
		if dictData["visFilter"] != None:
			self.visFilter = AsModels.VnfIndicatorNotificationsFilter().fromDictionary(dictData["visFilter"])
		else:
			self.visFilter = dictData["visFilter"]
		self.visCallback = dictData["visCallback"]
		self.visLinks = dictData["visLinks"]
		return self

	def toSql(self):
		if self.visFilter != None:
			return ('''INSERT INTO SubscriptionInstance(visId,visFilter,visCallback,visLinks)
              	   	VALUES(?,?,?,?)''', (self.visId, json.dumps(self.visFilter.toDictionary()), self.visCallback, json.dumps(self.visLinks)))
		else:
			return ('''INSERT INTO SubscriptionInstance(visId,visFilter,visCallback,visLinks)
              	   	VALUES(?,?,?,?)''', (self.visId, self.visFilter, self.visCallback, json.dumps(self.visLinks)))

	def toDictionary(self):
		if self.visFilter != None:
			return {"visId":self.visId, "visFilter":self.visFilter.toDictionary(), "visCallback":self.visCallback, "visLinks":self.visLinks}
		else:
			return {"visId":self.visId, "visFilter":self.visFilter, "visCallback":self.visCallback, "visLinks":self.visLinks}

'''
CLASS: VibMaInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 05 Nov. 2020
L. UPDATE: 04 Dez. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the MaInstance table of the VIB.
			 Note that modifications on this class, particulary in
			 the attributes, must be updated in the VibSummaryModels
			 too.
ERROR CODES: -1 -> Invalid data type
'''
class VibMaInstance:
	maId = None
	maSource = None

	def __init__(self):
		return

	def validate(self):
		if type(self.maId) != str:
			return ("0", -1)
		if type(self.maSource) != str:
			return ("1", -1)

		return ("2", 0)

	def fromData(self, maId, maSource):
		self.maId = maId
		self.maSource = maSource
		return self

	def fromSql(self, sqlData):
		self.maId = sqlData[0]
		self.maSource = sqlData[1]
		return self

	def fromDictionary(self, dictData):
		self.maId = dictData["maId"]
		self.maSource = dictData["maSource"]
		return self

	def toSql(self):
		return ('''INSERT INTO MaInstance(maId,maSource)
              	   VALUES(?,?)''', (self.maId, self.maSource))

	def toDictionary(self):
		return {"maId":self.maId, "maSource":self.maSource}

'''
CLASS: VibVnfInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 30 Oct. 2020
L. UPDATE: 05 Nov. 2020 (Fulber-Garcia; New vnfAddress attribute; Update of vnfExtAgents; fromData method)
DESCRIPTION: This class represents the VnfInstance table of the
			 VIB. Note that modifications on this class, parti-
			 culary in the attributes, must be updated in the
			 VibSummaryModels too.
'''
class VibVnfInstance:
	vnfId = None
	vnfAddress = None
	vnfPlatform = None
	vnfExtAgents = None			
	vnfAuth = None
	
	def __init__(self):
		return	

	def fromData(self, vnfId, vnfAddress, vnfPlatform, vnfExtAgents, vnfAuth):
		self.vnfId = vnfId
		self.vnfAddress = vnfAddress
		self.vnfPlatform = vnfPlatform
		self.vnfExtAgents = vnfExtAgents
		self.vnfAuth = vnfAuth
		return self

	def fromSql(self, sqlData):
		self.vnfId = sqlData[0]
		self.vnfAddress = sqlData[1]
		self.vnfPlatform = sqlData[2]
		self.vnfExtAgents = json.loads(sqlData[3])
		self.vnfAuth = bool(sqlData[3])
		return self

	def fromDictionary(self, dictData):
		self.vnfId = dictData["vnfId"]
		self.vnfAddress = dictData["vnfAddress"]
		self.vnfPlatform = dictData["vnfPlatform"]
		self.vnfExtAgents = dictData["vnfExtAgents"]
		self.vnfAuth = dictData["vnfAuth"]
		return self

	def toSql(self):
		return ('''INSERT INTO VnfInstance(vnfId,vnfAddress,vnfPlatform,vnfExtAgents,vnfAuth)
              	   VALUES(?,?,?,?,?)''', (self.vnfId, self.vnfAddress, self.vnfPlatform, json.dumps(self.vnfExtAgents), self.vnfAuth))

	def toDictionary(self):
		return {"vnfId":self.vnfId, "vnfAddress":self.vnfAddress, "vnfPlatform":self.vnfPlatform, "vnfExtAgents":self.vnfExtAgents, "vnfAuth":self.vnfAuth}
	
'''
CLASS: VibPlatformInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 05 Nov. 2020
L. UPDATE: 02 Dez. 2020 (Fulber-Garcia; Implemetation of "validate" method)
DESCRIPTION: This class represents the PlatformInstance table of
			 the VIB. Note that modifications on this class, par-
			 ticulary in the attributes, must be updated in the
			 VibSummaryModels too.
ERROR CODES: -1 -> Invalid data type
'''
class VibPlatformInstance:
	platformId = None
	platformDriver = None

	def __init__(self):
		return

	def validate(self):
		if type(self.platformId) != str:
			return ("0", -1)
		if type(self.platformDriver) != str:
			return ("1", -1)

		return ("2", 0)

	def fromData(self, platformId, platformDriver):
		self.platformId = platformId
		self.platformDriver = platformDriver
		return self

	def fromSql(self, sqlData):
		self.platformId = sqlData[0]
		self.platformDriver = sqlData[1]
		return self

	def fromDictionary(self, dictData):
		self.platformId = dictData["platformId"]
		self.platformDriver = dictData["platformDriver"]
		return self

	def toSql(self):
		return ('''INSERT INTO PlatformInstance(platformId,platformDriver)
              	   VALUES(?,?)''', (self.platformId, self.platformDriver))

	def toDictionary(self):
		return {"platformId":self.platformId, "platformDriver":self.platformDriver}

'''
CLASS: VibVnfmInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 01 Dez. 2020
L. UPDATE: 01 Dez. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the VnfmInstance table of the
			 VIB. Note that modifications on this class, particu-
			 lary in the attributes, must be updated in the Vib-
			 SummaryModels too.
'''
class VibVnfmInstance:
	vnfmId = None
	vnfmDriver = None

	def __init__(self):
		return

	def fromData(self, vnfmId, vnfmDriver):
		self.vnfmId = vnfmId
		self.vnfmDriver = vnfmDriver
		return self

	def fromSql(self, sqlData):
		self.vnfmId = sqlData[0]
		self.vnfmDriver = sqlData[1]
		return self

	def fromDictionary(self, dictData):
		self.vnfmId = dictData["vnfmId"]
		self.vnfmDriver = dictData["vnfmDriver"]
		return self

	def toSql(self):
		return ('''INSERT INTO VnfmInstance(vnfmId,vnfmDriver)
              	   VALUES(?,?)''', (self.vnfmId, self.vnfmDriver))

	def toDictionary(self):
		return {"vnfmId":self.platformId, "vnfmDriver":self.platformDriver}

