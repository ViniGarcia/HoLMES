import AsModels
import VibModels
import VibManager

import os
import uuid
import importlib

'''
CLASS: MsManager
AUTHOR: Vinicius Fulber-Garcia
CREATION: 19 Nov. 2020
L. UPDATE: 06 Dez. 2020 (Fulber-Garcia; Receiving vibPlatformInstance in the setup operation)
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
			-6: Agent is already setup
'''	
class MsManager:

	__monitoringAgents = {}
	
	def __init__(self):
		return

	def getAgents(self):

		return self.__monitoringAgents

	def requestAgent(self, vnfIndicatorSubscriptionRequest):

		agentInstances = []
		for monitoringAgent in vnfIndicatorSubscriptionRequest.filter.indicatorIds:
			if type(monitoringAgent) != str:
				return -1
			if not os.path.isfile("Monitoring Subsystem/Monitoring Agents/" + monitoringAgent + ".py"):
				return -2

		vnfIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromData(str(uuid.uuid1()), vnfIndicatorSubscriptionRequest.filter, vnfIndicatorSubscriptionRequest.callbackUri, {"self":"127.0.0.1"})

		return vnfIndicatorSubscription

	def setupAgent(self, vibSubscriptionInstance, vibVnfInstances, vibPlatformInstance):

		if vibSubscriptionInstance.visId in self.__monitoringAgents:
			return -6

		agentInstances = []
		for monitoringAgent in vibSubscriptionInstance.visFilter.indicatorIds:
			if type(monitoringAgent) != str:
				return -1
			if not os.path.isfile("Monitoring Subsystem/Monitoring Agents/" + monitoringAgent + ".py"):
				return -2
			try:
				agentInstances.append(getattr(importlib.import_module("Monitoring Agents." + monitoringAgent), monitoringAgent)(vibPlatformInstance))
			except Exception as e:
				print(e)
				return -3

		for agent in agentInstances:
			for instance in vibVnfInstances:
				agent.includeInstance(instance)			
			agent.includeSubscriber(vibSubscriptionInstance)

		vnfIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromData(vibSubscriptionInstance.visId, vibSubscriptionInstance.visFilter, vibSubscriptionInstance.visCallback, vibSubscriptionInstance.visLinks)
		self.__monitoringAgents[vnfIndicatorSubscription.id] = agentInstances

		return vnfIndicatorSubscription

	def startAgent(self, vibVnfIndicatorSubscription, resourcesData):
		
		if not vibVnfIndicatorSubscription.visId in self.__monitoringAgents:
			return -4

		if len(self.__monitoringAgents[vibVnfIndicatorSubscription.visId]) != len(resourcesData):
			return -5

		for data in resourcesData:
			if type(data) != dict:
				return -1

		for index in range(len(self.__monitoringAgents[vibVnfIndicatorSubscription.visId])):
			if not self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].getRunning():
				self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].monitoringStart(resourcesData[index])

		return 0

	def stopAgent(self, vibVnfIndicatorSubscription):

		if not vibVnfIndicatorSubscription.visId in self.__monitoringAgents:
			return -4

		for index in range(len(self.__monitoringAgents[vibVnfIndicatorSubscription.visId])):
			if self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].getRunning():
				self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].monitoringStop()

		return 0

	def removeAgent(self, vibVnfIndicatorSubscription):

		if not vibVnfIndicatorSubscription.visId in self.__monitoringAgents:
			return -4

		for index in range(len(self.__monitoringAgents[vibVnfIndicatorSubscription.visId])):
			if self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].getRunning():
				self.__monitoringAgents[vibVnfIndicatorSubscription.visId][index].monitoringStop()

		self.__monitoringAgents.pop(vibVnfIndicatorSubscription.visId)

		return 0