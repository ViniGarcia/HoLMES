import sys
sys.path.insert(0,'../../VNF Information Base/')
sys.path.insert(0,'../../Access Subsystem/')

import CommunicationModels
import VibTableModels

'''
CLASS: VnfDriverTemplate
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 16 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Template for the implementation of VNF drivers that run in the "VNF Subsystem"inter-
			 nal module. The drivers must inhert this class and overload the functions that return
			 the HTTP code 501 (Not Implemented).
'''
class VnfDriverTemplate:
	className = None

	def __init__(self, className):
		self.className = className

	'''
	PATH: 		 Internal EMS Method
	ACTION: 	 GET
	DESCRIPTION: Query the subsystem for the standard management operations
				 of the VNF platform which the driver is developed for.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + PlatformOperation (Class) [0..N]
	 			 - Integer error code (HTTP)
	'''
	def get_p_operations(self):
		return 501

	'''
	PATH: 		 Internal EMS Method
	ACTION: 	 GET
	DESCRIPTION: Query the subsystem for the standard monitoring operations
				 that return indicators (metrics) values of the VNF platform
				 which the driver is developed for.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + PlatformOperation (Class) [0..N]
	 			 - Integer error code (HTTP)
	'''
	def get_po_monitoring(self):
		return 501

	'''
	PATH: 		 Internal EMS Method 
	ACTION: 	 GET
	DESCRIPTION: Query the subsystem for the standard modification operations
				 that modify the operational behaviour of the VNF platform which
				 the driver is developed for.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + PlatformOperation (Class) [0..N]
	 			 - Integer error code (HTTP)
	'''
	def get_po_modification(self):
		return 501

	'''
	PATH: 		 Internal EMS Method
	ACTION: 	 GET
	DESCRIPTION: Query the subsystem for the standard operations that are not
				 categorized neither as monitoring nor modification of the VNF
				 ehich the driver is developed for.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + PlatformOperation (Class) [0..N]
	 			 - Integer error code (HTTP)
	'''
	def get_po_other(self):
		return 501

	'''
	PATH: 		 Internal EMS Method
	ACTION: 	 GET | POST | PUT | PATCH | DELETE
	DESCRIPTION: Query a the subsystem for the standard operations that are not
				 categorized neither as monitoring nor modification of the VNF
				 ehich the driver is developed for.
	ARGUMENT: 	 vibVnfInstance (VibVnfInstance), platformOperation (PlatformOperation), arguments (Dictionary)
	RETURN: 	 - 200 (HTTP) + Platform data (????) [????]
	 			 - Integer error code (HTTP)
	'''
	def exec_p_operation(self, vibVnfInstance, platformOperation, arguments):
		return 501

	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}
	ACTION: 	 GET
	DESCRIPTION: Query multiple VNF indicators related to one VNF instance. This re-
				 source allows to query all VNF indicators that are known to the API
				 producer.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [0..N]
				 - Integer error code (HTTP)
	'''
	def get_vii_i_vnfInstanceID(self, vibVnfInstance):

		vnfIndicators = []
		vnfMonitoring = self.get_po_monitoring()
		
		for vnfOperation in vnfMonitoring:
			if vnfOperation.arguments == {}:
				indicatorValue = vnfOperation.method(vibInstance)
				#TODO: check if indicatorValue is 200
				vnfIndicators.append(indicatorValue)

		return vnfIndicators


	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}/{indicatorId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual VNF indicator to one VNF instance.
	ARGUMENT: 	 vnfInstanceId (String), indicatorId (String)
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [1]
				 - Integer error code (HTTP)
	'''
	def get_vii_iid_indicatorID(self, vibVnfInstance, indicatorId):

		vnfMonitoring = self.get_po_monitoring()
		vnfMonitoringIds = [vm.id for vm in vnfMonitoring]

		if not indicatorId in vnfMonitoringIds:
			return 405

		index = vnfMonitoringIds.index(indicatorId)
		if vnfMonitoring[index].arguments != {}:
			return 406

		indicatorValue = vnfMonitoring.method(vibVnfInstance)
		#TODO: check if indicatorValue is 200
		return indicatorValue