import socket

def running():
    return "/click_plugin/running - OK"

def metrics():
	return "/click_plugin/metrics - OK"

vnfSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
vnfSocket.bind(("127.0.0.1", 5005))

print("RUNNING")
while True:

	request = vnfSocket.recvfrom(1024)
	print(request[0].decode("utf-8"), request[1])
	if request[0].decode("utf-8") == "get_click_running":
		vnfSocket.sendto(str.encode(running()), request[1])
	elif request[0].decode("utf-8") == "get_click_metrics":
		vnfSocket.sendto(str.encode(metrics()), request[1])


