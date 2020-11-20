import sys

sys.path.insert(0,'VNF Subsystem/')
sys.path.insert(0,'Access Subsystem/')
sys.path.insert(0,'VNF Information Base/')
sys.path.insert(0,'Monitoring Subsystem/')

sys.path.insert(0,'VNF Subsystem/Ve-Em-vnf/')
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')
sys.path.insert(0,'Monitoring Subsystem/Monitoring Agents/')

import AsModels
import VibModels
import VsModels

import VibManager
import AsAuthAgent
import AsOpAgent
import VsAgent

import VnfDriverTemplate
import VnfmDriverTemplate
import MonitoringAgentTemplate

import CooDriver

'''#AS OP AGENT TESTING
vibTester = VibManager.VibManager()
authTester = AsAuthAgent.AuthenticationAgent("PlainText", vibTester)
operationTester = OperationAgent()
operationTester.setupAgent(vibTester, "VnfmDriverTemplate", None, authTester)
#operationTester.get_vii_indicators()
#operationTester.get_vii_i_vnfInstanceID("VNF01")
#operationTester.get_vii_iid_indicatorID("VNF01", "CPU")
#operationTester.get_vii_i_indicatorID("CPU")
#print(operationTester.post_vii_subscriptions(AsModels.VnfIndicatorSubscriptionRequest().fromData(None, "192.168.0.100:8000", "USER01;BatataFrita")))
#print(operationTester.get_vii_subscriptions()[1].id)
#print(operationTester.get_vii_s_subscriptionID("0a16e784-237f-11eb-b84f-782bcbee2213"))
#print(operationTester.delete_vii_s_subscriptionID("0a16e784-237f-11eb-b84f-782bcbee2213"))'''

'''#AS AUTH AGENT TESTING
vibTester = VibManager.VibManager()
authTester = AuthenticationAgent("PlainText", vibTester)
authentication = authTester.authRequest("USER01;BatataFrita")
print(authentication)'''

'''#VS AGENT TESTING
vsAgent = VsAgent.VsAgent().setup("CooDriver")
vnfOperations = vsAgent.get_p_operations()
vnfAgent.exec_p_operation(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_click_version"])
vnfAgent.exec_p_operation(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_vii_i_vnfInstanceID"])
vnfOperations["get_vii_iid_indicatorID"].arguments["indicatorId"] = "get_click_running"
vnfAgent.exec_p_operation(VibTableModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True), vnfOperations["get_vii_iid_indicatorID"])'''

'''#MONITORING AGENT TEMPLATE TESTING
mat = MonitoringAgentTemplate.MonitoringAgentTemplate(vnfOperations["get_click_version"])
mat.monitoringStart("oi")'''

import time
import multiprocessing


def main():
	vsAgent = VsAgent.VsAgent().setup("CooDriver")
	mat = MonitoringAgentTemplate.MonitoringAgentTemplate("get_click_version", vsAgent)
	mat.includeInstance(VibModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "COO", ["OP01", "OP02"], True))
	mat.monitoringStart([])
	time.sleep(4)
	mat.monitoringStop()

if __name__ == '__main__':
    main()