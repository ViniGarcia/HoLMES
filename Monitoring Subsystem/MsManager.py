import AsModels
import VibModels
import VibManager

import uuid

'''
CLASS: MonitoringAgentTemplate
AUTHOR: Vinicius Fulber-Garcia
CREATION: 19 Nov. 2020
L. UPDATE: 19 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the monitoring susbsytem manager.
			 This class abstracts the operation of every monitoring
			 agent. Furthermore, it deals with the models from the
			 ETSI standard of VNFM/EM.
ERROR CODES: 
			-1: Invalid argument data type
			-2: Invalid file path
			-3: Error during importing module
			-4: Key is not in the dictionary
			-5: Argument missing
'''	

class MsManager:

	__vibManager = None
	__monitoringAgents = {}
	
	def __init__(self, vibManager):
		
		self.__vibManager = vibManager

	def requestAgent(self, vnfIndicatorSubscriptionRequest):

		agentInstances = []
		for monitoringAgent in vnfIndicatorSubscriptionRequest.filter.indicatorsIds:
			if type(monitoringAgent) != str:
				return -1
			if not os.path.isfile("Monitoring Subsystem/Monitoring Agents/" + monitoringAgent + ".py"):
				return -2
			try:
				agentInstances.append(getattr(importlib.import_module("Monitoring Agents." + monitoringAgent), monitoringAgent)())
			except Exception as e:
				return -3

		vibVnfInstances = []
		for vnfId in vnfIndicatorSubscriptionRequest.filter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
			vibVnfInstance = self.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")

			for agent in agentInstances:
				agent.includeInstance(vibVnfInstance)

		vnfIndicatorSubscription = VnfIndicatorSubscription().fromData(str(uuid.uuid1()), vnfIndicatorSubscriptionRequest.filter, vnfIndicatorSubscriptionRequest.callbackUri, vnfIndicatorSubscriptionRequest.links)
		vibVnfIndicatorSubscription = VibVnfIndicatorSubscription().fromData(vnfIndicatorSubscription.id, vnfIndicatorSubscription.filter, vnfIndicatorSubscription.callbackUri, vnfIndicatorSubscription.links)
		self.__vibManager.insertVibDatabase(vibVnfIndicatorSubscription)
		self.__monitoringAgents[vnfIndicatorSubscription.id] = agentInstances

		return vnfIndicatorSubscription

	def startAgent(self, vibVnfIndicatorSubscription, resourcesData):
		
		if not vibVnfIndicatorSubscription.id in self.__vibManager:
			return -4

		if len(self.__monitoringAgents[vibVnfIndicatorSubscription.id]) != len(resourcesData):
			return -5

		for data in resourcesData:
			if type(data) != dict:
				return -1

		for index in range(len(self.__monitoringAgents[vibVnfIndicatorSubscription.id])):
			if not agent.getRunning(self):
				agent.monitoringStart()

	def stopAgent(self, vibVnfIndicatorSubscription):
		return

	def deleteAgent(self, vibVnfIndicatorSubscription):
		return