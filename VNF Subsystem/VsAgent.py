import AsModels
import IrModels
import VibModels

import os
import importlib

'''
CLASS: VnfAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 24 Nov. 2020 (Fulber-Garcia; Setup and Exec updated)
DESCRIPTION: VNF agent implementation. This class has the
			 most important functionalites of the VNF sub-
			 system. It holds the implementation of all
			 the methods provided for the EMS platform and
			 accordingly to the external users. The methods
			 implementation are provided in the VNF drivers.
CODES:  -1 -> Invalid data type of vibPlatformInstance
		-2 -> Invalid driver name in vibPlatformInstance
		-3 -> Invalid class instantiation of __veEmVnf
		-4 -> Invalid operationId provided
'''
class VsAgent:

	__veEmVnf = None

	def __init__(self):
		return

	def setup(self, vibPlatformInstance):

		if self.__veEmVnf != None:
			if self.__veEmVnf.className == vibPlatformInstance.platformId:
				return self

		if type(vibPlatformInstance) != VibModels.VibPlatformInstance:
			return -1
		if not os.path.isfile("VNF Subsystem/Ve-Em-vnf/" + vibPlatformInstance.platformDriver + ".py"):
			return -2
		try:
			self.__veEmVnf = getattr(importlib.import_module("Ve-Em-vnf." + vibPlatformInstance.platformDriver), vibPlatformInstance.platformDriver)()
		except Exception as e:
			return -3

		return self

	def detach(self):

		if self.__veEmVnf != None:
			self.__veEmVnf = None

		return None

	def get_p_id(self):

		if self.__veEmVnf != None:
			return self.__veEmVnf.className

		return None

	def get_p_operations(self):

		if self.__veEmVnf != None:
			return self.__veEmVnf.get_p_operations()

		return None

	def get_po_monitoring(self):

		if self.__veEmVnf != None:
			return self.__veEmVnf.get_po_monitoring()

		return None

	def get_po_modification(self):

		if self.__veEmVnf != None:
			return self.__veEmVnf.get_po_modification()

		return None

	def get_po_other(self):

		if self.__veEmVnf != None:
			return self.__veEmVnf.get_po_other()

		return None

	def exec_p_operation(self, vsData):

		self.setup(vsData.vibPlatformInstance)
		availableOperations = self.get_p_operations()

		if not vsData.operationId in availableOperations:
			return -4
		platformOperation = availableOperations[vsData.operationId]

		return platformOperation.method(vsData.vibVnfInstance, vsData.operationArgs)