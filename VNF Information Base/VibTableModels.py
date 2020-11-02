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
L. UPDATE: 02 Nov. 2020 (Fulber-Garcia; Comments creation)
DESCRIPTION: This class represents the table creation rou-
			 tines of all the tables of the VIB. Once a
			 table is updated in its respective class, the
			 creation routine must be updated here too.
'''
class VibSummaryModels:
	VibVnfInstance = """ CREATE TABLE IF NOT EXISTS VnfInstance (
                     id integer PRIMARY KEY,
                     vnfId text NOT NULL,
                     vnfPlatform text NOT NULL,
                     vnfExtAgents text,
                     vnfAuth text,
                     UNIQUE (vnfId)
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
	
	def __init__(self):
		return

	def __init__(self, vnfId, vnfPlatform, vnfExtAgents, vnfAuth):
		self.vnfId = vnfId
		self.vnfPlatform = vnfPlatform
		self.vnfExtAgents = vnfExtAgents
		self.vnfAuth = vnfAuth

	def fromSql(self, sqlData):
		self.vnfId = sqlData[1]
		self.vnfPlatform = sqlData[2]
		self.vnfExtAgents = sqlData[3]
		self.vnfAuth = sqlData[4]

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