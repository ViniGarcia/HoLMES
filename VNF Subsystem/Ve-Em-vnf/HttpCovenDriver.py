import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import requests

class HttpCovenDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("COVEN")

	def get_p_operations(self):
		opDict = {"post_package":VsModels.PlatformOperation().fromData("post_package", self.post_coven_package, {"name":"", "data":""}),
				  "post_install":VsModels.PlatformOperation().fromData("post_install", self.post_coven_install, {"name":""}),
				  "post_setup":VsModels.PlatformOperation().fromData("post_setup", self.post_coven_setup, {"name":"", "data":""}),
				  "post_nf":VsModels.PlatformOperation().fromData("post_nf", self.post_coven_nf, {"package":""}),
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

		return {"post_package":VsModels.PlatformOperation().fromData("post_package", self.post_coven_package, {"name":"", "data":""}),
				"post_install":VsModels.PlatformOperation().fromData("post_install", self.post_coven_install, {"name":""}),
				"post_setup":VsModels.PlatformOperation().fromData("post_setup", self.post_coven_setup, {"name":"", "data":""}),
				"post_nf":VsModels.PlatformOperation().fromData("post_nf", self.post_coven_nf, {"package":""}),
				"post_start":VsModels.PlatformOperation().fromData("post_start", self.post_coven_start, {}),
				"post_stop":VsModels.PlatformOperation().fromData("post_stop", self.post_coven_stop, {}),
				"post_reset":VsModels.PlatformOperation().fromData("post_reset", self.post_coven_reset, {}),
				"post_off":VsModels.PlatformOperation().fromData("post_off", self.post_coven_off, {})}

	def get_po_other(self):

		opDict = {"get_list":VsModels.PlatformOperation().fromData("get_list", self.get_coven_list, {}),
				  "get_request":VsModels.PlatformOperation().fromData("get_request", self.post_coo_click_stop, {"vnfc":"", "request":""})}
		opDict.update(self.standardOperations)
		return opDict

	def post_coven_package(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/package/" + covenOperationArguments["name"] + "/", data = covenOperationArguments["data"])
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_install(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/install/" + covenOperationArguments["name"] + "/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_setup(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/setup/" + covenOperationArguments["name"] + "/", data = covenOperationArguments["data"])
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_nf(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/configure/", data = covenOperationArguments["package"])
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_start(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/start/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_stop(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/stop/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_reset(self, vibVnfInstance, covenOperationArguments):
		
		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/reset/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_coven_off(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/off/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_coven_status(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/status/")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_coven_list(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/ma/list")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_coven_check(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/ma/check")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_coven_request(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/ma/request/"+ covenOperationArguments["vnfc"] + "/" + covenOperationArguments["request"], data = covenOperationArguments["args"])
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)