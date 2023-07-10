import statistics
import requests
import socket
import time
import yaml
import json
import sys
import os

def requestEncode(request):

	if len(request) > 50:
		return False
	request = bytearray(request.encode())
	request.extend(bytearray(50 - len(request)))
	return request

def httpRoutine(operation, url, arguments, secondary, rounds, signal):

	measures = []
	responses = []
	content = []

	try:
		if operation == "GET" or operation == "get":
			for r in range(rounds):
				while True:
					mark = time.time()
					if signal:
						data = requests.get(url, data = arguments)
					else:
						data = requests.get(url, params = arguments)
					timing = time.time() - mark
					if data.status_code == 200:
						break
				measures.append(timing)
				responses.append(data.status_code)
				content.append(data.content)
				print(str(r), "MAIN:", data.status_code, ";", data.content)
				if secondary:
					time.sleep(1)
					try:
						while True:
							data = requests.post(secondary)
							print(str(r), "SEC:", data.status_code, ";", data.content)
							break
					except:
						continue
		elif operation == "POST" or operation == "post":
			for r in range(rounds):
				while True:
					mark = time.time()
					if signal:
						data = requests.post(url, data = arguments)
					else:
						data = requests.post(url, params = arguments)
					timing = time.time() - mark
					if data.status_code == 200:
						break
				measures.append(timing)
				responses.append(data.status_code)
				content.append(data.content)
				print(str(r), "MAIN:", data.status_code, ";", data.content)
				if secondary:
					time.sleep(1)
					try:
						while True:
							data = requests.post(secondary)
							print(str(r), "SEC:", data.status_code, ";", data.content)
							break
					except:
						continue
		else:
			return (-2, "THE REQUESTED OPERATION IS NOT SUPPORTED!")
	except Exception as e:
		return (-1, "AN ERROR OCCURED WHILE EXECUTING THE ROUTINE (" + str(e) + ")!")

	return (0, (measures, responses, content))

def socketRoutine(sendIp, sendPort, message, secondary, rounds):

	measures = []
	responses = []
	content = []

	try:
		for r in range(rounds):
			try:
				while True:
					sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sender.settimeout(8.0)
					sender.connect((sendIp, sendPort))
					mark = time.time()
					sender.send(message.encode())
					data = sender.recv(1024)
					timing = time.time() - mark
					break
			except:
				continue
			measures.append(timing)
			responses.append(data)
			print(str(r), "MAIN:", data)
			sender.close()
			if secondary != None:
				time.sleep(1)
				try:
					while True:
						sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
						sender.settimeout(8.0)
						sender.connect((sendIp, sendPort))
						sender.send(secondary.encode())
						data = sender.recv(1024)
						break
				except:
					continue
				print(str(r), "SEC:", data)
				sender.close()

	except Exception as e:
		return (-1, "AN ERROR OCCURED WHILE EXECUTING THE ROUTINE (" + str(e) + ")!")

	return (0, (measures, responses, responses))

def socketPackage(sendIp, sendPort, package, rounds):

	measures = []
	responses = []
	content = []

	if not os.path.isfile(package):
		return "406"
	if not package.endswith(".zip"):
		return "406"

	package = package.replace("\\", "/")
	packageName = package.split("/")[-1]
	fileSize = os.path.getsize(package)
	
	for r in range(rounds):
		while True:
			try:
				sender = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sender.settimeout(8.0)
				sender.connect((sendIp, sendPort))

				fileData = open(package, "rb")

				mark = time.time()
				sender.send(requestEncode("setup|" + packageName + "|" + str(fileSize)))
				while True:
					fileBytes = fileData.read(1024)
					if not fileBytes:
						break
					sender.send(fileBytes)
				response = sender.recv(1024)
				timing = time.time() - mark
				break
			except:
				continue
		measures.append(timing)
		responses.append(response.decode())
		print("MAIN:", r, "--", response)

		sender.close()

	return (0, (measures, responses, responses))

def processResults(measures, responses, output):

	if len(set(responses)) > 1:
		print("WARNING: DIFFERENT RESPONSES OBTAINED FROM THE SAME OPERATION!\n")

	file = open(output, "w+")

	measures.sort()
	discarding = int(len(measures)/10)
	if discarding:
		measures = measures[discarding:-discarding]

	mean = statistics.mean(measures)
	stdev = statistics.stdev(measures)

	file.write("MEAN TIME:;" + str(mean) + "\nSTDEV TIME:;" + str(stdev) + "\nTIMING DATA:;")
	for timing in measures:
		file.write(str(timing) + ";")

print("============================== EXECUTING OPERATIONS LATENCY TEST ==============================")

print("OPERATION: GET -- VNF EXECUTION PLATFORM STATUSES")

'''print("\nClick-On-OSv")
results = httpRoutine("GET", "http://192.168.18.24:8000/click_plugin/running", "", None, 150, False)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COO-Direct.csv")
else:
	print(results[1])

print("\nClick-On-OSv by local EMS")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/ClickOnOSv-VNF/get_click_running", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, None, 150, False)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COO-EMS.csv")
else:
	print(results[1])'''

'''print("\nLEAF")
results = httpRoutine("GET", "http://192.168.18.25:8000/api/emsstatus", "", None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-Leaf-Direct.csv")
else:
	print(results[1])

print("\nLEAF by local EMS")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/Leaf-VNF/get_vnf_status", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-Leaf-EMS.csv")
else:
	print(results[1])'''

'''print("\nCOVEN-HTTP")
results = httpRoutine("GET", "http://192.168.18.23:6667/status/", "", None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COVENHTTP-Direct.csv")
else:
	print(results[1])

print("\nCOVEN-HTTP by local EMS")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-HTTP-VNF/get_status", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COVENHTTP-EMS.csv")
else:
	print(results[1])

print("\nCOVEN-Socket")
results = socketRoutine("192.168.18.23", 6668, "status", None, 150)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COVENSocket-Direct.csv")
else:
	print(results[1])

print("\nCOVEN-Socket by local EMS")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-Socket-VNF/get_status", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Get-Status-COVENSocket-EMS.csv")
else:
	print(results[1])'''

#############################################################################################################################################################

print("\nOPERATION: POST -- VNF SENDING NEW NETWORK FUNCTION")

'''print("\nClick-On-OSv")
function = open("firewall.click", "r")
results = httpRoutine("POST", "http://192.168.18.24:8000/click_plugin/write_file", {"path": "/func.click", "content": str(function.read()).translate(str.maketrans({'"':r'\"'}))}, None, 150, False)
function.close()
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COO-Direct.csv")
else:
	print(results[1])

print("\nClick-On-OSv by local EMS")
function = open("firewall.click", "r")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/ClickOnOSv-VNF/post_nf", {'userAuth': 'admin;admin', 'operationArguments': '{"path": "/func.click", "content": "' + str(function.read()).translate(str.maketrans({'"':r'\"'})) + '"}'}, None, 150, True)
function.close()
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COO-EMS.csv")
else:
	print(results[1])'''

'''print("\nLEAF")
function = open("apache2-vines-leaf.zip", "rb")
results = httpRoutine("POST", "http://192.168.18.25:8000/api/push_vnfp", function.read(), None, 150, True)
function.close()
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-Leaf-Direct.csv")
else:
	print(results[1])

print("\nLEAF by local EMS")
function = open("apache2-vines-leaf.zip", "rb")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/Leaf-VNF/post_vnfp", {'userAuth': 'admin;admin', 'operationArguments': yaml.dump({"package": function.read()})}, None, 150, True)
function.close()
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-Leaf-EMS.csv")
else:
	print(results[1])'''

'''print("\nCOVEN-HTTP")
function = open("/home/research/Desktop/Forwarder.zip", "rb")
results = httpRoutine("POST", "http://192.168.18.23:6667/setup/Forwarder.zip/", function.read(), None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COVENHTTP-Direct.csv")
else:
	print(results[1])

print("\nCOVEN-HTTP by local EMS")
function = open("/home/research/Desktop/Forwarder.zip", "rb")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-HTTP-VNF/post_setup", {'userAuth': 'admin;admin', 'operationArguments': yaml.dump({"name": "Forwarder.zip", "data": function.read()})}, None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COVENHTTP-EMS.csv")
else:
	print(results[1])

print("\nCOVEN-Socket")
results = socketPackage("192.168.18.23", 6668, "/home/research/Desktop/Forwarder.zip", 150)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COVENSocket-Direct.csv")
else:
	print(results[1])

print("\nCOVEN-Socket by local EMS")
function = open("/home/research/Desktop/Forwarder.zip", "rb")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-Socket-VNF/post_setup", {'userAuth': 'admin;admin', 'operationArguments': yaml.dump({"name": "Forwarder.zip", "size": str(os.path.getsize("Forwarder.zip")), "package": function.read()})}, None, 150, True)
if results[0] == 0:
	processResults(results[1][0], results[1][1], "Post-NF-COVENSocket-EMS.csv")
else:
	print(results[1])'''

#############################################################################################################################################################

print("\nOPERATION: POST -- START A NETWORK FUNCTION")

'''print("\nClick-On-OSv")
function = open("firewall.click", "r")
httpRoutine("POST", "http://192.168.18.24:8000/click_plugin/write_file", {"path": "/func.click", "content": str(function.read()).translate(str.maketrans({'"':r'\"'}))}, None, 1, False)
function.close()
results = [[], [], []]
for r in range(15):
	p_results = httpRoutine("POST", "http://192.168.18.24:8000/click_plugin/start", {}, "http://192.168.18.24:8000/click_plugin/stop", 10, False)
	results[0].extend(p_results[1][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
	try:
		requests.post("http://192.168.18.24:8000/os/reboot")
		time.sleep(10)
	except:
		time.sleep(2)
		continue
processResults(results[0], results[1], "Post-Start-COO-Direct.csv")

print("\nClick-On-OSv by local EMS")
function = open("firewall.click", "r")
results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/ClickOnOSv-VNF/post_nf", {'userAuth': 'admin;admin', 'operationArguments': '{"path": "/func.click", "content": "' + str(function.read()).translate(str.maketrans({'"':r'\"'})) + '"}'}, None, 1, True)
function.close()
results = [[], [], []]
for r in range(15):
	p_results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/ClickOnOSv-VNF/post_click_start", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, "http://192.168.18.24:8000/click_plugin/stop", 10, True)
	results[0].extend(p_results[1][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
	try:
		requests.post("http://192.168.18.24:8000/os/reboot")
		time.sleep(10)
	except:
		time.sleep(2)
		continue
processResults(results[0], results[1], "Post-Start-COO-EMS.csv")'''

print("\nLEAF")
function = open("apache2-vines-leaf.zip", "rb")
results = httpRoutine("POST", "http://192.168.18.25:8000/api/push_vnfp", function.read(), None, 1, True)
function.close()
results = [[], [], [], [], []]
for r in range(150):
	print(r)
	p_results_i	= httpRoutine("POST", "http://192.168.18.25:8000/api/install", "", None, 1, True)
	p_results_s = httpRoutine("POST", "http://192.168.18.25:8000/api/start", "", "http://192.168.18.25:8000/api/stop", 1, True)
	results[0].append(p_results_i[1][0][0] + p_results_s[1][0][0])
	results[1].extend(p_results_i[1][1])
	results[2].extend(p_results_i[1][2])
	results[3].extend(p_results_s[1][1])
	results[4].extend(p_results_s[1][2])
	time.sleep(2)
processResults(results[0], results[1], "Post-Start-Leaf-Direct.csv")

print("\nLEAF by local EMS")
function = open("apache2-vines-leaf.zip", "rb")
results = httpRoutine("POST", "http://192.168.18.25:8000/api/push_vnfp", function.read(), None, 1, True)
function.close()
results = [[], [], [], [], []]
for r in range(150):
	print(r)
	p_results_i = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/Leaf-VNF/post_install", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, None, 1, True)
	p_results_s = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/Leaf-VNF/post_start", {'userAuth': 'admin;admin', 'operationArguments': '{}'}, "http://192.168.18.25:8000/api/stop", 1, True)
	results[0].append(p_results_i[1][0][0] + p_results_s[1][0][0])
	results[1].extend(p_results_i[1][1])
	results[2].extend(p_results_i[1][2])
	results[3].extend(p_results_s[1][1])
	results[4].extend(p_results_s[1][2])
	time.sleep(2)
processResults(results[0], results[1], "Post-Start-Leaf-EMS.csv")

'''print("\nCOVEN-HTTP")
socketPackage("192.168.18.23", 6668, "/home/research/Desktop/Forwarder.zip", 1)
results = [[], [], []]
for r in range(150):
	print("MAIN", r)
	p_results = httpRoutine("POST", "http://192.168.18.23:6667/launch/", yaml.dump({"PPS": [{"Framework": "JavaFramework", "NFs":[{"File": "NFPackages/Forwarder/Forward.java", "Order": 1, "Input": 8008, "Output": 8009, "EMA": {"Port": 8020, "Requests": {"Packets": "PP"}}}]}, {"Framework": "ExeFramework", "NFs":[{"File": "NFPackages/Forwarder/ForwardC", "Order": 2, "Input": 8012, "Output": 8013}]}], "VNS": {"Tool": "L2Socket", "Input":["ens4"], "Output":["ens5"]}, "NSHP": False}), None, 1, True)
	time.sleep(1)
	httpRoutine("POST", "http://192.168.18.23:6667/stop/", {}, "http://192.168.18.23:6667/reset/", 1, True)
	time.sleep(2)
	results[0].append(p_results[1][0][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
processResults(results[0], results[1], "Post-Start-COVENHTTP-Direct.csv")

print("\nCOVEN-HTTP by local EMS")
socketPackage("192.168.18.23", 6668, "/home/research/Desktop/Forwarder.zip", 1)
results = [[], [], []]
for r in range(150):
	print("MAIN", r)
	p_results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-HTTP-VNF/post_launch", {'userAuth': 'admin;admin', 'operationArguments': yaml.dump({'package': "{'PPS': [{'Framework': 'JavaFramework', 'NFs':[{'File': 'NFPackages/Forwarder/Forward.java', 'Order': 1, 'Input': 8008, 'Output': 8009, 'EMA': {'Port': 8020, 'Requests': {'Packets': 'PP'}}}]}, {'Framework': 'ExeFramework', 'NFs':[{'File': 'NFPackages/Forwarder/ForwardC', 'Order': 2, 'Input': 8012, 'Output': 8013}]}], 'VNS': {'Tool': 'L2Socket', 'Input':['ens4'], 'Output':['ens5']}, 'NSHP': false}"})}, None, 1, True)
	time.sleep(1)
	httpRoutine("POST", "http://192.168.18.23:6667/stop/", {}, "http://192.168.18.23:6667/reset/", 1, True)
	time.sleep(2)
	results[0].append(p_results[1][0][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
processResults(results[0], results[1], "Post-Start-COVENHTTP-EMS.csv")

print("\nCOVEN-Socket")
socketPackage("192.168.18.23", 6668, "/home/research/Desktop/Forwarder.zip", 1)
results = [[], [], []]
for r in range(150):
	print("MAIN:", r)
	p_results = socketRoutine("192.168.18.23", 6668, "launch|Forwarder", None, 1)
	time.sleep(1)
	httpRoutine("POST", "http://192.168.18.23:6667/stop/", {}, "http://192.168.18.23:6667/reset/", 1, True)
	time.sleep(2)
	results[0].append(p_results[1][0][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
processResults(results[0], results[1], "Post-Start-COVENSocket-Direct.csv")

print("\nCOVEN-Socket by local EMS")
socketPackage("192.168.18.23", 6668, "/home/research/Desktop/Forwarder.zip", 1)
results = [[], [], []]
for r in range(150):
	print("MAIN:", r)
	p_results = httpRoutine("POST", "http://127.0.0.1:9000//vnf/operation/COVEN-Socket-VNF/post_launch", {'userAuth': 'admin;admin', 'operationArguments': yaml.dump({'package': 'Forwarder'})}, None, 1, True)
	time.sleep(1)
	httpRoutine("POST", "http://192.168.18.23:6667/stop/", {}, "http://192.168.18.23:6667/reset/", 1, True)
	time.sleep(2)
	results[0].append(p_results[1][0][0])
	results[1].extend(p_results[1][1])
	results[2].extend(p_results[1][2])
processResults(results[0], results[1], "Post-Start-COVENSocket-EMS.csv")'''

print("\n===============================================================================================")