import sys
sys.path.insert(0,'../VNF Information Base/')
sys.path.insert(0,'../Access Subsystem/')
sys.path.insert(0,'Ve-Em-vnf/')

import CommunicationModels
import VibTableModels
import VnfDriverTemplate

import os
import importlib

'''
CLASS: VnfAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 16 Nov. 2020 (Fulber-Garcia; Class creation)
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
class VnfAgent:

	__veEmVnf = None

	def __init__(self):
		return

	def setupAgent(self, veEmVnf):

		if type(veEmVnf) != str:
			return -1
		if not os.path.isfile("Ve-Em-vnf/" + veEmVnf + ".py"):
			return -2
		try:
			self.__veEmVnf = getattr(importlib.import_module("Ve-Em-vnf." + veEmVnf), veEmVnf)()
		except Exception as e:
			print(e)
			return -3

		return self

	def requestOperations(self):

		return self.__veEmVnf.get_p_operations()

	def requestAgent(self, vibVnfInstance, platformOperation):

		return platformOperation.method(vibVnfInstance, platformOperation.arguments)


'''#TEMPORARY
vnfAgent = VnfAgent().setupAgent("CooDriver")
vnfOperations = vnfAgent.requestOperations()
vnfAgent.requestAgent(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_click_version"])
vnfAgent.requestAgent(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_vii_i_vnfInstanceID"])
vnfOperations["get_vii_iid_indicatorID"].arguments["indicatorId"] = "get_click_running"
vnfAgent.requestAgent(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_vii_iid_indicatorID"])
'''