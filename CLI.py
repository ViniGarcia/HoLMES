import re
import os
import sys
import cmd
import time
import json
import flask
import socket
import os.path
import getpass
import logging
import readline
import requests
import netifaces
import rlcompleter
import multiprocessing

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

class EmsCli(cmd.Cmd):

	prompt = "HoLMES> "
	user = ""
	password = ""
	address = ""
	exit = False

	operations = {
		"vlmi":{"/vlmi/vnf_instances/":{"GET":[], "POST":["createVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>":{"GET":[], "PATCH":["vnfInfoModificationRequest"], "DELETE":[]},
				"/vlmi/vnf_instances/<vnfInstanceId>/instantiate":{"POST":["instantiateVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/scale":{"POST":["scaleVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/scale_to_level":{"POST":["scaleVnfToLevelRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/change_flavour":{"POST":["changeVnfFlavourRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/terminate":{"POST":["terminateVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/heal":{"POST":["healVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/operate":{"POST":["operateVnfRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/changeExtConn":{"POST":["changeExtVnfConnectivityRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/changeVnfPkg":{"POST":["changeCurrentVnfPkgRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/createSnapshot":{"POST":["createVnfSnapshotRequest"]},
				"/vlmi/vnf_instances/<vnfInstanceId>/revertToSnapshot":{"POST":["revertToVnfSnapshotRequest"]},
				"/vlmi/vnf_lcm_op_occs":{"GET":[]},
				"/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>":{"GET":[]},
				"/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/retry":{"POST":[]},
				"/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/rollback":{"POST":[]},
				"/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/fail":{"POST":[]},
				"/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/cancel":{"POST":["cancelMode"]},
				"/vlmi/vnf_snapshots":{"GET":[], "POST":["createVnfSnapshotInfoRequest"]},
				"/vlmi/vnf_snapshots/<vnfSnapshotInfoId>":{"GET":[], "DELETE":[]},
				"/vlmi/subscriptions":{"GET":[], "POST":["lccnSubscriptionRequest"]},
				"/vlmi/subscriptions/<subscriptionId>":{"GET":[], "POST":[]}
		},
		"vpmi":{"/vpmi/pm_jobs":{"GET":[], "POST":["createPmJobRequest"]},
				"/vpmi/pm_jobs/<pmJobId>":{"GET":[], "PATCH":["pmJobModifications"], "DELETE":[]},
				"/vpmi/pm_jobs/<pmJobId>/reports/<reportId>":{"GET":[]},
				"/vpmi/thresholds":{"GET":[], "POST":["createThresholdRequest"]},
				"/vpmi/thresholds/<thresholdId>":{"GET":[], "POST":["thresholdModifications"], "DELETE":[]}
		},
		"vfmi":{"/vfmi/alarms":{"GET":[]},
				"/vfmi/alarms/<alarmId>":{"GET":[], "PATCH":["alarmModifications"]},
				"/vfmi/alarms/<alarmId>/escalate":{"POST":["perceivedSeverityRequest"]},
				"/vfmi/subscriptions":{"GET":[], "POST":["fmSubscriptionRequest"]},
				"/vfmi/subscriptions/<subscriptionId>":{"GET":[], "DELETE":[]}
		},
		"vii": {"/vii/indicators":{"GET":[]},
				"/vii/indicators/<vnfInstanceId>":{"GET":[]},
				"/vii/indicators/<vnfInstanceId>/<indicatorId>":{"GET":[]},
				"/vii/subscriptions":{"GET":[], "POST":["vnfIndicatorSubscriptionRequest"]},
				"/vii/subscriptions/<subscriptionId>":{"GET":[], "DELETE":[]}
		},
		"vci": {"/vci/configuration/<vnfId>":{"GET":[], "PATCH":["vnfConfigModifications"]}},
		"vib": {"/im/vib/users":{"GET":[], "POST":["vibUserInstance"]},
				"/im/vib/users/<userId>":{"GET":[], "PATCH":["vibUserInstance"], "DELETE":[]},
				"/im/vib/credentials":{"GET":[], "POST":["vibCredentialInstance"]},
				"/im/vib/credentials/<userId>/<vnfId>":{"GET":[], "DELETE":[]},
				"/im/vib/credentials/user/<userId>":{"GET":[]},
				"/im/vib/credentials/vnf/<vnfId>":{"GET":[]},
				"/im/vib/subscriptions":{"GET":[], "POST":["vibSubscriptionInstance"]},
				"/im/vib/subscriptions/<subscriptionId>":{"GET":[], "PATCH":["vibSubscriptionInstance"], "DELETE":[]},
				"/im/vib/management_agents":{"GET":[], "POST":["vibMaInstance"]},
				"/im/vib/management_agents/<agentId>":{"GET":[], "PATCH":["vibMaInstance"], "DELETE":[]},
				"/im/vib/vnf_instances":{"GET":[], "POST":["vibVnfInstance"]},
				"/im/vib/vnf_instances/<vnfId>":{"GET":[], "PATCH":["vibVnfInstance"], "DELETE":[]},
				"/im/vib/platforms":{"GET":[], "POST":["vibPlatformInstance"]},
				"/im/vib/platforms/<platformId>":{"GET":[], "PATCH":["vibPlatformInstance"], "DELETE":[]},
				"/im/vib/vnf_managers":{"GET":[], "POST":["vibVnfmInstance"]},
				"/im/vib/vnf_managers/<managerId>":{"GET":[], "PATCH":["vibVnfmInstance"], "DELETE":[]}
		},
		"ms":  {"/im/ms/running_subscription":{"GET":[]},
				"/im/ms/running_subscription/<subscriptionId>":{"GET":[], "POST":[], "PATCH":["agentArguments"], "DELETE":[]},
				"/im/ms/subscription":{"GET":[], "POST":["vnfIndicatorSubscriptionRequest"]},
				"/im/ms/subscription/<subscriptionId>":{"GET":[], "PATCH":["vnfIndicatorSubscription"], "DELETE":[]},
				"/im/ms/agent":{"GET":[], "POST":["vibMaInstance"]},
				"/im/ms/agent/<agentId>":{"GET":[], "PATCH":["vibMaInstance"], "DELETE":[]}
		},
		"as":   {"/im/as/authenticator":{"GET":[]},
				 "/im/as/authenticator/<authenticatorId>":{"GET":[]},
				 "/im/as/running_authenticator":{"GET":[]},
				 "/im/as/running_authenticator/<authenticatorId>":{"GET":[], "POST":[]},
				 "/im/as/user":{"GET":[], "POST":["vibUserInstance"]},
				 "/im/as/user/<userId>":{"GET":[], "PATCH":["vibUserInstance"], "DELETE":[]},
				 "/im/as/credential":{"GET":[], "POST":["vibCredentialInstance"]},
				 "/im/as/credential/<userId>/<vnfId>":{"GET":[], "DELETE":[]},
				 "/im/as/credential/user/<userId>":{"GET":[]},
				 "/im/as/credential/vnf/<vnfId>":{"GET":[]},
				 "/im/as/vnfm/running_driver":{"GET":[]},
				 "/im/as/vnfm/running_driver/<vnfmId>":{"GET":[], "POST":[]},
				 "/im/as/vnfm/driver":{"GET":[], "POST":["vibVnfmInstance"]},
				 "/im/as/vnfm/driver/<vnfmId>":{"GET":[], "PATCH":["vibVnfmInstance"], "DELETE":[]}
		},
		"vs":   {"/vnf/operation/<vnfId>/<operationId>":{"POST":["operationArguments"]},
				 "/im/vs/vnf_instance":{"GET":[], "POST":["vibVnfInstance"]},
				 "/im/vs/vnf_instance/<instanceId>":{"GET":[], "PATCH":["vibVnfInstance"], "DELETE":[]},
				 "/im/vs/running_driver":{"GET":[]},
				 "/im/vs/running_driver/<platformId>":{"GET":[], "POST":[]},
				 "/im/vs/driver":{"GET":[], "POST":["vibPlatformInstance"]},
				 "/im/vs/driver/<platformId>":{"GET":[], "PATCH":["vibPlatformInstance"], "DELETE":[]},
				 "/im/vs/running_driver/operations":{"GET":[]},
				 "/im/vs/running_driver/operations/monitoring":{"GET":[]},
				 "/im/vs/running_driver/operations/modification":{"GET":[]},
				 "/im/vs/running_driver/operations/other":{"GET":[]}
		}
	}

	def __init__(self, user, password, address):

		super().__init__()
		self.user = user
		self.password = password
		self.address = address
		self.prompt = user + "> "

	def do_help(self, args):

		print("############## Holistic Lightweight and Malleable EMS Solution ###############")
		print("==================================== HELP ====================================")
		print("\tsend $execution $operation $arguments -> Send requests as user to the\n\t\t\t\t\t\t\taccess subsystem")
		print("\t\t$execution = GET | POST | PUT | PATCH | DELETE")
		print("\t\tNOTE: use a double line (||) to separe arguments")
		print("\t\tNOTE: url arguments must be between <>")
		print("")
		print("\tcheck $operation -> Show the required arguments for an operation")
		print("")
		print("\tlist $module -> Show the available standard operations")
		print("\t\t$module = all  -> Show complete operations list")
		print("\t\t$module = vlmi -> Show VLMI module operations list")
		print("\t\t$module = vpmi -> Show VPMI module operations list")
		print("\t\t$module = vfmi -> Show VFMI module operations list")
		print("\t\t$module = vii  -> Show VII module operations list")
		print("\t\t$module = vci  -> Show VCI module operations list")
		print("\t\t$module = vib  -> Show VIB module operations list")
		print("\t\t$module = ms   -> Show MS module operations list")
		print("\t\t$module = as   -> Show AS module operations list")
		print("\t\t$module = vs   -> Show VS module operations list")
		print("")
		print("\tclear -> Clear the console screen")
		print("")
		print("\tlogout -> Logout the current user")
		print("")
		print("\texit -> Turn down the system")
		print("==============================================================================\n")

	def do_send(self, args):

		args = args.split(" ")
		if len(args) > 2:
			args = [args[0], args[1], " ".join(args[2:])]
		elif len(args) < 2:
			print("ERROR: INVALID \"SEND\" OPERATION REQUESTED (TWO OR THREE STRING ARGUMENTS EXPECTED)!\n")
			return

		if not args[0] in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
			print("ERROR: INVALID \"SEND\" OPERATION REQUESTED (INVALID EXECUTION TYPE RECEIVED)!\n")
			return 

		url = re.findall(r"<([^>]*)>", args[1])
		if len(url) > 0:
			args[1] = "/".join(args[1].split("/")[:-len(url)])

		required = None
		for module in self.operations:
			for operation in self.operations[module]:
				if operation.startswith(args[1]):
					check = re.findall(r"<([^>]*)>", operation)
					if len(check) == len(url):
						if not args[0] in self.operations[module][operation]:
							print ("ERROR: INVALID \"SEND\" OPERATION REQUESTED (OPERATION DOES NOT EXIST)!\n")
							return
						if len(url) > 0:
							args[1] = args[1] + "/" + "/".join(url)
						required = self.operations[module][operation][args[0]]
						break
		if required == None:
			print ("ERROR: INVALID \"SEND\" OPERATION REQUESTED (OPERATION DOES NOT EXIST)!\n")
			return

		resources = {"userAuth":self.user + ";" + self.password}
		if len(args) == 3:
			args[2] = args[2].split("||")
			if len(required) != len(args[2]):
				print ("ERROR: INVALID \"SEND\" OPERATION REQUESTED (NUMBER OF ARGUMENTS DO NOT MATCH)!\n")
				return
			for index in range(len(args[2])):
				resources[required[index]] = args[2][index]

		if args[0] == "GET":
			responseData = requests.get("http://"+ self.address + ":9000/" + args[1], params=resources)
		elif args[0] == "POST":
			responseData = requests.post("http://"+ self.address + ":9000/" + args[1], params=resources)
		elif args[0] == "PUT":
			responseData = requests.put("http://"+ self.address + ":9000/" + args[1], params=resources)
		elif args[0] == "PATCH":
			responseData = requests.patch("http://"+ self.address + ":9000/" + args[1], params=resources)
		elif args[0] == "DELETE":
			responseData = requests.delete("http://"+ self.address + ":9000/" + args[1], params=resources)
		print("#RESPONSE:", responseData.content, "[" + str(responseData.status_code) + "]\n")

	def complete_send(self, text, line, begidx, endidx):

		generalContexts = ["vlmi", "vpmi", "vfmi", "vii", "vci", "im"] 
		imContexts = ["vib", "ms", "as", "vs"]

		def next_hierachy(im, text, path, req):

			if im:
				candidates = [o for o in list(self.operations[path[2]].keys()) if o.startswith(text) and req in self.operations[path[2]][o]]
			else:
				candidates = [o for o in list(self.operations[path[1]].keys()) if o.startswith(text) and req in self.operations[path[1]][o]]
			if len(candidates) < 2:
				if text in candidates:
					return []
				else:
					return candidates
			else:
				if not text.endswith("/") and text in candidates:
					return [text, text + "/"]
				else:
					return list(set(["/".join(c.split("/")[:len(path)+1]) for c in candidates]))

		args = line.split(' ')
		if len(args) == 2:
			if len(text) == 0:
				return ["GET", "POST", "PUT", "PATCH", "DELETE"]
			else:
				selection = [a for a in ["GET", "POST", "PUT", "PATCH", "DELETE"] if a.startswith(text)]
				if len(selection) == 1 and selection[0] == text:
					return []
				else:
					return selection
		
		elif len(args) == 3:
			if not args[1] in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
				return []
			if len(text) == 0:
				readline.insert_text("/")
				text = "/"
			if len(text) == 1:
				if text != "/":
					return []
				else:
					return generalContexts
			else:
				path = text.split("/")
				if len(path) == 1:
					return []
				if not path[1] in generalContexts:
					if len(path) == 2:
						return ["/" + a + "/" for a in generalContexts if a.startswith(path[1])]
					else:
						return []
				if len(path) == 2:
					readline.insert_text("/")
					path.append("")
				if len(path) == 3 and path[1] == "im":
					if path[2] == "":
						return imContexts
					else:
						return ["/im/" + a + "/" for a in imContexts if a.startswith(path[2])]
				if path[1] == "im":
					return next_hierachy(True, text, path, args[1])
				else:
					return next_hierachy(False, text, path, args[1])

		elif len(args) == 4:
			if len(text) > 0:
				return []
			if not args[1] in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
				return []
			path = args[2].split("/")
			if len(path) < 3:
				return []
			if path[1] == "im":
				if not path[2] in imContexts:
					return []
				if not args[2] in self.operations[path[2]]:
					return []
				if not args[1] in self.operations[path[2]][args[2]]:
					return []
				return [str(self.operations[path[2]][args[2]][args[1]])]
			else:
				if not path[1] in self.operations:
					return []
				if not args[2] in self.operations[path[1]]:
					return []
				if not args[1] in self.operations[path[1]][args[2]]:
					return []
				return [str(self.operations[path[1]][args[2]][args[1]])]

		return []

	def do_check(self, args):

		for module in self.operations:
			if args in self.operations[module]:
				print("==============================================================================")
				print(args, "-->")
				for execution in self.operations[module][args]:
					print("  ", execution, "- ARGUMENTS:", self.operations[module][args][execution])
				print("==============================================================================\n")
				return

	def complete_check(self, text, line, begidx, endidx):

		def next_hierachy(im, text, path):

			if im:
				candidates = [o for o in list(self.operations[path[2]].keys()) if o.startswith(text)]
			else:
				candidates = [o for o in list(self.operations[path[1]].keys()) if o.startswith(text)]
			if len(candidates) < 2:
				if text in candidates:
					return []
				else:
					return candidates
			else:
				if not text.endswith("/") and text in candidates:
					return [text, text + "/"]
				else:
					return list(set(["/".join(c.split("/")[:len(path)+1]) for c in candidates]))

		generalContexts = ["vlmi", "vpmi", "vfmi", "vii", "vci", "im"] 
		imContexts = ["vib", "ms", "as", "vs"]

		if len(text) == 0:
			readline.insert_text("/")
			text = "/"
		if len(text) == 1:
			if text != "/":
				return []
			else:
				return generalContexts
		else:
			path = text.split("/")
			if len(path) == 1:
				return []
			if not path[1] in generalContexts:
				if len(path) == 2:
					return ["/" + a + "/" for a in generalContexts if a.startswith(path[1])]
				else:
					return []
			if len(path) == 2:
				readline.insert_text("/")
				path.append("")
			if len(path) == 3 and path[1] == "im":
				if path[2] == "":
					return imContexts
				else:
					return ["/im/" + a + "/" for a in imContexts if a.startswith(path[2])]
			if path[1] == "im":
				return next_hierachy(True, text, path)
			else:
				return next_hierachy(False, text, path)

	def do_list(self, args):

		args = args.split(" ")

		if (len(args) == 1 and args[0] == "") or "all" in args:
			args = ["vlmi", "vpmi", "vfmi", "vii", "vci", "vib", "ms", "as", "vs"]
				
		for module in args:
			if module in self.operations:
				print("==============================================================================")
				print("-> MODULE:", module)
				print("-> OPERATIONS: ")
				for operation in self.operations[module]:
					print("  ", operation, "-->") 
					for execution in self.operations[module][operation]:
						print("    ", execution, "- ARGUMENTS:", self.operations[module][operation][execution])
				print("==============================================================================")
		print("")

	def complete_list(self, text, line, begidx, endidx):

		args = ["all", "vlmi", "vpmi", "vfmi", "vii", "vci", "vib", "ms", "as", "vs"]
		if len(text) == 0:
			return args
		else:
			selection = [a for a in args if a.startswith(text)]
			if len(selection) == 1 and selection[0] == text:
				return []
			else:
				return selection

	def do_clear(self, args):
		os.system('cls' if os.name=='nt' else 'clear')

	def do_logout(self, args):
		return True

	def do_exit(self, args):
		self.exit = True
		return True

	def preloop(self):
		try:
			if 'libedit' in readline.__doc__:
				readline.parse_and_bind("bind ^I rl_complete")
			else:
				readline.parse_and_bind("tab: complete")
			readline.set_completer_delims(readline.get_completer_delims().replace('/', ''))
			readline.set_completer_delims(readline.get_completer_delims().replace('<', ''))
			readline.set_completer_delims(readline.get_completer_delims().replace('>', ''))
			readline.set_completer_delims(readline.get_completer_delims().replace('[', ''))
			readline.set_completer_delims(readline.get_completer_delims().replace(']', ''))
			readline.set_history_length(100)
			readline.read_history_file(os.path.abspath(__file__)[:os.path.abspath(__file__).rindex("/")] + "/CLIMEM")
			return True
		except Exception as e:
			return False

	def postloop(self):
		try:
			readline.write_history_file(os.path.abspath(__file__)[:os.path.abspath(__file__).rindex("/")] + "/CLIMEM")
			return True
		except Exception as e:
			return False

def validate(ip):

	for iface in netifaces.interfaces():
		try:
			if ip == netifaces.ifaddresses(iface)[netifaces.AF_INET][0]['addr']:
				return True
		except:
			continue

	return False

def environment(aiIp):
	sys.stdout = open(os.devnull, "w")

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

	asOpAgent.setupAgent(vibManager, "DummyVnfm", aiAgent, asAuthAgent, irAgent)
	imAgent.setupAgent(vibManager, msManager, asAuthAgent, asOpAgent, vsAgent)
	irAgent.setupAgent(imAgent, vsAgent)

	aiAgent.run(host=aiIp, port=9000)

if __name__ == '__main__':

	if len(sys.argv) == 2:
		if validate(sys.argv[1]):
			address = sys.argv[1]
		else:
			print("HoLMES ERROR: INVALID IP PROVIDED!")
			exit()
	elif len(sys.argv) == 1:
		address = socket.gethostbyname(socket.gethostname())
	else:
		print("HoLMES ERROR: INVALID ARGUMENTS PROVIDES (0 OR 1 [IP] ARGUMENT SUPPORTED)!")
		exit()

	emsProcess = multiprocessing.Process(target=environment, args=(address,))
	emsProcess.start()

	print("\n                         ,--,                                          ")    
	print("        ,--,          ,---.'|             ____                           ")
	print("      ,--.'|          |   | :           ,'  , `.    ,---,.  .--.--.      ")
	print("   ,--,  | :          :   : |        ,-+-,.' _ |  ,'  .' | /  /    '.    ")
	print(",---.'|  : '   ,---.  |   ' :     ,-+-. ;   , ||,---.'   ||  :  /`. /    ")
	print("|   | : _' |  '   ,'\\ ;   ; '    ,--.'|'   |  ;||   |   .';  |  |--`    ")
	print(":   : |.'  | /   /   |'   | |__ |   |  ,', |  '::   :  |-,|  :  ;_       ")
	print("|   ' '  ; :.   ; ,. :|   | :.'||   | /  | |  ||:   |  ;/| \\  \\    `.  ")
	print("'   |  .'. |'   | |: :'   :    ;'   | :  | :  |,|   :   .'  `----.   \\  ")
	print("|   | :  | ''   | .; :|   |  ./ ;   . |  ; |--' |   |  |-,  __ \\  \\  | ")
	print("'   : |  : ;|   :    |;   : ;   |   : |  | ,    '   :  ;/| /  /`--'  /   ")
	print("|   | '  ,/  \\   \\  / |   ,/    |   : '  |/     |   |    \'--'.     /  ")
	print(";   : ;--'    `----'  '---'     ;   | |`-'      |   :   .'  `--'---'     ")
	print("|   ,/                          |   ;/          |   | ,'                 ")
	print("'---'                           '---'           `----'                 \n")
                                                                       

	while True:
		print("############## Holistic Lightweight and Malleable EMS Solution ###############")
		print("[Running at " +  address + ":9000]")
		user = input("User: ")
		password = getpass.getpass()
		responseData = requests.get("http://" + address + ":9000/aa/authenticate/" + user + ";" + password)
		if responseData.content.decode("utf-8") == "True":
			print("##############################################################################\n")
			cli = EmsCli(user, password, address)
			cli.cmdloop()
			if cli.exit:
				break
		else:
			print("ERROR: AUTHENTICATION FAILED")
			print("##############################################################################\n")
	
	emsProcess.terminate()