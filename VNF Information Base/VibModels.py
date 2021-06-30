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
L. UPDATE: 31 Dez. 2020 (Fulber-Garcia; New table of users;
						modifications on credential table)
DESCRIPTION: This class represents the table creation rou-
			 tines of all the tables of the VIB. Once a
			 table is updated in its respective class, the
			 creation routine must be updated here too.
'''
class VibSummaryModels:
	VibUserInstance = """ CREATE TABLE IF NOT EXISTS UserInstance (
                     userId text PRIMARY KEY,
                     userAuthentication text NOT NULL,
                     userSecrets text,
                     userPrivileges text NOT NULL
                    ); """

	VibCredentialInstance = """ CREATE TABLE IF NOT EXISTS CredentialInstance (
                     userId text NOT NULL,
                     vnfId text NOT NULL,
                     FOREIGN KEY (userId)
       					REFERENCES UserInstance (userId)
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
                     maSource text NOT NULL,
                     maPlatform text NOT NULL
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
                     vnfAuth int,
                     FOREIGN KEY (vnfPlatform)
       					REFERENCES PlatformInstance (platformId)
                    ); """

	VibVnfmInstance = """ CREATE TABLE IF NOT EXISTS VnfmInstance (
                     	 vnfmId text PRIMARY KEY,
                     	 vnfmDriver text NOT NULL,
                     	 vnfmCredentials text
                    	); """

'''
CLASS: VibUserInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 31 Dez. 2020
L. UPDATE: 31 Dez. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the UserInstance table of the
			 VIB. Note that modifications on this class, parti-
			 culary in the attributes, must be updated in the
			 VibSummaryModels too.
'''
class VibUserInstance:
	userId = None
	userAuthentication = None
	userSecrets = None
	userPrivileges = []

	def __init__(self):
		return

	def validate(self):
		if type(self.userId) != str:
			return ("0", -1)
		if type(self.userAuthentication) != str:
			return ("1", -1)
		if type(self.userSecrets) != str:
			return ("2", -1)
		if type(self.userPrivileges) != list:
			return ("3", -1)
		for index in range(len(self.userPrivileges)):
			if not self.userPrivileges[index] in ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"]:
				return ("3." + str(index), -1)

		return ("4", 0)

	def fromData(self, userId, userAuthentication, userSecrets, userPrivileges):
		self.userId = userId
		self.userAuthentication = userAuthentication
		self.userSecrets = userSecrets
		self.userPrivileges = userPrivileges
		return self

	def fromSql(self, sqlData):
		self.userId = sqlData[0]
		self.userAuthentication = sqlData[1]
		self.userSecrets = sqlData[2]
		self.userPrivileges = json.loads(sqlData[3])
		return self

	def fromDictionary(self, dictData):
		self.userId = dictData["userId"]
		self.userAuthentication = dictData["userAuthentication"]
		self.userSecrets = dictData["userSecrets"]
		self.userPrivileges = dictData["userPrivileges"]
		return self

	def toSql(self):
		return ('''INSERT INTO UserInstance(userId,userAuthentication,userSecrets,userPrivileges)
              	   VALUES(?,?,?,?)''', (self.userId, self.userAuthentication, self.userSecrets, json.dumps(self.userPrivileges)))

	def toDictionary(self):
		return {"userId":self.userId, "userAuthentication":self.userAuthentication, "userSecrets":self.userSecrets, "userPrivileges":self.userPrivileges}

'''
CLASS: VibCredentialInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 31 Dez. 2020 (Fulber-Garcia; Moved authentication to
						 the UserInstance table)
DESCRIPTION: This class represents the CredentialInstance table
			 of the VIB. Note that modifications on this class,
			 particulary in the attributes, must be updated in
			 the VibSummaryModels too.
'''
class VibCredentialInstance:
	userId = None
	vnfId = None

	def __init__(self):
		return

	def validate(self):
		if type(self.userId) != str:
			return ("0", -1)
		if type(self.vnfId) != str:
			return ("1", -1)

		return ("2", 0) 

	def fromData(self, userId, vnfId):
		self.userId = userId
		self.vnfId = vnfId
		return self

	def fromSql(self, sqlData):
		self.userId = sqlData[0]
		self.vnfId = sqlData[1]
		return self

	def fromDictionary(self, dictData):
		self.userId = dictData["userId"]
		self.vnfId = dictData["vnfId"]
		return self

	def toSql(self):
		return ('''INSERT INTO CredentialInstance(userId,vnfId)
              	   VALUES(?,?)''', (self.userId, self.vnfId))

	def toDictionary(self):
		return {"userId":self.userId, "vnfId":self.vnfId}

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
L. UPDATE: 06 Dez. 2020 (Fulber-Garcia; Included maPLatform)
DESCRIPTION: This class represents the MaInstance table of the VIB.
			 Note that modifications on this class, particulary in
			 the attributes, must be updated in the VibSummaryModels
			 too.
ERROR CODES: -1 -> Invalid data type
'''
class VibMaInstance:
	maId = None
	maSource = None
	maPlatform = None

	def __init__(self):
		return

	def validate(self):
		if type(self.maId) != str:
			return ("0", -1)
		if type(self.maSource) != str:
			return ("1", -1)
		if type(self.maPlatform) != str:
			return ("2", -1)

		return ("3", 0)

	def fromData(self, maId, maSource, maPlatform):
		self.maId = maId
		self.maSource = maSource
		self.maPlatform = maPlatform
		return self

	def fromSql(self, sqlData):
		self.maId = sqlData[0]
		self.maSource = sqlData[1]
		self.maPlatform = sqlData[2]
		return self

	def fromDictionary(self, dictData):
		self.maId = dictData["maId"]
		self.maSource = dictData["maSource"]
		self.maPlatform = dictData["maPlatform"]
		return self

	def toSql(self):
		return ('''INSERT INTO MaInstance(maId,maSource,maPlatform)
              	   VALUES(?,?,?)''', (self.maId, self.maSource, self.maPlatform))

	def toDictionary(self):
		return {"maId":self.maId, "maSource":self.maSource, "maPlatform":self.maPlatform}

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

	def validate(self):
		if type(self.vnfId) != str:
			return ("0", -1)
		if type(self.vnfAddress) != str:
			return ("1", -1)
		if type(self.vnfPlatform) != str:
			return ("2", -1)
		if type(self.vnfExtAgents) != list:
			return ("3", -1)
		for index in range(len(self.vnfExtAgents)):
			if type(self.vnfExtAgents[index]) != str:
				return ("3." + str(index), -1)
		if type(self.vnfAuth) != bool:
			return ("4", -1)

		return ("5", 0)

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
		self.vnfAuth = bool(sqlData[4])
		return self

	def fromDictionary(self, dictData):
		self.vnfId = dictData["vnfId"]
		self.vnfAddress = dictData["vnfAddress"]
		self.vnfPlatform = dictData["vnfPlatform"]
		self.vnfExtAgents = dictData["vnfExtAgents"]
		self.vnfAuth = bool(dictData["vnfAuth"])
		return self

	def toSql(self):
		return ('''INSERT INTO VnfInstance(vnfId,vnfAddress,vnfPlatform,vnfExtAgents,vnfAuth)
              	   VALUES(?,?,?,?,?)''', (self.vnfId, self.vnfAddress, self.vnfPlatform, json.dumps(self.vnfExtAgents), int(self.vnfAuth)))

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
L. UPDATE: 07 Dez. 2020 (Fulber-Garcia; "validate" method implementation)
DESCRIPTION: This class represents the VnfmInstance table of the
			 VIB. Note that modifications on this class, particu-
			 lary in the attributes, must be updated in the Vib-
			 SummaryModels too.
'''
class VibVnfmInstance:
	vnfmId = None
	vnfmDriver = None
	vnfmCredentials = None

	def __init__(self):
		return

	def validate(self):
		if type(self.vnfmId) != str:
			return ("0", -1)
		if type(self.vnfmDriver) != str:
			return ("1", -1)
		if type(self.vnfmCredentials) != str:
			return ("2", -1)

		return ("3", 0)

	def fromData(self, vnfmId, vnfmDriver, vnfmCredentials):
		self.vnfmId = vnfmId
		self.vnfmDriver = vnfmDriver
		self.vnfmCredentials = vnfmCredentials
		return self

	def fromSql(self, sqlData):
		self.vnfmId = sqlData[0]
		self.vnfmDriver = sqlData[1]
		self.vnfmCredentials = sqlData[2]
		return self

	def fromDictionary(self, dictData):
		self.vnfmId = dictData["vnfmId"]
		self.vnfmDriver = dictData["vnfmDriver"]
		self.vnfmCredentials = dictData["vnfmCredentials"]
		return self

	def toSql(self):
		return ('''INSERT INTO VnfmInstance(vnfmId,vnfmDriver,vnfmCredentials)
              	   VALUES(?,?,?)''', (self.vnfmId, self.vnfmDriver, self.vnfmCredentials))

	def toDictionary(self):
		return {"vnfmId":self.vnfmId, "vnfmDriver":self.vnfmDriver, "vnfmCredentials":self.vnfmCredentials}