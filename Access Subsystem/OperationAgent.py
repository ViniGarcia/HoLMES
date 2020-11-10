import sys
sys.path.insert(0,'../VNF Information Base/')

import importlib
import os.path
import uuid
import json

import CommunicationModels
import AuthenticationAgent
import VibTableModels
import VibManager

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
		-5 -> Invalid data type of oaAa
		-6 -> Unavailable authentication attribute
		-7 -> Error during request authentication
		-8 -> Invalid argument type received
		-9 -> Invalid id of VNF provided
		-10 -> Invalid id of indicator provided
		-11 -> Error during VIB table entry creation
		-12 -> Error on database operation
		-13 -> Invalid id of subscription provided
		-14 -> Error on response creation
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
		if not os.path.isfile("Ve-Vnfm-em/" + veVnfmEm + ".py"):
			return -3
		try:
			self.__veVnfmEm = getattr(importlib.import_module("Ve-Vnfm-em." + veVnfmEm), veVnfmEm)(veVnfmEm)
		except:
			return -4

		#TODO: class check
		self.__aiAs = aiAs

		if type(oaAa) != AuthenticationAgent.AuthenticationAgent:
			return -5
		self.__oaAa = oaAa

		return 0

	def __authenticateRequest(self, operationRequest):
		
		if not hasattr(operationRequest, "authentication"):
			return -6

		authResult = self.__oaAa.authRequest(operationRequest.authentication)
		if type(authResult) == int:
			return -7

		return authResult

	# ================================ Ve-Vnfm-em Operations (EMS -> VNFM) ================================

	def get_vlmi_vnfInstances(self):

		return self.__veVnfmEm.get_vlmi_vnfInstances()
		
	def post_vlmi_vnfInstances(self, createVnfRequest):
		
		if type(createVnfRequest) != CreateVnfRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_vnfInstances(createVnfRequest)
		
	def put_vlmi_vnfInstances(self):
		
		return self.__veVnfmEm.put_vlmi_vnfInstances()
		
	def patch_vlmi_vnfInstances(self):

		return self.__veVnfmEm.patch_vlmi_vnfInstances()
		
	def delete_vlmi_vnfInstances(self):

		return self.__veVnfmEm.delete_vlmi_vnfInstances()
		
	def get_vlmi_vi_vnfInstanceID(self, vnfInstanceId):

		if type(vnfInstanceId) != str:
			return -8

		return self.__veVnfmEm.get_vlmi_vi_vnfInstanceID()
		
	def patch_vlmi_vi_vnfInstanceID(self, vnfInstanceId, vnfInfoModificationRequest):

		if type(vnfInstanceId) != str or type(vnfInfoModificationRequest) != VnfInfoModificationRequest:
			return -8

		return self.__veVnfmEm.patch_vlmi_vi_vnfInstanceID(vnfInstanceId, vnfInfoModificationRequest)
		
	def delete_vlmi_vi_vnfInstanceID(self, vnfInstanceId):

		if type(vnfInstanceId) != str:
			return -8

		return self.__veVnfmEm.delete_vlmi_vi_vnfInstanceID(vnfInstanceId)
		
	def post_vlmi_vi_vnfInstanceID(self):

		return self.__veVnfmEm.post_vlmi_vi_vnfInstanceID()
		
	def put_vlmi_vi_vnfInstanceID(self):

		return self.__veVnfmEm.put_vlmi_vi_vnfInstanceID()
		
	def post_vlmi_viid_instantiate(self, vnfInstanceId, instantiateVnfRequest):

		if type(vnfInstanceId) != str or type(instantiateVnfRequest) != InstantiateVnfRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_instantiate(vnfInstanceId, instantiateVnfRequest)
		
	def get_vlmi_viid_instantiate(self):
		
		return self.__veVnfmEm.get_vlmi_viid_instantiate()
		
	def put_vlmi_viid_instantiate(self):

		return self.__veVnfmEm.put_vlmi_viid_instantiate()
		
	def patch_vlmi_viid_instantiate(self):

		return self.__veVnfmEm.patch_vlmi_viid_instantiate()
		
	def delete_vlmi_viid_instantiate(self):

		return self.__veVnfmEm.delete_vlmi_viid_instantiate()
		
	def post_vlmi_viid_scale(self, vnfInstanceId, scaleVnfRequest):

		if type(vnfInstanceId) != str or type(scaleVnfRequest) != ScaleVnfRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_scale(vnfInstanceId, scaleVnfRequest)
		
	def get_vlmi_viid_scale(self):
		
		return self.__veVnfmEm.get_vlmi_viid_scale()
		
	def put_vlmi_viid_scale(self):
		
		return self.__veVnfmEm.put_vlmi_viid_scale()
		
	def patch_vlmi_viid_scale(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_scale()
		
	def delete_vlmi_viid_scale(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_scale()
		
	def post_vlmi_viid_scaleToLevel(self, vnfInstanceId, scaleVnfToLevelRequest):
		
		if type(vnfInstanceId) != str or type(scaleVnfToLevelRequest) != ScaleVnfToLevelRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_scaleToLevel(vnfInstanceId, scaleVnfToLevelRequest)
		
	def get_vlmi_viid_scaleToLevel(self):
		
		return self.__veVnfmEm.get_vlmi_viid_scaleToLevel()
		
	def put_vlmi_viid_scaleToLevel(self):
		
		return self.__veVnfmEm.put_vlmi_viid_scaleToLevel()
		
	def patch_vlmi_viid_scaleToLevel(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_scaleToLevel()
		
	def delete_vlmi_viid_scaleToLevel(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_scaleToLevel()
		
	def post_vlmi_viid_changeFlavour(self, vnfInstanceId, changeVnfFlavourRequest):
		
		if type(vnfInstanceId) != str or type(changeVnfFlavourRequest) != ChangeVnfFlavourRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_changeFlavour(vnfInstanceId, changeVnfFlavourRequest)
		
	def get_vlmi_viid_changeFlavour(self):
		
		return self.__veVnfmEm.get_vlmi_viid_changeFlavour()
		
	def put_vlmi_viid_changeFlavour(self):
		
		return self.__veVnfmEm.put_vlmi_viid_changeFlavour()
		
	def patch_vlmi_viid_changeFlavour(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_changeFlavour()
		
	def delete_vlmi_viid_changeFlavour(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_changeFlavour()
		
	def post_vlmi_viid_terminate(self, vnfInstanceId, terminateVnfRequest):

		if type(vnfInstanceId) != str or type(terminateVnfRequest) != TerminateVnfRequest:
			return -8
		
		return self.__veVnfmEm.post_vlmi_viid_terminate(vnfInstanceId, terminateVnfRequest)
		
	def get_vlmi_viid_terminate(self):
		
		return self.__veVnfmEm.get_vlmi_viid_terminate()
		
	def put_vlmi_viid_terminate(self):
		
		return self.__veVnfmEm.put_vlmi_viid_terminate()
		
	def patch_vlmi_viid_terminate(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_terminate()
		
	def delete_vlmi_viid_terminate(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_terminate()
		
	def post_vlmi_viid_heal(self, vnfInstanceId, healVnfRequest):
		
		if type(vnfInstanceId) != str or type(healVnfRequest) != HealVnfRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_heal(vnfInstanceId, healVnfRequest)
		
	def get_vlmi_viid_heal(self):
		
		return self.__veVnfmEm.get_vlmi_viid_heal()
		
	def put_vlmi_viid_heal(self):
		
		return self.__veVnfmEm.put_vlmi_viid_heal()
		
	def patch_vlmi_viid_heal(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_heal()
		
	def delete_vlmi_viid_heal(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_heal()
		
	def post_vlmi_viid_operate(self, vnfInstanceId, operateVnfRequest):
		
		if type(vnfInstanceId) != str or type(operateVnfRequest) != OperateVnfRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_operate(vnfInstanceId, operateVnfRequest)
		
	def get_vlmi_viid_operate(self):
		
		return self.__veVnfmEm.get_vlmi_viid_operate()
		
	def put_vlmi_viid_operate(self):
		
		return self.__veVnfmEm.put_vlmi_viid_operate()
		
	def patch_vlmi_viid_operate(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_operate()
		
	def delete_vlmi_viid_operate(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_operate()
		
	def post_vlmi_viid_changeExtConn(self, vnfInstanceId, changeExtVnfConnectivityRequest):
		
		if type(vnfInstanceId) != str or type(changeExtVnfConnectivityRequest) != ChangeExtVnfConnectivityRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_changeExtConn(vnfInstanceId, changeExtVnfConnectivityRequest)
		
	def get_vlmi_viid_changeExtConn(self):
		
		return self.__veVnfmEm.get_vlmi_viid_changeExtConn()
		
	def put_vlmi_viid_changeExtConn(self):
		
		return self.__veVnfmEm.put_vlmi_viid_changeExtConn()
		
	def patch_vlmi_viid_changeExtConn(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_changeExtConn()
		
	def delete_vlmi_viid_changeExtConn(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_changeExtConn()
		
	def post_vlmi_viid_changeVnfPkg(self, vnfInstanceId, changeCurrentVnfPkgRequest):
		
		if type(vnfInstanceId) != str or type(changeCurrentVnfPkgRequest) != ChangeCurrentVnfPkgRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_changeVnfPkg(vnfInstanceId, changeCurrentVnfPkgRequest)
		
	def get_vlmi_viid_changeVnfPkg(self):
		
		return self.__veVnfmEm.get_vlmi_viid_changeVnfPkg()
		
	def put_vlmi_viid_changeVnfPkg(self):
		
		return self.__veVnfmEm.put_vlmi_viid_changeVnfPkg()
		
	def patch_vlmi_viid_changeVnfPkg(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_changeVnfPkg()
		
	def delete_vlmi_viid_changeVnfPkg(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_changeVnfPkg()
		
	def post_vlmi_viid_createSnapshot(self, vnfInstanceId, createVnfSnapshotRequest):
		
		if type(vnfInstanceId) != str or type(createVnfSnapshotRequest) != CreateVnfSnapshotRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_createSnapshot(vnfInstanceId, createVnfSnapshotRequest)
		
	def get_vlmi_viid_createSnapshot(self):
		
		return self.__veVnfmEm.get_vlmi_viid_createSnapshot()
		
	def put_vlmi_viid_createSnapshot(self):
		
		return self.__veVnfmEm.put_vlmi_viid_createSnapshot()
		
	def patch_vlmi_viid_createSnapshot(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_createSnapshot()
		
	def delete_vlmi_viid_createSnapshot(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_createSnapshot()
		
	def post_vlmi_viid_revertToSnapshot(self, vnfInstanceId, revertToVnfSnapshotRequest):
		
		if type(vnfInstanceId) != str or type(revertToVnfSnapshotRequest) != RevertToVnfSnapshotRequest:
			return -8

		return self.__veVnfmEm.post_vlmi_viid_revertToSnapshot(vnfInstanceId, revertToVnfSnapshotRequest)
		
	def get_vlmi_viid_revertToSnapshot(self):
		
		return self.__veVnfmEm.get_vlmi_viid_revertToSnapshot()
		
	def put_vlmi_viid_revertToSnapshot(self):
		
		return self.__veVnfmEm.put_vlmi_viid_revertToSnapshot()
		
	def patch_vlmi_viid_revertToSnapshot(self):
		
		return self.__veVnfmEm.patch_vlmi_viid_revertToSnapshot()
		
	def delete_vlmi_viid_revertToSnapshot(self):
		
		return self.__veVnfmEm.delete_vlmi_viid_revertToSnapshot()
		
	def get_vlmi_vnfLcmOpOccs(self):
		
		return self.__veVnfmEm.get_vlmi_vnfLcmOpOccs()
		
	def post_vlmi_vnfLcmOpOccs(self):
		
		return self.__veVnfmEm.post_vlmi_vnfLcmOpOccs()
		
	def put_vlmi_vnfLcmOpOccs(self):
		
		return self.__veVnfmEm.put_vlmi_vnfLcmOpOccs()
		
	def patch_vlmi_vnfLcmOpOccs(self):
		
		return self.__veVnfmEm.patch_vlmi_vnfLcmOpOccs()
		
	def delete_vlmi_vnfLcmOpOccs(self):
		
		return self.__veVnfmEm.delete_vlmi_vnfLcmOpOccs()
		
	def get_vlmi_vloo_vnfOperationID(self, vnfLcmOpOccId):

		if type(vnfLcmOpOccId) != str:
			return -8
		
		return self.__veVnfmEm.get_vlmi_vloo_vnfOperationID(vnfLcmOpOccId)
		
	def post_vlmi_vloo_vnfOperationID(self):
		
		return self.__veVnfmEm.post_vlmi_vloo_vnfOperationID()
		
	def put_vlmi_vloo_vnfOperationID(self):
		
		return self.__veVnfmEm.put_vlmi_vloo_vnfOperationID()
		
	def patch_vlmi_vloo_vnfOperationID(self):
		
		return self.__veVnfmEm.patch_vlmi_vloo_vnfOperationID()
		
	def delete_vlmi_vloo_vnfOperationID(self):
		
		return self.__veVnfmEm.delete_vlmi_vloo_vnfOperationID()
		
	def post_vlmi_vlooid_retry(self, vnfLcmOpOccId):
		
		if type(vnfLcmOpOccId) != str:
			return -8

		return self.__veVnfmEm.post_vlmi_vlooid_retry(vnfLcmOpOccId)
		
	def get_vlmi_vlooid_retry(self):
		
		return self.__veVnfmEm.get_vlmi_vlooid_retry()
		
	def put_vlmi_vlooid_retry(self):
		
		return self.__veVnfmEm.put_vlmi_vlooid_retry()
		
	def patch_vlmi_vlooid_retry(self):
		
		return self.__veVnfmEm.patch_vlmi_vlooid_retry()
		
	def delete_vlmi_vlooid_retry(self):
		
		return self.__veVnfmEm.delete_vlmi_vlooid_retry()
		
	def post_vlmi_vlooid_rollback(self, vnfLcmOpOccId):
		
		if type(vnfLcmOpOccId) != str:
			return -8

		return self.__veVnfmEm.post_vlmi_vlooid_rollback(vnfLcmOpOccId)
		
	def get_vlmi_vlooid_rollback(self):
		
		return self.__veVnfmEm.get_vlmi_vlooid_rollback()
		
	def put_vlmi_vlooid_rollback(self):
		
		return self.__veVnfmEm.put_vlmi_vlooid_rollback()
		
	def patch_vlmi_vlooid_rollback(self):
		
		return self.__veVnfmEm.patch_vlmi_vlooid_rollback()
		
	def delete_vlmi_vlooid_rollback(self):
		
		return self.__veVnfmEm.delete_vlmi_vlooid_rollback()
		
	def post_vlmi_vlooid_fail(self, vnfLcmOpOccId):
		
		if type(vnfLcmOpOccId) != str:
			return -8

		return self.__veVnfmEm.post_vlmi_vlooid_fail(vnfLcmOpOccId)
		
	def get_vlmi_vlooid_fail(self):
		
		return self.__veVnfmEm.get_vlmi_vlooid_fail()
		
	def put_vlmi_vlooid_fail(self):
		
		return self.__veVnfmEm.put_vlmi_vlooid_fail()
		
	def patch_vlmi_vlooid_fail(self):
		
		return self.__veVnfmEm.patch_vlmi_vlooid_fail()
		
	def delete_vlmi_vlooid_fail(self):
		
		return self.__veVnfmEm.delete_vlmi_vlooid_fail()
		
	def post_vlmi_vlooid_cancel(self, vnfLcmOpOccId, cancelMode):
		
		if type(vnfLcmOpOccId) != str or type(cancelMode) != cancelMode:
			return -8

		return self.__veVnfmEm.post_vlmi_vlooid_cancel(vnfLcmOpOccId, cancelMode)
		
	def get_vlmi_vlooid_cancel(self):
		
		return self.__veVnfmEm.get_vlmi_vlooid_cancel()
		
	def put_vlmi_vlooid_cancel(self):
		
		return self.__veVnfmEm.put_vlmi_vlooid_cancel()
		
	def patch_vlmi_vlooid_cancel(self):
		
		return self.__veVnfmEm.patch_vlmi_vlooid_cancel()
		
	def delete_vlmi_vlooid_cancel(self):
		
		return self.__veVnfmEm.delete_vlmi_vlooid_cancel()
		
	def get_vlmi_vnfSnapshots(self):
		
		return self.__veVnfmEm.get_vlmi_vnfSnapshots()
		
	def post_vlmi_vnfSnapshots(self):
		
		return self.__veVnfmEm.post_vlmi_vnfSnapshots()
		
	def put_vlmi_vnfSnapshots(self):
		
		return self.__veVnfmEm.put_vlmi_vnfSnapshots()
		
	def patch_vlmi_vnfSnapshots(self):
		
		return self.__veVnfmEm.patch_vlmi_vnfSnapshots()
		
	def delete_vlmi_vnfSnapshots(self):
		
		return self.__veVnfmEm.delete_vlmi_vnfSnapshots()
		
	def get_vlmi_vs_vnfSnapshotID(self, vnfSnapshotInfoId):
		
		if type(vnfSnapshotInfoId) != str:
			return -8

		return self.__veVnfmEm.get_vlmi_vs_vnfSnapshotID(vnfSnapshotInfoId)
		
	def delete_vlmi_vs_vnfSnapshotID(self, vnfSnapshotID):
		
		if type(vnfSnapshotID) != str:
			return -8

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
			return -8

		return self.__veVnfmEm.post_vlmi_subscriptions(lccnSubscriptionRequest)
		
	def put_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.put_vlmi_subscriptions()
		
	def patch_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.patch_vlmi_subscriptions()
		
	def delete_vlmi_subscriptions(self):
		
		return self.__veVnfmEm.delete_vlmi_subscriptions()
		
	def get_vlmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

		return self.__veVnfmEm.get_vlmi_s_subscriptionID(subscriptionId)
		
	def post_vlmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

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
			return -8

		return self.__veVnfmEm.get_vpmi_pmj_pmJobID(pmJobID)
		
	def patch_vpmi_pmj_pmJobID(self, pmJobId, pmJobModifications):
		
		if type(pmJobId) != str or type(pmJobModifications) != PmJobModifications:
			return -8

		return self.__veVnfmEm.patch_vpmi_pmj_pmJobID(pmJobID, pmJobModifications)
		
	def delete_vpmi_pmj_pmJobID(self, pmJobId):
		
		if type(pmJobId) != str:
			return -8

		return self.__veVnfmEm.delete_vpmi_pmj_pmJobID(pmJobId)
		
	def post_vpmi_pmj_pmJobID(self):
		
		return self.__veVnfmEm.post_vpmi_pmj_pmJobID()
		
	def put_vpmi_pmj_pmJobID(self):
		
		return self.__veVnfmEm.put_vpmi_pmj_pmJobID()
		
	def get_vpmi_pmjid_r_reportID(self, pmJobId, reportId):
		
		if type(pmJobId) != str or type(reportId) != str:
			return -8

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
			return -8

		return self.__veVnfmEm.get_vpmi_t_thresholdID(thresholdId)
		
	def patch_vpmi_t_thresholdID(self, thresholdId, thresholdModifications):
		
		if type(thresholdId) != str and type(thresholdModifications) != ThresholdModifications:
			return -8

		return self.__veVnfmEm.patch_vpmi_t_thresholdID(thresholdId, thresholdModifications)
		
	def delete_vpmi_t_thresholdID(self, thresholdId):
		
		if type(thresholdId) != str:
			return -8

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
			return -8

		return self.__veVnfmEm.get_vfmi_a_alarmID(alarmId)
		
	def patch_vfmi_a_alarmID(self, alarmId, alarmModifications):
		
		if type(alarmId) != str and type(alarmModifications) != AlarmModifications:
			return -8

		return self.__veVnfmEm.patch_vfmi_a_alarmID(alarmId, alarmModifications)
		
	def post_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.post_vfmi_a_alarmID()
		
	def put_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.put_vfmi_a_alarmID()
		
	def delete_vfmi_a_alarmID(self):
		
		return self.__veVnfmEm.delete_vfmi_a_alarmID()
		
	def post_vfmi_aid_escalate(self, alarmId, perceivedSeverityRequest):
		
		if type(alarmId) != str and type(perceivedSeverityRequest) != PerceivedSeverityRequest:
			return -8

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
			return -8

		return self.__veVnfmEm.post_vfmi_subscriptions(fmSubscriptionRequest)
		
	def put_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.put_vfmi_subscriptions()
		
	def patch_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.patch_vfmi_subscriptions()
		
	def delete_vfmi_subscriptions(self):
		
		return self.__veVnfmEm.delete_vfmi_subscriptions()
		
	def get_vfmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

		return self.__veVnfmEm.get_vfmi_s_subscriptionID(subscriptionId)
		
	def delete_vfmi_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

		return self.__veVnfmEm.delete_vfmi_s_subscriptionID(subscriptionId)
		
	def post_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.post_vfmi_s_subscriptionID()
		
	def put_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.put_vfmi_s_subscriptionID()
		
	def patch_vfmi_s_subscriptionID(self):
		
		return self.__veVnfmEm.patch_vfmi_s_subscriptionID()
	
	# ================================ Ve-Vnfm-em Operations (VNFM -> EMS) ================================

	#TODO: change operation request routine to the VNF Driver
	def get_vii_indicators(self):

		vnfIndicators = []
		vibVnfInstances = [VibTableModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		vibPlarformInstances = {vpi[0]:VibTableModels.VibPlatformInstance().fromSql(vpi) for vpi in self.__vibManager.queryVibDatabase("SELECT * FROM PlatformInstance;")}
		
		for vnfInstance in vibVnfInstances:
			vnfPlatform = vibPlarformInstances[vnfInstance.vnfPlatform]
			for vnfOperation in vnfPlatform.monitoringOperations:
				print("TODO - Send operation to router:", vnfInstance.vnfId, vnfOperation)

		return vnfIndicators
	
	#TODO: change operation request routine to the VNF Driver
	def get_vii_i_vnfInstanceID(self, vnfInstanceId):

		if type(vnfInstanceId) != str:
			return -8

		vnfIndicators = []
		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -9
		vibVnfInstance = VibTableModels.VibVnfInstance().fromSql(vibVnfInstance[0])
		vibPlarformInstance = VibTableModels.VibPlatformInstance().fromSql(self.__vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + vibVnfInstance.vnfPlatform + "\";")[0])

		for vnfOperation in vibPlarformInstance.monitoringOperations:
			print("TODO - Send operation to router:", vibVnfInstance.vnfId, vnfOperation)

		return vnfIndicators
	
	#TODO: change operation request routine to the VNF Driver	
	def get_vii_iid_indicatorID(self, vnfInstanceId, indicatorId):
		
		if type(vnfInstanceId) != str or type(indicatorId) != str:
			return -8

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -9
		vibVnfInstance = VibTableModels.VibVnfInstance().fromSql(vibVnfInstance[0])
		vibPlarformInstance = VibTableModels.VibPlatformInstance().fromSql(self.__vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + vibVnfInstance.vnfPlatform + "\";")[0])
		if not indicatorId in vibPlarformInstance.monitoringOperations:
			return -10

		print("TODO - Send operation to router:", vibVnfInstance.vnfId, indicatorId)

		return None
	
	#TODO: change operation request routine to the VNF Driver
	def get_vii_i_indicatorID(self, indicatorId):
		
		if type(indicatorId) != str:
			return -8

		vnfIndicators = []
		vibVnfInstances = [VibTableModels.VibVnfInstance().fromSql(vvi) for vvi in self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")]
		vibPlarformInstances = {vpi[0]:VibTableModels.VibPlatformInstance().fromSql(vpi) for vpi in self.__vibManager.queryVibDatabase("SELECT * FROM PlatformInstance;")}
		
		for vnfInstance in vibVnfInstances:
			if indicatorId in vibPlarformInstances[vnfInstance.vnfPlatform].monitoringOperations:
				print("TODO - Send operation to router:", vnfInstance.vnfId, indicatorId)

		return vnfIndicators
	
	#TODO: change operation request routine to the Internal Manager
	def get_vii_subscriptions(self):
		
		vibIndicatorSubscriptions = [VibTableModels.VibVnfIndicatorSubscription().fromSql(vvis) for vvis in self.__vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription;")]	
		return [CommunicationModels.VnfIndicatorSubscription().fromData(vvis.visId, vvis.visFilter, vvis.visCallback, vvis.visLinks) for vvis in vibIndicatorSubscriptions]
	
	#TODO: change operation request routine to the Internal Manager
	def post_vii_subscriptions(self, vnfIndicatorSubscriptionRequest):
		
		if type(vnfIndicatorSubscriptionRequest) != CommunicationModels.VnfIndicatorSubscriptionRequest:
			return -8

		if self.__oaAa.authRequest(vnfIndicatorSubscriptionRequest.authentication) == True:
			vnfIndicatorSubscription = CommunicationModels.VnfIndicatorSubscription().fromData(str(uuid.uuid1()), vnfIndicatorSubscriptionRequest.filter, vnfIndicatorSubscriptionRequest.callbackUri, {"self":"192.168.100:8000"})
			if not vnfIndicatorSubscription:
				return -11
			
			if self.__vibManager.insertVibDatabase(VibTableModels.VibVnfIndicatorSubscription().fromData(vnfIndicatorSubscription.id, vnfIndicatorSubscription.filter, vnfIndicatorSubscription.callbackUri, vnfIndicatorSubscription.links).toSql()) > 0:
				return 0
			else:
				return -12

		return -7
	
	#TODO: change operation request routine to the Internal Manager
	def get_vii_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

		vibIndicatorSubscription = self.__vibManager.queryVibDatabase("SELECT * FROM VnfIndicatorSubscription WHERE visId = \"" + subscriptionId + "\";")
		if len(vibIndicatorSubscription) == 0:
			return -13

		if vibIndicatorSubscription[0][1] == None:
			vibIndicatorSubscription = CommunicationModels.VnfIndicatorSubscription().fromData(vibIndicatorSubscription[0][0], vibIndicatorSubscription[0][1], vibIndicatorSubscription[0][2], json.loads(vibIndicatorSubscription[0][3]))
		else:
			vibIndicatorSubscription = CommunicationModels.VnfIndicatorSubscription().fromData(vibIndicatorSubscription[0][0], CommunicationModels.VnfIndicatorNotificationsFilter().fromDictionary(json.loads(vibIndicatorSubscription[0][1])), vibIndicatorSubscription[0][2], json.loads(vibIndicatorSubscription[0][3]))
		
		if vibIndicatorSubscription:
			return vibIndicatorSubscription
		else:
			return -14
	
	#TODO: change operation request routine to the Internal Manager
	def delete_vii_s_subscriptionID(self, subscriptionId):
		
		if type(subscriptionId) != str:
			return -8

		if self.__vibManager.deleteVibDatabase("DELETE FROM VnfIndicatorSubscription WHERE visId = \"" + subscriptionId + "\""):
			return 0
		else:
			return -12
	
	def get_vci_configuration(self, vnfId):
		
		if type(vnfId) != str:
			return -8

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -9
		
		print("TODO - Send operation to router:", vibVnfInstance)
		return None
		
	def patch_vci_configuration(self, vnfId, vnfConfigModifications):

		if type(vnfId) != str:
			return -8

		if type(vnfConfigModifications) != VnfConfigModifications:
			return -8

		vibVnfInstance = self.__vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfInstanceId + "\";")
		if len(vibVnfInstance) == 0:
			return -9
		
		print("TODO - Send operation to router:", vibVnfInstance, vnfConfigModifications)
		return None
	
	# ===================================== VNF Management Operations =====================================
	#TO DO

	# ===================================== EMS Management Operations =====================================
	#TO DO


'''#TEMPORARY
vibTester = VibManager.VibManager()
authTester = AuthenticationAgent.AuthenticationAgent("PlainText", vibTester)
operationTester = OperationAgent()
operationTester.setupAgent(vibTester, "VnfmDriverTemplate", None, authTester)
#operationTester.get_vii_indicators()
#operationTester.get_vii_i_vnfInstanceID("VNF01")
#operationTester.get_vii_iid_indicatorID("VNF01", "CPU")
#operationTester.get_vii_i_indicatorID("CPU")
#print(operationTester.post_vii_subscriptions(CommunicationModels.VnfIndicatorSubscriptionRequest().fromData(None, "192.168.0.100:8000", "USER01;BatataFrita")))
#print(operationTester.get_vii_subscriptions()[1].id)
#print(operationTester.get_vii_s_subscriptionID("0a16e784-237f-11eb-b84f-782bcbee2213"))
#print(operationTester.delete_vii_s_subscriptionID("0a16e784-237f-11eb-b84f-782bcbee2213"))'''