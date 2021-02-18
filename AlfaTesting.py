import sys
import flask

sys.path.insert(0,'VNF Subsystem/')
sys.path.insert(0,'Internal Router/')
sys.path.insert(0,'Access Subsystem/')
sys.path.insert(0,'Internal Manager/')
sys.path.insert(0,'VNF Information Base/')
sys.path.insert(0,'Monitoring Subsystem/')

sys.path.insert(0,'VNF Subsystem/Ve-Em-vnf/')
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')
sys.path.insert(0,'Monitoring Subsystem/Monitoring Agents/')

sys.path.insert(0,'AlfaTesting Resources/')

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

##############################################################################################################################################################

import multiprocessing
import subprocess
import requests
import logging
import time
import json

def main():
	vibManager = VibManager.VibManager()

	asAuthAgent = AsAuthAgent.AuthenticationAgent(vibManager)
	asOpAgent = AsOpAgent.OperationAgent()
	msManager = MsManager.MsManager()
	vsAgent = VsAgent.VsAgent()
	imAgent = ImAgent.ImAgent()
	irAgent = IrAgent.IrAgent()

	aiAgent = flask.Flask(__name__)
	aiLog = logging.getLogger('werkzeug')
	aiLog.disabled = True

	asAuthAgent.setupAuthentication("PlainText")

	asOpAgent.setupAgent(vibManager, "DummyVnfmDriver", aiAgent, asAuthAgent, irAgent)
	imAgent.setupAgent(vibManager, msManager, asAuthAgent, asOpAgent, vsAgent)
	irAgent.setupAgent(imAgent, vsAgent)

	aiAgent.run(port=9000)

if __name__ == '__main__':
    
	emsProcess = multiprocessing.Process(target=main, args=())
	emsProcess.start()

	dummyCooHttp = subprocess.Popen(['python3', 'AlfaTesting Resources/DummyCooVnf.py'])
	dummyCooSocket = subprocess.Popen(['python3', 'AlfaTesting Resources/DummyCooSocketVnf.py'])

	time.sleep(2)

	#SETUP: ALFA TESTING DEFAULT CONFIGURATIONS
	requests.post("http://127.0.0.1:9000/" + "im/as/user", params={"vibUserInstance":json.dumps({"userId": "USER01", "userAuthentication": "AUTH01", "userSecrets": "", "userPrivileges": ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"]}), "userAuth":"admin;admin"})
	requests.post("http://127.0.0.1:9000/" + "im/as/user", params={"vibUserInstance":json.dumps({"userId": "USER02", "userAuthentication": "AUTH02", "userSecrets": "", "userPrivileges": ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"]}), "userAuth":"admin;admin"})

	requests.post("http://127.0.0.1:9000/" + "im/vs/driver", params={"vibPlatformInstance":json.dumps({"platformId": "Click-On-OSv-F", "platformDriver": "AlfaTesting Resources/CooDriver.py"}), "userAuth":"admin;admin"})
	requests.post("http://127.0.0.1:9000/" + "im/vs/driver", params={"vibPlatformInstance":json.dumps({"platformId": "Click-On-OSv-S", "platformDriver": "AlfaTesting Resources/CooSocketDriver.py"}), "userAuth":"admin;admin"})
	
	requests.post("http://127.0.0.1:9000/" + "im/vs/vnf_instance", params={"vibVnfInstance":json.dumps({"vnfId": "VNF01", "vnfAddress": "127.0.0.1:5000", "vnfPlatform": "Click-On-OSv-F", "vnfExtAgents": ["OP01", "OP02"], "vnfAuth": True}), "userAuth":"admin;admin"})
	requests.post("http://127.0.0.1:9000/" + "im/vs/vnf_instance", params={"vibVnfInstance":json.dumps({"vnfId": "VNF02", "vnfAddress": "127.0.0.1:5005", "vnfPlatform": "Click-On-OSv-S", "vnfExtAgents": ["OP01", "OP02"], "vnfAuth": True}), "userAuth":"admin;admin"})

	requests.post("http://127.0.0.1:9000/" + "im/as/credential", params={"vibCredentialInstance":json.dumps({"userId": "USER01", "vnfId": "VNF01"}), "userAuth":"admin;admin"})
	requests.post("http://127.0.0.1:9000/" + "im/as/credential", params={"vibCredentialInstance":json.dumps({"userId": "USER01", "vnfId": "VNF02"}), "userAuth":"admin;admin"})
	
	requests.post("http://127.0.0.1:9000/" + "im/ms/agent", params={"vibMaInstance":json.dumps({"maId": "CooRunning", "maSource": "AlfaTesting Resources/CooRunningAgent.py", "maPlatform": "Click-On-OSv-F"}), "userAuth":"admin;admin"})

	requests.post("http://127.0.0.1:9000/" + "/im/vib/subscriptions", params={"vibSubscriptionInstance":json.dumps({"visId": "SUBS01", "visFilter": {"vnfInstanceSubscriptionFilter": {"vnfdIds": [], "vnfProductsFromProviders": [], "vnfInstanceIds": ["VNF01"], "vnfInstanceNames": []}, "notificationTypes": [], "indicatorIds": ["CooRunningAgent"]}, "visCallback": "http://127.0.0.1:5000/response", "visLinks": {"self": "127.0.0.1:5000"}}), "userAuth":"admin;admin"})
	
	requests.post("http://127.0.0.1:9000/" + "im/as/vnfm/driver", params={"vibPlatformInstance":json.dumps({"vnfmId": "DummyVnfmDriver", "vnfmDriver": "AlfaTesting Resources/DummyVnfmDriver.py"}), "userAuth":"admin;admin"})

	#MAIN: ALFA TESTING
	print("\n===================================================================================================\n")

	print("#LOG 1: RUNNING TEST ROUTINES\n")

	print("#LOG 1.1: RUNNING TEST ROUTINES OF IM\n")
    
	print("#LOG 1.1.1: RUNNING TEST ROUTINES OF IM/VIB\n")

	print("LOG 1.1.1.1: RUNNING TEST ROUTINES OF IM/VIB -- USER TABLE\n")
	
	print("LOG 1.1.1.1.1: RUNNING TEST ROUTINES OF IM/VIB -- USER TABLE (/im/vib/users)")
	vibUserInstance = VibModels.VibUserInstance().fromData("USER03", "PolentaFrita", "", ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
	imRequest = ("/im/vib/users", {"vibUserInstance":json.dumps(vibUserInstance.toDictionary()), "userAuth":"USER01;AUTH01"})
    
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.1.2: RUNNING TEST ROUTINES OF IM/VIB -- USER TABLE (/im/vib/users/<userId>)")
	vibCredentialInstance = vibUserInstance = VibModels.VibUserInstance().fromData("USER03", "PolentaFrita2", "", ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
	imRequest = ("/im/vib/users/USER03", {"vibUserInstance":json.dumps(vibUserInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("LOG 1.1.1.2: RUNNING TEST ROUTINES OF IM/VIB -- CREDENTIAL TABLE\n")
	
	print("LOG 1.1.1.2.1: RUNNING TEST ROUTINES OF IM/VIB -- CREDENTIAL TABLE (/im/vib/credentials)")
	vibCredentialInstance = VibModels.VibCredentialInstance().fromData("USER02", "VNF01")
	imRequest = ("/im/vib/credentials", {"vibCredentialInstance":json.dumps(vibCredentialInstance.toDictionary()), "userAuth":"USER01;AUTH01"})
    
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.2.2: RUNNING TEST ROUTINES OF IM/VIB -- CREDENTIAL TABLE (/im/vib/credentials/<userId>/<vnfId>)")
	vibCredentialInstance = VibModels.VibCredentialInstance().fromData("USER02", "VNF01")
	imRequest = ("/im/vib/credentials/USER02/VNF01", {"vibCredentialInstance":json.dumps(vibCredentialInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.2.3: RUNNING TEST ROUTINES OF IM/VIB -- CREDENTIAL TABLE (/im/vib/credentials/user/<userId>)")
	imRequest = ("/im/vib/credentials/user/USER01", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.2.4: RUNNING TEST ROUTINES OF IM/VIB -- CREDENTIAL TABLE (/im/vib/credentials/vnf/<vnfId>)")
	imRequest = ("/im/vib/credentials/vnf/VNF01", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.3: RUNNING TEST ROUTINES OF IM/VIB -- SUBSCRIPTION TABLE\n")

	print("LOG 1.1.1.3.1: RUNNING TEST ROUTINES OF IM/VIB -- SUBSCRIPTION TABLE (/im/vib/subscriptions)")
	vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], []), [], ["CooRunningAgent"])
	vibSubscriptionInstance = VibModels.VibSubscriptionInstance().fromData("1234567890", vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", {"self":"127.0.0.1"})
	imRequest = ("/im/vib/subscriptions", {"vibSubscriptionInstance":json.dumps(vibSubscriptionInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.3.2: RUNNING TEST ROUTINES OF IM/VIB -- SUBSCRIPTION TABLE (/im/vib/subscriptions/<subscriptionId>)")
	vibSubscriptionInstance = VibModels.VibSubscriptionInstance().fromData("1234567890", vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", {"self":"127.0.0.2"})
	imRequest = ("/im/vib/subscriptions/1234567890", {"vibSubscriptionInstance":json.dumps(vibSubscriptionInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.4: RUNNING TEST ROUTINES OF IM/VIB -- MANAGEMENT AGENT TABLE\n")

	print("LOG 1.1.1.4.1: RUNNING TEST ROUTINES OF IM/VIB -- MANAGEMENT AGENT TABLE (/im/vib/management_agents)")
	vibMaInstance = VibModels.VibMaInstance().fromData("DummyAgent", "AlfaTesting Resources/DummyMonitoringAgent.py", "Click-On-OSv-F")
	imRequest = ("/im/vib/management_agents", {"vibMaInstance":json.dumps(vibMaInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.4.2: RUNNING TEST ROUTINES OF IM/VIB -- MANAGEMENT AGENT TABLE (/im/vib/management_agents/<agentId>)")
	vibMaInstance = VibModels.VibMaInstance().fromData("DummyAgent", "AlfaTesting Resources/DummyMonitoringAgent2.py", "Click-On-OSv-F")
	imRequest = ("/im/vib/management_agents/DummyAgent", {"vibMaInstance":json.dumps(vibMaInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.5: RUNNING TEST ROUTINES OF IM/VIB -- VNF INSTANCE TABLE\n")

	print("LOG 1.1.1.5.1: RUNNING TEST ROUTINES OF IM/VIB -- VNF INSTANCE TABLE (/im/vib/vnf_instances)")
	vibVnfInstance = VibModels.VibVnfInstance().fromData("VNF03", "127.0.0.1", "Click-On-OSv-F", ["EXT01"], True)
	imRequest = ("/im/vib/vnf_instances", {"vibVnfInstance":json.dumps(vibVnfInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.5.2: RUNNING TEST ROUTINES OF IM/VIB -- VNF INSTANCE TABLE (/im/vib/vnf_instances/<vnfId>)")
	vibVnfInstance = VibModels.VibVnfInstance().fromData("VNF03", "127.0.0.2", "Click-On-OSv-F", ["EXT01"], True)
	imRequest = ("/im/vib/vnf_instances/VNF03", {"vibVnfInstance":json.dumps(vibVnfInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.6: RUNNING TEST ROUTINES OF IM/VIB -- PLATFORM TABLE\n")

	print("LOG 1.1.1.6.1: RUNNING TEST ROUTINES OF IM/VIB -- PLATFORM TABLE (/im/vib/platforms)")
	vibPlatformInstance = VibModels.VibPlatformInstance().fromData("Coven-On-OSv", "AlfaTesting Resources/DummyPlatformDriver.py")
	imRequest = ("/im/vib/platforms", {"vibPlatformInstance":json.dumps(vibPlatformInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.6.2: RUNNING TEST ROUTINES OF IM/VIB -- PLATFORM TABLE (/im/vib/platforms/<platformId>)")
	vibVnfInstance = VibModels.VibPlatformInstance().fromData("Coven-On-OSv", "AlfaTesting Resources/DummyPlatformDriver2.py")
	imRequest = ("/im/vib/platforms/Coven-On-OSv", {"vibPlatformInstance":json.dumps(vibPlatformInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.7: RUNNING TEST ROUTINES OF IM/VIB -- VNF MANAGER TABLE\n")

	print("LOG 1.1.1.7.1: RUNNING TEST ROUTINES OF IM/VIB -- VNF MANAGER TABLE (/im/vib/vnf_managers)")
	vibVnfmInstance = VibModels.VibVnfmInstance().fromData("Vines", "AlfaTesting Resources/DummyVnfmDriver.py")
	imRequest = ("/im/vib/vnf_managers", {"vibVnfmInstance":json.dumps(vibVnfmInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.1.7.2: RUNNING TEST ROUTINES OF IM/VIB -- VNF MANAGER TABLE (/im/vib/vnf_managers/<vnfmId>)")
	vibVnfmInstance = VibModels.VibVnfmInstance().fromData("Vines", "AlfaTesting Resources/DummyVnfmDriver2.py")
	imRequest = ("/im/vib/vnf_managers/Vines", {"vibVnfmInstance":json.dumps(vibVnfmInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("#LOG 1.1.2: RUNNING TEST ROUTINES OF IM/MS\n")

	print("LOG 1.1.2.1: RUNNING TEST ROUTINES OF IM/MS (/im/ms/running_subscription)")
	imRequest = ("/im/ms/running_subscription", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.2.2: RUNNING TEST ROUTINES OF IM/MS (/im/ms/running_subscription/<subscriptionId>)")
	imRequest = ("/im/ms/running_subscription/SUBS01", {"agentArguments":json.dumps([{}]), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH ON:", responseData.content, "[" + str(responseData.status_code) + "]")
	time.sleep(8)
	imRequest = ("/im/ms/running_subscription/SUBS01", {"agentArguments":None, "userAuth":"USER01;AUTH01"})
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH OFF:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.2.3: RUNNING TEST ROUTINES OF IM/MS (/im/ms/subscription)")
	vnfIndicatorNotificationsFilter = AsModels.VnfIndicatorNotificationsFilter().fromData(AsModels.VnfInstanceSubscriptionFilter().fromData([], [], ["VNF01"], []), [], ["CooRunningAgent"])
	vnfIndicatorSubscriptionRequest = AsModels.VnfIndicatorSubscriptionRequest().fromData(vnfIndicatorNotificationsFilter, "http://127.0.0.1:5000/response", None)
	imRequest = ("/im/ms/subscription", {"vnfIndicatorSubscriptionRequest":json.dumps(vnfIndicatorSubscriptionRequest.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	vnfIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromDictionary(json.loads(responseData.content.decode("utf-8")))
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.2.4: RUNNING TEST ROUTINES OF IM/MS (/im/ms/subscription/<subscriptionId>)")
	vnfIndicatorSubscription.callbackUri = "http://127.0.0.1:5001/response"
	imRequest = ("/im/ms/subscription/" + vnfIndicatorSubscription.id, {"vnfIndicatorSubscription":json.dumps(vnfIndicatorSubscription.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.2.5: RUNNING TEST ROUTINES OF IM/MS (/im/ms/agent)")
	vibMaInstance = VibModels.VibMaInstance().fromData("DummyAgent", "AlfaTesting Resources/DummyMonitoringAgent.py", "Click-On-OSv-F")
	imRequest = ("/im/ms/agent", {"vibMaInstance":json.dumps(vibMaInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.2.6: RUNNING TEST ROUTINES OF IM/MS (/im/ms/agent/<agentId>)")
	imRequest = ("/im/ms/agent/DummyAgent", {"vibMaInstance":json.dumps(vibMaInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("#LOG 1.1.3: RUNNING TEST ROUTINES OF IM/AS\n")

	print("LOG 1.1.3.1: RUNNING TEST ROUTINES OF IM/AS (/im/as/authenticator)")
	imRequest = ("/im/as/authenticator", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.2: RUNNING TEST ROUTINES OF IM/AS (/im/as/authenticator/<authenticatorId>)")
	imRequest = ("/im/as/authenticator/PlainText", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.3: RUNNING TEST ROUTINES OF IM/AS (/im/as/running_authenticator)")
	imRequest = ("/im/as/running_authenticator", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.4: RUNNING TEST ROUTINES OF IM/AS (/im/as/running_authenticator/<authenticatorId>)")
	imRequest = ("/im/as/running_authenticator/PlainText", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.5: RUNNING TEST ROUTINES OF IM/AS (/im/as/user)")
	vibUserInstance = VibModels.VibUserInstance().fromData("USER03", "PolentaFrita", "", ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
	imRequest = ("/im/as/user", {"vibUserInstance":json.dumps(vibUserInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.6: RUNNING TEST ROUTINES OF IM/AS (/im/as/user/<userId>)")
	vibUserInstance = VibModels.VibUserInstance().fromData("USER03", "PolentaFrita2", "", ["VLMI", "VPMI", "VFMI", "VII", "VCI", "VNF", "VIB", "MS", "AS", "VS"])
	imRequest = ("/im/as/user/USER03", {"vibUserInstance":json.dumps(vibUserInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1]) #TODO: AJUSTAR ESSA OPERAÇÃO
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.7: RUNNING TEST ROUTINES OF IM/AS (/im/as/credential)")
	vibCredentialInstance = VibModels.VibCredentialInstance().fromData("USER02", "VNF01")
	imRequest = ("/im/as/credential", {"vibCredentialInstance":json.dumps(vibCredentialInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.8: RUNNING TEST ROUTINES OF IM/AS (/im/as/credential/<userId>/<vnfId>)")
	vibCredentialInstance = VibModels.VibCredentialInstance().fromData("USER02", "VNF01")
	imRequest = ("/im/as/credential/USER02/VNF01", {"vibCredentialInstance":json.dumps(vibCredentialInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.9: RUNNING TEST ROUTINES OF IM/AS (/im/as/credential/user/<userId>)")
	imRequest = ("/im/as/credential/user/USER01", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.10: RUNNING TEST ROUTINES OF IM/AS (/im/as/credential/vnf/<vnfId>)")
	imRequest = ("/im/as/credential/vnf/VNF01", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	
	input("\nCONTINUE...")

	print("\nLOG 1.1.3.11: RUNNING TEST ROUTINES OF IM/AS (/im/as/vnfm/running_driver)")
	imRequest = ("/im/as/vnfm/running_driver", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.12: RUNNING TEST ROUTINES OF IM/AS (/im/as/vnfm/running_driver/<vnfmId>)")
	imRequest = ("/im/as/vnfm/running_driver/DummyVnfmDriver", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.13: RUNNING TEST ROUTINES OF IM/AS (/im/as/vnfm/driver)")
	vibVnfmInstance = VibModels.VibVnfmInstance().fromData("Vines", "AlfaTesting Resources/DummyVnfmDriver2.py")
	imRequest = ("/im/as/vnfm/driver", {"vibVnfmInstance":json.dumps(vibVnfmInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.3.14: RUNNING TEST ROUTINES OF IM/AS (/im/as/vnfm/driver/<vnfmId>)")
	imRequest = ("/im/as/vnfm/driver/Vines", {"vibVnfmInstance":json.dumps(vibVnfmInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\n#LOG 1.1.4: RUNNING TEST ROUTINES OF IM/VS")

	print("\nLOG 1.1.4.1: RUNNING TEST ROUTINES OF IM/VS (/im/vs/vnf_instance)")
	vibVnfInstance = VibModels.VibVnfInstance().fromData("VNF03", "127.0.0.1", "Click-On-OSv-F", ["EXT01"], True)
	imRequest = ("/im/vs/vnf_instance", {"vibVnfInstance":json.dumps(vibVnfInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.2: RUNNING TEST ROUTINES OF IM/VS (/im/vs/vnf_instance/<vnfId>)")
	vibVnfInstance = VibModels.VibVnfInstance().fromData("VNF03", "127.0.0.2", "Click-On-OSv-F", ["EXT01"], True)
	imRequest = ("/im/vs/vnf_instance/VNF03", {"vibVnfInstance":json.dumps(vibVnfInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.3: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver)")
	imRequest = ("/im/vs/running_driver", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.4: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver/<platformId>)")
	imRequest = ("/im/vs/running_driver/Click-On-OSv-F", {"userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.5: RUNNING TEST ROUTINES OF IM/VS (/im/vs/driver/)")
	vibPlatformInstance = VibModels.VibPlatformInstance().fromData("Coven-On-OSv", "AlfaTesting Resources/DummyPlatformDriver.py")
	imRequest = ("/im/vs/driver", {"vibPlatformInstance":json.dumps(vibPlatformInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.6: RUNNING TEST ROUTINES OF IM/VS (/im/vs/driver/<vnfId>)")
	vibPlatformInstance = VibModels.VibPlatformInstance().fromData("Coven-On-OSv", "AlfaTesting Resources/DummyPlatformDriver.py")
	imRequest = ("/im/vs/driver/Coven-On-OSv", {"vibPlatformInstance":json.dumps(vibPlatformInstance.toDictionary()), "userAuth":"USER01;AUTH01"})

	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.7: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver/operations)")
	imRequest = ("/im/vs/running_driver/operations", {"userAuth":"USER01;AUTH01"})
	
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.8: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver/operations/monitoring)")
	imRequest = ("/im/vs/running_driver/operations/monitoring", {"userAuth":"USER01;AUTH01"})
	
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.9: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver/operations/modification)")
	imRequest = ("/im/vs/running_driver/operations/modification", {"userAuth":"USER01;AUTH01"})
	
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("\nLOG 1.1.4.10: RUNNING TEST ROUTINES OF IM/VS (/im/vs/running_driver/operations/other)")
	imRequest = ("/im/vs/running_driver/operations/other", {"userAuth":"USER01;AUTH01"})
	
	responseData = requests.get("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#GET:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#POST:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.put("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PUT:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.patch("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#PATCH:", responseData.content, "[" + str(responseData.status_code) + "]")
	responseData = requests.delete("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#DELETE:", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("#LOG 1.2: RUNNING TEST ROUTINES OF VS\n")

	print("#LOG 1.2.1: RUNNING TEST ROUTINES OF VS/Click-On-OSv-F\n")

	print("LOG 1.2.1.1: RUNNING TEST ROUTINES OF VS/Click-On-OSv-F (/vnf/operation/<vnfId>/<operationId>)")
	imRequest = ("/vnf/operation/VNF01/get_click_running", {"operationArguments":json.dumps({}), "userAuth":"USER01;AUTH01"})
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#", responseData.content, "[" + str(responseData.status_code) + "]")

	imRequest = ("/vnf/operation/VNF01/get_click_metrics", {"operationArguments":json.dumps({}), "userAuth":"USER01;AUTH01"})
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#", responseData.content, "[" + str(responseData.status_code) + "]")

	input("\nCONTINUE...")

	print("#LOG 1.2.2: RUNNING TEST ROUTINES OF VS/Click-On-OSv-S\n")

	print("LOG 1.2.1.1: RUNNING TEST ROUTINES OF VS/Click-On-OSv-S (/vnf/operation/<vnfId>/<operationId>)")

	imRequest = ("/vnf/operation/VNF02/get_click_running", {"operationArguments":json.dumps({}), "userAuth":"USER01;AUTH01"})
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#", responseData.content, "[" + str(responseData.status_code) + "]")

	imRequest = ("/vnf/operation/VNF02/get_click_metrics", {"operationArguments":json.dumps({}), "userAuth":"USER01;AUTH01"})
	responseData = requests.post("http://127.0.0.1:9000/" + imRequest[0], params=imRequest[1])
	print("#", responseData.content, "[" + str(responseData.status_code) + "]")

	#DELETE: ALFA TESTING DEFAULT CONFIGURATIONS
	requests.delete("http://127.0.0.1:9000/" + "im/as/vnfm/driver/DummyVnfmDriver", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/vib/subscriptions/SUBS01", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/ms/agent/CooRunning", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/as/credential/USER01/VNF01", params={"userAuth":"admin;admin"})
	requests.delete("http://127.0.0.1:9000/" + "im/as/credential/USER01/VNF02", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/vs/vnf_instance/VNF01", params={"userAuth":"admin;admin"})
	requests.delete("http://127.0.0.1:9000/" + "im/vs/vnf_instance/VNF02", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/vs/driver/Click-On-OSv-F", params={"userAuth":"admin;admin"})
	requests.delete("http://127.0.0.1:9000/" + "im/vs/driver/Click-On-OSv-S", params={"userAuth":"admin;admin"})

	requests.delete("http://127.0.0.1:9000/" + "im/as/user/USER01", params={"userAuth":"admin;admin"})
	requests.delete("http://127.0.0.1:9000/" + "im/as/user/USER02", params={"userAuth":"admin;admin"})

	emsProcess.terminate()
	dummyCooHttp.terminate()
	dummyCooSocket.terminate()
	
