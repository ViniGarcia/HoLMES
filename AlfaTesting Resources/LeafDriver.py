import AsModels
import VsModels
import VibModels
import VnfDriverTemplate

import requests

class LeafDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("Leaf")

	def get_p_operations(self):
		opDict = {"get_vnf_status":VsModels.PlatformOperation().fromData("get_vnf_status", self.get_leaf_vnf_status, {}),
				  "get_status":VsModels.PlatformOperation().fromData("get_status", self.get_leaf_status, {}),
				  "get_log":VsModels.PlatformOperation().fromData("get_log", self.get_leaf_log, {}),
				  "post_vnfp":VsModels.PlatformOperation().fromData("post_vnfp", self.post_leaf_vnfp, {"package":""}),
				  "post_install":VsModels.PlatformOperation().fromData("post_install", self.post_leaf_install, {}),
				  "post_start":VsModels.PlatformOperation().fromData("post_start", self.post_leaf_start, {}),
				  "post_stop":VsModels.PlatformOperation().fromData("post_stop", self.post_leaf_stop, {})}
		opDict.update(self.standardOperations)
		return opDict

	def get_po_monitoring(self):

		return {"get_vnf_status":VsModels.PlatformOperation().fromData("get_vnf_status", self.get_leaf_vnf_status, {}),
				"get_status":VsModels.PlatformOperation().fromData("get_status", self.get_leaf_status, {})}

	def get_po_modification(self):

		return {"post_vnfp":VsModels.PlatformOperation().fromData("post_vnfp", self.post_leaf_vnfp, {"package":""}),
				"post_install":VsModels.PlatformOperation().fromData("post_install", self.post_leaf_install, {}),
				"post_start":VsModels.PlatformOperation().fromData("post_start", self.post_leaf_start, {}),
				"post_stop":VsModels.PlatformOperation().fromData("post_stop", self.post_leaf_stop, {})}

	def get_po_other(self):

		opDict = {"get_log":VsModels.PlatformOperation().fromData("get_log", self.get_leaf_log, {})}
		opDict.update(self.standardOperations)
		return opDict

	def get_leaf_vnf_status(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/api/emsstatus")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_leaf_status(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/api/running")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def get_leaf_log(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.get("http://" + vibVnfInstance.vnfAddress + "/api/log")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_leaf_vnfp(self, vibVnfInstance, covenOperationArguments):
		
		try:
			packageData = open(covenOperationArguments["package"], 'rb').read()
		except:
			return "400"

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/api/push_vnfp", data = packageData, headers = {'Content-Type': 'application/octet-stream'})
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_leaf_install(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/api/install")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_leaf_start(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/api/start")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

	def post_leaf_stop(self, vibVnfInstance, covenOperationArguments):

		responseData = requests.post("http://" + vibVnfInstance.vnfAddress + "/api/stop")
		if responseData.status_code >= 200 and responseData.status_code < 300:
			return str(responseData.content)
		else:
			return str(responseData.status_code)

#send POST /vnf/operation/<Leaf-VNF>/<get_vnf_status> {}