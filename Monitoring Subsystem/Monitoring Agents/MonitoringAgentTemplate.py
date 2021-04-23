import AsModels
import VibModels

import time
import json
import psutil
import requests
import multiprocessing

import pickle
import base64

def killProcess(pid):
    mainProcess = psutil.Process(pid)
    for process in mainProcess.children(recursive=True):
        process.kill()
    mainProcess.kill()

'''
CLASS: MonitoringAgentTemplate
AUTHOR: Vinicius Fulber-Garcia
CREATION: 18 Nov. 2020
L. UPDATE: 24 Nov. 2020 (Fulber-Garcia; Testing methods and bug corrections)
DESCRIPTION: Template for the implementation of monitoring agents that run in the "Monitoring Sub-
			 system" internal module. The drivers must inhert this class and overload the functions
			 that return the HTTP code 501 (Not Implemented).
ERROR CODES: 
			-1: Invalid argument data type
			-2: Invalid keys in dictionary
			-3: Element already in the list
			-4: Element is not in the list
'''
class MonitoringAgentTemplate:
	monitoredInstances = [] 	  #VibPlatformInstance (Class), optional [0..N]
	monitoringOperation = None    #PlatformOperation (Dictionary), mandatory [1]
	monitoringSubscribers = []    #VibVnfIndicatorSubscription (Class), optional [0..N]

	__asMs = None				  #AsOpAgent (Class), internal [1]
	__running = False			  #Boolean, internal [1]
	__processInstance = None	  #Process (Class), internal [1]			

	def __init__(self, monitoringOperation, asMs):

		self.monitoringOperation = monitoringOperation
		self.__asMs = asMs

	def monitoringRoutine(self, resourceData):

		return 501

	def monitoringProcess(self, resourceData, monitoredInstances, monitoringSubscribers):

		self.monitoringOperation = self.__asMs.get_p_operations()[self.monitoringOperation.id]
		self.monitoredInstances = monitoredInstances
		self.monitoringSubscribers = monitoringSubscribers
		self.monitoringRoutine(resourceData)

	#PRIVATE METHOD, SET PUBLIC ONLY TO PROCESS STARTING
	def executeOperation(self, operationArguments):
		
		if type(operationArguments) != dict:
			return -1

		if set(self.monitoringOperation.arguments.keys()) != set(operationArguments.keys()):
			return -2

		instancesIndicator = []
		for requestInstance in self.monitoredInstances:
			indicatorValue = self.monitoringOperation.method(requestInstance, operationArguments)
			if type(indicatorValue) != str:
				indicatorValue = "!EMS Error Message: " + str(indicatorValue)
			instancesIndicator.append(AsModels.VnfIndicator().fromData(self.monitoringOperation.id, self.monitoringOperation.id, indicatorValue, requestInstance.vnfId, {"self":self.monitoringOperation.id, "vnfInstance":requestInstance.vnfAddress}))

		return instancesIndicator

	#PRIVATE METHOD, SET PUBLIC ONLY TO PROCESS STARTING
	def executeNotification(self, vibSubscriptionInstance, notificationData):
		
		if type(vibSubscriptionInstance) != VibModels.VibSubscriptionInstance:
			return -1

		if type(notificationData) != str:
			return -1

		responseData = requests.post(vibSubscriptionInstance.visCallback, params=notificationData)
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def includeInstance(self, vibVnfInstance):
		
		if type(vibVnfInstance) != VibModels.VibVnfInstance:
			return -1

		if vibVnfInstance in self.monitoredInstances:
			return -3

		self.monitoredInstances.append(vibVnfInstance)

	def removeInstance(self, vibVnfInstance):
		
		if type(self.vibVnfInstance) != VibModels.VibVnfInstance:
			return -1

		if not vibVnfInstance in self.monitoredInstances:
			return -4

		self.monitoredInstances.remove(vibVnfInstance)

	def includeSubscriber(self, vibSubscriptionInstance):
		
		if type(vibSubscriptionInstance) != VibModels.VibSubscriptionInstance:
			return -1

		if vibSubscriptionInstance in self.monitoringSubscribers:
			return -3

		self.monitoringSubscribers.append(vibSubscriptionInstance)

	def removeSubscriber(self, vibSubscriptionInstance):
		
		if type(self.vibSubscriptionInstance) != VibModels.VibSubscriptionInstance:
			return -1

		if not vibSubscriptionInstance in self.monitoringSubscribers:
			return -4

		self.monitoringSubscribers.remove(vibSubscriptionInstance)

	def monitoringStart(self, resourceData):

		
		self.__processInstance = multiprocessing.Process(target=self.monitoringProcess, args=(resourceData, self.monitoredInstances, self.monitoringSubscribers, ))
		self.__processInstance.start()
		self.__running = True

	def monitoringStop(self):
		
		killProcess(self.__processInstance.pid)
		self.__processInstance = None
		self.__running = False

	def monitoringRefresh(self):

		self.monitoringStop()
		self.__running = False
		self.monitoringStart()
		self.__running = True

	def getRunning(self):

		return self.__running