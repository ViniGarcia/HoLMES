import VibModels

import uuid
import json

'''
GENERAL INFORMATION: This file contains classes regarding the communication
					 between an internal module and the Internal Router.
VALIDATION ERROR CODES:
					 -1: Invalid origin/destination, impossible communication
					 -2: No data was provided to be sent
					 -3: Invalid data type
					 -4: Invalid member in the structure
					 -5: Invalid data format
'''

#######################################################################################################
#######################################################################################################

'''
CLASS: IrMessage
AUTHOR: Vinicius Fulber-Garcia
CREATION: 24 Nov. 2020
L. UPDATE: 24 Nov. 2020 (Fulber-Garcia; Class creation)
NOTE: The "messageData" attribute to the VsAgent consists of a "VsData" instance;
DESCRIPTION: This class is the standard communication model
			 between the IR and other modules.
'''
class IrMessage:

	messageId = None			#Identifier (String), auto-attributed (1)
	messageData = None			#Specific message (Class), madatory (1)
	originModule = None			#Module name (String), mandatory (1)
	destinationModule = None	#Module name (String), mandatory (1)

	def __init__(self):
		return

	def validate(self):

		availableConnections = ["AS", "MS", "IM", "VS"]
		if not self.originModule in availableConnections:
			return ("1", -1)
		if not self.destinationModule in availableConnections:
			return ("2", -1)
		if self.messageData == None: #TODO: adjust here
			return ("3", -2) 

		return ("4", 0)

	def fromData(self, messageData, originModule, destinationModule):
		
		self.messageId = uuid.uuid1()
		self.messageData = messageData
		self.originModule = originModule
		self.destinationModule = destinationModule

		if self.validate()[1] == 0:
			return self
		else:
			return False

'''
CLASS: VsData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 24 Nov. 2020
L. UPDATE: 24 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class is the standard communication model
			 to request an operation to the VNF subsystem.
'''
class VsData:

	vibVnfInstance = None
	vibPlatformInstance = None

	operationId = None
	operationArgs = None

	def __init__(self):
		return

	def validate(self):
		
		if type(self.vibVnfInstance) != VibModels.VibVnfInstance:
			return ("0", -3)

		if type(self.vibPlatformInstance) != VibModels.VibPlatformInstance:
			return ("1", -3)
		
		if type(self.operationId) != str:
			return ("2", -3)
		
		if type(self.operationArgs) != dict:
			return ("3", -3)
		for key in self.operationArgs:
			if type(key) != str:
				return ("3." + str(key), -3)
			if type(self.operationArgs[key]) != str:
				return ("3." + str(key), -4)

		return ("4", 0) 

	def fromData(self, vibVnfInstance, vibPlatformInstance, operationId, operationArgs):

		self.vibVnfInstance = vibVnfInstance
		self.vibPlatformInstance = vibPlatformInstance

		self.operationId = operationId
		self.operationArgs = operationArgs

		if self.validate()[1] == 0:
			return self
		else:
			return False

'''
CLASS: VibManagement
AUTHOR: Vinicius Fulber-Garcia
CREATION: 01 Dez. 2020
L. UPDATE: 01 Dez. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class is the standard communication model
			 to request an operation to the VIB manager.
'''
class VibManagement:

	operationId = None
	operationArgs = None

	def __init__(self):
		return

	def validate(self):

		if type(self.operationId) != str:
			return ("0", -3)

		return ("2", 0)

	def fromData(self, operationId, operationArgs):

		self.operationId = operationId
		self.operationArgs = operationArgs

		if self.validate()[1] == 0:
			return self
		else:
			return False