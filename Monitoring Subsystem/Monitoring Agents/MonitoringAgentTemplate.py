import VibModels

import time
import psutil
import requests
import multiprocessing

def killProcess(pid):
    mainProcess = psutil.Process(pid)
    for process in mainProcess.children(recursive=True):
        process.kill()
    mainProcess.kill()

'''
CLASS: MonitoringAgentTemplate
AUTHOR: Vinicius Fulber-Garcia
CREATION: 18 Nov. 2020
L. UPDATE: 18 Nov. 2020 (Fulber-Garcia; Template creation)
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
	monitoringOperation = None    #PlatformOperation (Class), mandatory [1]
	monitoringSubscribers = []    #VibVnfIndicatorSubscription (Class), optional [0..N]

	__monitoringProcess = None	#Subprocess, internal usage

	def __init__(self, monitoringOperation):

		self.monitoringOperation = monitoringOperation

	def monitoringProcess(self, resourceData, monitoredInstances, monitoringSubscribers):

		while True:
			print(monitoredInstances, monitoringSubscribers)
			print(self.__executeOperation({}, monitoredInstances, monitoringSubscribers))
			time.sleep(3)

		return 501

	def __executeOperation(self, operationArguments, monitoredInstances, monitoringSubscribers):
		
		if type(operationArguments) != dict:
			return -1

		print(self.monitoringOperation.arguments.keys())
		if set(self.monitoringOperation.arguments.keys()) != set(operationArguments.keys()):
			return -2

		instanceIndicators = []
		for requestInstance in monitoredInstances:
			indicatorValue = self.monitoringOperation.method(requestInstance, operationArguments)
			if type(indicatorValue) != str:
				indicatorValue = "!EMS Error Message: " + str(indicatorValue)
			instancesIndicator.append(AsModels.VnfIndicator.fromData(self.monitoringOperation.id, self.monitoringOperation.id, indicatorValue, requestInstance.vnfId, {"self":self.monitoringOperation.id, "vnfInstance":requestInstance.vnfAddress}))

		return instancesIndicator

	def __executeNotification(self, vibVnfIndicatorSubscription, notificationData):
		
		if type(vibVnfIndicatorSubscription) != VibModels.vibVnfIndicatorSubscription:
			return -1

		if type(notificationData) != dict:
			return -1

		for key in notificationData.keys():
			if type(key) != str:
				return -1
			if type(notificationData[key]) != str:
				return -1 

		responseData = requests.post(vibVnfIndicatorSubscription.visCallback, params=notificationData)
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

	def includeSubscriber(self, vibVnfIndicatorSubscription):
		
		if type(self.vibVnfIndicatorSubscription) != VibModels.VibVnfIndicatorSubscription:
			return -1

		if vibVnfIndicatorSubscription in self.monitoringSubscribers:
			return -3

		self.monitoringSubscribers.append(vibVnfIndicatorSubscription)

	def removeSubscriber(self, vibVnfIndicatorSubscription):
		
		if type(self.vibVnfIndicatorSubscription) != VibModels.VibVnfIndicatorSubscription:
			return -1

		if not vibVnfIndicatorSubscription in self.monitoringSubscribers:
			return -4

		self.monitoringSubscribers.remove(vibVnfIndicatorSubscription)

	def monitoringStart(self, resourceData):
		
		self.__monitoringProcess = multiprocessing.Process(target=self.monitoringProcess, args=(resourceData, self.monitoredInstances, self.monitoringSubscribers))
		self.__monitoringProcess.start()

	def monitoringStop(self):
		
		killProcess(self.__monitoringProcess.pid)
		self.__monitoringProcess = None
