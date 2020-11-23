import VsAgent
import VsModels
import MonitoringAgentTemplate

import json
import time

class CooRunningAgent(MonitoringAgentTemplate.MonitoringAgentTemplate):

	def __init__(self):

		vsAgent = VsAgent.VsAgent().setup("CooDriver")
		super().__init__(vsAgent.get_p_operations()["get_click_running"], vsAgent)

	def monitoringRoutine(self, resourceData):
		
		while True:
			runningInfo = self.executeOperation({})
			for subscriber in self.monitoringSubscribers:
				self.executeNotification(subscriber, json.dumps(runningInfo))
			time.sleep(1)