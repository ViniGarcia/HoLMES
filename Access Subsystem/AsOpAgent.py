import uuid
import json
import flask
import os.path
import importlib

import AsModels
import VibModels

import VibManager
import AsAuthAgent

'''
CLASS: OperationAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 05 Nov. 2020
L. UPDATE: 10 Nov. 2020 (Fulber-Garcia; Implementation of get_vii_subscriptions, post_vii_subscriptions, get_vii_s_subscriptionID, delete_vii_s_subscriptionID, get_vci_configuration, patch_vci_configuration)
DESCRIPTION: Operation agent implementation. This class
			 has the kernel functionalites of the access
			 subsystem. It holds the implementation of all
			 the methods provided for external users. We
			 have a natural division of standardized me-
			 thods (Ve-Vnfm-em) and particular methods 
			 of the EMS platform.
CODES:  -1 -> Invalid data type of __vibManager
	    -2 -> Invalid data type of __veVnfmEm
	    -3 -> Invalid driver name of __veVnfmEm
		-4 -> Invalid class instantiation of __veVnfmEm
		-5 -> Invalid data type of aiAs
		-6 -> Invalid data type of oaAa
		-7 -> Unavailable authentication attribute
		-8 -> Error during request authentication
		-9 -> Invalid argument type received
		-10 -> Invalid id of VNF provided
		-11 -> Invalid id of indicator provided
		-12 -> Error during VIB table entry creation
		-13 -> Error on database operation
		-14 -> Invalid id of subscription provided
		-15 -> Error on response creation
'''
class OperationAgent:

	__vibManager = None
	__veVnfmEm = None
	__aiAs = None
	__oaAa = None

	def __init__(self):
		return

	def setupAgent(self, vibManager, veVnfmEm, aiAs, oaAa):

		if type(vibManager) != VibManager.VibManager:
			return -1
		self.__vibManager = vibManager

		if type(veVnfmEm) != str:
			return -2
		if not os.path.isfile("Access Subsystem/Ve-Vnfm-em/" + veVnfmEm + ".py"):
			return -3
		try:
			self.__veVnfmEm = getattr(importlib.import_module("Ve-Vnfm-em." + veVnfmEm), veVnfmEm)()
		except Exception as e:
			return -4

		if type(aiAs) != flask.Flask:
			return -5
		self.__aiAs = aiAs
		self.__setupAccessInterface()

		if type(oaAa) != AsAuthAgent.AuthenticationAgent:
			return -6
		self.__oaAa = oaAa

		return self

	def setupDriver(self, vibVnfmInstance):

		if not os.path.isfile("Access Subsystem/Ve-Vnfm-em/" + vibVnfmInstance.vnfmDriver + ".py"):
			return -3
		try:
			self.__veVnfmEm = getattr(importlib.import_module("Ve-Vnfm-em." + vibVnfmInstance.vnfmDriver), vibVnfmInstance.vnfmDriver)()
		except Exception as e:
			return -4

		return 0

	def getRunningDriver(self):

		if self.__veVnfmEm != None:
			return self.__veVnfmEm.vnfmId

		return None

	def __authenticateRequest(self, operationRequest):
		
		if not hasattr(operationRequest, "authentication"):
			return -7

		authResult = self.__oaAa.authRequest(operationRequest.authentication)
		if type(authResult) == int:
			return -8

		return authResult

	def __setupAccessInterface(self):

		self.__aiAs.add_url_rule("/vlmi/vnf_instances/", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vnfInstances)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vi_vnfInstanceID)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/instantiate", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_instantiate)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/scale", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_scale)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/scale_to_level", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_scaleToLevel)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/change_flavour", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_changeFlavour)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/terminate", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_terminate)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/heal", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_heal)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/operate", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_operate)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/changeExtConn", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_changeExtConn)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/changeVnfPkg", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_changeVnfPkg)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/createSnapshot", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_createSnapshot)
		self.__aiAs.add_url_rule("/vlmi/vnf_instances/<vnfInstanceId>/revertToSnapshot", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_viid_revertToSnapshot)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vnfLcmOpOccs)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vloo_vnfOperationID)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/retry", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vlooid_retry)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/rollback", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vlooid_rollback)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/fail", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vlooid_fail)
		self.__aiAs.add_url_rule("/vlmi/vnf_lcm_op_occs/<vnfLcmOpOccId>/cancel", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vlooid_cancel)
		self.__aiAs.add_url_rule("/vlmi/vnf_snapshots", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vnfSnapshots)

	# ================================ Ve-Vnfm-em Operations (EMS -> VNFM) ================================

	def vlmi_vnfInstances(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vnfInstances()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vnfInstances(flask.request.values.get("createVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vnfInstances()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vnfInstances()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vnfInstances()
	
	def vlmi_vi_vnfInstanceID(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vi_vnfInstanceID(vnfInstanceId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vi_vnfInstanceID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vi_vnfInstanceID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vi_vnfInstanceID(vnfInstanceId, flask.request.values.get("vnfInfoModificationRequest"))
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vi_vnfInstanceID(vnfInstanceId)
	
	def vlmi_viid_instantiate(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_instantiate()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_instantiate(vnfInstanceId, flask.request.values.get("instantiateVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_instantiate()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_instantiate()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_instantiate()

	def vlmi_viid_scale(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_scale()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_scale(vnfInstanceId, flask.request.values.get("scaleVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_scale()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_scale()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_scale()
	
	def vlmi_viid_scaleToLevel(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_scaleToLevel()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_scaleToLevel(vnfInstanceId, flask.request.values.get("scaleVnfToLevelRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_scaleToLevel()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_scaleToLevel()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_scaleToLevel()

	def vlmi_viid_changeFlavour(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_changeFlavour()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_changeFlavour(vnfInstanceId, flask.request.values.get("changeVnfFlavourRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_changeFlavour()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_changeFlavour()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_changeFlavour()
	
	def vlmi_viid_terminate(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_terminate()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_terminate(vnfInstanceId, flask.request.values.get("terminateVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_terminate()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_terminate()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_terminate()
	
	def vlmi_viid_heal(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_heal()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_heal(vnfInstanceId, flask.request.values.get("healVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_heal()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_heal()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_heal()

	def vlmi_viid_operate(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_operate()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_operate(vnfInstanceId, flask.request.values.get("operateVnfRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_operate()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_operate()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_operate()

	def vlmi_viid_changeExtConn(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_changeExtConn()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_changeExtConn(vnfInstanceId, flask.request.values.get("changeExtVnfConnectivityRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_changeExtConn()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_changeExtConn()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_changeExtConn()

	def vlmi_viid_changeVnfPkg(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_changeVnfPkg()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_changeVnfPkg(vnfInstanceId, flask.request.values.get("changeCurrentVnfPkgRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_changeVnfPkg()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_changeVnfPkg()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_changeVnfPkg()

	def vlmi_viid_createSnapshot(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_createSnapshot()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_createSnapshot(vnfInstanceId, flask.request.values.get("createVnfSnapshotRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_createSnapshot()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_createSnapshot()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_createSnapshot()	

	def vlmi_viid_revertToSnapshot(self, vnfInstanceId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_viid_revertToSnapshot()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_viid_revertToSnapshot(vnfInstanceId, flask.request.values.get("revertToVnfSnapshotRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_viid_revertToSnapshot()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_viid_revertToSnapshot()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_viid_revertToSnapshot()

	def vlmi_vnfLcmOpOccs(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vnfLcmOpOccs()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vnfLcmOpOccs()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vnfLcmOpOccs()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vnfLcmOpOccs()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vnfLcmOpOccs()

	def vlmi_vloo_vnfOperationID(self, vnfLcmOpOccId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vloo_vnfOperationID(vnfLcmOpOccId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vloo_vnfOperationID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vloo_vnfOperationID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vloo_vnfOperationID()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vloo_vnfOperationID()	

	def vlmi_vlooid_retry(self, vnfLcmOpOccId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vlooid_retry()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vlooid_retry(vnfLcmOpOccId)
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vlooid_retry()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vlooid_retry()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vlooid_retry()

	def vlmi_vlooid_rollback(self, vnfLcmOpOccId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vlooid_rollback()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vlooid_rollback(vnfLcmOpOccId)
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vlooid_rollback()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vlooid_rollback()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vlooid_rollback()
		
	def vlmi_vlooid_fail(self, vnfLcmOpOccId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vlooid_fail()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vlooid_fail(vnfLcmOpOccId)
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vlooid_fail()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vlooid_fail()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vlooid_fail()

	def vlmi_vlooid_cancel(self, vnfLcmOpOccId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vlooid_cancel()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vlooid_cancel(vnfLcmOpOccId, flask.request.values.get("cancelMode"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vlooid_cancel()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vlooid_cancel()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vlooid_cancel()

	def vlmi_vnfSnapshots(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vnfSnapshots()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vnfSnapshots(flask.request.values.get("createVnfSnapshotInfoRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vnfSnapshots()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vnfSnapshots()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vnfSnapshots()
		
	def get_vlmi_vs_vnfSnapshotID(self, vnfSnapshotInfoId):
		
		if type(vnfSnapshotInfoId) != str:
			return -9

		return self.__veVnfmEm.get_vlmi_vs_vnfSnapshotID(vnfSnapshotInfoId)
		
	def delete_vlmi_vs_vnfSnapshotID(self, vnfSnapshotID):
		
		if type(vnfSnapshotID) != str:
			return -9

		return self.__veVnfmEm.delete_vlmi_vs_vnfSnapshotID(vnfSnapshotID)
		
	def post_vlmi_vs_vnfSnapshotID(self):
		
		return self.__veVnfmEm.post_vlmi_vs_vnfSnapshotID()
		
	def put_vlmi_vs_vnfSnapshotID(self):
		
		return self.__veVnfmEm.put_vlmi_vs_vnfSnapshotID()
		
	def patch_vlmi_vs_vnfSnapshotID(self):
		
		return self.__veVnfmEm.patch_vlmi_vs_vnfSnapshotID()
		
	def get_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.get_vlmi_subscriptions()
		
	def post_vlmi_subscriptions(self, lccnSubscriptionRequest):
		
		if type(lccnSubscriptionRequest) != LccnSubscriptionRequest:
			return -9

		return self.__veVnfmEm.post_vlmi_subscriptions(lccnSubscriptionRequest)
		
	def put_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.put_vlmi_subscriptions()
		
	def patch_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.patch_vlmi_subscriptions()
		
	def delete_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.delete_vlmi_subscriptions()
		
	def get_vlmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		return self.__veVnfmEm.get_vlmi_s_subscriptionID(subscriptionId)
		
	def post_vlmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		return self.__veVnfmEm.post_vlmi_s_subscriptionID(subscriptionId)
		
	def put_vlmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.put_vlmi_s_subscriptionID()
		
	def patch_vlmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.patch_vlmi_s_subscriptionID()
		
	def delete_vlmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.delete_vlmi_s_subscriptionID()
		
	def get_vpmi_pm_jobs(self):
		
		return self.__veVnfmEm.get_vpmi_pm_jobs()
		
	def post_vpmi_pm_jobs(self):
		
		return self.__veVnfmEm.post_vpmi_pm_jobs()
		
	def put_vpmi_pm_jobs(self):
		
		return self.__veVnfmEm.put_vpmi_pm_jobs()
		
	def patch_vpmi_pm_jobs(self):
		
		return self.__veVnfmEm.patch_vpmi_pm_jobs()
		
	def delete_vpmi_pm_jobs(self):
		
		return self.__veVnfmEm.delete_vpmi_pm_jobs()
		
	def get_vpmi_pmj_pmJobID(self, pmJobId):
		
		if type(pmJobId) != str:
			return -9

		return self.__veVnfmEm.get_vpmi_pmj_pmJobID(pmJobID)
		
	def patch_vpmi_pmj_pmJobID(self, pmJobId, pmJobModifications):
		
		if type(pmJobId) != str or type(pmJobModifications) != PmJobModifications:
			return -9

		return self.__veVnfmEm.patch_vpmi_pmj_pmJobID(pmJobID, pmJobModifications)
		
	def delete_vpmi_pmj_pmJobID(self, pmJobId):
		
		if type(pmJobId) != str:
			return -9

		return self.__veVnfmEm.delete_vpmi_pmj_pmJobID(pmJobId)
		
	def post_vpmi_pmj_pmJobID(self):
		
		return self.__veVnfmEm.post_vpmi_pmj_pmJobID()
		
	def put_vpmi_pmj_pmJobID(self):
		
		return self.__veVnfmEm.put_vpmi_pmj_pmJobID()
		
	def get_vpmi_pmjid_r_reportID(self, pmJobId, reportId):
		
		if type(pmJobId) != str or type(reportId) != str:
			return -9

		return self.__veVnfmEm.get_vpmi_pmjid_r_reportID(pmJobId, reportId)
		
	def post_vpmi_pmjid_r_reportID(self):
		
		return self.__veVnfmEm.post_vpmi_pmjid_r_reportID()
		
	def put_vpmi_pmjid_r_reportID(self):
		
		return self.__veVnfmEm.put_vpmi_pmjid_r_reportID()
		
	def patch_vpmi_pmjid_r_reportID(self):
		
		return self.__veVnfmEm.patch_vpmi_pmjid_r_reportID()
		
	def delete_vpmi_pmjid_r_reportID(self):
		
		return self.__veVnfmEm.delete_vpmi_pmjid_r_reportID()
		
	def get_vpmi_thresholds(self):
		
		return self.__veVnfmEm.get_vpmi_thresholds()
		
	def post_vpmi_thresholds(self):
		
		return self.__veVnfmEm.post_vpmi_thresholds()
		
	def put_vpmi_thresholds(self):
		
		return self.__veVnfmEm.put_vpmi_thresholds()
		
	def patch_vpmi_thresholds(self):
		
		return self.__veVnfmEm.patch_vpmi_thresholds()
		
	def delete_vpmi_thresholds(self):
		
		return self.__veVnfmEm.delete_vpmi_thresholds()
		
	def get_vpmi_t_thresholdID(self, thresholdId):
		
		if type(thresholdId) != str:
			return -9

		return self.__veVnfmEm.get_vpmi_t_thresholdID(thresholdId)
		
	def patch_vpmi_t_thresholdID(self, thresholdId, thresholdModifications):
		
		if type(thresholdId) != str and type(thresholdModifications) != ThresholdModifications:
			return -9

		return self.__veVnfmEm.patch_vpmi_t_thresholdID(thresholdId, thresholdModifications)
		
	def delete_vpmi_t_thresholdID(self, thresholdId):
		
		if type(thresholdId) != str:
			return -9

		return self.__veVnfmEm.delete_vpmi_t_thresholdID(thresholdId)
		
	def post_vpmi_t_thresholdID(self):
		
		return self.__veVnfmEm.post_vpmi_t_thresholdID()
		
	def put_vpmi_t_thresholdID(self):
		
		return self.__veVnfmEm.put_vpmi_t_thresholdID()
		
	def get_vfmi_alarms(self):
		
		return self.__veVnfmEm.get_vfmi_alarms()
		
	def post_vfmi_alarms(self):
		
		return self.__veVnfmEm.post_vfmi_alarms()
		
	def put_vfmi_alarms(self):
		
		return self.__veVnfmEm.put_vfmi_alarms()
		
	def patch_vfmi_alarms(self):
		
		return self.__veVnfmEm.patch_vfmi_alarms()
		
	def delete_vfmi_alarms(self):
		
		return self.__veVnfmEm.delete_vfmi_alarms()
		
	def get_vfmi_a_alarmID(self, alarmId):
		
		if type(alarmId) != str:
			return -9

		return self.__veVnfmEm.get_vfmi_a_alarmID(alarmId)
		
	def patch_vfmi_a_alarmID(self, alarmId, alarmModifications):
		
		if type(alarmId) != str and type(alarmModifications) != AlarmModifications:
			return -9

		return self.__veVnfmEm.patch_vfmi_a_alarmID(alarmId, alarmModifications)
		
	def post_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.post_vfmi_a_alarmID()
		
	def put_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.put_vfmi_a_alarmID()
		
	def delete_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.delete_vfmi_a_alarmID()
		
	def post_vfmi_aid_escalate(self, alarmId, perceivedSeverityRequest):
		
		if type(alarmId) != str and type(perceivedSeverityRequest) != PerceivedSeverityRequest:
			return -9

		return self.__veVnfmEm.post_vfmi_aid_escalate(alarmId, perceivedSeverityRequest)
		
	def get_vfmi_aid_escalate(self):
		
		return self.__veVnfmEm.get_vfmi_aid_escalate()
		
	def put_vfmi_aid_escalate(self):
		
		return self.__veVnfmEm.put_vfmi_aid_escalate()
		
	def patch_vfmi_aid_escalate(self):
		
		return self.__veVnfmEm.patch_vfmi_aid_escalate()
		
	def delete_vfmi_aid_escalate(self):
		
		return self.__veVnfmEm.delete_vfmi_aid_escalate()
		
	def get_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.get_vfmi_subscriptions()
		
	def post_vfmi_subscriptions(self, fmSubscriptionRequest):
		
		if type(fmSubscriptionRequest) != FmSubscriptionRequest:
			return -9

		return self.__veVnfmEm.post_vfmi_subscriptions(fmSubscriptionRequest)
		
	def put_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.put_vfmi_subscriptions()
		
	def patch_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.patch_vfmi_subscriptions()
		
	def delete_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.delete_vfmi_subscriptions()
		
	def get_vfmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		return self.__veVnfmEm.get_vfmi_s_subscriptionID(subscriptionId)
		
	def delete_vfmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		return self.__veVnfmEm.delete_vfmi_s_subscriptionID(subscriptionId)
		
	def post_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.post_vfmi_s_subscriptionID()
		
	def put_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.put_vfmi_s_subscriptionID()
		
	def patch_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.patch_vfmi_s_subscriptionID()
	
	# ================================ Ve-Vnfm-em Operations (VNFM -> EMS) ================================

	def get_vii_indicators(self):

		vnfIndicators = []
		vibVnfInstances = [VibModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		
		for vnfInstance in vibVnfInstances:
			#print("TODO - Request the the allocation of the instance platform", vnfInstance.vnfPlatform, "driver") - Router task??
			print("TODO - Send operation to router:", [vnfInstance], "get_vii_i_vnfInstanceID")
			print("TODO - Check if the response is 200")

		return vnfIndicators
	
	def get_vii_i_vnfInstanceID(self, vnfInstanceId):

		if type(vnfInstanceId) != str:
			return -9

		vnfIndicators = []
		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -10
		vibVnfInstance = VibModels.VibVnfInstance().fromSql(vibVnfInstance[0])

		#print("TODO - Request the the allocation of the instance platform", vnfInstance.vnfPlatform, "driver") - Router task??
		print("TODO - Send operation to router:", [vibVnfInstance], "get_vii_i_vnfInstanceID")
		print("TODO - Check if the response is 200")

		return vnfIndicators
		
	def get_vii_iid_indicatorID(self, vnfInstanceId, indicatorId):
		
		if type(vnfInstanceId) != str or type(indicatorId) != str:
			return -9

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -10
		vibVnfInstance = VibModels.VibVnfInstance().fromSql(vibVnfInstance[0])
		
		#print("TODO - Request the the allocation of the instance platform", vnfInstance.vnfPlatform, "driver") - Router task??
		print("TODO - Send operation to router:", [vibVnfInstance, indicatorId], "get_vii_iid_indicatorID")
		print("TODO - Check if the response is 200")

		return None
	
	def get_vii_i_indicatorID(self, indicatorId):
		
		if type(indicatorId) != str:
			return -9

		vnfIndicators = []
		vibVnfInstances = [VibModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		
		for vnfInstance in vibVnfInstances:
			#print("TODO - Request the the allocation of the instance platform", vnfInstance.vnfPlatform, "driver") - Router task??
			print("TODO - Send operation to router:", [vnfInstance, indicatorId], "get_vii_iid_indicatorID")
			print("TODO - Check if the response is 200")

		return vnfIndicators
	
	#TODO: change operation request routine to the Internal Manager
	def get_vii_subscriptions(self):
		
		vibIndicatorSubscriptions = [VibModels.VibVnfIndicatorSubscription().fromSql(vvis) for vvis in self.__vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription;")]	
		return [AsModels.VnfIndicatorSubscription().fromData(vvis.visId, vvis.visFilter, vvis.visCallback, vvis.visLinks) for vvis in vibIndicatorSubscriptions]
	
	#TODO: change operation request routine to the Internal Manager
	def post_vii_subscriptions(self, vnfIndicatorSubscriptionRequest):
		
		if type(vnfIndicatorSubscriptionRequest) != AsModels.VnfIndicatorSubscriptionRequest:
			return -9

		if self.__oaAa.authRequest(vnfIndicatorSubscriptionRequest.authentication) == True:
			vnfIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromData(str(uuid.uuid1()), vnfIndicatorSubscriptionRequest.filter, vnfIndicatorSubscriptionRequest.callbackUri, {"self":"192.168.100:8000"})
			if not vnfIndicatorSubscription:
				return -12
			
			if self.__vibManager.insertVibDatabase(VibModels.VibVnfIndicatorSubscription().fromData(vnfIndicatorSubscription.id, vnfIndicatorSubscription.filter, vnfIndicatorSubscription.callbackUri, vnfIndicatorSubscription.links).toSql()) > 0:
				return 0
			else:
				return -13

		return -8
	
	#TODO: change operation request routine to the Internal Manager
	def get_vii_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		vibIndicatorSubscription = self.__vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription WHERE visId = \"" + subscriptionId + "\";")
		if len(vibIndicatorSubscription) == 0:
			return -14

		if vibIndicatorSubscription[0][1] == None:
			vibIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromData(vibIndicatorSubscription[0][0], vibIndicatorSubscription[0][1], vibIndicatorSubscription[0][2], json.loads(vibIndicatorSubscription[0][3]))
		else:
			vibIndicatorSubscription = AsModels.VnfIndicatorSubscription().fromData(vibIndicatorSubscription[0][0], AsModels.VnfIndicatorNotificationsFilter().fromDictionary(json.loads(vibIndicatorSubscription[0][1])), vibIndicatorSubscription[0][2], json.loads(vibIndicatorSubscription[0][3]))
		
		if vibIndicatorSubscription:
			return vibIndicatorSubscription
		else:
			return -15
	
	#TODO: change operation request routine to the Internal Manager
	def delete_vii_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -9

		if self.__vibManager.deleteVibDatabase("DELETE FROM VnfIndicatorSubscription WHERE visId = \"" + subscriptionId + "\""):
			return 0
		else:
			return -13
	
	def get_vci_configuration(self, vnfId):
		
		if type(vnfId) != str:
			return -9

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -10
		
		print("TODO - Send operation to router:", vibVnfInstance)
		return None
		
	def patch_vci_configuration(self, vnfId, vnfConfigModifications):

		if type(vnfId) != str:
			return -9

		if type(vnfConfigModifications) != VnfConfigModifications:
			return -9

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -10
		
		print("TODO - Send operation to router:", vibVnfInstance, vnfConfigModifications)
		return None
	
	# ===================================== VNF Management Operations =====================================
	#TO DO

	# ===================================== EMS Management Operations =====================================
	#TO DO