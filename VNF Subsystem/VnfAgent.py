import sys
sys.path.insert(0,'../VNF Information Base/')
sys.path.insert(0,'../Access Subsystem/')

import CommunicationModels
import VibTableModels

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
		-3 -> Invalid class instantiation of __veVnfmEm
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
			self.__veVnfmEm = getattr(importlib.import_module("Ve-Em-vnf." + veEmVnf), veEmVnf)(veEmVnf)
		except:
			return -3

		return 0

	
