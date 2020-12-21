import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import socket

class CooSocketDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("Click-On-OSv")

	def get_p_operations(self):
		opDict = {"get_click_running":VsModels.PlatformOperation().fromData("get_click_running", self.get_coo_click_running, {}),
				  "get_click_metrics":VsModels.PlatformOperation().fromData("get_click_metrics", self.get_coo_click_metrics, {})}
		return opDict

	def get_po_monitoring(self):

		return {"get_click_running":VsModels.PlatformOperation().fromData("get_click_running", self.get_coo_click_running, {}),
				"get_click_metrics":VsModels.PlatformOperation().fromData("get_click_metrics", self.get_coo_click_metrics, {})}

	def get_po_modification(self):

		return {}

	def get_po_other(self):

		return {}

	def get_coo_click_running(self, vibVnfInstance, cooOperationArguments):

		vnfSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		vnfSocket.bind(("127.0.0.1", 8999))
		vnfAddress = vibVnfInstance.vnfAddress.split(":")
		vnfAddress = (vnfAddress[0], int(vnfAddress[1]))

		vnfSocket.sendto(str.encode("get_click_running"), vnfAddress)
		return vnfSocket.recvfrom(1024)[0]

	def get_coo_click_metrics(self, vibVnfInstance, cooOperationArguments):

		vnfSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
		vnfSocket.bind(("127.0.0.1", 8999))
		vnfAddress = vibVnfInstance.vnfAddress.split(":")
		vnfAddress = (vnfAddress[0], int(vnfAddress[1]))

		vnfSocket.sendto(str.encode("get_click_metrics"), vnfAddress)
		return vnfSocket.recvfrom(1024)[0]