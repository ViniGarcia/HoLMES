import uuid
import json
import flask
import os.path
import importlib

import AsModels
import IrModels
import VibModels

import IrAgent
import VibManager
import AsAuthAgent

'''
CLASS: OperationAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 05 Nov. 2020
L. UPDATE: 14 Dez. 2020 (Fulber-Garcia; Vs operation access implemented [not
						 tested yet]; Vib credential operations access imple-
						 mented [not tested yet])
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
		-7 -> Invalid data type of asIr
		-8 -> Unavailable authentication attribute
		-9 -> Error during request authentication
		-10 -> Invalid argument type received
		-11 -> Invalid id of VNF provided
		-12 -> Invalid id of indicator provided
		-13 -> Error during VIB table entry creation
		-14 -> Error on database operation
		-15 -> Invalid id of subscription provided
		-16 -> Error on response creation
'''
class OperationAgent:

	__vibManager = None
	__veVnfmEm = None

	__aiAs = None
	__oaAa = None
	__asIr = None

	def __init__(self):
		return

	def setupAgent(self, vibManager, veVnfmEm, aiAs, oaAa, asIr):

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

		if type(asIr) != IrAgent.IrAgent:
			return -7
		self.__asIr = asIr

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
			return -8

		authResult = self.__oaAa.authRequest(operationRequest.authentication)
		if type(authResult) == int:
			return -9

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
		self.__aiAs.add_url_rule("/vlmi/vnf_snapshots/<vnfSnapshotInfoId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_vs_vnfSnapshotID)
		self.__aiAs.add_url_rule("/vlmi/subscriptions", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_subscriptions)
		self.__aiAs.add_url_rule("/vlmi/subscriptions/<subscriptionId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vlmi_s_subscriptionID)
		self.__aiAs.add_url_rule("/vpmi/pm_jobs", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vpmi_pm_jobs)
		self.__aiAs.add_url_rule("/vpmi/pm_jobs/<pmJobId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vpmi_pmj_pmJobID)
		self.__aiAs.add_url_rule("/vpmi/pm_jobs/<pmJobId>/reports/<reportId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vpmi_pmjid_r_reportID)
		self.__aiAs.add_url_rule("/vpmi/thresholds", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vpmi_thresholds)
		self.__aiAs.add_url_rule("/vpmi/thresholds/<thresholdId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vpmi_t_thresholdID)
		self.__aiAs.add_url_rule("/vfmi/alarms", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vfmi_alarms)
		self.__aiAs.add_url_rule("/vfmi/alarms/<alarmId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vfmi_a_alarmID)
		self.__aiAs.add_url_rule("/vfmi/alarms/<alarmId>/escalate", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vfmi_aid_escalate)
		self.__aiAs.add_url_rule("/vfmi/subscriptions", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vfmi_subscriptions)
		self.__aiAs.add_url_rule("/vfmi/subscriptions/<subscriptionId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vfmi_s_subscriptionID)
		
		self.__aiAs.add_url_rule("/vii/indicators", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vii_indicators)
		self.__aiAs.add_url_rule("/vii/indicators/<vnfInstanceId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vii_i_vnfInstanceID)
		self.__aiAs.add_url_rule("/vii/indicators/<vnfInstanceId>/<indicatorId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vii_iid_indicatorID)
		self.__aiAs.add_url_rule("/vii/subscriptions", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vii_subscriptions)
		self.__aiAs.add_url_rule("/vii/subscriptions/<subscriptionId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vii_s_subscriptionID)
		self.__aiAs.add_url_rule("/vci/configuration/<vnfId>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"], view_func=self.vci_configuration)

		
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
	
	def vlmi_vs_vnfSnapshotID(self, vnfSnapshotInfoId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_vs_vnfSnapshotID(vnfSnapshotInfoId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_vs_vnfSnapshotID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_vs_vnfSnapshotID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_vs_vnfSnapshotID()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_vs_vnfSnapshotID(vnfSnapshotInfoId)
	
	def vlmi_subscriptions(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_subscriptions()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_subscriptions(flask.request.values.get("lccnSubscriptionRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_subscriptions()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_subscriptions()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_subscriptions()

	def vlmi_s_subscriptionID(self, subscriptionId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vlmi_s_subscriptionID(subscriptionId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vlmi_s_subscriptionID(subscriptionId)
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vlmi_s_subscriptionID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vlmi_s_subscriptionID()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vlmi_s_subscriptionID()

	def vpmi_pm_jobs(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vpmi_pm_jobs()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vpmi_pm_jobs(flask.request.values.get("createPmJobRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vpmi_pm_jobs()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vpmi_pm_jobs()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vpmi_pm_jobs()

	def vpmi_pmj_pmJobID(self, pmJobId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vpmi_pmj_pmJobID(pmJobId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vpmi_pmj_pmJobID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vpmi_pmj_pmJobID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vpmi_pmj_pmJobID(pmJobId, flask.request.values.get("pmJobModifications"))
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vpmi_pmj_pmJobID(pmJobId)
		
	def vpmi_pmjid_r_reportID(self, pmJobId, reportId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vpmi_pmjid_r_reportID(pmJobId, reportId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vpmi_pmjid_r_reportID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vpmi_pmjid_r_reportID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vpmi_pmjid_r_reportID()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vpmi_pmjid_r_reportID()
	
	def vpmi_thresholds(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vpmi_thresholds()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vpmi_thresholds(flask.request.values.get("createThresholdRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vpmi_thresholds()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vpmi_thresholds()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vpmi_thresholds()

	def vpmi_t_thresholdID(self, thresholdId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vpmi_t_thresholdID(thresholdId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vpmi_t_thresholdID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vpmi_t_thresholdID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vpmi_t_thresholdID(thresholdId, flask.request.values.get("thresholdModifications"))
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vpmi_t_thresholdID(thresholdId)
		
	def vfmi_alarms(self):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vfmi_alarms()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vfmi_alarms()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vfmi_alarms()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vfmi_alarms()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vfmi_alarms()

	def vfmi_a_alarmID(self, alarmId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vfmi_a_alarmID(alarmId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vfmi_a_alarmID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vfmi_a_alarmID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vfmi_a_alarmID(alarmId, flask.request.values.get("alarmModifications"))
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vfmi_a_alarmID()

	def vfmi_aid_escalate(self, alarmId):

		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vfmi_aid_escalate()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vfmi_aid_escalate(alarmId, flask.request.values.get("perceivedSeverityRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vfmi_aid_escalate()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vfmi_aid_escalate()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vfmi_aid_escalate()

	def vfmi_subscriptions(self):
		
		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vfmi_subscriptions()
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vfmi_subscriptions(flask.request.values.get("fmSubscriptionRequest"))
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vfmi_subscriptions()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vfmi_subscriptions()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vfmi_subscriptions()

	def vfmi_s_subscriptionID(self, subscriptionId):
		
		if flask.request.method == "GET":
			return self.__veVnfmEm.get_vfmi_s_subscriptionID(subscriptionId)
		elif flask.request.method == "POST":
			return self.__veVnfmEm.post_vfmi_s_subscriptionID()
		elif flask.request.method == "PUT":
			return self.__veVnfmEm.put_vfmi_s_subscriptionID()
		elif flask.request.method == "PATCH":
			return self.__veVnfmEm.patch_vfmi_s_subscriptionID()
		elif flask.request.method == "DELETE":
			return self.__veVnfmEm.delete_vfmi_s_subscriptionID(subscriptionId)

	def vii_indicators(self):
		
		if flask.request.method == "GET":
			return self.get_vii_indicators()
		elif flask.request.method == "POST":
			return self.post_vii_indicators()
		elif flask.request.method == "PUT":
			return self.put_vii_indicators()
		elif flask.request.method == "PATCH":
			return self.patch_vii_indicators()
		elif flask.request.method == "DELETE":
			return self.delete_vii_indicators()

	def vii_i_vnfInstanceID(self, vnfInstanceId):

		if flask.request.method == "GET":
			result = self.get_vii_i_vnfInstanceID(vnfInstanceId)
			if result == "204":
				return self.vii_i_indicatorID(vnfInstanceId)
			return result
		elif flask.request.method == "POST":
			return self.post_vii_i_vnfInstanceID()
		elif flask.request.method == "PUT":
			return self.put_vii_i_vnfInstanceID()
		elif flask.request.method == "PATCH":
			return self.patch_vii_i_vnfInstanceID()
		elif flask.request.method == "DELETE":
			return self.delete_vii_i_vnfInstanceID()

	def vii_iid_indicatorID(self, vnfInstanceId, indicatorId):

		if flask.request.method == "GET":
			return self.get_vii_iid_indicatorID(vnfInstanceId, indicatorId)
		elif flask.request.method == "POST":
			return self.post_vii_iid_indicatorID()
		elif flask.request.method == "PUT":
			return self.put_vii_iid_indicatorID()
		elif flask.request.method == "PATCH":
			return self.patch_vii_iid_indicatorID()
		elif flask.request.method == "DELETE":
			return self.delete_vii_iid_indicatorID()

	def vii_i_indicatorID(self, indicatorId):

		if flask.request.method == "GET":
			return self.get_vii_i_indicatorID(indicatorId)
		elif flask.request.method == "POST":
			return self.post_vii_i_indicatorID()
		elif flask.request.method == "PUT":
			return self.put_vii_i_indicatorID()
		elif flask.request.method == "PATCH":
			return self.patch_vii_i_indicatorID()
		elif flask.request.method == "DELETE":
			return self.delete_vii_i_indicatorID()
	
	def vii_subscriptions(self):

		if flask.request.method == "GET":
			return self.get_vii_subscriptions()
		elif flask.request.method == "POST":
			return self.post_vii_subscriptions(flask.request.values.get("vnfIndicatorSubscriptionRequest"))
		elif flask.request.method == "PUT":
			return self.put_vii_subscriptions()
		elif flask.request.method == "PATCH":
			return self.patch_vii_subscriptions()
		elif flask.request.method == "DELETE":
			return self.delete_vii_subscriptions()

	def vii_s_subscriptionID(self, subscriptionId):

		if flask.request.method == "GET":
			return self.get_vii_s_subscriptionID(subscriptionId)
		elif flask.request.method == "POST":
			return self.post_vii_s_subscriptionID()
		elif flask.request.method == "PUT":
			return self.put_vii_s_subscriptionID()
		elif flask.request.method == "PATCH":
			return self.patch_vii_s_subscriptionID()
		elif flask.request.method == "DELETE":
			return self.delete_vii_s_subscriptionID(subscriptionId)

	def vci_configuration(self, vnfId):

		if flask.request.method == "GET":
			return self.get_vci_configuration(vnfId)
		elif flask.request.method == "POST":
			return self.post_vci_configuration()
		elif flask.request.method == "PUT":
			return self.put_vci_configuration()
		elif flask.request.method == "PATCH":
			return self.patch_vci_configuration(vnfId, flask.request.values.get("vnfConfigModifications"))
		elif flask.request.method == "DELETE":
			return self.delete_vci_configuration()



	# ================================ Ve-Vnfm-em Operations (VNFM -> EMS) ================================

	'''
	PATH: 		 /vii/indicators
	ACTION: 	 GET
	DESCRIPTION: Query multiple VNF indicators. This resource allows to query all
				 VNF indicators that are known to the API producer.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vii_indicators(self):

		vnfIndicators = []
		vnfPlatforms = {}

		vibVnfInstances = [VibModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		for instance in vibVnfInstances:
			if instance.vnfPlatform in vnfPlatforms:
				operations = vnfPlatforms[instance.vnfPlatform][0]
			else:
				platform = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "post_vs_running_driver", instance.vnfPlatform), "AS", "IM"))
				if type(platform.messageData) == tuple:
					return platform.messageData[0], 400
				operations = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_rdo_monitoring", None), "AS", "IM"))
				if type(operations.messageData) == tuple:
					return platform.messageData[0], 400
				vnfPlatforms[instance.vnfPlatform] = (operations.messageData, platform.messageData)
				operations = operations.messageData

			for indicator in operations:
				result = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.VsData().fromData(instance, vnfPlatforms[instance.vnfPlatform][1], indicator, {}), "AS", "VS"))
				vnfIndicators.append(AsModels.VnfIndicator().fromData(instance.vnfId + ";"+ indicator, indicator, result.messageData, instance.vnfId, {"self":flask.request.host, "vnfInstance":instance.vnfAddress}).toDictionary())

		return json.dumps(vnfIndicators), 200

	'''
	PATH: 		 /vii/indicators
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vii_indicators(self):
		return "NOT AVAILABLE", 405
	def put_vii_indicators(self):
		return "NOT AVAILABLE", 405
	def patch_vii_indicators(self):
		return "NOT AVAILABLE", 405
	def delete_vii_indicators(self):
		return "NOT AVAILABLE", 405
	
	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}
	ACTION: 	 GET
	DESCRIPTION: Query multiple VNF indicators related to one VNF instance. This re-
				 source allows to query all VNF indicators that are known to the API
				 producer.
	ARGUMENT: 	 vnfInstanceId (String)
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vii_i_vnfInstanceID(self, vnfInstanceId):

		if type(vnfInstanceId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		vnfIndicators = []

		instance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(instance) == 0:
			return "204", 200
		instance = VibModels.VibVnfInstance().fromSql(instance[0])

		platform = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "post_vs_running_driver", instance.vnfPlatform), "AS", "IM"))
		if type(platform.messageData) == tuple:
			return platform.messageData[0], 400
		operations = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_rdo_monitoring", None), "AS", "IM"))
		if type(operations.messageData) == tuple:
			return platform.messageData[0], 400

		for indicator in operations.messageData:
			result = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.VsData().fromData(instance, platform.messageData, indicator, {}), "AS", "VS"))
			vnfIndicators.append(AsModels.VnfIndicator().fromData(instance.vnfId + ";"+ indicator, indicator, result.messageData, instance.vnfId, {"self":flask.request.host, "vnfInstance":instance.vnfAddress}).toDictionary())

		return json.dumps(vnfIndicators), 200

	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vii_i_vnfInstanceID(self):
		return "NOT AVAILABLE", 405
	def put_vii_i_vnfInstanceID(self):
		return "NOT AVAILABLE", 405
	def patch_vii_i_vnfInstanceID(self):
		return "NOT AVAILABLE", 405
	def delete_vii_i_vnfInstanceID(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}/{indicatorId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual VNF indicator to one VNF instance.
	ARGUMENT: 	 vnfInstanceId (String), indicatorId (String)
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''		
	def get_vii_iid_indicatorID(self, vnfInstanceId, indicatorId):
		
		if type(vnfInstanceId) != str or type(indicatorId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		instance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(instance) == 0:
			return "ERROR CODE #1 (AS): INSTANCE ELEMENT NOT FOUND", 400
		instance = VibModels.VibVnfInstance().fromSql(instance[0])

		platform = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "post_vs_running_driver", instance.vnfPlatform), "AS", "IM"))
		if type(platform.messageData) == tuple:
			return platform.messageData[0], 400
		operations = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_rdo_monitoring", None), "AS", "IM"))
		if type(operations.messageData) == tuple:
			return platform.messageData[0], 400
		if not indicatorId in operations.messageData:
			return "ERROR CODE #1 (AS): INDICATOR ELEMENT NOT FOUND FOR INSTANCE", 400

		result = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.VsData().fromData(instance, platform.messageData, indicatorId, {}), "AS", "VS"))

		return json.dumps(AsModels.VnfIndicator().fromData(instance.vnfId + ";"+ indicatorId, indicatorId, result.messageData, instance.vnfId, {"self":flask.request.host, "vnfInstance":instance.vnfAddress}).toDictionary()), 200

	'''
	PATH: 		 /vii/indicators/{vnfInstanceId}/{indicatorId}
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vii_iid_indicatorID(self):
		return "NOT AVAILABLE", 405
	def put_vii_iid_indicatorID(self):
		return "NOT AVAILABLE", 405
	def patch_vii_iid_indicatorID(self):
		return "NOT AVAILABLE", 405
	def delete_vii_iid_indicatorID(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /vii/indicators/{indicatorId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual VNF indicator to all VNF instances.
	ARGUMENT: 	 indicatorId (String)
	RETURN: 	 - 200 (HTTP) + VnfIndicator (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vii_i_indicatorID(self, indicatorId):
		
		if type(indicatorId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		vnfIndicators = []
		vnfPlatforms = {}

		vibVnfInstances = [VibModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		for instance in vibVnfInstances:
			if instance.vnfPlatform in vnfPlatforms:
				operations = vnfPlatforms[instance.vnfPlatform][0]
			else:
				platform = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "post_vs_running_driver", instance.vnfPlatform), "AS", "IM"))
				if type(platform.messageData) == tuple:
					return platform.messageData[0], 400
				operations = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_rdo_monitoring", None), "AS", "IM"))
				if type(operations.messageData) == tuple:
					return platform.messageData[0], 400
				vnfPlatforms[instance.vnfPlatform] = (operations.messageData, platform.messageData)
				operations = operations.messageData

			if indicatorId in operations:
				result = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.VsData().fromData(instance, vnfPlatforms[instance.vnfPlatform][1], indicatorId, {}), "AS", "VS"))
				vnfIndicators.append(AsModels.VnfIndicator().fromData(instance.vnfId + ";"+ indicatorId, indicatorId, result.messageData, instance.vnfId, {"self":flask.request.host, "vnfInstance":instance.vnfAddress}).toDictionary())

		return json.dumps(vnfIndicators), 200
	
	'''
	PATH: 		 /vii/indicators/{indicatorId}
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vii_i_indicatorID(self):
		return "NOT AVAILABLE", 405
	def put_vii_i_indicatorID(self):
		return "NOT AVAILABLE", 405
	def patch_vii_i_indicatorID(self):
		return "NOT AVAILABLE", 405
	def delete_vii_i_indicatorID(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /vii/subscriptions
	ACTION: 	 GET
	DESCRIPTION: Query multiple subscriptions of indicators.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfIndicatorSubscription (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vii_subscriptions(self):
		
		subscriptions = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("MS", "get_ms_subscription", None), "AS", "IM"))
		if type(subscriptions.messageData) == list:
			return json.dumps([AsModels.VnfIndicatorSubscription().fromData(s.visId, s.visFilter, s.visCallback, s.visLinks).toDictionary() for s in subscriptions.messageData]), 200
		return subscriptions.messageData[0], 400

	'''
	PATH: 		 /vii/subscriptions
	ACTION: 	 POST
	DESCRIPTION: Subscribe to VNF indicator change notifications.
	ARGUMENT: 	 VnfIndicatorSubscriptionRequest (Class)
	RETURN: 	 - 201 (HTTP) + VnfIndicatorSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def post_vii_subscriptions(self, vnfIndicatorSubscriptionRequest):
		
		try:
			request = AsModels.VnfIndicatorSubscriptionRequest().fromDictionary(json.loads(vnfIndicatorSubscriptionRequest))
		except:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		subscription = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("MS", "post_ms_subscription", request), "AS", "IM"))
		if type(subscription.messageData) == AsModels.VnfIndicatorSubscription:
			subscription.messageData.links["self"] = flask.request.host
			return json.dumps(subscription.messageData.toDictionary()), 201
		return subscription.messageData[0], 400

	'''
	PATH: 		 /vii/subscriptions
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vii_subscriptions(self):
		return "NOT AVAILABLE", 405
	def patch_vii_subscriptions(self):
		return "NOT AVAILABLE", 405
	def delete_vii_subscriptions(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /vii/subscriptions/{subscriptionId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual subscription.
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 200 (HTTP) + VnfIndicatorSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vii_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		subscription = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("MS", "get_mss_subscriptionId", subscriptionId), "AS", "IM"))
		if type(subscription.messageData) == VibModels.VibSubscriptionInstance:
			return json.dumps(AsModels.VnfIndicatorSubscription().fromData(subscription.messageData.visId, subscription.messageData.visFilter, subscription.messageData.visCallback, subscription.messageData.visLinks).toDictionary()), 200
		return subscription.messageData[0], 400

	'''
	PATH: 		 /vii/subscriptions/{subscriptionId}
	ACTION: 	 DELETE
	DESCRIPTION: Terminate a subscription.
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def delete_vii_s_subscriptionID(self, subscriptionId):

		if type(subscriptionId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400
		
		delete = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("MS", "delete_mss_subscriptionId", subscriptionId), "AS", "IM"))
		if type(delete.messageData) == VibModels.VibSubscriptionInstance:
			return "", 204
		return delete.messageData[0], 400

	'''
	PATH: 		 /vii/subscriptions/{subscriptionId}
	N/A ACTIONS: POST, PUT, PATCH
	**Do not change these methods**
	'''
	def post_vii_s_subscriptionID(self):
		return "NOT AVAILABLE", 405
	def put_vii_s_subscriptionID(self):
		return "NOT AVAILABLE", 405
	def patch_vii_s_subscriptionID(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /vci/configuration/{vnfId}
	ACTION: 	 GET
	DESCRIPTION: Read configuration data of a VNF instance and its VNFC
				 instances.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfConfiguration (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def get_vci_configuration(self, vnfId):
		
		if type(vnfId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400

		instance = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_vnfi_instanceId", vnfId), "AS", "IM"))
		if type(instance.messageData) == VibModels.VibVnfInstance:
			return json.dumps(AsModels.VnfConfiguration().fromData(AsModels.VnfConfigurationData().fromData([], None, instance.messageData.toDictionary()), []).toDictionary()), 200
		return instance.messageData[0], 400
		
	'''
	PATH: 		 /vci/configuration/{vnfId}
	ACTION: 	 PATCH
	DESCRIPTION: Set configuration data of a VNF instance and/or its VNFC
				 instances.
	ARGUMENT: 	 VnfConfigModifications (Class)
	RETURN: 	 - 200 (HTTP) + VnfConfigModifications (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 VNFM -> EM
	'''
	def patch_vci_configuration(self, vnfId, vnfConfigModifications):

		if type(vnfId) != str:
			return "ERROR CODE #0 (AS): INVALID ARGUMENTS PROVIDED", 400
		request = AsModels.VnfConfigModifications().fromDictionary(json.loads(vnfConfigModifications))
		


		instance = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "get_vs_vnfi_instanceId", vnfId), "AS", "IM"))
		if type(instance.messageData) != VibModels.VibVnfInstance:
			return delete.messageData[0], 400

		if request.vnfConfigurationData == None or request.vnfConfigurationData.vnfSpecificData == None:
			return "ERROR CODE #2 (AS): MODIFICATIONS NOT SUPPORTED"

		if "vnfAddress" in request.vnfConfigurationData.vnfSpecificData:
			instance.messageData.vnfAddress = request.vnfConfigurationData.vnfSpecificData["vnfAddress"]
		if "vnfPlatform" in request.vnfConfigurationData.vnfSpecificData:
			instance.messageData.vnfPlatform = request.vnfConfigurationData.vnfSpecificData["vnfPlatform"]
		if "vnfExtAgents" in request.vnfConfigurationData.vnfSpecificData:
			instance.messageData.vnfExtAgents = request.vnfConfigurationData.vnfSpecificData["vnfExtAgents"]
		if "vnfAuth" in request.vnfConfigurationData.vnfSpecificData:
			instance.messageData.vnfExtAgents = request.vnfConfigurationData.vnfSpecificData["vnfAuth"]

		instance = self.__asIr.sendMessage(IrModels.IrMessage().fromData(IrModels.IrManagement().fromData("VS", "patch_vib_i_instanceId", instance.messageData), "AS", "IM"))
		if type(instance.messageData) == VibModels.VibVnfInstance:
			return vnfConfigModifications, 200
		return instance.messageData[0], 400

	'''
	PATH: 		 /vci/configuration
	N/A ACTIONS: POST, PUT, DELETE
	**Do not change these methods**
	'''
	def post_vci_configuration(self):
		return "NOT AVAILABLE", 405
	def put_vci_configuration(self):
		return "NOT AVAILABLE", 405
	def delete_vci_configuration(self):
		return "NOT AVAILABLE", 405
	
	#TO DO FOR ALFA.2: IN/OUT METHODS IN DRIVER TO OPERATIONS FROM VNFM TO EM

	# ===================================== VNF Management Operations =====================================
	
	'''
	PATH: 		 /vnf/{vnfId}/{operationId}
	ACTION: 	 POST
	DESCRIPTION: Execute a running VNF operation, it could receive arguments
				 through an dictionary, but it can be an empty dictionary if
				 there is no arguments.
	ARGUMENT: 	 Dictionary (operationArguments)
	RETURN: 	 - 200 (HTTP) + String [1]
				 - Integer error code (HTTP)
	'''
	def post_vnf_operation(self, vnfId, operationId, operationArguments):

		instance = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "get_vib_i_instanceId", vnfId), "AS", "IM")
		if type(instance) == tuple:
			return instance[0]
		platform = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "get_vib_p_platformId", instance.vnfPlatform), "AS", "IM")
		if type(platform) == tuple:
			return platform[0]

		request = IrModels.IrMessage().fromData(IrModels.VsData().fromData(instance, platform, operationId, operationArguments), "AS", "VS")
		result = self.asIr.sendMessage(request)
		if type(result) != IrMessage:
			return ("ERROR CODE #3 (AS): VS ERROR DURING VNF OPERATION", 3), 400

		return result.messageData, 200

	# ===================================== EMS Management Operations =====================================
	
	'''
	PATH: 		 /im/vib/credentials
	ACTION: 	 GET
	DESCRIPTION: Retrieve the available credentials from the VIB
				 database.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VibCredentialInstance [0..N]
				 - Integer error code (HTTP)
	
	'''
	def get_vib_credentials(self):
		
		request = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "get_vib_credentials", None), "AS", "IM")
		credentials = self.asIr.sendMessage(request)
		if type(credentials) == tuple:
			return ("ERROR CODE #3 (AS): IM/VIB ERROR DURING CREDENTIAL OPERATION (" + credentials[1] + ")", 3), 400
		return [json.dumps(c.toDictionary()) for c in credentials], 200

	'''
	PATH: 		 /im/vib/credentials
	ACTION: 	 POST
	DESCRIPTION: Send a new credential instance to the VIB
				 database.
	ARGUMENT: 	 VibCredentialInstance (JSON Dictionary)
	RETURN: 	 - 200 (HTTP) + VibCredentialInstance [1]
				 - Integer error code (HTTP)
	'''
	def post_vib_credentials(self, vibCredentialInstance):
		
		try:
			vibCredentialInstance = VibModels.VibCredentialInstance().fromDictionary(json.loads(vibCredentialInstance))
		except:
			return ("ERROR CODE #0 (AS): INVALID CREDENTIAL INSTANCE PROVIDED", 0), 400

		request = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "post_vib_credentials", vibCredentialInstance), "AS", "IM")
		credential = self.asIr.sendMessage(request)
		if type(credential) == tuple:
			return ("ERROR CODE #3 (AS): IM/VIB ERROR DURING CREDENTIAL OPERATION (" + credential[1] + ")", 3), 400

		return json.dumps(credential.toDictionary())

	'''
	PATH: 		 /im/vib/credentials
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vib_credentials(self):
		return "NOT AVAILABLE", 405
	def patch_vib_credentials(self):
		return "NOT AVAILABLE", 405
	def delete_vib_credentials(self):
		return "NOT AVAILABLE", 405

	'''
	PATH: 		 /im/vib/credentials/{userId}/{vnfId}
	ACTION: 	 GET
	DESCRIPTION: Send a new credential instance to the VIB
				 database.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VibCredentialInstance [1]
				 - Integer error code (HTTP)
	'''
	def get_vib_c_credentialId(self, userId, vnfId):
		
		request = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "get_vib_c_credentialId", (userId, vnfId)), "AS", "IM")
		credential = self.asIr.sendMessage(request)
		if type(credential) == tuple:
			return ("ERROR CODE #3 (AS): IM/VIB ERROR DURING CREDENTIAL OPERATION (" + credential[1] + ")", 3), 400
		return json.dumps(credential.toDictionary())

	'''
	PATH: 		 /im/vib/credentials/{userId}/{vnfId}
	ACTION: 	 PATCH
	DESCRIPTION: Send updates to a credential instance already
				 in the VIB database.
	ARGUMENT: 	 VibCredentialInstance (JSON Dictionary)
	RETURN: 	 - 200 (HTTP) + VibCredentialInstance [1]
				 - Integer error code (HTTP)
	'''
	def patch_vib_c_credentialId(self, userId, vnfId, vibCredentialInstance):
		
		try:
			vibCredentialInstance = VibModels.VibCredentialInstance().fromDictionary(json.loads(vibCredentialInstance))
			if userId != vibCredentialInstance.userId or vnfId != vibCredentialInstance.vnfId:
				return ("ERROR CODE #0 (AS): INVALID CREDENTIAL INSTANCE PROVIDED", 0), 400
		except:
			return ("ERROR CODE #0 (AS): INVALID CREDENTIAL INSTANCE PROVIDED", 0), 400

		request = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "patch_vib_c_credentialId", vibCredentialInstance), "AS", "IM")
		credential = self.asIr.sendMessage(request)
		if type(credential) == tuple:
			return ("ERROR CODE #3 (AS): IM/VIB ERROR DURING CREDENTIAL OPERATION (" + credential[1] + ")", 3), 400

		return json.dumps(credential.toDictionary())

	'''
	PATH: 		 /im/vib/credentials/{userId}/{vnfId}
	ACTION: 	 DELETE
	DESCRIPTION: Delete a credential instance in the VIB data-
				 base.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VibCredentialInstance [1]
				 - Integer error code (HTTP)
	'''
	def delete_vib_c_credentialId(self, userId, vnfId):
		
		request = IrModels.IrMessage().fromData(IrModels.IrManagement("VIB", "delete_vib_c_credentialId", (userId, vnfId)), "AS", "IM")
		credential = self.asIr.sendMessage(request)
		if type(credential) == tuple:
			return ("ERROR CODE #3 (AS): IM/VIB ERROR DURING CREDENTIAL OPERATION (" + credential[1] + ")", 3), 400
		return json.dumps(credential.toDictionary())

	'''
	PATH: 		 /im/vib/credentials/{userId}/{vnfId}
	N/A ACTIONS: POST, PUT
	**Do not change these methods**
	'''
	def post_vib_c_credentialId(self):
		return "NOT AVAILABLE", 405
	def put_vib_c_credentialId(self):
		return "NOT AVAILABLE", 405

	#TO DO FOR ALFA.1