import enum

'''
GENERAL INFORMATION: This file contains several classes that enable the
					 EMS to communicate other management components, as
					 well as other management components communicate with
					 the EMS platform.
NOTE:				 The classes are implemente and fully compliant with 
					 the ETSI specification. However, the validation me-
					 thods are not implemented for most of the classes (
					 TODO).
VALIDATION ERROR CODES:
					 -1: Attribute type not satisfied
					 -2: Mandatory attribute not satisfied
					 -3: Invalid member in structure
'''

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfInstanceSubscriptionFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Methods implementation)
DESCRIPTION: This type represents subscription filter cri-
			 teria to match VNF instances.
'''
class VnfInstanceSubscriptionFilter:
	vnfdIds = None 							#Identifier (String), mandatory (1)
	vnfProductsFromProviders = []			#Structure (Dictionary), optional (0..N)
	vnfInstanceIds = []						#Identifier (String), optional (0..N)
	vnfInstanceNames = []					#String, optional (0..N)

	def vnfProductsFromProvidersStruct(self):
		return {"vnfProducts":[]}			#Structure (Dictionary), optional (0..N)

	def vnfProductsStruct(self):
		return {"vnfProductName":None, 		#String, mandatory (1)
				"versions":[]}				#Structure (Dictionary), optional (0..N)

	def versionsStruct(self):
		return {"vnfSoftwareVersion":None,	#Version (String), mandatory (1)
				"vnfdVersions":[]}			#Version (String), optional (0..N)

	def validate(self):
		if type(self.id) != str:
			if self.id == None:
				return ("0", -2)
			else:
				return ("0", -1)

		if type(self.vnfProductsFromProviders) != list:
			return ("1", -1)
		for index in range(len(self.vnfProductsFromProviders)):
			if type(self.vnfProductsFromProviders[index]) != dict:
				return ("1." + str(index), -1)

			keyList = ["vnfProducts"]
			for key in self.vnfProductsFromProviders[index]:
				if not type(key) == str:
					return ("1." + str(index) + "." + str(key), -1)
				if not key in keyList:
					return ("1." + str(index) + "." + str(key), -3)
				keyList.remove(key)

			if not "vnfProducts" in keyList:
				if type(self.vnfProductsFromProviders[index]["vnfProducts"]) != list:
					return ("1." + str(index) + ".vnfProducts", -1)

				for subindex in range(len(self.vnfProductsFromProviders[index]["vnfProducts"])):
					if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]) != dict:
						return ("1." + str(index) + ".vnfProducts." + str(subindex), -1)

					keyList = ["vnfProductName", "versions"]
					for key in self.vnfProductsFromProviders[index]["vnfProducts"][subindex]:
						if not type(key) == str:
							return ("1." + str(index) + ".vnfProducts." + str(subindex) + "." + str(key), -1)
						if not key in keyList:
							return ("1." + str(index) + ".vnfProducts." + str(subindex) + "." + str(key), -3)
						keyList.remove(key)

					if "vnfProductName" in keyList:
						return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".vnfProductName", -2)
					if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"]) != str:
						if self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"] == None:
							return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".vnfProductName", -2)
						else:
							return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".vnfProductName", -1)

					if not "versions" in keyList:
						if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["versions"]) != list:
							return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions", -1)

						for subsubindex in range(len(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["versions"])):
							if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["versions"]) != dict:
								return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex), -1)

							keyList = ["vnfSoftwareVersion", "vnfdVersions"]
							for key in self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["versions"][subsubindex]:
								if not type(key) == str:
									return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + "." + str(key), -1)
								if not key in keyList:
									return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + "." + str(key), -3)
							keyList.remove(key)

							if "vnfSoftwareVersion" in keyList:
								return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + ".vnfSoftwareVersion", -2)
							if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"][subsubindex]["vnfSoftwareVersion"]) != str:
								if self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"][subsubindex]["vnfSoftwareVersion"] == None:
									return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + ".vnfSoftwareVersion", -2)
								else:
									return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + ".vnfSoftwareVersion", -1)

							if not "vnfdVersions" in keyList:
								if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"][subsubindex]["vnfdVersions"]) != list:
									return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + ".vnfdVersions", -1)

								for subsubsubindex in range(len(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"][subsubindex]["vnfdVersions"])):
									if type(self.vnfProductsFromProviders[index]["vnfProducts"][subindex]["vnfProductName"][subsubindex]["vnfdVersions"][subsubsubindex]) != str:
										return ("1." + str(index) + ".vnfProducts." + str(subindex) + ".versions." + str(subsubindex) + ".vnfdVersions" + str(subsubsubindex), -1)

		if type(self.vnfInstanceIds) != list:
			return ("2", -1)

		for index in range(len(self.vnfInstanceIds)):
			if not type(self.vnfInstanceIds[index]) == str:
				return ("2." + str(index), -1) 

		if type(self.vnfInstanceNames) != list:
			return ("3", -1)

		for index in range(len(self.vnfInstanceNames)):
			if not type(self.vnfInstanceNames[index]) == str:
				return ("3." + str(index), -1)

		return ("4", 0)

	def fromData(self, vnfdIds, vnfProductsFromProviders, vnfInstanceIds, vnfInstanceNames):
		
		self.vnfdIds = vnfdIds
		self.vnfProductsFromProviders = vnfProductsFromProviders
		self.vnfInstanceIds = vnfInstanceIds
		self.vnfInstanceNames = vnfInstanceNames

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):

		return {"vnfdIds":self.vnfdIds, "vnfProductsFromProviders":self.vnfProductsFromProviders, "vnfInstanceIds":self.vnfInstanceIds, "vnfInstanceNames":self.vnfInstanceNames} 

	def fromDictionary(self, dictData):
		
		self.vnfdIds = dictData["vnfdIds"]
		self.vnfProductsFromProviders = dictData["vnfProductsFromProviders"]
		self.vnfInstanceIds = dictData["vnfInstanceIds"]
		self.vnfInstanceNames = dictData["vnfInstanceNames"]
		return self

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF instance in the Ve-Vnfm-em re-
			 ference point.
'''
class VnfInstance:
	id = None											#Identifier (String), mandatory (1)
	vnfInstanceName = None								#String, optional (0..1)
	vnfInstanceDescription = None						#String, optional (0..1)
	vnfdId = None										#Identifier (String), mandatory (1)
	vnfProvider = None									#String, mandatory (1)
	vnfProductName = None								#String, mandatory (1)
	vnfSoftwareVersion = None							#Version (String), mandatory (1)
	vnfdVersion = None									#Version (String), mandatory (1)
	vnfConfigurableProperties = None					#KeyValuePairs (Dictionary), optional (0..1)
	instantiationState = None							#String (NOT_INSTANTIATED | NSTANTIATED), madatory (1)
	instantiatedVnfInfo = None 							#Structure (Dictionary), optional (0..1)						
	metadata = None										#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None									#KeyValuePairs (Dictionary), optional (0..1)
	links = None 										#Structure (Dictionary), mandatory (1)

	def instantiatedVnfInfoStruct(self):
		return {"flavourId":None,						#IdentifierInVnfd (String), mandatory (1)
				"vnfState":None,						#VnfOperationalStateType (Class), mandatory (1)
				"scaleStatus":[],						#ScaleInfo (Class), optional (0..N)
				"maxScaleLevels":[],					#ScaleInfo (Class), optional (0..N)
				"extCpInfo":[],							#VnfExtCpInfo (Class), mandatory (1..N)
				"extVirtualLinkInfo":[],				#ExtVirtualLinkInfo (Class), optional (0..N)
				"extManagedVirtualLinkInfo":[],			#ExtManagedVirtualLinkInfo (Class), optional (0..N)
				"monitoringParameters":[],				#MonitoringParameter (Class), optional (0..N)
				"localizationLanguage":None,			#String, optional (0..1)
				"vnfcResourceInfo":[],					#VnfcResourceInfo (Class), optional (0..N)
				"vnfVirtualLinkResourceInfo":[],		#VnfVirtualLinkResourceInfo (Class), optional (0..N)
				"virtualStorageResourceInfo":[],		#VirtualStorageResourceInfo (Class), optional (0..N)
				"vnfcInfo":[]}							#VnfcInfo (Class), optional (0..N)

	def linksStruct(self):
		return {"self":None,							#URI (String), mandatory (1)
			 "indicators":None,							#URI (String), optinal (0..1)
			 "instantiate":None,						#URI (String), optinal (0..1)
			 "terminate":None,							#URI (String), optinal (0..1)
			 "scale":None,								#URI (String), optinal (0..1)
			 "scaleToLevel":None,						#URI (String), optinal (0..1)
			 "changeFlavour":None,						#URI (String), optinal (0..1)
			 "heal":None,								#URI (String), optinal (0..1)
			 "operate":None,							#URI (String), optinal (0..1)
			 "changeExtConn":None,						#URI (String), optinal (0..1)
			 "createSnapshot":None,						#URI (String), optinal (0..1)
			 "revertToSnapshot":None}					#URI (String), optinal (0..1)

'''
CLASS: CreateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a creation request of a VNF instance
			 in the Ve-Vnfm-em reference point.
'''
class CreateVnfRequest:
	vnfdId = None							#Identifier (String), mandatory (1)
	vnfInstanceName = None					#String, optional (0..1)
	vnfInstanceDescription = None			#String, optional (0..1)
	metadata = None							#Structure (Dictionary), optinal (0..1)

'''
CLASS: InstantiateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an instantiation request of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class InstantiateVnfRequest:
	flavourId = None						#IdentifierInVnfd (String), mandatory (1)
	instantiationLevelId = None				#IdentifierInVnfd (String), optional (0..1)
	extVirtualLinks = []					#ExtVirtualLinkData (Class), optional (0..N)
	extManagedVirtualLinks = []				#ExtManagedVirtualLinkData (Class), optional (0..N)
	localizationLanguage = None				#String, optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ScaleVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a resource scaling request of a VNF 
			 instance in the Ve-Vnfm-em reference point.
'''
class ScaleVnfRequest:
	type = None								#String (SCALE_OUT | SCALE_IN), madatory (1)
	aspectId = None							#IdentifierInVnfd (String), mandatory (1)
	numberOfSteps = None					#Integer, optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ScaleVnfToLevelRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a level scaling request of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class ScaleVnfToLevelRequest:
	instantiationLevelId = None 			#IdentifierInVnfd (String), optional (0..1)
	scaleInfo = []							#ScaleInfo (Class), optinal (0..N)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ChangeVnfFlavourRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a changing flavour request of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class ChangeVnfFlavourRequest:
	newFlavourId = None						#IdentifierInVnfd (String), mandatory (1)
	instantiationLevelId = None				#IdentifierInVnfd (String), optional (0..1)
	extVirtualLinks = []					#ExtVirtualLinkData (Class), optinal (0..N)
	extManagedVirtualLinks = []				#ExtManagedVirtualLinkData (Class), optinal (0..N)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: TerminateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a termination request of a VNF instan-
			 ce in the Ve-Vnfm-em reference point.
'''
class TerminateVnfRequest:
	terminationType = None					#String (FORCEFUL | GRACEFUL), madatory (1)
	gracefulTerminationTimeout = None		#Integer, optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: HealVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a healing request of a VNF instance
			 in the Ve-Vnfm-em reference point.
'''
class HealVnfRequest:
	vnfcInstanceId = []						#Identifier (String), optional (0..N)
	cause = None							#String, optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)
	healScript = None						#String, optional (0..1)

'''
CLASS: OperateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an operation request of a VNF instan-
			 ce in the Ve-Vnfm-em reference point.
'''
class OperateVnfRequest:
	vnfcInstanceId = []						#Identifier (String), optional (0..N)
	changeStateTo = None					#VnfOperationalStateType (Class), optional (0..N)
	stopType = None							#StopType (Class), optional (0..1)
	gracefulStopTimeout = None				#Integer, optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ChangeExtVnfConnectivityRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an external connectivity changing re-
			 quest of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ChangeExtVnfConnectivityRequest:
	extVirtualLinks = []					#ExtVirtualLinkData (Class), mandatory (1..N)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ChangeCurrentVnfPkgRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF package changing request of a
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class ChangeCurrentVnfPkgRequest:
	vnfdId = None							#Identifier (String), mandatory (1)
	extVirtualLinks = []					#ExtVirtualLinkData (Class), optional (0..N)
	extManagedVirtualLinks = []				#ExtManagedVirtualLinkData (Class), optional (0..N)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: VnfInfoModificationRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF package changing request of a
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfInfoModificationRequest:
	vnfInstanceName = None					#String, optional (0..1)
	vnfInstanceDescription = None			#String, optional (0..1)
	vnfdId = ""								#Identifier (String), optional (0..1)
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	vnfcInfoModifications = []				#VnfcInfoModifications (Class), optional (0..N)

'''
CLASS: VnfInfoModificationRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF information changing request of 
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfInfoModificationRequest:
	vnfInstanceName = None					#String, optional (0..1)
	vnfInstanceDescription = None			#String, optional (0..1)
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	vnfdId = None							#Identifier (String), optional (0..1)
	vnfProvider = None						#String, optional (0..1)
	vnfProductName = None					#String, optional (0..1)
	vnfSoftwareVersion = None				#Version (String), optional (0..1)
	vnfdVersion = None						#Version (String), optional (0..1)
	vnfcInfoModifications = []				#VnfcInfoModifications (String), optional (0..N)

'''
CLASS: VnfLcmOpOcc
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF LCM operation occurence of a 
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfLcmOpOcc:
	id = None											#Identifier (String), mandatory (1)
	operationState = None								#LcmOperationStateType (Class), mandatory (1)
	stateEnteredTime = None								#DateTime (String), mandatory (1)
	startTime = None									#DateTime (String), mandatory (1)
	vnfInstanceId = None								#Identifier (String), mandatory (1)
	grantId = None										#Identifier (String), optional (0..1)
	operation = None									#LcmOperationType (Class), mandatory (1)
	isAutomaticInvocation = None						#Boolean, mandatory (1)
	operationParams = None								#KeyValuePairs (Dictionary), optional (0..N)
	isCancelPending = None								#Boolean, mandatory (1)
	cancelMode = None									#CancelModeType (Class), optional (0..1)
	error = None										#String, optional (0..1)
	resourceChanges = None								#Structure (Dictionary), optional (0..1)
	changedInfo = None									#VnfInfoModifications (Class), optional (0..1)
	changedExtConnectivity = []							#ExtVirtualLinkInfo (Class), optional (0..N)
	modificationsTriggeredByVnfPkgChange = None			#ModificationsTriggeredByVnfPkgChange (Class), optional (0..1)
	vnfSnapshotInfoId = None							#Identifier (String), optional (0..1)
	links = None										#Structure (Dictionary), mandatory (1)

	def resourceChanges(self):
		return {"affectedVnfcs":[],						#AffectedVnfc (Class), optional (0..N)
				"affectedVirtualLinks":[],				#AffectedVirtualLink (Class), optional (0..N)
				"affectedExtLinkPorts":[],				#AffectedExtLinkPort (Class), optional (0..N)
				"affectedVirtualStorages":[]}			#AffectedVirtualStorage (Class), optional (0..N)

	def links(self):
		return {"self":None,							#URI (String), mandatory (1)
	 			"vnfInstance":None,						#URI (String), mandatory (1)
	 			"grant":None,							#URI (String), optional (0..1)
	 			"cancel":None,							#URI (String), optional (0..1)
	 			"retry":None,							#URI (String), optional (0..1)
	 			"rollback":None,						#URI (String), optional (0..1)
	 			"fail":None,							#URI (String), optional (0..1)
	 			"vnfSnapshot":None}						#URI (String), optional (0..1)

'''
CLASS: CancelMode
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a cancel mode selection of an opera-
			 tion of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class CancelMode:
	cancelMode = None						#CancelModeType (Class), mandatory (1)

'''
CLASS: LccnSubscriptionRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a LCN subscription request of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class LccnSubscriptionRequest:
	filter = None 							#LifecycleChangeNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)
	verbosity = None 						#LcmOpOccNotificationVerbosityType (Class), optional (0..1)

'''
CLASS: LccnSubscription
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a LCN subscription of a VNF instance
			 in the Ve-Vnfm-em reference point.
'''
class LccnSubscription:
	id = None								#Identifier (String), mandatory (1)
	filter = None							#LifecycleChangeNotificationsFilter (Class), optional (0..1)
	callbackUri = None						#URI (String), mandatory (1)
	verbosity = None						#LcmOpOccNotificationVerbosityType (Class), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linksStruct(self):
		return {"self":None}				#URI (String), mandatory (1)
	

'''
CLASS: VnfLcmOperationOccurrenceNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a LCN occurence notification of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfLcmOperationOccurrenceNotification:
	id = None											#Identifier (String), mandatory (1)
	notificationType = None								#String, mandatory (1)
	subscriptionId = None								#Identifier (String), mandatory (1)
	timeStamp = None									#DateTime (String), mandatory (1)
	notificationStatus = None							#String (START | RESULT), mandatory (1)
	operationState = None								#LcmOperationStateType (Class), mandatory (1)
	vnfInstanceId = None								#Identifier (String), mandatory (1)
	operation = None									#LcmOperationType (Class), mandatory (1)
	isAutomaticInvocation = None						#Boolean, mandatory (1)
	verbosity = None									#LcmOpOccNotificationVerbosityType (Class), optional (0..1)
	vnfLcmOpOccId = None								#Identifier (String), mandatory (1)
	affectedVnfcs = []									#AffectedVnfc (Class), optional (0..N)
	affectedVirtualLinks = []							#AffectedVirtualLink (Class), optional (0..N)
	affectedExtLinkPorts = []							#AffectedExtLinkPort (Class), optional (0..N)
	affectedVirtualStorages = []						#AffectedVirtualStorage (Class), optional (0..N)
	changedInfo = None									#VnfInfoModifications (Class), optional (0..1)
	changedExtConnectivity = []							#ExtVirtualLinkInfo (Class), optional (0..N)
	modificationsTriggeredByVnfPkgChange = None			#ModificationsTriggeredByVnfPkgChange (, optional (0..1)
	error = None										#String, optional (0..1)
	_links = None										#LccnLinks, mandatory (1)

'''
CLASS: VnfIdentifierCreationNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a creation operation notification of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfIdentifierCreationNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String, mandatory (1)
	subscriptionId = None					#Identifier (String), mandatory (1)
	timeStamp = None						#DateTime (String), mandatory (1)
	vnfInstanceId = None					#Identifier (String), mandatory (1)
	links = None							#LccnLinks, mandatory (1)

'''
CLASS: VnfIdentifierDeletionNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a deletion operation notification of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfIdentifierDeletionNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String, mandatory (1)
	subscriptionId = None					#Identifier (String), mandatory (1)
	timeStamp = None						#DateTime (String), mandatory (1)
	vnfInstanceId = None					#Identifier (String), mandatory (1)
	links = None							#LccnLinks, mandatory (1)

'''
CLASS: CreateVnfSnapshotInfoRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a snapshot information operation no-
			 tification of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class CreateVnfSnapshotInfoRequest:
	vnfSnapshotPkgId = None					#Identifier (String), optional (0..1)

'''
CLASS: CreateVnfSnapshotRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a snapshot creation notification of
			 a VNF instance in the Ve-Vnfm-em reference po-
			 int.
'''
class CreateVnfSnapshotRequest:
	vnfSnapshotInfoId = None				#Identifier (String), mandatory (1)
	vnfcInstanceId = None					#IdentifierInVnf (String), optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)
	userDefinedData = None					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: VnfSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a individual VNF snapshot of a VNF 
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfSnapshotInfo:
	id = None								#Identifier (String), mandatory (1)
	vnfSnapshotPkgId = None					#Identifier (String), optional (0..1)
	vnfSnapshot = None						#VnfSnapshot (Class), optional (0..1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linksStruct(self):
		return {"self":None,				#URI (String), mandatory (1)
	 			"takenFrom":None}			#URI (String), optional (0..1)

'''
CLASS: VnfSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF snapshot of a VNF instance in
			 the Ve-Vnfm-em reference point.
'''
class VnfSnapshot:
	id = None								#Identifier (String), mandatory (1)
	vnfInstanceId = None					#Identifier (String), mandatory (1)
	creationStartedAt = None				#DateTime (String), mandatory (1)
	creationFinishedAt = None				#DateTime (String), optional (0..1)
	vnfdId = None							#Identifier (String), mandatory (1)
	vnfInstance = None						#VnfInstance (Class), mandatory (1)
	vnfcSnapshots = []						#VnfcSnapshotInfo (Class), mandatory (1..N)
	userDefinedData = None					#KeyValuePairs (Dictionary), optional (0..1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linksStruct(self):					
		return {"self":None}				#URI (String), mandatory (1)
	

'''
CLASS: RevertToVnfSnapshotRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a revertion to a snapshot request of
			 a VNF instance in the Ve-Vnfm-em reference po-
			 int.
'''
class RevertToVnfSnapshotRequest:
	vnfSnapshotInfoId = None				#Identifier (String), optional (0..1)
	vnfcInstanceId = None					#Identifier (String), optional (0..1)
	vnfcSnapshotInfoId = None				#Identifier (String), optional (0..1)
	additionalParams = None					#KeyValuePairs (Dictionary), optional (0..1)

#######################################################################################################
#######################################################################################################

'''
CLASS: ExtVirtualLinkData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a external virtual link of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class ExtVirtualLinkData:
	id = None								#Identifier (String), mandatory (1)
	vimConnectionId = None					#Identifier (String), optional (0..1)
	resourceProviderId = None				#Identifier (String), optional (0..1)
	resourceId = None						#IdentifierInVim (String), mandatory (1)
	extCps = []								#VnfExtCpData (Class), mandatory (1..N)
	extLinkPorts = []						#ExtLinkPortData (Class), optional (0..1)

'''
CLASS: ExtVirtualLinkInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an external virtual
			 link of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ExtVirtualLinkInfo:
	id = None								#Identifier (String), mandatory (1)
	resourceHandle = None					#ResourceHandle (Class), mandatory (1)
	extLinkPorts = []						#ExtLinkPortInfo (Class), optional (0..N)
	currentVnfExtCpData = []				#VnfExtCpData (Class), mandatory (1..N)

'''
CLASS: ExtManagedVirtualLinkData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an externally-managed internal virtual
			 link of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ExtManagedVirtualLinkData:
	id = None								#Identifier (String), mandatory (1)
	vnfVirtualLinkDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vimConnectionId = None					#Identifier (String), optional (0..1)
	resourceProviderId = None				#Identifier (String), optional (0..1)
	resourceId = None						#IdentifierInVim (String), mandatory (1)

'''
CLASS: ExtManagedVirtualLinkInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about externally-managed
			 internal virtual link of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class ExtManagedVirtualLinkInfo:
	id = None								#Identifier (String), mandatory (1)
	vnfVirtualLinkDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	networkResource = None					#ResourceHandle (Class), mandatory (1)
	vnfLinkPorts = []						#VnfLinkPortInfo (Class), optional (0..N)

'''
CLASS: VnfExtCpData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes external connection points of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfExtCpData:
	cpdId = None							#IdentifierInVnfd (String), mandatory (1)
	cpConfig = []							#KeyValuePairs (Dictionary), mandatory (1..N)

'''
CLASS: VnfExtCpConfig
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes the configuration of an external co-
			 nnection point of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfExtCpConfig:
	parentCpConfigId = None					#IdentifierInVnf (String), optional (0..1)
	linkPortId = None						#Identifier (String), optional (0..1)
	cpProtocolData = []						#CpProtocolData (Class), optional (0..N)

'''
CLASS: CpProtocolData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes network protocols data of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class CpProtocolData:
	layerProtocol = None					#String (P_OVER_ETHERNET), mandatory (1)
	ipOverEthernet = None					#IpOverEthernetAddressData (Class), optional (0..1)

'''
CLASS: IpOverEthernetAddressData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an IP over ethernet internet address 
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class IpOverEthernetAddressData:
	macAddress = None						#MacAddress (String), optional (0..1)
	segmentationId = None					#String, optional (0..1)
	ipAddresses = []						#Structure (Dictionary), optional (0..N)

	def ipAddressesStruct(self):
		return {"type":None,				#String (IPV4 | IPV6), mandatory (1)
				"fixedAddresses":[],		#IpAddress (String), optional (0..N)
				"numDynamicAddresses":None,	#Integer, optional (0..1)
				"addressRange":None, 		#Structure (Dictionary), optional (0..1)
				"subnetId":None}			#IdentifierInVim (String), optional (0..1)
	
	def addressRangeStruct(self):
		return {"minAddress":None,			#IpAddress (String), mandatory (1)
				"maxAddress":None}			#IpAddress (String), mandatory (1)
				  
'''
CLASS: ScaleInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about scaling operations
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class ScaleInfo:
	aspectId = None							#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	scaleLevel = None						#Integer, mandatory (1)

'''
CLASS: VnfcResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized compute
			 and storage resources of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class VnfcResourceInfo:
	id = None								#Identifier (String), mandatory (1)
	vduId = None							#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	computeResource = None					#ResourceHandle (Class), mandatory (1)
	storageResourceIds = []					#IdentifierInVnf (String), optional (0..N)
	reservationId = None					#Identifier (String), optional (0..N)
	vnfcCpInfo = []							#Structure (Dictionary), optional (0..N)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)

	def vnfcCpInfoStruct(self):
		return {"id":None,					#IdentifierInVnf (String), mandatory (1)
		 		"cpdId":None,				#IdentifierInVnfd (String), mandatory (1)
		 		"vnfExtCpId":None,			#IdentifierInVnf (String), optional (0..1)
		 		"cpProtocolInfo":[],		#CpProtocolInfo (Class), optional (0..N)
				"vnfLinkPortId":None,		#IdentifierInVnf (String), optional (0..1)
		 		"metadata":None}			#KeyValuePairs (Dictionary), optional (0..1)
	

'''
CLASS: VnfVirtualLinkResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized link
			 resources of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfVirtualLinkResourceInfo:
	id = None								#IdentifierInVnf (String), mandatory (1)
	vnfVirtualLinkDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	networkResource = None					#ResourceHandle (Class), mandatory (1)
	reservationId = None					#Identifier (String), optional (0..1)
	vnfLinkPorts = []						#VnfLinkPortInfo (Class), optional (0..N)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: VirtualStorageResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized storage
			 resources of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VirtualStorageResourceInfo:
	id = None								#IdentifierInVnf (String), mandatory (1)
	virtualStorageDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	storageResource = None					#ResourceHandle (Class), mandatory (1)
	reservationId = None					#Identifier (String), optional (0..1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: VnfLinkPortInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about ports of internal
			 virtual links of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfLinkPortInfo:
	id = None								#IdentifierInVnf (String), mandatory (1)
	resourceHandle = None					#ResourceHandle (Class), mandatory (1)
	cpInstanceId = None						#IdentifierInVnf (String), optional (0..1)
	cpInstanceType = None					#String (VNFC_CP | EXT_CP), optional (0..1)

'''
CLASS: ExtLinkPortInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about link ports of ext-
			 ernal virtual links of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class VnfLinkPortInfo:
	id = None								#Identifier (String), mandatory (1)
	resourceHandle = None					#ResourceHandle (Class), mandatory (1)
	cpInstanceId = None						#IdentifierInVnf (String), optional (0..1)

'''
CLASS: ExtLinkPortData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a link ports of external virtual li-
			 nks of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class VnfLinkPortInfo:
	id = None								#Identifier (String), mandatory (1)
	resourceHandle = None					#ResourceHandle (Class), mandatory (1)

'''
CLASS: ResourceHandle
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a particular computational resource 
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class ResourceHandle:
	vimConnectionId = None					#Identifier (String), optional (0..1)
	resourceProviderId = None				#Identifier (String), optional (0..1)
	resourceId = None						#IdentifierInVim (String), mandatory (1)
	vimLevelResourceType = None				#String, optional (0..1)

'''
CLASS: CpProtocolInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about the protocol layers
			 of a CP of a VNF instance in the Ve-Vnfm-em re-
			 ference point.
'''
class CpProtocolInfo:
	layerProtocol = None					#String (IP_OVER_ETHERNET), mandatory (1)
	ipOverEthernet = None					#IpOverEthernetAddressInfo (Class), optional (0..1)

'''
CLASS: IpOverEthernetAddressInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about the network address
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class IpOverEthernetAddressInfo:
	macAddress = None						#MacAddress (String), optional (0..1)
	segmentationId = None					#String, optional (0..1)
	ipAddresses = []						#Structure (Dictionary), optional (0..N)

	def ipAddresses(self):
		return {"type":None,				#String (IPV4 | IPV6), mandatory (1)
				"addresses":[],				#IpAddress (String), optional (0..N)
				"isDynamic":None,			#Boolean, optional (0..1)
				"addressRange":None,		#Structure (Dictionary), optional (0..1)
				"subnetId":None}			#String, optional (0..1)

	def addressRangeStruct(self):
		return {"minAddress":"",			#IpAddress (String), optional (0..1)
				"maxAddress":""}			#IpAddress (String), optional (0..1)

'''
CLASS: MonitoringParameter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a monitoring parameter of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class MonitoringParameter:
	id = None								#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	name = None								#String, optional (0..1)
	performanceMetric = None				#String, mandatory (1)

'''
CLASS: LifecycleChangeNotificationsFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a subscription filter of notifications
			 related lifecycle changes of a VNF instance in
			 the Ve-Vnfm-em reference point.
'''
class LifecycleChangeNotificationsFilter:
	vnfInstanceSubscriptionFilter = None	#VnfInstanceSubscriptionFilter (Class), optional (0..1)
	notificationTypes = []					#String (VnfLcmOperationOccurrenceNotification | VnfIdentifierCreationNotification | VnfIdentifierDeletionNotification), optional (0..1)
	operationTypes = []						#LcmOperationType (Class), optional (0..N)
	operationStates = []					#LcmOperationStateType (Class), optional (0..N)

'''
CLASS: AffectedVnfc
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a VNFC of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class AffectedVnfc:
	id = None								#IdentifierInVnf (String), mandatory (1)
	vduId = None							#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	changeType = None						#String (ADDED | REMOVED | MODIFIED | TEMPORARY), mandatory (1)
	computeResource = None					#ResourceHandle (Class), mandatory (1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)
	affectedVnfcCpIds = []					#IdentifierInVnf (String), optional (0..N)
	addedStorageResourceIds = []			#IdentifierInVnf (String), optional (0..N)
	removedStorageResourceIds = []			#IdentifierInVnf (String), optional (0..N)

'''
CLASS: AffectedVirtualLink
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a virtual link of a VNF instance in the Ve-
			 Vnfm-em reference point.
'''
class AffectedVirtualLink:
	id = None								#IdentifierInVnf (String), mandatory (1)
	vnfVirtualLinkDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	changeType = None						#String (ADDED | REMOVED | MODIFIED | TEMPORARY | LINK_PORT_ADDED | LINK_PORT_REMOVED), mandatory (1)
	networkResource = None					#ResourceHandle (Class), mandatory (1)
	vnfLinkPortIds = []						#IdentifierInVnf (String), optional (0..N)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: AffectedExtLinkPort
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition or remotion of an external
			 link port of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class AffectedVirtualLink:
	id = None								#IdentifierInVnf (String), mandatory (1)
	changeType = None						#String (ADDED | REMOVED), mandatory (1)
	extCpInstanceId = None					#IdentifierInVnf (String), mandatory (1)
	resourceHandle = None					#ResourceHandle (Class), mandatory (1)

'''
CLASS: AffectedVirtualStorage
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a virtual storage of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class AffectedVirtualStorage:
	id = None								#IdentifierInVnf (String), mandatory (1)
	virtualStorageDescId = None				#IdentifierInVnfd (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	changeType = None						#String (ADDED | REMOVED | MODIFIED | TEMPORARY), mandatory (1)
	storageResource = None					#ResourceHandle (Class), mandatory (1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: LccnLinks
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes a link to resource that a notificati-
			 on can contain to a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class LccnLinks:
	vnfInstance = None						#URI (String), mandatory (1)
	subscription = None						#URI (String), mandatory (1)
	vnfLcmOpOcc = None						#URI (String), optional (0..1)

'''
CLASS: VnfcInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about a VNFC instance of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfcInfo:
	id = None								#IdentifierInVnf (String), mandatory (1)
	vduId = None							#IdentifierInVnfd (String), mandatory (1)
	vnfcResourceInfoId = None				#IdentifierInVnf (String), optional (0..1)
	vnfcState = None						#String (STARTED | STOPPED), mandatory (1)
	vnfcConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: VnfcInfoModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes the modification of an entry in an arr-
			 ay of "VnfcInfo" of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfcInfoModifications:
	id = None								#IdentifierInVnf (String), mandatory (1)
	vnfcConfigurableProperties = None		#KeyValuePairs (Dictionary), mandatory (1)

'''
CLASS: VnfExtCpInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an external connec-
			 tion point of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfExtCpInfo:
	id = None								#IdentifierInVnf (String), mandatory (1)
	cpdId = None							#IdentifierInVnfd (String), mandatory (1)
	cpConfigId = None						#IdentifierInVnf (String), mandatory (1)
	vnfdId = None							#Identifier (String), optional (0..1)
	cpProtocolInfo = []						#CpProtocolInfo (Class), mandatory (1..N)
	extLinkPortId = None					#Identifier (String), optional (0..1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)
	associatedVnfcCpId = None				#Identifier (String), optional (0..1)
	associatedVnfVirtualLinkId = None		#Identifier (String), optional (0..1)

'''
CLASS: VnfcSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an snapshot of a VN-
			 FC of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfcSnapshotInfo:
	id = None											#IdentifierLocal (String), mandatory (1)
	vnfcInstanceId = None								#IdentifierInVnf (String), mandatory (1)
	creationStartedAt = None							#DateTime (String), mandatory (1)
	creationFinishedAt = None							#DateTime (String), optional (0..1)
	vnfcResourceInfoId = None							#IdentifierInVnf (String), mandatory (1)
	computeSnapshotResource = None						#ResourceHandle (Class), optional (0..1)
	storageSnapshotResources = []						#Structure (Dictionary), optional (0..N)

	def storageSnapshotResourcesStruct(self):
		return {"storageResourceId":None,				#IdentifierInVnf (String), mandatory (1)
				"storageSnapshotResource":None,			#ResourceHandle (Class), optional (0..1)
				"userDefinedData":None}					#KeyValuePairs (Dictionary), optional (0..1)

	def validate(self):
		if not type(self.id) == str:
			if self.id == None:
				return ("0", -2)
			else:
				return ("0", -1)

		if not type(self.vnfcInstanceId) == str:
			if self.vnfcInstanceId == None:
				return ("1", -2)
			else:
				return ("1", -1)

		if not type(self.creationStartedAt) == str:
			if self.creationStartedAt == None:
				return ("2", -2)
			else:
				return ("2", -1)

		if not type(self.creationFinishedAt) == str and self.creationFinishedAt != None:
			return ("3", -1)

		if not type(self.vnfcResourceInfoId) == str:
			if self.vnfcResourceInfoId == None:
				return ("4", -2)
			else:
				return ("4", -1)

		if not type(self.computeSnapshotResource) == ResourceHandle and self.computeSnapshotResource != None:
			return ("5", -1)

		if not type(self.storageSnapshotResources) == list:
			return ("6", -1)
		for index in range(len(self.storageSnapshotResources)):
			if not type(self.storageSnapshotResources[index]) == dict:
				return ("6." + str(index), -1)

			keyList = ["storageResourceId", "storageSnapshotResource", "userDefinedData"]
			for key in self.storageSnapshotResources[index]:
				if not type(key) == str:
					return ("6." + str(index) + "." + str(key), -1)
				if not key in keyList:
					return ("6." + str(index) + "." + str(key), -3)
				keyList.remove(key)

			if "storageResourceId" in keyList:
				return ("6." + str(index) + ".storageResourceId", -2)
			if type(self.storageSnapshotResources[index]["storageResourceId"]) != str:
				return ("6." + str(index) + ".storageResourceId", -1)
			if not "storageSnapshotResource" in keyList:
				if type(self.storageSnapshotResources[index]["storageSnapshotResource"]) != ResourceHandle and self.storageSnapshotResources[index]["storageSnapshotResource"] != None:
					return ("6." + str(index) + ".storageSnapshotResource", -1)
			if not "userDefinedData" in keyList:
				if type(self.storageSnapshotResources[index]["userDefinedData"]) != dict:
					return ("6." + str(index) + ".userDefinedData", -1)

				for key in self.storageSnapshotResources[index]["userDefinedData"]:
					if not type(key) == str:
						return ("6." + str(index) + ".userDefinedData." + str(key), -1)

		return ("7", 0)

'''
CLASS: ModificationsTriggeredByVnfPkgChange
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: Implementation of the reference structure that
			 describes the modification of an entry in an
			 VNF instance when a previous modification occur
			 in its VNF package in the Ve-Vnfm-em reference
			 point.
'''
class ModificationsTriggeredByVnfPkgChange:
	vnfConfigurableProperties = None		#KeyValuePairs (Dictionary), optional (0..1)
	metadata = None							#KeyValuePairs (Dictionary), optional (0..1)
	extensions = None						#KeyValuePairs (Dictionary), optional (0..1)
	vnfdId = None							#Identifier (String), optional (0..1)
	vnfProvider = None						#String, optional (0..1)
	vnfProductName = None					#String, optional (0..1)
	vnfSoftwareVersion = None				#Version (String), optional (0..1)
	vnfdVersion = None						#Version (String), optional (0..1)

	def validate(self):
		
		if not type(self.vnfConfigurableProperties) == dict:
			return ("0", -1)
		for key in self.vnfConfigurableProperties:
			if not type(key) == str:
				return ("0." + str(key), -1)

		if not type(self.metadata) == dict:
			return ("1", -1) 
		for key in self.metadata:
			if not type(key) == str:
				return ("1." + str(key), -1)

		if not type(self.extensions) == dict:
			return ("2", -1)
		for key in self.extensions:
			if not type(key) == str:
				return ("2." + str(key), -1)

		if not type(self.vnfdId) == str and self.vnfdId != None:
			return ("3", -1)

		if not type(self.vnfProvider) == str and self.vnfProvider != None:
			return ("4", -1)

		if not type(self.vnfProductName) == str and self.vnfProductName != None:
			return ("5", -1)

		if not type(self.vnfSoftwareVersion) == str and self.vnfSoftwareVersion != None:
			return ("6", -1)

		if not type(self.vnfdVersion) == str and self.vnfdVersion != None:
			return ("7", -1)

		return ("8", 0)

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfOperationalStateType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of VNF operational states. Do 
			 not modify the object values of this class.
'''
class VnfOperationalStateType(enum.Enum):
	STARTED = 0
	STOPPED = 1

'''
CLASS: StopType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of stopping operation states. Do 
			 not modify the object values of this class.
'''
class StopType(enum.Enum):
	FORCEFUL = 0
	GRACEFUL = 1

'''
CLASS: LcmOperationType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of LCM operation states. Do not 
			 modify the object values of this class.
'''
class LcmOperationType(enum.Enum):
	INSTANTIATE 	   = 0
	SCALE 			   = 1
	SCALE_TO_LEVEL 	   = 2
	CHANGE_FLAVOUR 	   = 3
	TERMINATE 		   = 4
	HEAL 			   = 5
	OPERATE 		   = 6
	CHANGE_EXT_CONN    = 7
	MODIFY_INFO 	   = 8
	CREATE_SNAPSHOT    = 9
	REVERT_TO_SNAPSHOT = 10
	CHANGE_VNFPKG 	   = 11

'''
CLASS: LcmOperationStateType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of LCM operation states. Do not 
			 modify the object values of this class.
'''
class LcmOperationStateType(enum.Enum):
	STARTING 	 = 0
	PROCESSING   = 1
	COMPLETED 	 = 2
	FAILED_TEMP  = 3
	FAILED 		 = 4
	ROLLING_BACK = 5
	ROLLED_BACK  = 6

'''
CLASS: CancelModeType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of canceling operation modes. Do 
			 not modify the object values of this class.
'''
class CancelModeType(enum.Enum):
	GRACEFUL = 0
	FORCEFUL = 1

'''
CLASS: LcmOpOccNotificationVerbosityType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of notification verbosity of LCM
			 operations occurences. Do not modify the ob-
			 ject values of this class.
'''
class LcmOpOccNotificationVerbosityType(enum.Enum):
	FULL  = 0
	SHORT = 1

#######################################################################################################
#######################################################################################################

'''
CLASS: ThresholdCrossedNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: This class represents a notification that is sent
			 through the Ve-Vnfm-em reference point when a th-
			 reshold has been crossed.
'''
class ThresholdCrossedNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String, mandatory (1)
	timeStamp = None						#DateTime (String), mandatory (1)
	thresholdId = None						#Identifier (String), mandatory (1)
	crossingDirection = None				#CrossingDirectionType (Class), mandatory (1)
	objectType = None						#String, mandatory (1)
	objectInstanceId = None					#Identifier (String), mandatory (1)
	subObjectInstanceId = None 				#IdentifierInVnf (String), optional (0..1)
	performanceMetric = None 				#String, mandatory (1)
	performanceValue = None 				#Anything, mandatory (1)
	context = None							#KeyValuePairs (Dictionary), optional (0..1)
	links = None 							#Structure (Dictionary), mandatory (1)	

	def linksStruct(self):
		return {"objectInstance":None, 		#URI (String), optional (0..1)
				"threshold":None} 			#URI (String), mandatory (1)

'''
CLASS: PerformanceInformationAvailableNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This notification informs the receiver that performan-
			 ce information is available. The notification shall be
			 triggered by the VNFM when new performance information
			 collected by a performance monitoring job is available.
'''
class PerformanceInformationAvailableNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String, mandatory (1)
	timeStamp = None						#DateTime (String), mandatory (1)
	pmJobId = None							#Identifier (String), mandatory (1)
	objectType = None						#String, mandatory (1)
	objectInstanceId = None					#Identifier (String), mandatory (1)
	subObjectInstanceIds = []				#IdentifierInVnf (String), optional (0..N)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linksStruct(self):
		return {"objectInstance":None, 		#URI (String), optional (0..1)
				"pmJob":None,				#URI (String), mandatory (1)
				"performanceReport":None}	#URI (String), mandatory (1)

'''
CLASS: CreatePmJobRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a request to create a perfomance
			 monitoring job.
'''
class CreatePmJobRequest:
	objectType = None						#String, mandatory (1)
	objectInstanceIds = []					#Identifier (String), mandatory (1..N)
	subObjectInstanceIds = []				#IdentifierInVnf (String), optional (0..N)
	criteria = None 						#PmJobCriteria (Class), mandatory (1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: PmJob
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a performance monitoring job.
'''
class PmJob:
	id = None								#Identifier (String), mandatory (1)
	objectType = None						#String, mandatory (1)
	objectInstanceIds = []					#Identifier (String), mandatory (1..N)
	subObjectInstanceIds = []				#IdentifierInVnf (String), optional (0..N)
	criteria = None 						#PmJobCriteria (Class), mandatory (1)
	callbackUri = None 						#URI (String), mandatory (1)
	reports = []							#Structure (Dictionary), optional (0..N)
	links = None 							#Structure (Dictionary), mandatory (1)

	def reportsStruct(self):
		return {"href":None, 				#URI (String), mandatory (1)
				"readyTime":None,			#DateTime (String), mandatory (1)
				"expiryTime":None, 			#DateTime (String), optional (0..1)
				"fileSize":0}				#Unsigend Integer, optional (0..1)

	def linksStruct(self):
		return {"self":None,				#URI (String), mandatory (1)
				"objects":None}				#URI (String), optional (0..N)

'''
CLASS: CreateThresholdRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a request to create a threshold.
'''
class CreateThresholdRequest:
	objectType = None						#String, mandatory (1)
	objectInstanceId = None 				#Identifier (String), mandatory (1)
	subObjectInstanceIds = []				#IdentifierInVnf (String), optional (0..N)
	criteria = None 						#ThresholdCriteria (Class), mandatory (1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (Class), optional (0..1)

'''
CLASS: Threshold
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a threshold.
'''
class Threshold:
	id = None								#Identifier (String), mandatory (1)
	objectType = None						#String, mandatory (1)
	objectInstanceId = None 				#Identifier (String), mandatory (1)
	subObjectInstanceIds = []				#IdentifierInVnf (String), optional (0..N)
	criteria = None 						#ThresholdCriteria (Class), mandatory (1)
	callbackUri = None 						#URI (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linksStruct(self):
		return {"self":None,				#URI (String), mandatory (1)
				"objects":None}				#URI (String), optional (0..N)

'''
CLASS: PerformanceReport
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: This class defines the format of a performance report
			 provided by the VNFM to the API consumer as a result of
			 collecting performance information as part of a PM job.
'''
class PerformanceReport:
	entries = []							#Structure (Dictionary), mandatory (1..N)

	def entriesStruct(self):
		return {"objectType":None,			#String, mandatory (1)
				"objectInstanceId":None, 	#Identifier (String), mandatory (1)
				"subObjectInstanceId":None,	#IdentifierInVnf (String), optional (0..1)
				"performanceMetric":None, 	#String, mandatory (1)
				"performanceValues":[]}		#Structure (Dictionary), mandatory (1..N)

	def performanceValuesStruct(self):
		return {"timeStamp":None, 			#DateTime (String), mandatory (1)
				"value":None,				#Anything, mandatory (1)
				"context":None} 			#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ThresholdModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents modifications to a threshold.
'''
class ThresholdModifications:
	callbackUri = None 						#URI (String), optional (0..1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: PmJobModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents modifications to a performance
		   	 monitoring job.
'''
class PmJobModifications:
	callbackUri = None 						#URI (String), optional (0..1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: PmJobCriteria
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: This class represents collection criteria for perfor-
			 mance monitoring jobs.
'''
class PmJobCriteria:
	performanceMetric = []					#String, optional (0..N)
	performanceMetricGroup = []				#String, optional (0..N)
	collectionPeriod = None					#Unsigned integer, mandatory (1)
	reportingPeriod = None					#Unsigned integer, mandatory (1)
	reportingBoundary = None 				#DateTime (String), optional (0..1)

'''
CLASS: ThresholdCriteria
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: This class represents criteria that define a threshold.
'''
class ThresholdCriteria:
	performanceMetric = None				#String, mandatory (1)
	thresholdType = None 					#String (SIMPLE), mandatory (1)
	simpleThresholdDetails = None 			#Structure (Dictionary), optional (0..1)

	def simpleThresholdDetailsStruct(self):
		return {"thresholdValue":None,		#Float, mandatory (1)
				"hysteresis":None}			#Float, mandatory (1)

#######################################################################################################
#######################################################################################################

'''
CLASS: CrossingDirectionType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of crossing direction type. Do not modify
			 the object values of this class.
'''
class CrossingDirectionType(enum.Enum):
	UP = 0
	DOWN = 1

#######################################################################################################
#######################################################################################################

'''
CLASS: FmSubscriptionRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription request related to
			 notifications about VNF faults.
'''
class FmSubscriptionRequest:
	filter = None 							#FmNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: FmSubscription
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription related to notifica-
			 tions about VNF faults.
'''
class FmSubscription:
	id = None								#Identifier (String), mandatory (1)
	filter = None 							#FmNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"self":None}				#URI (String), mandatory (1)

'''
CLASS: Alarm
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 28 Oct. 2020 (Fulber-Garcia; Data update)
DESCRIPTION: The alarm class encapsulates information about an alarm.
'''
class Alarm:
	id = None								#Identifier (String), mandatory (1)
	managedObjectId = None 					#Identifier (String), mandatory (1)
	vnfcInstanceIds = []					#IdentifierVnf (String), optional (0..N)
	rootCauseFaultyResource = None 			#FaultyResourceInfo (Class), optional (0..1)
	alarmRaisedTime = None 					#DateTime (String), mandatory (1)
	alarmChangedTime = None 				#DateTime (String), optional (0..1)
	alarmClearedTime = None 				#DateTime (String), optional (0..1)
	alarmAcknowledgedTime = None 			#DateTime (String), optional (0..1)
	ackState = None 						#AckState (Enum), mandatory (1)
	perceivedSeverity = None 				#PerceivedSeverityType (Class), mandatory (1)
	eventTime = None 						#DateTime (String), mandatory (1)
	eventType = None 						#EventType (Class), mandatory (1)
	faultType = None 						#String, optional (0..1)
	probableCause = None 					#String, mandatory (1)
	isRootCause = None 						#Boolean, mandatory (1)
	correlatedAlarmIds = [] 				#Identifier (String), optional (0..N)
	faultDetails = [] 						#String, optional (0..N)
	links = None 							#Structure (Dictionary), mandatory (1)
	
	def linkStruct(self):
		return {"self":None,				#URI (String), mandatory (1)
				"objectInstance":None}		#URI (String), optional (0..1)

'''
CLASS: AlarmNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents an alarm notification about VNF faults.
			 This notification shall be triggered by the VNFM when an a-
			 larm has been created or an alarm has been updated.
'''
class AlarmNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String (AlarmNotification), mandatory (1)
	subscriptionId = None 					#Identifier (String), mandatory (1)
	timeStamp = None 						#DateTime (String), mandatory (1)
	alarm = None 							#Alarm (Class), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"subscription":None}		#URI (String), mandatory (1)

'''
CLASS: AlarmClearedNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents an alarm cleared notification about VNF
			 faults. The notification shall be triggered by the VNFM when
			 an alarm has been cleared.
'''
class AlarmClearedNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String (AlarmClearedNotification), mandatory (1)
	subscriptionId = None 					#Identifier (String), mandatory (1)
	timeStamp = None 						#DateTime (String), mandatory (1)
	alarmId = None							#Identifier (String), mandatory (1)
	alarmClearedTime = None 				#DateTime (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"subscription":None, 		#URI (String), mandatory (1)
				"alarm":None}				#URI (String), mandatory (1)

'''
CLASS: PerceivedSeverityRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the escalated value of the perceived
			 severity for an alarm.
'''
class PerceivedSeverityRequest:
	proposedPerceivedSeverity = None 		#PerceivedSeverityType (Class), mandatory (1)

'''
CLASS: AlarmListRebuiltNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a notification that the alarm list
			 has been rebuilt. The notification shall be triggered by
			 the VNFM when the alarm list has been rebuilt.
'''
class AlarmListRebuiltNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String (AlarmListRebuiltNotification), mandatory (1)
	subscriptionId = None 					#Identifier (String), mandatory (1)
	timeStamp = None 						#DateTime (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"subscription":None, 		#URI (String), mandatory (1)
				"alarms":None}				#URI (String), mandatory (1)

'''
CLASS: AlarmModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents attribute modifications for an indivi-
			 dual alarm resource, i.e. modifications to a resource repre-
			 sentation based on the "Alarm" data type.
'''
class AlarmModifications:
	ackState = None 						#AckState (Enum), mandatory (1)

'''
CLASS: FmNotificationsFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription filter related to notifi-
			 cations about VNF faults.
'''
class FmNotificationsFilter:
	vnfInstanceSubscriptionFilter = None 	#VnfInstanceSubscriptionFilter (Class), optional (0..1)
	notificationTypes = []					#String (AlarmNotification | AlarmClearedNotification | AlarmListRebuiltNotification), optional (0..N)
	faultyResourceTypes = []				#FaultyResourceType (Class), optional (0..N)
	perceivedSeverities = []				#PerceivedSeverityType (Class), optional (0..N)
	eventTypes = []							#EventType (Class), optional (0..N)
	probableCauses = [] 					#String, optional (0..N)

'''
CLASS: FaultyResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents the faulty virtual resources that have a
			 negative impact on a VNF.
'''
class FaultyResourceInfo:
	faultyResource = None 					#ResourceHandle (Class), mandatory (1)
	faultyResourceType = None 				#FaultyResourceType (Class), mandatory (1)

#######################################################################################################
#######################################################################################################

'''
CLASS: PerceivedSeverityType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of perceived severity type. Do not modify
			 the object values of this class.
'''
class PerceivedSeverityType(enum.Enum):
	CRITICAL = 0
	MAJOR = 1
	MINOR = 2
	WARNING = 3
	INDETERMINATE = 4
	CLEARED = 5

'''
CLASS: EventType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of event type. Do not modify the object values
			 of this class.
'''
class EventType(enum.Enum):
	COMMUNICATIONS_ALARM = 0
	PROCESSING_ERROR_ALARM = 1
	ENVIRONMENTAL_ALARM = 2
	QOS_ALARM = 3
	EQUIPMENT_ALARM = 4

'''
CLASS: FaultyResourceType
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Enumerator of faulty resource type. Do not modify the object
			 values of this class.
'''
class FaultyResourceType(enum.Enum):
	COMPUTE = 0
	STORAGE = 1
	NETWORK = 2

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfIndicator
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a VNF indicator value.
'''
class VnfIndicator:
	id = None								#Identifier (String), mandatory (1)
	name = None 							#String, optional (0..1)
	value = None 							#String, mandatory (1)
	vnfInstanceId = None 					#Identifier (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"self":None, 				#URI (String), mandatory (1)
				"vnfInstance":None}			#URI (String), mandatory (1)

'''
CLASS: VnfIndicatorSubscriptionRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Methods implementation)
DESCRIPTION: This class represents a subscription request
			 related to VNF indicator value change noti-
			 fications.
'''
class VnfIndicatorSubscriptionRequest:
	filter = None 							#VnfIndicatorNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

	def validate(self):

		if self.filter != None:
			if type(self.filter) != VnfIndicatorNotificationsFilter:
				return ("0", -1)
			filterValidation = self.filter.validate()
			if filterValidation[1] != 0:
				return ("0." + filterValidation[0], filterValidation[1])

		if type(self.callbackUri) != str:
			if self.callbackUri == None:
				return ("1", -2)
			else:
				return ("1", -1)

		if type(self.authentication) != None:
			if type(self.authentication) != str:
				return ("2", -1)

		return ("3", 0)

	def fromData(self, filter, callbackUri, authentication):
		
		self.filter = filter
		self.callbackUri = callbackUri
		self.authentication = authentication

		if self.validate()[1] == 0:
			return self
		else:
			return False 

	def toDictionary(self):
		
		if self.filter != None:
			return {"filter":self.filter.toDictionary(), "callbackUri":self.callbackUri, "authentication":self.authentication}
		else:
			return {"filter":self.filter, "callbackUri":self.callbackUri, "authentication":self.authentication}

	def fromDictionary(self, dictData):
		
		if dictData["filter"] != None:
			self.filter = VnfIndicatorNotificationsFilter().fromDictionary(dictData["filter"])
		else:
			self.filter = dictData["filter"]
		self.callbackUri = dictData["callbackUri"]
		self.authentication = dictData["authentication"]

'''
CLASS: VnfIndicatorSubscription
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; fromData method implementation)
DESCRIPTION: This class represents a subscription related
			 to notifications about VNF indicator value
			 changes.
'''
class VnfIndicatorSubscription:
	id = None								#Identifier (String), mandatory (1)
	filter = None 							#VnfIndicatorNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"self":None}				#URI (String), mandatory (1)

	def validate(self):
		if type(self.id) != str:
			if self.id == None:
				return ("0", -2)
			else:
				return ("0", -1)

		if self.filter != None:
			if type(self.filter) != VnfIndicatorNotificationsFilter:
				return ("1", -1)
			filterValidation = self.filter.validate()
			if filterValidation[1] != 0:
				return ("1." + filterValidation[0], filterValidation[1])

		if type(self.callbackUri) != str:
			if self.callbackUri == None:
				return ("2", -2)
			else:
				return ("2", -1)

		if not type(self.links) == dict:
			return ("3", -1)

		keyList = ["self"]
		for key in self.links:
			if not type(key) == str:
				return ("3." + str(key), -1)
			if not key in keyList:
				return ("3." + str(key), -3)
			keyList.remove(key)

		if "self" in keyList:
			return ("3." + str(index) + ".self", -2)
		if type(self.links["self"]) != str:
				return ("3." + str(index) + ".self", -1)

		return ("4", 0)	

	def fromData(self, id, filter, callbackUri, links):
		self.id = id
		self.filter = filter
		self.callbackUri = callbackUri
		self.links = links

		if self.validate()[1] == 0:
			return self
		else:
			return False 

	def toDictionary(self):
		if self.filter != None:
			return {"id":self.id, "filter":self.filter.toDictionary(), "callbackUri":self.callbackUri, "links":self.links}
		else:
			return {"id":self.id, "filter":self.filter, "callbackUri":self.callbackUri, "links":self.links}

	def fromDictionary(self, dictData):
		self.id = dictData["id"]
		if dictData["filter"] != None:
			self.filter = VnfIndicatorNotificationsFilter().fromDictionary(dictData["filter"])
		else:
			self.filter = dictData["filter"]
		self.callbackUri = dictData["callbackUri"]
		self.links = dictData["links"]
		return self
		
'''
CLASS: VnfIndicatorValueChangeNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a VNF indicator value
			 change notification.
'''
class VnfIndicatorValueChangeNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String (VnfIndicatorValueChangeNotification), mandatory (1)
	subscriptionId = None 					#Identifier (String), mandatory (1)
	timeStamp = None 						#DateTime (String), mandatory (1)
	vnfIndicatorId = None 					#IdentifierInVnfd (String), mandatory (1)
	name = None 							#String, optional (0..1)
	value = None 							#String, mandatory (1)
	vnfInstanceId = None 					#Identifier (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"subscription":None, 		#URI (String), mandatory (1)
				"vnfInstance":None}			#URI (String), mandatory (1)

'''
CLASS: SupportedIndicatorsChangeNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a notification to in-
			 form the receiver that the set of indicators
			 supported by a VNF instance has changed.
'''
class SupportedIndicatorsChangeNotification:
	id = None								#Identifier (String), mandatory (1)
	notificationType = None					#String (VnfIndicatorValueChangeNotification), mandatory (1)
	subscriptionId = None 					#Identifier (String), mandatory (1)
	timeStamp = None 						#DateTime (String), mandatory (1)
	vnfInstanceId = None 					#Identifier (String), mandatory (1)
	supportedIndicators = [] 				#Structure (Dictionary), optional (0..N)
	links = None 							#Structure (Dictionary), mandatory (1)

	def supportedIndicatorsStruct(self):
		return {"vnfIndicatorId":None, 		#IdentifierInVnfd (String), mandatory (1)
				"name":None} 				#String, optional (0..1)
	
	def linkStruct(self):
		return {"subscription":None, 		#URI (String), mandatory (1)
				"vnfInstance":None}			#URI (String), mandatory (1)

'''
CLASS: VnfIndicatorNotificationsFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; fromData method implementation)
DESCRIPTION: This class represents a subscription filter
			 for notifications related to VNF indicators.
'''
class VnfIndicatorNotificationsFilter:
	vnfInstanceSubscriptionFilter = None 	#VnfInstanceSubscriptionFilter (Class), optional (0..1)
	notificationTypes = []					#String (VnfIndicatorValueChangeNotification | SupportedIndicatorsChangeNotification), optional (0..N)
	indicatorIds = []						#IdentifierInVnfd (String), optional (0..N)

	def validate(self):

		if self.vnfInstanceSubscriptionFilter != None:
			if type(self.vnfInstanceSubscriptionFilter) != VnfInstanceSubscriptionFilter:
				return ("0", -1)
			filterValidation = self.vnfInstanceSubscriptionFilter.validate()
			if filterValidation[1] != 0:
				return ("0." + filterValidation[0], filterValidation[1])

		if not type(self.notificationTypes) == list:
			return ("1.", -1)
		for index in range(len(self.notificationTypes)):
			if type(self.notificationTypes[index]) != str:
				return ("1." + str(index), -1)
			if self.notificationTypes[index] in ["VnfIndicatorValueChangeNotification", "SupportedIndicatorsChangeNotification"]:
				return ("1." + str(index), -3)

		if not type(self.indicatorIds) == list:
			return ("2", -1)
		for index in range(len(self.indicatorIds)):
			if type(self.indicatorIds[index]) != str:
				return ("2." + str(index), -1)

		return ("3", 0)

	def fromData(self, vnfInstanceSubscriptionFilter, notificationTypes, indicatorIds):
		
		self.vnfInstanceSubscriptionFilter = vnfInstanceSubscriptionFilter
		self.notificationTypes = notificationTypes
		self.indicatorIds = indicatorIds

		if self.validate()[1] == 0:
			return self
		else:
			return False 

	def toDictionary(self):

		if self.vnfInstanceSubscriptionFilter != None:
			return {"vnfInstanceSubscriptionFilter":self.vnfInstanceSubscriptionFilter.toDictionary(), "notificationTypes":self.notificationTypes, "indicatorIds":self.indicatorIds}
		else:
			return {"vnfInstanceSubscriptionFilter":self.vnfInstanceSubscriptionFilter, "notificationTypes":self.notificationTypes, "indicatorIds":self.indicatorIds}

	def fromDictionary(self, dictData):

		if dictData["vnfInstanceSubscriptionFilter"] != None:
			self.filter = VnfInstanceSubscriptionFilter().fromDictionary(dictData["vnfInstanceSubscriptionFilter"])
		else:
			self.filter = dictData["vnfInstanceSubscriptionFilter"]
		self.notificationTypes = dictData["notificationTypes"]
		self.indicatorIds = dictData["indicatorIds"]
		return self

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfConfigModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Method implementation)
DESCRIPTION: This class represents request parameters for
			 the "Set Configuration" operation.
'''
class VnfConfigModifications:
	vnfConfigurationData = None 			#VnfConfigurationData (Class), optional (0..1)
	vnfcConfigurationData = [] 				#VnfcConfigurationData (Class), optinal (0..N)
	vnfcConfigurationDataDeleteIds = []		#Identifier (String), optinal (0..N)

	def validate(self):

		if self.vnfConfigurationData != None:
			if type(self.vnfConfigurationData) != VnfConfigurationData:
				return ("0", -1)
			confValidation = self.vnfConfigurationData.validate()
			if confValidation[1] != 0:
				return ("0." + confValidation[0], confValidation[1])

		if type(self.vnfcConfigurationData) != list:
			return ("1", -1)
		for index in range(len(self.vnfcConfigurationData)):
			if type(self.vnfcConfigurationData[index]) != VnfcConfigurationData:
				return ("1." + str(index), -1)

			confValidation = self.vnfcConfigurationData[index].validate()
			if confValidation[1] != 0:
				return ("1." + str(index) + "." + confValidation[0], confValidation[1])

		if type(self.vnfcConfigurationDataDeleteIds) != list:
			return ("2", -1)
		for index in range(len(self.vnfcConfigurationDataDeleteIds)):
			if type(self.vnfcConfigurationDataDeleteIds[index]) != str:
				return ("2." + str(index), -1)

		return ("3", 0)

	def fromData(self, vnfConfigurationData, vnfcConfigurationData, vnfcConfigurationDataDeleteIds):
		
		self.vnfConfigurationData = vnfConfigurationData
		self.vnfcConfigurationData = vnfcConfigurationData
		self.vnfcConfigurationDataDeleteIds = vnfcConfigurationDataDeleteIds

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		if self.vnfConfigurationData != None:
			return {"vnfConfigurationData":self.vnfConfigurationData.toDictionary(), "vnfcConfigurationData":[vcd.toDictionary() for vcd in self.vnfcConfigurationData], "vnfcConfigurationDataDeleteIds":self.vnfcConfigurationDataDeleteIds}
		else:
			return {"vnfConfigurationData":self.vnfConfigurationData, "vnfcConfigurationData":[vcd.toDictionary() for vcd in self.vnfcConfigurationData], "vnfcConfigurationDataDeleteIds":self.vnfcConfigurationDataDeleteIds}

	def fromDictionary(self, dictData):
		
		if dictData["vnfConfigurationData"] != None:
			self.vnfConfigurationData = VnfConfigurationData.fromDictionary(dictData["vnfConfigurationData"])
		else:
			self.vnfConfigurationData = dictData["vnfConfigurationData"]
		self.vnfcConfigurationData = [VnfcConfigurationData.fromDictionary(vcd) for vcd in dictData["vnfConfigurationData"]]
		self.vnfcConfigurationDataDeleteIds = dictData["vnfConfigurationData"]
		return self

'''
CLASS: VnfConfiguration
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Methods implementation)
DESCRIPTION: This class represents configuration parameters
			 of a VNF instance and its VNFC instances.
'''
class VnfConfiguration:
	vnfConfigurationData = None 			#VnfConfigurationData, mandatory (1)
	vnfcConfigurationData = [] 				#VnfcConfigurationData, optional (0..N)

	def validate(self):
		
		if type(self.vnfConfigurationData) != VnfConfigurationData:
			return ("0", -1)
		confValidation = self.vnfConfigurationData.validate()
		if confValidation[1] != 0:
			return ("0." + confValidation[0], confValidation[1])

		if type(self.vnfcConfigurationData) != list:
			return ("1", -1)
		for index in range(len(self.vnfcConfigurationData)):
			if type(self.vnfcConfigurationData[index]) != VnfcConfigurationData:
				return ("1." + str(index), -1)

			confValidation = self.vnfcConfigurationData[index].validate()
			if confValidation[1] != 0:
				return ("1." + str(index) + "." + confValidation[0], confValidation[1])

		return ("2", 0)

	def fromData(self, vnfConfigurationData, vnfcConfigurationData):
		
		self.vnfConfigurationData = vnfConfigurationData
		self.vnfcConfigurationData = vnfcConfigurationData

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		
		return {"vnfConfigurationData":self.vnfConfigurationData.toDictionary(), "vnfcConfigurationData":[vcd.toDictionary() for vcd in self.vnfcConfigurationData]}

	def fromDictionary(self, dictData):
		
		self.vnfConfigurationData = VnfConfigurationData.fromDictionary(dictData["vnfConfigurationData"])
		self.vnfcConfigurationData = [VnfcConfigurationData.fromDictionary(vcd) for vcd in dictData["vnfConfigurationData"]]
		return self

'''
CLASS: VnfConfigurationData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Method implementation)
DESCRIPTION: This class represents configuration parameters
			 of a VNF instance.
'''
class VnfConfigurationData:
	extCpConfig = [] 						#CpConfiguration (Class), optional (0..N)
	dhcpServer = None 						#IpAddress (String), optional (0..1)
	vnfSpecificData = None 					#KeyValuePairs (Dictionary), optional (0..1)

	def validate(self):
		
		if type(self.extCpConfig) != list:
			return ("0", -1)
		for index in range(len(self.extCpConfig)):
			if type(self.extCpConfig[index]) != CpConfiguration:
				return ("0." + str(index), -1)

			confValidation = self.extCpConfig[index].validate()
			if confValidation[1] != 0:
				return ("0." + str(index) + "." + confValidation[0], confValidation[1])

		if self.dhcpServer != None:
			if type(self.dhcpServer) != str:
				return ("1", -1)

		if self.vnfSpecificData != None:
			if type(self.vnfSpecificData) != dict:
				return ("2", -1)

		return ("3", 0)

	def fromData(self, extCpConfig, dhcpServer, vnfSpecificData):
		
		self.extCpConfig = extCpConfig
		self.dhcpServer = dhcpServer
		self.vnfSpecificData = vnfSpecificData

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		
		return {"extCpConfig":[ecc.toDictionary() for ecc in self.extCpConfig], "dhcpServer":self.dhcpServer, "vnfSpecificData":self.vnfSpecificData}

	def fromDictionary(self, dictData):
		
		self.extCpConfig = [CpConfiguration().fromDictionary(ecc) for ecc in dictData["extCpConfig"]]
		self.dhcpServer = dictData["dhcpServer"]
		self.vnfSpecificData = dictData["vnfSpecificData"]
		return self

'''
CLASS: VnfcConfigurationData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Method implementation)
DESCRIPTION: This class represents configuration parameters
			 of a VNFC instance.
'''
class VnfcConfigurationData:
	vnfcInstanceId = None 					#IdentifierInVnf (String), mandatory (1)
	intCpConfig = [] 						#CpConfiguration (Class), optional (0..N)
	dhcpServer = None 						#IpAddress (String), optional (0..1)
	vnfcSpecificData = None 				#KeyValuePairs (Dictionary), optional (0..1)

	def validate(self):

		if type(self.vnfcInstanceId) != str:
			return ("0", -1)

		if type(self.intCpConfig) != list:
			return ("1", -1)
		for index in range(len(self.intCpConfig)):
			if type(self.intCpConfig[index]) != CpConfiguration:
				return ("1." + str(index), -1)

			confValidation = self.intCpConfig[index].validate()
			if confValidation[1] != 0:
				return ("1." + str(index) + "." + confValidation[0], confValidation[1])

		if self.dhcpServer != None:
			if type(self.dhcpServer) != str:
				return ("2", -1)

		if self.vnfcSpecificData != None:
			if type(self.vnfcSpecificData) != dict:
				return ("3", -1)

		return ("4", 0)

	def fromData(self, vnfcInstanceId, intCpConfig, dhcpServer, vnfcSpecificData):
		
		self.vnfcInstanceId = vnfcInstanceId
		self.intCpConfig = intCpConfig
		self.dhcpServer = dhcpServer
		self.vnfcSpecificData = vnfcSpecificData

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		
		return {"vnfcInstanceId":self.vnfcInstanceId, "intCpConfig":[icc.toDictionary() for icc in self.intCpConfig], "dhcpServer":self.dhcpServer, "vnfcSpecificData":self.vnfcSpecificData}

	def fromDictionary(self, dictData):
		
		self.vnfcInstanceId = dictData["vnfcInstanceId"]
		self.extCpConfig = [CpConfiguration().fromDictionary(icc) for icc in dictData["intCpConfig"]]
		self.dhcpServer = dictData["dhcpServer"]
		self.vnfcSpecificData = dictData["vnfcSpecificData"]
		return self

'''
CLASS: CpConfiguration
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Method implementation)
DESCRIPTION: This class represents configuration parameters
			of a CP instance.
'''
class CpConfiguration:
	cpId = None 							#IdentifierInVnf (String), mandatory (1)
	cpdId = None 							#IdentifierInVnfd (String), mandatory (1)
	addresses = []							#CpAddress (Class), mandatory (1..N)

	def validate(self):

		if type(self.cpId) != str:
			return ("0", -1)

		if type(self.cpdId) != str:
			return ("1", -1)

		if type(self.addresses) != list:
			return ("2", -1)
		if len(self.addresses) == 0:
			return ("2", -2)
		for index in range(len(self.addresses)):
			if type(self.addresses[index]) != CpAddress:
				return ("2." + str(index), -1)

			confValidation = self.addresses[index].validate()
			if confValidation[1] != 0:
				return ("2." + str(index) + "." + confValidation[0], confValidation[1])

	def fromData(self, cpId, cpdId, addresses):
		
		self.cpId = cpId
		self.cpdId = cpdId
		self.addresses = addresses

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		
		return {"cpId":self.cpId, "cpdId":self.cpdId, "addresses":[a.toDictionary() for a in self.addresses]}

	def fromDictionary(self, dictData):
		
		self.cpId = dictData["cpId"]
		self.cpdId = dictData["cpdId"]
		self.addresses = [CpAddress().fromData(a) for a in dictData["addresses"]]
		return self

'''
CLASS: CpAddress
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Method implementation)
DESCRIPTION: This class represents configuration parameters
			 of a CP instance address.
'''
class CpAddress:
	address = None 							#Structure (Dictionary), optional (0..1)
	useDynamicAddress = None 				#Boolean, optional (0..1)
	port = None								#Unsigned integer, optional (0..1)

	def addressStruct(self):
		return {"macAddress":None, 			#MacAddress (String), optional (0..1)
				"ipAddress":None}			#IpAddress (String), optional (0..1)

	def validate(self):
		
		if self.address != None:
			if type(self.address) != dict:
				return ("0", -1)

			keyList = ["macAddress", "ipAddress"]
			for key in self.address:
				if not type(key) == str:
					return ("0." + str(key), -1)
				if not key in keyList:
					return ("0." + str(key), -3)
				keyList.remove(key)

			if not "macAddress" in keyList:
				if not self.address["macAddress"] == str:
					return ("0.macAddress", -1)
			if not "ipAddress" in keyList:
				if not self.address["ipAddress"] == str:
					return ("0.ipAddress", -1)

		if self.useDynamicAddress != None:
			if type(self.useDynamicAddress) != bool:
				return ("1", -1)

		if self.port != None:
			if type(self.port) != int:
				return ("2", -1)
			if self.port < 0:
				return ("2", -1)

	def fromData(self, address, useDynamicAddress, port):
		
		self.address = address
		self.useDynamicAddress = useDynamicAddress
		self.port = port

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		
		return {"address":self.address, "useDynamicAddress":self.useDynamicAddress, "port":self.port}

	def fromDictionary(self, dictData):
		
		self.address = dictData["address"]
		self.useDynamicAddress = dictData["useDynamicAddress"]
		self.port = dictData["port"]
		return self
