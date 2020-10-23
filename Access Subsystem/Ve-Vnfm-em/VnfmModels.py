import enum

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
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes information about an snapshot of a VN-
			 FC of a VNF instance in the Ve-Vnfm-em
			 reference point.
'''
class VnfcSnapshotInfo:
	id = ""														#String, mandatory (1)
	vnfcInstanceId = ""											#String, mandatory (1)
	creationStartedAt = ""										#String, mandatory (1)
	creationFinishedAt = ""										#String, optional (0..1)
	vnfcResourceInfoId = ""										#String, mandatory (1)
	computeSnapshotResource = ""								#String, optional (0..1)
	storageSnapshotResources = [{								#Dictionary, optional (0..N)
								"storageResourceId":"",				#String, mandatory (1)
								"storageSnapshotResource":"",		#String, optional (0..1)
								"userDefinedData":{}				#String, optional (0..1)
								}]

'''
CLASS: ModificationsTriggeredByVnfPkgChange
AUTHOR: Vinicius Fulber-Garcia
CREATION: 23 Oct. 2020
L. UPDATE: 23 Oct. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the reference structure that
			 describes the modification of an entry in an
			 VNF instance when a previous modification occur
			 in its VNF package in the Ve-Vnfm-em reference
			 point.
'''
class ModificationsTriggeredByVnfPkgChange:
	vnfConfigurableProperties = {}		#Dictionary, optional (0..1)
	metadata = {}						#Dictionary, optional (0..1)
	extensions = {}						#Dictionary, optional (0..1)
	vnfdId = ""							#String, optional (0..1)
	vnfProvider = ""					#String, optional (0..1)
	vnfProductName = ""					#String, optional (0..1)
	vnfSoftwareVersion = ""				#String, optional (0..1)
	vnfdVersion = ""					#String, optional (0..1)

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