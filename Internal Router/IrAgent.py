import IrModels

import ImAgent
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
CODES:  -1 -> Invalid internal manager instance
		-2 -> Invalid vnf subsystem instance
		-3 -> Invalid origin
		-4 -> Wrong message type for destination
		-5 -> Invalid destination
'''
class IrAgent:

	irMs = None
	irIm = None
	irVs = None

	def __init__(self):
		return

	def setupAgent(self, irIm, irVs):

		if type(irIm) != ImAgent.ImAgent:
			return -1
		if type(irVs) != VsAgent.VsAgent:
			return -2

		self.irIm = irIm
		self.irVs = irVs

		return self

	def sendMessage(self, irMessage):
		
		if not irMessage.originModule in ["AS", "VS", "IM"]:
			return -3

		if irMessage.destinationModule == "VS":
			if type(irMessage.messageData) == IrModels.VsData:
				irMessage.messageData = self.irVs.exec_p_operation(irMessage.messageData)
			else:
				return -4
		elif irMessage.destinationModule == "IM":
			if type(irMessage.messageData) == IrModels.IrManagement:
				irMessage.messageData = self.irIm.requestOperation(irMessage.messageData)
			else:
				return -4
		else:
			return -5

		saveOrigin = irMessage.originModule
		irMessage.originModule = irMessage.destinationModule
		irMessage.destinationModule = saveOrigin
		return irMessage

