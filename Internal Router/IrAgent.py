import IrModels

import AsOpAgent
import MsManager
import VsAgent


'''
CLASS: IrAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 24 Nov. 2020
L. UPDATE: 24 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Internal router agent implementation. This
			 class has the kernel functionalites to en-
			 able the communication between the internal
			 modules of the EMS platform.
CODES:  -1 -> Invalid operationagent instance
		-2 -> Invalid monitoring subsystem instance
		-3 -> Invalid internal manager instance
		-4 -> Invalid vnf subsystem instance
'''
class IrAgent:

	asIr = None
	irMs = None
	irIm = None
	irVs = None

	def __init__(self):
		return

	def setupAgent(self, asIr, irMs, irIm, irVs):

		if type(asIr) != AsOpAgent.OperationAgent:
			return -1
		if type(irMs) != MsManager.MsManager:
			return -2
		if type(irVs) != VsAgent.VsAgent:
			return -4

		self.asIr = asIr
		self.irMs = irMs
		self.irIm = irIm
		self.irVs = irVs

		return self

	def sendMessage(self, irMessage):
		
		if type(irMessage.messageData) == IrModels.VsData:
			irMessage.messageData = self.irVs.exec_p_operation(irMessage.messageData)

		saveOrigin = irMessage.originModule
		irMessage.originModule = irMessage.destinationModule
		irMessage.destinationModule = saveOrigin
		return irMessage

