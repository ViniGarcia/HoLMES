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
			 describes an VNF package changing request of a
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
			 describes an VNF package changing request of a
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
