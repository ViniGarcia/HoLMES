import enum

'''
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
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
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

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfInstance
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF instance in the Ve-Vnfm-em re-
			 ference point.
'''
class VnfInstance:
	id = ""														#String, mandatory (1)
	vnfInstanceName = ""										#String, optional (0..1)
	vnfInstanceDescription = ""									#String, optional (0..1)
	vnfdId = ""													#String, mandatory (1)
	vnfProvider = ""											#String, mandatory (1)
	vnfProductName = ""											#String, mandatory (1)
	vnfSoftwareVersion = ""										#String, mandatory (1)
	vnfdVersion = ""											#String, mandatory (1)
	vnfConfigurableProperties = {}								#Dictionary, optinal (0..1)
	instantiationState = ""										#String (NOT_INSTANTIATED | NSTANTIATED), madatory (1)
	instantiatedVnfInfo = {										#Dictionary, optinal (0..1)
						   "flavourId":"",							#String, mandatory (1)
						   "vnfState":"",							#String, mandatory (1)
						   "scaleStatus":[],						#String, optinal (0..N)
						   "maxScaleLevels":[],						#String, optinal (0..N)
						   "extCpInfo":[],							#String, mandatory (1..N)
						   "extVirtualLinkInfo":[],					#String, optinal (0..N)
						   "extManagedVirtualLinkInfo":[],			#String, optinal (0..N)
						   "monitoringParameters":[],				#String, optinal (0..N)
						   "localizationLanguage":"",				#String, optinal (0..1)
						   "vnfcResourceInfo":[],					#String, optinal (0..N)
						   "vnfVirtualLinkResourceInfo":[],			#String, optinal (0..N)
						   "virtualStorageResourceInfo":[],			#String, optinal (0..N)
						   "vnfcInfo":[]							#String, optinal (0..N)							
						  }							
	metadata = {}												#Dictionary, optinal (0..1)
	extensions = {}												#Dictionary, optinal (0..1)
	links = {													#Dictionary, mandatory (1)
			 "self":"",												#String, mandatory (1)
			 "indicators":"",										#String, optinal (0..1)
			 "instantiate":"",										#String, optinal (0..1)
			 "terminate":"",										#String, optinal (0..1)
			 "scale":"",											#String, optinal (0..1)
			 "scaleToLevel":"",										#String, optinal (0..1)
			 "changeFlavour":"",									#String, optinal (0..1)
			 "heal":"",												#String, optinal (0..1)
			 "operate":"",											#String, optinal (0..1)
			 "changeExtConn":"",									#String, optinal (0..1)
			 "createSnapshot":"",									#String, optinal (0..1)
			 "revertToSnapshot":""									#String, optinal (0..1)
			}

'''
CLASS: CreateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a creation request of a VNF instance
			 in the Ve-Vnfm-em reference point.
'''
class CreateVnfRequest:
	vnfdId = ""						#String, mandatory (1)
	vnfInstanceName = ""			#String, optional (0..1)
	vnfInstanceDescription = ""		#String, optional (0..1)
	metadata = {}					#Dictionary, optinal (0..1)

'''
CLASS: InstantiateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an instantiation request of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class InstantiateVnfRequest:
	flavourId = ""					#String, mandatory (1)
	instantiationLevelId = ""		#String, optional (0..1)
	extVirtualLinks = []			#String, optinal (0..N)
	extManagedVirtualLinks = []		#String, optinal (0..N)
	localizationLanguage = ""		#String, optional (0..1)
	extensions = {}					#Dictionary, optinal (0..1)
	additionalParams = {}			#Dictionary, optinal (0..1)
	vnfConfigurableProperties = {}	#Dictionary, optinal (0..1)

'''
CLASS: ScaleVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a resource scaling request of a VNF 
			 instance in the Ve-Vnfm-em reference point.
'''
class ScaleVnfRequest:
	type = ""						#String (SCALE_OUT | SCALE_IN), madatory (1)
	aspectId = ""					#String, mandatory (1)
	numberOfSteps = 0				#Integer, optional (0..1)
	additionalParams = {}			#Dictionary, optinal (0..1)

'''
CLASS: ScaleVnfToLevelRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a level scaling request of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class ScaleVnfToLevelRequest:
	instantiationLevelId = "" 		#Integer, optional (0..1)
	scaleInfo = []					#String, optinal (0..N)
	additionalParams = {}			#Dictionary, optinal (0..1)

'''
CLASS: ChangeVnfFlavourRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a changing flavour request of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class ChangeVnfFlavourRequest:
	newFlavourId = ""				#String, mandatory (1)
	instantiationLevelId = ""		#String, optional (0..1)
	extVirtualLinks = []			#String, optinal (0..N)
	extManagedVirtualLinks = []		#String, optinal (0..N)
	additionalParams = {}			#Dictionary, optinal (0..1)
	extensions = {}					#Dictionary, optinal (0..1)
	vnfConfigurableProperties = {}	#Dictionary, optinal (0..1)

'''
CLASS: TerminateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a termination request of a VNF instan-
			 ce in the Ve-Vnfm-em reference point.
'''
class TerminateVnfRequest:
	terminationType = ""			#String (FORCEFUL | GRACEFUL), madatory (1)
	gracefulTerminationTimeout = 0	#Integer, optional (0..1)
	additionalParams = {}			#Dictionary, optinal (0..1)

'''
CLASS: HealVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a healing request of a VNF instance
			 in the Ve-Vnfm-em reference point.
'''
class HealVnfRequest:
	vnfcInstanceId = []				#String, optinal (0..N)
	cause = ""						#Dictionary, optinal (0..1)
	additionalParams = {}			#Dictionary, optinal (0..1)
	healScript = ""					#String, optional (0..1)

'''
CLASS: OperateVnfRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an operation request of a VNF instan-
			 ce in the Ve-Vnfm-em reference point.
'''
class OperateVnfRequest:
	vnfcInstanceId = []				#String, optinal (0..N)
	changeStateTo = ""				#String, optinal (0..N)
	stopType = ""					#String (FORCEFUL | GRACEFUL), optional (0..1)
	gracefulStopTimeout = 0			#Integer, optional (0..1)
	additionalParams = {}			#Dictionary, optinal (0..1)

'''
CLASS: ChangeExtVnfConnectivityRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an external connectivity changing re-
			 quest of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ChangeExtVnfConnectivityRequest:
	extVirtualLinks = []			#String, mandatory (1..N)
	additionalParams = {}			#Dictionary, optinal (0..1)

'''
CLASS: ChangeCurrentVnfPkgRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF package changing request of a
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class ChangeCurrentVnfPkgRequest:
	vnfdId = ""						#String, mandatory (1)
	extVirtualLinks = []			#String, optional (0..N)
	extManagedVirtualLinks = []		#String, optional (0..N)
	additionalParams = {}			#Dictionary, optinal (0..1)
	extensions = {}					#Dictionary, optinal (0..1)
	vnfConfigurableProperties = {}	#Dictionary, optinal (0..1)

'''
CLASS: VnfInfoModificationRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 22 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF package changing request of a
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfInfoModificationRequest:
	vnfInstanceName = ""			#String, optional (0..1)
	vnfInstanceDescription = ""		#String, optional (0..1)
	vnfdId = ""						#String, optional (0..1)
	vnfConfigurableProperties = {}	#Dictionary, optinal (0..1)
	metadata = {}					#Dictionary, optinal (0..1)
	extensions = {}					#Dictionary, optinal (0..1)
	vnfcInfoModifications = []		#String, optional (0..N)

'''
CLASS: VnfInfoModificationRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF information changing request of 
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfInfoModificationRequest:
	vnfInstanceName = ""			#String, optional (0..1)
	vnfInstanceDescription = ""		#String, optional (0..1)
	vnfConfigurableProperties = {}	#Dictionary, optinal (0..1)
	metadata = {}					#Dictionary, optinal (0..1)
	extensions = {}					#Dictionary, optinal (0..1)
	vnfdId = ""						#String, optional (0..1)
	vnfProvider = ""				#String, optional (0..1)
	vnfProductName = ""				#String, optional (0..1)
	vnfSoftwareVersion = ""			#String, optional (0..1)
	vnfdVersion = ""				#String, optional (0..1)
	vnfcInfoModifications = []		#String, optional (0..N)

'''
CLASS: VnfLcmOpOcc
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF LCM operation occurence of a 
			 VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfLcmOpOcc:
	id = ""											#String, mandatory (1)
	operationState = ""								#String, mandatory (1)
	stateEnteredTime = ""							#String, mandatory (1)
	startTime = ""									#String, mandatory (1)
	vnfInstanceId = ""								#String, mandatory (1)
	grantId = ""									#String, optional (0..1)
	operation = ""									#String, mandatory (1)
	isAutomaticInvocation = False					#Boolean, mandatory (1)
	operationParams = []							#String, optional (0..N)
	isCancelPending = False							#Boolean, mandatory (1)
	cancelMode = ""									#String, optional (0..1)
	error = ""										#String, optional (0..1)
	resourceChanges = {								#Dictionary, optinal (0..N)
						"affectedVnfcs":[],				#String, optional (0..N)
						"affectedVirtualLinks":[],		#String, optional (0..N)
						"affectedExtLinkPorts":[],		#String, optional (0..N)
						"affectedVirtualStorages":[],	#String, optional (0..N)
					  }
	changedInfo = ""								#String, optional (0..1)
	changedExtConnectivity = []						#String, optional (0..N)
	modificationsTriggeredByVnfPkgChange = ""		#String, optional (0..1)
	vnfSnapshotInfoId = ""							#String, optional (0..1)
	links = {										#Dictionary, mandatory (1)
				"self":"",								#String, mandatory (1)
				"vnfInstance":"",						#String, mandatory (1)
				"grant":"",								#String, optional (0..1)
				"cancel":"",							#String, optional (0..1)
				"retry":"",								#String, optional (0..1)
				"rollback":"",							#String, optional (0..1)
				"fail":"",								#String, optional (0..1)
				"vnfSnapshot":""						#String, optional (0..1)
			}

'''
CLASS: CancelMode
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a cancel mode selection of an opera-
			 tion of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class CancelMode:
	cancelMode = ""				#String, mandatory (1)

'''
CLASS: LccnSubscriptionRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a LCN subscription request of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class LccnSubscriptionRequest:
	id = ""						#String, mandatory (1)
	filter = ""					#String, optional (0..1)
	callbackUri = ""			#String, mandatory (1)
	verbosity = ""				#String, mandatory (1)
	links = {					#Dictionary, mandatory (1)
		"self":""					#String, mandatory (1)
	}

'''
CLASS: VnfLcmOperationOccurrenceNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a LCN occurence notification of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfLcmOperationOccurrenceNotification:
	id = ""										#String, mandatory (1)
	notificationType = ""						#String, mandatory (1)
	subscriptionId = ""							#String, mandatory (1)
	timeStamp = ""								#String, mandatory (1)
	notificationStatus = ""						#String (START | RESULT), mandatory (1)
	operationState = ""							#String, mandatory (1)
	vnfInstanceId = ""							#String, mandatory (1)
	operation = ""								#String, mandatory (1)
	isAutomaticInvocation = ""					#String, mandatory (1)
	verbosity = ""								#String, optional (0..1)
	vnfLcmOpOccId = ""							#String, mandatory (1)
	affectedVnfcs = []							#String, optional (0..N)
	affectedVirtualLinks = []					#String, optional (0..N)
	affectedExtLinkPorts = []					#String, optional (0..N)
	affectedVirtualStorages = []				#String, optional (0..N)
	changedInfo = ""							#String, optional (0..1)
	changedExtConnectivity = []					#String, optional (0..N)
	modificationsTriggeredByVnfPkgChange = ""	#String, optional (0..1)
	error = ""									#String, optional (0..1)
	_links = ""									#String, mandatory (1)

'''
CLASS: VnfIdentifierCreationNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a creation operation notification of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfIdentifierCreationNotification:
	id = ""						#String, mandatory (1)
	notificationType = ""		#String, mandatory (1)
	subscriptionId = ""			#String, mandatory (1)
	timeStamp = ""				#String, mandatory (1)
	vnfInstanceId = ""			#String, mandatory (1)
	links = ""					#String, mandatory (1)

'''
CLASS: VnfIdentifierDeletionNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a deletion operation notification of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfIdentifierDeletionNotification:
	id = ""						#String, mandatory (1)
	notificationType = ""		#String, mandatory (1)
	subscriptionId = ""			#String, mandatory (1)
	timeStamp = ""				#String, mandatory (1)
	vnfInstanceId = ""			#String, mandatory (1)
	links = ""					#String, mandatory (1)

'''
CLASS: CreateVnfSnapshotInfoRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a snapshot information operation no-
			 tification of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class CreateVnfSnapshotInfoRequest:
	vnfSnapshotPkgId = ""		#String, optional (0..1)

'''
CLASS: CreateVnfSnapshotRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a snapshot creation notification of
			 a VNF instance in the Ve-Vnfm-em reference po-
			 int.
'''
class CreateVnfSnapshotRequest:
	vnfSnapshotInfoId = ""		#String, mandatory (1)
	vnfcInstanceId = ""			#String, optional (0..1)
	additionalParams = {}		#Dictionary, optional (0..1)
	userDefinedData = {}		#Dictionary, optional (0..1)

'''
CLASS: VnfSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a individual VNF snapshot of a VNF 
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfSnapshotInfo:
	id = ""						#String, mandatory (1)
	vnfSnapshotPkgId = ""		#String, optional (0..1)
	vnfSnapshot = ""			#String, optional (0..1)
	links = {					#Dictionary, mandatory (1)
				"self":"",			#String, mandatory (1)
				"takenFrom":""		#String, optional (0..1)
			}

'''
CLASS: VnfSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a VNF snapshot of a VNF instance in
			 the Ve-Vnfm-em reference point.
'''
class VnfSnapshot:
	id = ""						#String, mandatory (1)
	vnfInstanceId = ""			#String, mandatory (1)
	creationStartedAt = ""		#String, mandatory (1)
	creationFinishedAt = ""		#String, optional (0..1)
	vnfdId = ""					#String, mandatory (1)
	vnfInstance = ""			#String, mandatory (1)
	vnfcSnapshots = []			#String, mandatory (1..N)
	userDefinedData = {}		#Dictionary, optional (0..1)
	links = {					#Dictionary, mandatory (1)
		"self":""					#String, mandatory (1)
	}

'''
CLASS: RevertToVnfSnapshotRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a revertion to a snapshot request of
			 a VNF instance in the Ve-Vnfm-em reference po-
			 int.
'''
class RevertToVnfSnapshotRequest:
	vnfSnapshotInfoId = ""		#String, optional (0..1)
	vnfcInstanceId = ""			#String, optional (0..1)
	vnfcSnapshotInfoId = ""		#String, optional (0..1)
	additionalParams = {}		#Dictionary, optional (0..1)

#######################################################################################################
#######################################################################################################

'''
CLASS: ExtVirtualLinkData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a external virtual link of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class ExtVirtualLinkData:
	id = ""						#String, mandatory (1)
	vimConnectionId = ""		#String, optional (0..1)
	resourceProviderId = ""		#String, optional (0..1)
	resourceId = ""				#String, mandatory (1)
	extCps = []					#String, mandatory (1..N)
	extLinkPorts = []			#String, optional (0..1)

'''
CLASS: ExtVirtualLinkInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an external virtual
			 link of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ExtVirtualLinkInfo:
	id = ""						#String, mandatory (1)
	resourceHandle = ""			#String, mandatory (1)
	extLinkPorts = []			#String, optional (0..N)
	currentVnfExtCpData = []	#String, mandatory (1..N)

'''
CLASS: ExtManagedVirtualLinkData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an externally-managed internal virtual
			 link of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class ExtManagedVirtualLinkData:
	id = ""						#String, mandatory (1)
	vnfVirtualLinkDescId = ""	#String, mandatory (1)
	vimConnectionId = ""		#String, optional (0..1)
	resourceProviderId = ""		#String, optional (0..1)
	resourceId = ""				#String, mandatory (1)

'''
CLASS: ExtManagedVirtualLinkInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about externally-managed
			 internal virtual link of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class ExtManagedVirtualLinkInfo:
	id = ""						#String, mandatory (1)
	vnfVirtualLinkDescId = ""	#String, mandatory (1)
	vnfdId = ""					#String, optional (0..1)
	networkResource = ""		#String, mandatory (1)
	vnfLinkPorts = []			#String, optional (0..N)

'''
CLASS: VnfExtCpData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes external connection points of a VNF
			 instance in the Ve-Vnfm-em reference point.
'''
class VnfExtCpData:
	cpdId = ""					#String, mandatory (1)
	cpConfig = []				#String, mandatory (1..N)

'''
CLASS: VnfExtCpConfig
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes the configuration of an external co-
			 nnection point of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfExtCpConfig:
	parentCpConfigId = ""		#String, optional (0..1)
	linkPortId = ""				#String, optional (0..1)
	cpProtocolData = []			#String, optional (0..N)

'''
CLASS: CpProtocolData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes network protocols data of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class CpProtocolData:
	layerProtocol = ""			#String (P_OVER_ETHERNET), mandatory (1)
	ipOverEthernet = ""			#String, optional (0..1)

'''
CLASS: IpOverEthernetAddressData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an IP over ethernet internet address 
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class IpOverEthernetAddressData:
	macAddress = ""									#String, optional (0..1)
	segmentationId = ""								#String, optional (0..1)
	ipAddresses = [{								#Dictionary, optional (0..N)
					"type":"",							#String (IPV4 | IPV6), mandatory (1)
					"fixedAddresses":[],				#String, optional (0..N)
					"numDynamicAddresses":0,			#Integer, optional (0..1)
					"addressRange":{					#Dictionary, optional (0..1)	
									"minAddress":"",		#String, mandatory (1)
									"maxAddress":""			#String, mandatory (1)
								   },
					"subnetId":""						#String, optional (0..1)
				  }]

'''
CLASS: ScaleInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about scaling operations
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class ScaleInfo:
	aspectId = ""				#String, mandatory (1)
	vnfdId = ""					#String, optional (0..1)
	scaleLevel = 0				#Integer, mandatory (1)

'''
CLASS: VnfcResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized compute
			 and storage resources of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class VnfcResourceInfo:
	id = ""								#String, mandatory (1)
	vduId = ""							#String, mandatory (1)
	vnfdId = ""							#String, optional (0..1)
	computeResource = ""				#String, mandatory (1)
	storageResourceIds = []				#String, optional (0..N)
	reservationId = ""					#String, optional (0..N)
	vnfcCpInfo = [{						#Dictionary, optional (0..N)
					"id":"",				#String, mandatory (1)
					"cpdId":"",				#String, mandatory (1)
					"vnfExtCpId":"",		#String, optional (0..1)
					"cpProtocolInfo":[],	#String, optional (0..N)
					"vnfLinkPortId":"",		#String, optional (0..1)
					"metadata":{}			#Dictionary, optional (0..1)
				 }]
	metadata = {}							#Dictionary, optional (0..1)

'''
CLASS: VnfVirtualLinkResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized link
			 resources of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfVirtualLinkResourceInfo:
	id = ""						#String, mandatory (1)
	vnfVirtualLinkDescId = ""	#String, mandatory (1)
	vnfdId = ""					#String, optional (0..1)
	networkResource = ""		#String, mandatory (1)
	reservationId = ""			#String, optional (0..1)
	vnfLinkPorts = []			#String, optional (0..N)
	metadata = {}				#Dictionary, optional (0..1)

'''
CLASS: VirtualStorageResourceInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about virtualized storage
			 resources of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VirtualStorageResourceInfo:
	id = ""						#String, mandatory (1)
	virtualStorageDescId = ""	#String, mandatory (1)
	vnfdId = ""					#String, optional (0..1)
	storageResource = ""		#String, mandatory (1)
	reservationId = ""			#String, optional (0..1)
	metadata = {}				#Dictionary, optional (0..1)

'''
CLASS: VnfLinkPortInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about ports of internal
			 virtual links of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfLinkPortInfo:
	id = ""						#String, mandatory (1)
	resourceHandle = ""			#String, mandatory (1)
	cpInstanceId = ""			#String, optional (0..1)
	cpInstanceType = ""			#String (VNFC_CP | EXT_CP), optional (0..1)

'''
CLASS: ExtLinkPortInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about link ports of ext-
			 ernal virtual links of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class VnfLinkPortInfo:
	id = ""						#String, mandatory (1)
	resourceHandle = ""			#String, mandatory (1)
	cpInstanceId = ""			#String, optional (0..1)

'''
CLASS: ExtLinkPortData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a link ports of external virtual li-
			 nks of a VNF instance in the Ve-Vnfm-em refe-
			 rence point.
'''
class VnfLinkPortInfo:
	id = ""						#String, mandatory (1)
	resourceHandle = ""			#String, mandatory (1)

'''
CLASS: ResourceHandle
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a particular computational resource 
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class ResourceHandle:
	vimConnectionId = ""		#String, optional (0..1)
	resourceProviderId = ""		#String, optional (0..1)
	resourceId = ""				#String, mandatory (1)
	vimLevelResourceType = ""	#String, optional (0..1)

'''
CLASS: CpProtocolInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about the protocol layers
			 of a CP of a VNF instance in the Ve-Vnfm-em re-
			 ference point.
'''
class CpProtocolInfo:
	layerProtocol = ""			#String (IP_OVER_ETHERNET), mandatory (1)
	ipOverEthernet = ""			#String, optional (0..1)

'''
CLASS: IpOverEthernetAddressInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about the network address
			 of a VNF instance in the Ve-Vnfm-em reference
			 point.
'''
class IpOverEthernetAddressInfo:
	macAddress = ""									#String, optional (0..1)
	segmentationId = ""								#String, optional (0..1)
	ipAddresses = [{								#Dictionary, optional (0..N)
					"type":"",							#String (IPV4 | IPV6), mandatory (1)
					"addresses":[],						#String, optional (0..N)
					"isDynamic":False,					#Boolean, optional (0..1)
					"addressRange":{					#Dictionary, optional (0..1)
									"minAddress":"",		#String, optional (0..1)
									"maxAddress":""			#String, optional (0..1)
									},
					"subnetId":""						#String, optional (0..1)
				  }]

'''
CLASS: MonitoringParameter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a monitoring parameter of a VNF ins-
			 tance in the Ve-Vnfm-em reference point.
'''
class MonitoringParameter:
	id = ""						#String, mandatory (1)
	vnfdId = ""					#String, optional (0..1)
	name = ""					#String, optional (0..1)
	performanceMetric = ""		#String, mandatory (1)

'''
CLASS: LifecycleChangeNotificationsFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a subscription filter of notifications
			 related lifecycle changes of a VNF instance in
			 the Ve-Vnfm-em reference point.
'''
class LifecycleChangeNotificationsFilter:
	vnfInstanceSubscriptionFilter = ""		#String, optional (0..1)
	notificationTypes = []					#String (VnfLcmOperationOccurrenceNotification | VnfIdentifierCreationNotification | VnfIdentifierDeletionNotification), optional (0..1)
	operationTypes = []						#String, optional (0..N)
	operationStates = []					#String, optional (0..N)

'''
CLASS: AffectedVnfc
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a VNFC of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class AffectedVnfc:
	id = ""							#String, mandatory (1)
	vduId = ""						#String, mandatory (1)
	vnfdId = ""						#String, optional (0..1)
	changeType = ""					#String (ADDED | REMOVED | MODIFIED | TEMPORARY), mandatory (1)
	computeResource = ""			#String, mandatory (1)
	metadata = {}					#Dictionary, optional (0..1)
	affectedVnfcCpIds = []			#String, optional (0..N)
	addedStorageResourceIds = []	#String, optional (0..N)
	removedStorageResourceIds = []	#String, optional (0..N)

'''
CLASS: AffectedVirtualLink
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a virtual link of a VNF instance in the Ve-
			 Vnfm-em reference point.
'''
class AffectedVirtualLink:
	id = ""							#String, mandatory (1)
	vnfVirtualLinkDescId = ""		#String, mandatory (1)
	vnfdId = ""						#String, optional (0..1)
	changeType = ""					#String (ADDED | REMOVED | MODIFIED | TEMPORARY | LINK_PORT_ADDED | LINK_PORT_REMOVED), mandatory (1)
	networkResource = ""			#String, mandatory (1)
	vnfLinkPortIds = []				#String, optional (0..N)
	metadata = {}					#Dictionary, optional (0..1)

'''
CLASS: AffectedExtLinkPort
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition or remotion of an external
			 link port of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class AffectedVirtualLink:
	id = ""							#String, mandatory (1)
	changeType = ""					#String (ADDED | REMOVED), mandatory (1)
	extCpInstanceId = ""			#String, mandatory (1)
	resourceHandle = ""				#String, mandatory (1)

'''
CLASS: AffectedVirtualStorage
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes an adition, remotion, or modification 
			 of a virtual storage of a VNF instance in the
			 Ve-Vnfm-em reference point.
'''
class AffectedVirtualStorage:
	id = ""							#String, mandatory (1)
	virtualStorageDescId = ""		#String, mandatory (1)
	vnfdId = ""						#String, optional (0..1)
	changeType = ""					#String (ADDED | REMOVED | MODIFIED | TEMPORARY), mandatory (1)
	storageResource = ""			#String, mandatory (1)
	metadata = {}					#Dictionary, optional (0..1)

'''
CLASS: LccnLinks
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes a link to resource that a notificati-
			 on can contain to a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class LccnLinks:
	vnfInstance = ""				#String, mandatory (1)
	subscription = ""				#String, mandatory (1)
	vnfLcmOpOcc = ""				#String, optional (0..1)

'''
CLASS: VnfcInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about a VNFC instance of
			 a VNF instance in the Ve-Vnfm-em reference point.
'''
class VnfcInfo:
	id = ""							#String, mandatory (1)
	vduId = ""						#String, mandatory (1)
	vnfcResourceInfoId = ""			#String, optional (0..1)
	vnfcState = ""					#String (STARTED | STOPPED), mandatory (1)
	vnfcConfigurableProperties = {}	#Dictionary, optional (0..1)

'''
CLASS: VnfcInfoModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes the modification of an entry in an arr-
			 ay of "VnfcInfo" of a VNF instance in the Ve-Vn-
			 fm-em reference point.
'''
class VnfcInfoModifications:
	id = ""								#String, mandatory (1)
	vnfcConfigurableProperties = {}		#Dictionary, mandatory (1)

'''
CLASS: VnfExtCpInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an external connec-
			 tion point of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfExtCpInfo:
	id = ""								#String, mandatory (1)
	cpdId = ""							#String, mandatory (1)
	cpConfigId = ""						#String, mandatory (1)
	vnfdId = ""							#String, optional (0..1)
	cpProtocolInfo = []					#String, mandatory (1..N)
	extLinkPortId = ""					#String, optional (0..1)
	metadata = {}						#Dictionary, optional (0..1)
	associatedVnfcCpId = ""				#String, optional (0..1)
	associatedVnfVirtualLinkId = ""		#String, optional (0..1)

'''
CLASS: VnfcSnapshotInfo
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Validation method)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an snapshot of a VN-
			 FC of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfcSnapshotInfo:
	id = None													#IdentifierLocal (String), mandatory (1)
	vnfcInstanceId = None										#IdentifierInVnf (String), mandatory (1)
	creationStartedAt = None									#DateTime (String), mandatory (1)
	creationFinishedAt = None									#DateTime (String), optional (0..1)
	vnfcResourceInfoId = None									#IdentifierInVnf (String), mandatory (1)
	computeSnapshotResource = None								#ResourceHandle (Class), optional (0..1)
	storageSnapshotResources = []								#Structure (Dictionary), optional (0..N)

	def storageSnapshotResourcesStruct(self):
		return {"storageResourceId":None,						#IdentifierInVnf (String), mandatory (1)
				"storageSnapshotResource":None,					#ResourceHandle (Class), optional (0..1)
				"userDefinedData":{}}							#KeyValuePairs (Dictionary), optional (0..1)

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

			if type(self.storageSnapshotResources[index]["storageResourceId"]) != str:
				return ("6." + str(index) + ".storageResourceId", -1)
			if type(self.storageSnapshotResources[index]["storageSnapshotResource"]) != ResourceHandle and self.storageSnapshotResources[index]["storageSnapshotResource"] != None:
				return ("6." + str(index) + ".storageSnapshotResource", -1)
			if type(self.storageSnapshotResources[index]["userDefinedData"]) != dict:
				return ("6." + str(index) + ".userDefinedData", -1)

			for key in self.storageSnapshotResources[index]["userDefinedData"]:
				if not type(key) == str:
					return ("6." + str(index) + ".userDefinedData." + str(key), -1)

'''
CLASS: ModificationsTriggeredByVnfPkgChange
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Validation method)
DESCRIPTION: Implementation of the reference structure that
			 describes the modification of an entry in an
			 VNF instance when a previous modification occur
			 in its VNF package in the Ve-Vnfm-em reference
			 point.
'''
class ModificationsTriggeredByVnfPkgChange:
	vnfConfigurableProperties = {}		#KeyValuePairs (Dictionary), optional (0..1)
	metadata = {}						#KeyValuePairs (Dictionary), optional (0..1)
	extensions = {}						#KeyValuePairs (Dictionary), optional (0..1)
	vnfdId = None						#Identifier (String), optional (0..1)
	vnfProvider = None					#String, optional (0..1)
	vnfProductName = None				#String, optional (0..1)
	vnfSoftwareVersion = None			#Version (String), optional (0..1)
	vnfdVersion = None					#Version (String), optional (0..1)

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
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
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
	context = {}							#KeyValuePairs (Dictionary), optional (0..1)
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
def CreateThresholdRequest:
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
def Threshold:
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
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class defines the format of a performance report
			 provided by the VNFM to the API consumer as a result of
			 collecting performance information as part of a PM job.
'''
def PerformanceReport:
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
				"context":{}} 				#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: ThresholdModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents modifications to a threshold.
'''
def ThresholdModifications:
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
def PmJobModifications:
	callbackUri = None 						#URI (String), optional (0..1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: PmJobCriteria
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents collection criteria for perfor-
			 mance monitoring jobs.
'''
def PmJobCriteria:
	performanceMetric = []					#String, optional (0..N)
	performanceMetricGroup = []				#String, optional (0..N)
	collectionPeriod = 0					#Unsigned integer, mandatory (1)
	reportingPeriod = 0						#Unsigned integer, mandatory (1)
	reportingBoundary = None 				#DateTime (String), optional (0..1)

'''
CLASS: ThresholdCriteria
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents criteria that define a threshold.
'''
def ThresholdCriteria:
	performanceMetric = None				#String, mandatory (1)
	thresholdType = None 					#String (SIMPLE), mandatory (1)
	simpleThresholdDetails = None 			#Structure (Dictionary), optional (0..1)

	def simpleThresholdDetailsStruct(self):
		return {"thresholdValue":0.0,		#Float, mandatory (1)
				"hysteresis":0.0}			#Float, mandatory (1)

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
def FmSubscriptionRequest:
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
def FmSubscription:
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
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: The alarm class encapsulates information about an alarm.
'''
def Alarm:
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
	isRootCause = False 					#Boolean, mandatory (1)
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
def AlarmNotification:
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
def AlarmClearedNotification:
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
def PerceivedSeverityRequest:
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
def AlarmListRebuiltNotification:
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
def AlarmModifications:
	ackState = None 						#AckState (Enum), mandatory (1)

'''
CLASS: FmNotificationsFilter
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription filter related to notifi-
			 cations about VNF faults.
'''
def FmNotificationsFilter:
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
def FaultyResourceInfo:
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
def VnfIndicator:
	id = None								#Identifier (String), mandatory (1)
	name = None 							#String, optional (0..1)
	value = None 							#String, mandatory (1)
	vnfInstanceId = None 					#Identifier (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"subscription":None, 		#URI (String), mandatory (1)
				"vnfInstance":None}			#URI (String), mandatory (1)

'''
CLASS: VnfIndicatorSubscriptionRequest
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription request
			 related to VNF indicator value change noti-
			 fications.
'''
def VnfIndicatorSubscriptionRequest:
	filter = None 							#VnfIndicatorNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	authentication = None 					#SubscriptionAuthentication (String), optional (0..1)

'''
CLASS: VnfIndicatorSubscription
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription related
			 to notifications about VNF indicator value
			 changes.
'''
def VnfIndicatorSubscription:
	id = None								#Identifier (String), mandatory (1)
	filter = None 							#VnfIndicatorNotificationsFilter (Class), optional (0..1)
	callbackUri = None 						#URI (String), mandatory (1)
	links = None 							#Structure (Dictionary), mandatory (1)

	def linkStruct(self):
		return {"self":None}				#URI (String), mandatory (1)

'''
CLASS: VnfIndicatorValueChangeNotification
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a VNF indicator value
			 change notification.
'''
def VnfIndicatorValueChangeNotification:
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
def SupportedIndicatorsChangeNotification:
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
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents a subscription filter
			 for notifications related to VNF indicators.
'''
def VnfIndicatorNotificationsFilter:
	vnfInstanceSubscriptionFilter = None 	#VnfInstanceSubscriptionFilter (Class), optional (0..1)
	notificationTypes = []					#String (VnfIndicatorValueChangeNotification | SupportedIndicatorsChangeNotification), optional (0..N)
	indicatorIds = []						#IdentifierInVnfd (String), optional (0..N)

#######################################################################################################
#######################################################################################################

'''
CLASS: VnfConfigModifications
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents request parameters for
			 the "Set Configuration" operation.
'''
def VnfConfigModifications:
	vnfConfigurationData = None 			#VnfConfigurationData (Class), optional (0..1)
	vnfcConfigurationData = [] 				#VnfcConfigurationData (Class), optinal (0..N)
	vnfcConfigurationDataDeleteIds = []		#Identifier (String), optinal (0..N)

'''
CLASS: VnfConfiguration
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents configuration parameters
			 of a VNF instance and its VNFC instances.
'''
def VnfConfiguration:
	vnfConfigurationData = None 			#VnfConfigurationData, mandatory (1)
	VnfcConfigurationData = [] 				#VnfcConfigurationData, optional (0..N)

'''
CLASS: VnfConfigurationData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents configuration parameters
			 of a VNF instance.
'''
def VnfConfigurationData:
	extCpConfig = [] 						#CpConfiguration (Class), optional (0..N)
	dhcpServer = None 						#IpAddress (String), optional (0..1)
	vnfSpecificData = {} 					#KeyValuePairs (Dictionary), optional (0..1)


'''
CLASS: VnfcConfigurationData
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents configuration parameters
			 of a VNFC instance.
'''
def VnfcConfigurationData:
	vnfcInstanceId = None 					#IdentifierInVnf (String), mandatory (1)
	intCpConfig = [] 						#CpConfiguration (Class), optional (0..N)
	dhcpServer = None 						#IpAddress (String), optional (0..1)
	vnfcSpecificData = {} 					#KeyValuePairs (Dictionary), optional (0..1)

'''
CLASS: CpConfiguration
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents configuration parameters
			of a CP instance.
'''
def CpConfiguration:
	cpId = None 							#IdentifierInVnf (String), mandatory (1)
	cpdId = None 							#IdentifierInVnfd (String), mandatory (1)
	addresses = []							#CpAddress (Class), mandatory (1..N)

'''
CLASS: CpAddress
AUTHOR: Vinicius Fulber-Garcia
CREATION: 27 Oct. 2020
L. UPDATE: 27 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class represents configuration parameters
			 of a CP instance address.
'''
def CpAddress:
	address = None 							#Structure (Dictionary), optional (0..1)
	useDynamicAddress = False 				#Boolean, optional (0..1)
	port = 0 								#Unsigned integer, optional (0..1)

	def addressStruct(self):
		return {"macAddress":None, 			#MacAddress (String), optional (0..1)
				"ipAddress":None}			#IpAddress (String), optional (0..1)