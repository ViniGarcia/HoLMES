import sys

sys.path.insert(0,'VNF Subsystem/')
sys.path.insert(0,'Internal Router/')
sys.path.insert(0,'Access Subsystem/')
sys.path.insert(0,'Internal Manager/')
sys.path.insert(0,'VNF Information Base/')
sys.path.insert(0,'Monitoring Subsystem/')

sys.path.insert(0,'VNF Subsystem/Ve-Em-vnf/')
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')
sys.path.insert(0,'Monitoring Subsystem/Monitoring Agents/')

import AsModels
import VibModels
import VsModels
import IrModels

import VibManager
import AsAuthAgent
import AsOpAgent
import VsAgent
import MsManager
import IrAgent
import ImAgent

import VnfDriverTemplate
import VnfmDriverTemplate
import MonitoringAgentTemplate

import CooDriver
import CooRunningAgent

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

'''
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
'''

'''
import time
def main():
	vibManager = VibManager.VibManager()
	msManager = MsManager.MsManager(vibManager)

	#vnfInstanceSubscriptionFilter = AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], [])
	#print(vnfInstanceSubscriptionFilter)
	#vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(vnfInstanceSubscriptionFilter, [], ["CooRunningAgent"])
	#print(vnfIndicatorNotificationsFilter)
	#vnfIndicatorSubscriptionRequest = AsModels.VnfIndicatorSubscriptionRequest().fromData(vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", None)
	#print(vnfIndicatorSubscriptionRequest)
	#subscription = msManager.requestAgent(vnfIndicatorSubscriptionRequest)
	#print(subscription)

	#visSql = vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription WHERE visId = \"421e1951-2b34-11eb-9d16-782bcbee2213\";")
	#vibVnfIndicatorSubscription = VibModels.VibVnfIndicatorSubscription().fromSql(visSql[0])
	#asSubscription = msManager.setupAgent(vibVnfIndicatorSubscription)
	#print(msManager.deleteAgent(vibVnfIndicatorSubscription))

	#print(vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription;"))

	visSql = vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription WHERE visId = \"e89b2fa3-2e44-11eb-8908-782bcbee2213\";")
	vibVnfIndicatorSubscription = VibModels.VibVnfIndicatorSubscription().fromSql(visSql[0])
	asSubscription = msManager.setupAgent(vibVnfIndicatorSubscription)
	msManager.startAgent(vibVnfIndicatorSubscription, [{}])
	time.sleep(2)

if __name__ == '__main__':
    main()
'''

'''
#VIB RESET AND TESTING
vibManager = VibManager.VibManager()
print(vibManager.vibTesting())
'''

'''vibManager = VibManager.VibManager()
#classTest = VibModels.VibVnfInstance().fromData("VNF01", "127.0.0.1:5000", "Click-On-OSv", [], True)
#vibManager.insertVibDatabase(classTest.toSql())
#print(vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF01\";"))

#classTest = VibModels.VibPlatformInstance().fromData("Click-On-OSv", "CooDriver")
#vibManager.insertVibDatabase(classTest.toSql())
#print(vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"Click-On-OSv\";"))'''

'''
#IR TESTING
vibManager = VibManager.VibManager()
asAuthAgent = AsAuthAgent.AuthenticationAgent("PlainText", vibManager)
operationAgent = AsOpAgent.OperationAgent().setupAgent(vibManager, "VnfmDriverTemplate", None, asAuthAgent)
msManager = MsManager.MsManager(vibManager)
vsAgent = VsAgent.VsAgent()

irAgent = IrAgent.IrAgent().setupAgent(operationAgent, msManager, None, vsAgent)

vibPlatformInstance = VibModels.VibPlatformInstance().fromSql(vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"Click-On-OSv\";")[0])
vibVnfInstance = VibModels.VibVnfInstance().fromSql(vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"VNF01\";")[0])

requestData = IrModels.VsData().fromData(vibVnfInstance, vibPlatformInstance, "get_click_running", {})
requestMessage = IrModels.IrMessage().fromData(requestData, "AS", "VS")

print(requestMessage)
print(irAgent.sendMessage(requestMessage).messageData)
'''

##############################################################################################################################################################

'''
#-->> MANAGEMENT TESTING ROUTINE #1 - INTERNAL MANAGER ACTING OVER THE VIB MODULE (CREDENTIAL TABLE) <<--#
vibManager = VibManager.VibManager()
imAgent = ImAgent.ImAgent().setupAgent(None, None, None, vibManager)

#GETTING FULL CREDENTIAL TABLE
vibManagement = IrModels.VibManagement().fromData("get_vib_credentials", None)
credentialTable = imAgent.executeVibOperation(vibManagement)
print(credentialTable)

#CREATE A CREDENTIAL INSTANCE WITH THE FIRST CREDENTIAL
vibCredentialInstance = VibModels.VibCredentialInstance().fromSql(credentialTable[0])

#TRYING TO INSERT AN ALREADY EXISTING CREDENTIAL
vibManagement = IrModels.VibManagement().fromData("post_vib_credentials", vibCredentialInstance)
print(imAgent.executeVibOperation(vibManagement))
vibCredentialInstance.vnfId = "NONE"
vibManagement = IrModels.VibManagement().fromData("post_vib_credentials", vibCredentialInstance)
print(imAgent.executeVibOperation(vibManagement))
vibCredentialInstance.vnfId = "VNF01"

#CONSULTING THE SAME CREDENTIAL PARTICULARY
vibManagement = IrModels.VibManagement().fromData("get_vib_c_credentialId", (vibCredentialInstance.userId, vibCredentialInstance.vnfId))
print(imAgent.executeVibOperation(vibManagement))

#UPDATING THE NON-KEY VALUES OF THE CREDENTIAL
vibCredentialInstance.authData = "PolentaFrita"
vibCredentialInstance.authResource = "BatataFrita"
vibManagement = IrModels.VibManagement().fromData("patch_vib_c_credentialId", vibCredentialInstance)
print(imAgent.executeVibOperation(vibManagement))

#DELETING THE CREDENTIAL FROM TABLE
vibManagement = IrModels.VibManagement().fromData("delete_vib_c_credentialId", (vibCredentialInstance.userId, vibCredentialInstance.vnfId))
print(imAgent.executeVibOperation(vibManagement))

#CHECKING IF THE DELETE OPERATION WAS SUCCESSFUL
vibManagement = IrModels.VibManagement().fromData("get_vib_credentials", None)
print(imAgent.executeVibOperation(vibManagement))

#INSERTING THE DELETED CREDENTIAL BACK
vibManagement = IrModels.VibManagement().fromData("post_vib_credentials", vibCredentialInstance)
print(imAgent.executeVibOperation(vibManagement))

#CHECK IF THE INSERT OPERATION WAS SUCCESSFUL
vibManagement = IrModels.VibManagement().fromData("get_vib_credentials", None)
print(imAgent.executeVibOperation(vibManagement))
'''

#-->> MANAGEMENT TESTING ROUTINE #2 - INTERNAL MANAGER ACTING OVER THE VIB MODULE (SUBSCRIPTION TABLE) <<--#
vibManager = VibManager.VibManager()
imAgent = ImAgent.ImAgent().setupAgent(None, None, None, vibManager)

#INSERTING AN TESTING SUBSCRIPTION
#vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], []), [], ["CooRunningAgent"])
#vibSubscriptionInstance = VibModels.VibSubscriptionInstance().fromData("1234567890", vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", {"self":"127.0.0.1"})
#vibManagement = IrModels.VibManagement().fromData("post_vib_subscriptions", vibSubscriptionInstance)
#print(imAgent.executeVibOperation(vibManagement))

#GETTING FULL SUBSCRIPTION TABLE
vibManagement = IrModels.VibManagement().fromData("get_vib_subscriptions", None)
print(imAgent.executeVibOperation(vibManagement), "\n")

#GETTING THE RECENTLY INSERTED SUBSCRIPTION
vibManagement = IrModels.VibManagement().fromData("get_vib_s_subscriptionId", "1234567890")
vibSubscriptionInstance = imAgent.executeVibOperation(vibManagement)
print(vibSubscriptionInstance, "\n")
vibSubscriptionInstance = VibModels.VibSubscriptionInstance().fromSql(vibSubscriptionInstance[0])

#INVALID UPDATING THE NON-KEY VALUES OF THE SUBSCRIPTION
vibSubscriptionInstance.visFilter.filter.vnfInstanceIds.append("VNF02")
vibManagement = IrModels.VibManagement().fromData("patch_vib_s_subscriptionId", vibSubscriptionInstance)
print(imAgent.executeVibOperation(vibManagement), "\n")