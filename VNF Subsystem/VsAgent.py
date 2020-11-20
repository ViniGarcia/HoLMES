import AsModels
import VibModels

import os
import importlib

'''
CLASS: VnfAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 18 Nov. 2020 (Fulber-Garcia; Methods update/creation)
DESCRIPTION: VNF agent implementation. This class has the
			 most important functionalites of the VNF sub-
			 system. It holds the implementation of all
			 the methods provided for the EMS platform and
			 accordingly to the external users. The methods
			 implementation are provided in the VNF drivers.
CODES:  -1 -> Invalid data type of veEmVnf
		-2 -> Invalid driver name of VeEmVnf
		-3 -> Invalid class instantiation of __veEmVnf
'''
class VsAgent:

	__veEmVnf = None

	def __init__(self):
		return

	def setup(self, veEmVnf):

		if type(veEmVnf) != str:
			return -1
		if not os.path.isfile("VNF Subsystem/Ve-Em-vnf/" + veEmVnf + ".py"):
			return -2
		try:
			self.__veEmVnf = getattr(importlib.import_module("Ve-Em-vnf." + veEmVnf), veEmVnf)()
		except Exception as e:
			return -3

		return self

	def get_p_operations(self):

		return self.__veEmVnf.get_p_operations()

	def get_po_monitoring(self):

		return self.__veEmVnf.get_po_monitoring()

	def get_po_modification(self):

		return self.__veEmVnf.get_po_modification()

	def get_po_other(self):

		return self.__veEmVnf.get_po_other()

	def exec_p_operation(self, vibVnfInstance, platformOperation):

		return platformOperation.method(vibVnfInstance, platformOperation.arguments)