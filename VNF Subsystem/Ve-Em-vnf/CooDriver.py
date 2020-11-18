import sys
sys.path.insert(0,'../')
sys.path.insert(0,'../../VNF Information Base/')
sys.path.insert(0,'../../Access Subsystem/')

import CommunicationModels
import VibTableModels
import VnfDriverTemplate
import VsModels

import requests

class CooDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		
		super().__init__("Click-On-OSv")

	def get_p_operations(self):
		opDict = {"get_nf":VsModels.PlatformOperation().fromData("get_nf", self.get_coo_nf, {}),
				  "post_nf":VsModels.PlatformOperation().fromData("post_nf", self.post_coo_nf, {"path":"", "content":""}),
				  "get_nf_id":VsModels.PlatformOperation().fromData("get_id_nf", self.get_coo_nf_id, {}),
				  "get_click_version":VsModels.PlatformOperation().fromData("get_click_version", self.get_coo_click_version, {"path":""}),
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

		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/read_file")

	def post_coo_nf(self, vibVnfInstance, cooOperationArguments):

		return requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/write_file", params=cooOperationArguments)

	def get_coo_nf_id(self, vibVnfInstance, cooOperationArguments):

		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/vnf_identification")

	def get_coo_click_version(self, vibVnfInstance, cooOperationArguments):
		
		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/version")

	def get_coo_click_running(self, vibVnfInstance, cooOperationArguments):

		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/running")

	def get_coo_click_metrics(self, vibVnfInstance, cooOperationArguments):

		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/metrics")

	def get_coo_click_log(self, vibVnfInstance, cooOperationArguments):

		return requests.get("http://" + vibVnfInstance.vnfAddress + "/click_plugin/log")

	def post_coo_click_start(self, vibVnfInstance, cooOperationArguments):

		return requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/start")

	def post_coo_click_stop(self, vibVnfInstance, cooOperationArguments):

		return requests.post("http://" + vibVnfInstance.vnfAddress + "/click_plugin/stop")