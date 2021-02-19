import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import socket
import yaml
import os

class SocketCovenDriver(VnfDriverTemplate.VnfDriverTemplate):

	globalSocket = None

	def __init__(self):
		
		super().__init__("COVEN")
		self.globalSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.globalSocket.bind(("0.0.0.0", 6668))

	def get_p_operations(self):
		opDict = {"post_package":VsModels.PlatformOperation().fromData("post_package", self.post_coven_package, {"package":""}),
				  "post_install":VsModels.PlatformOperation().fromData("post_install", self.post_coven_install, {"package":""}),
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

		if not os.path.isfile(covenOperationArguments["package"]):
			return 406
		if not covenOperationArguments["package"].endswith(".zip"):
			return 406

		covenOperationArguments["package"] = covenOperationArguments["package"].replace("\\", "/")
		packageName = covenOperationArguments["package"].split("/")[-1]

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		fileSize = os.path.getsize(covenOperationArguments["package"])
		fileData = open(covenOperationArguments["package"], "rb")

		self.globalSocket.sendto(("package|" + packageName + "|" + str(fileSize)).encode(), (requestAddress[0], int(requestAddress[1])))
		while True:
			fileBytes = fileData.read(1024)
			if not fileBytes:
				break
			self.globalSocket.sendto(fileBytes, (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def post_coven_install(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto(("install|" + covenOperationArguments["package"]).encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def post_coven_start(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("start".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def post_coven_stop(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("stop".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def post_coven_reset(self, vibVnfInstance, covenOperationArguments):
		
		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("reset".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def post_coven_off(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("off".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def get_coven_status(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("status".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def get_coven_list(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("list".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def get_coven_check(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto("check".encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()

	def get_coven_request(self, vibVnfInstance, covenOperationArguments):

		requestAddress = vibVnfInstance.vnfAddress.split(":")
		self.globalSocket.sendto(("request|" + covenOperationArguments["vnfc"] + "|" + covenOperationArguments["request"] + "|" + yaml.dump(covenOperationArguments["request"])).encode(), (requestAddress[0], int(requestAddress[1])))

		response, server = self.globalSocket.recvfrom(1024)
		return response.decode()