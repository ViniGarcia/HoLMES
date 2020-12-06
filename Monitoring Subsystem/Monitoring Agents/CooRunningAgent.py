import VsAgent
import VsModels
import MonitoringAgentTemplate

import json
import time

class CooRunningAgent(MonitoringAgentTemplate.MonitoringAgentTemplate):

	def __init__(self, cooPlatformDriver):
		
		vsAgent = VsAgent.VsAgent().setup(cooPlatformDriver)
		super().__init__(vsAgent.get_p_operations()["get_click_running"], vsAgent)
		
	def monitoringRoutine(self, resourceData):
		
		while True:
			runningInfo = self.executeOperation({})
			for subscriber in self.monitoringSubscribers:
				self.executeNotification(subscriber, json.dumps([ri.toDictionary() for ri in runningInfo]))
			time.sleep(2)