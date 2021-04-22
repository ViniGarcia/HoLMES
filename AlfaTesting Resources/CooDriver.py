import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import requests

class CooDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("Click-On-OSv")

	def get_p_operations(self):
		opDict = {"get_nf":VsModels.PlatformOperation().fromData("get_nf", self.get_coo_nf, {}),
				  "post_nf":VsModels.PlatformOperation().fromData("post_nf", self.post_coo_nf, {"path":"", "content":""}),
				  "get_nf_id":VsModels.PlatformOperation().fromData("get_id_nf", self.get_coo_nf_id, {}),
				  "get_click_version":VsModels.PlatformOperation().fromData("get_click_version", self.get_coo_click_version, {}),
				  "get_click_running":VsModels.PlatformOperation().fromData("get_click_running", self.get_coo_click_running, {}),
				  "get_click_metrics":VsModels.PlatformOperation().fromData("get_click_metrics", self.get_coo_click_metrics, {}),
				  "get_click_log":VsModels.PlatformOperation().fromData("get_click_log", self.get_coo_click_log, {}),
				  "post_click_start":VsModels.PlatformOperation().fromData("post_click_start", self.post_coo_click_start, {}),
				  "post_click_stop":VsModels.PlatformOperation().fromData("post_click_stop", self.post_coo_click_stop, {})}
		opDict.update(self.standardOperations)
		return opDict

	def get_po_monitoring(self):

		return {"get_click_running":VsModels.PlatformOperation().fromData("get_click_running", self.get_coo_click_running, {}),
				"get_click_metrics":VsModels.PlatformOperation().fromData("get_click_metrics", self.get_coo_click_metrics, {})}

	def get_po_modification(self):

		return {"post_nf":VsModels.PlatformOperation().fromData("post_nf", self.post_coo_nf, {"path":"", "content":""}),
				"post_click_start":VsModels.PlatformOperation().fromData("post_click_start", self.post_coo_click_start, {}),
				"post_click_stop":VsModels.PlatformOperation().fromData("post_click_stop", self.post_coo_click_stop, {})}

	def get_po_other(self):

		opDict = {"get_nf":VsModels.PlatformOperation().fromData("get_nf", self.get_coo_nf, {}),
				  "get_nf_id":VsModels.PlatformOperation().fromData("get_id_nf", self.get_coo_nf_id, {}),
				  "get_click_version":VsModels.PlatformOperation().fromData("get_click_version", self.get_coo_click_version, {}),
				  "get_click_log":VsModels.PlatformOperation().fromData("get_click_log", self.get_coo_click_log, {})}
		opDict.update(self.standardOperations)
		return opDict

	def get_coo_nf(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/read_file")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def post_coo_nf(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/write_file", params=cooOperationArguments)
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def get_coo_nf_id(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/vnf_identification")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def get_coo_click_version(self, vibVnfInstance, cooOperationArguments):
		
		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/version")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def get_coo_click_running(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/running")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def get_coo_click_metrics(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/metrics")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def get_coo_click_log(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/log")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def post_coo_click_start(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/start")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code

	def post_coo_click_stop(self, vibVnfInstance, cooOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/stop")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return responseData.status_code