import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import socket
import yaml
import os

class SocketCovenDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("COVEN")

	def get_p_operations(self):
		opDict = {"post_package":VsModels.PlatformOperation().fromData("post_package", self.post_coven_package, {"name":"", "size":"", "package":""}),
				  "post_install":VsModels.PlatformOperation().fromData("post_install", self.post_coven_install, {"package":""}),
				  "post_setup":VsModels.PlatformOperation().fromData("post_setup", self.post_coven_setup, {"name":"", "size":"", "package":""}),
				  "post_configure":VsModels.PlatformOperation().fromData("post_configure", self.post_coven_configure, {"package":""}),
				  "post_start":VsModels.PlatformOperation().fromData("post_start", self.post_coven_start, {}),
				  "post_stop":VsModels.PlatformOperation().fromData("post_stop", self.post_coven_stop, {}),
				  "post_reset":VsModels.PlatformOperation().fromData("post_reset", self.post_coven_reset, {}),
				  "post_off":VsModels.PlatformOperation().fromData("post_off", self.post_coven_off, {}),
				  "get_status":VsModels.PlatformOperation().fromData("get_status", self.get_coven_status, {}),
				  "get_list":VsModels.PlatformOperation().fromData("get_list", self.get_coven_list, {}),
				  "get_check":VsModels.PlatformOperation().fromData("get_check", self.get_coven_check, {}),
				  "get_request":VsModels.PlatformOperation().fromData("get_request", self.get_coven_request, {"vnfc":"", "request":"", "args":{}})}
		opDict.update(self.standardOperations)
		return opDict

	def get_po_monitoring(self):

		return {"get_status":VsModels.PlatformOperation().fromData("get_status", self.get_coven_status, {}),
				"get_check":VsModels.PlatformOperation().fromData("get_check", self.get_coven_check, {})}

	def get_po_modification(self):

		return {"post_package":VsModels.PlatformOperation().fromData("post_package", self.post_coven_package, {"package":""}),
				"post_install":VsModels.PlatformOperation().fromData("post_install", self.post_coven_install, {"package":""}),
				"post_setup":VsModels.PlatformOperation().fromData("post_setup", self.post_coven_setup, {"package":""}),
				"post_configure":VsModels.PlatformOperation().fromData("post_configure", self.post_coven_configure, {"package":""}),
				"post_start":VsModels.PlatformOperation().fromData("post_start", self.post_coven_start, {}),
				"post_stop":VsModels.PlatformOperation().fromData("post_stop", self.post_coven_stop, {}),
				"post_reset":VsModels.PlatformOperation().fromData("post_reset", self.post_coven_reset, {}),
				"post_off":VsModels.PlatformOperation().fromData("post_off", self.post_coven_off, {})}

	def get_po_other(self):

		opDict = {"get_list":VsModels.PlatformOperation().fromData("get_list", self.get_coven_list, {}),
				  "get_request":VsModels.PlatformOperation().fromData("get_request", self.post_coo_click_stop, {"vnfc":"", "request":"", "args":""})}
		opDict.update(self.standardOperations)
		return opDict

	def post_coven_package(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send(("package|" + covenOperationArguments["name"] + "|" + covenOperationArguments["size"]).encode())
		while True:
			if len(covenOperationArguments["package"]) > 1024:
				vnfSocket.send(covenOperationArguments["package"][:1024])
				covenOperationArguments["package"] = covenOperationArguments["package"][1024:]
			else:
				vnfSocket.send(covenOperationArguments["package"])
				break

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_install(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send(("install|" + covenOperationArguments["package"]).encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_setup(self, vibVnfInstance, covenOperationArguments):
		
		response = self.post_coven_package(vibVnfInstance, covenOperationArguments)
		if not response.startswith("200"):
			return response
		covenOperationArguments["package"] = covenOperationArguments["name"]
		return self.post_coven_install(vibVnfInstance, covenOperationArguments)

	def post_coven_configure(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send(("configure|" + covenOperationArguments["package"]).encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_start(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))
		
		vnfSocket.send("start".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_stop(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send("stop".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_reset(self, vibVnfInstance, covenOperationArguments):
		
		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send("reset".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def post_coven_off(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send("off".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def get_coven_status(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send("status".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def get_coven_list(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send("list".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def get_coven_check(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket.send("check".encode())

		response = vnfSocket.recv(1024)
		vnfSocket.close()
		return response.decode()

	def get_coven_request(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		vnfSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		vnfSocket.settimeout(8.0)
		vnfSocket.connect((requestAddress[0], int(requestAddress[1])))

		vnfSocket.send(("request|" + covenOperationArguments["vnfc"] + "|" + covenOperationArguments["request"] + "|" + yaml.dump(covenOperationArguments["request"])).encode())

		response = self.globalSocket.recv(1024)
		vnfSocket.close()
		return response.decode()