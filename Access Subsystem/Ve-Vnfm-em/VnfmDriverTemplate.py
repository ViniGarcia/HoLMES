'''
CLASS: VnfmDriverTemplate
AUTHOR: Vinicius Fulber-Garcia
CREATION: 21 Oct. 2020
L. UPDATE: 29 Oct. 2020 (Fulber-Garcia; Template refactoring)
DESCRIPTION: Template for the implementation of VNFM drivers that run in the "Access Subsystem"
			 internal module. The drivers must inhert this class and overload the functions that
			 return the HTTP code 501 (Not Implemented).
'''
class VnfmDriverTemplate:
	vnfmId = None

	def __init__(self, vnfmId):
		self.vnfmId = vnfmId
	
	'''
	PATH: 		 /vlmi/vnf_instances/
	ACTION: 	 GET
	DESCRIPTION: Query multiple VNF instances, thus returning information 
				 from the VNFM of all the VNF instances managed by the EMS
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfInstance (Class) [0..N]
	 			 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vnfInstances(self):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/ 
	ACTION: 	 POST
	DESCRIPTION: Create a new "Individual VNF instance" resource in the VNFM
				 and set it to be managed by the EMS as an idle instance (do 
				 not instantiate the VNF, just create the resource).
	ARGUMENT: 	 CreateVnfRequest (Class)
	RETURN: 	 - 201 (HTTP) + VnfInstance (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vnfInstances(self, createVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vlmi_vnfInstances(self):
		return "405"
	def patch_vlmi_vnfInstances(self):
		return "405"
	def delete_vlmi_vnfInstances(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}
	ACTION: 	 GET
	DESCRIPTION: Read an "Individual VNF instance" resource. Return the same
				 information than the "/vnfInstances/" operation, but for
				 a single VNF instance.
	ARGUMENT: 	 vnfInstanceId (String)
	RETURN: 	 - 200 (HTTP) + VnfInstance (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vi_vnfInstanceID(self, vnfInstanceId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId} 
	ACTION: 	 PATCH
	DESCRIPTION: Modify VNF instance information through the replacement of
				 its VNF descriptor. Note that it does not require an update
				 of the runnig instances (the modification occur only in in-
				 formational data).
	ARGUMENT: 	 vnfInstanceId (String), VnfInfoModificationRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def patch_vlmi_vi_vnfInstanceID(self, vnfInstanceId, vnfInfoModificationRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId} 
	ACTION: 	 DELETE
	DESCRIPTION: Delete an "Individual VNF instance" resource. This opera-
				 tion must be used with caution. It is recommended that it
				 can be executed only in inactive VNF instances (avoiding
				 management errors and false alerts triggered by the EMS).
	ARGUMENT: 	 vnfInstanceId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def delete_vlmi_vi_vnfInstanceID(self, vnfInstanceId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId} 
	N/A ACTIONS: POST, PUT
	**Do not change these methods**
	'''
	def post_vlmi_vi_vnfInstanceID(self):
		return "405"
	def put_vlmi_vi_vnfInstanceID(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/instantiate 
	ACTION: 	 POST
	DESCRIPTION: Instantiate an already created and idle "Individual VNF
				 instance".
	ARGUMENT: 	 vnfInstanceId (String), InstantiateVnfRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_instantiate(self, vnfInstanceId, instantiateVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/instantiate
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_instantiate(self):
		return "405"
	def put_vlmi_viid_instantiate(self):
		return "405"
	def patch_vlmi_viid_instantiate(self):
		return "405"
	def delete_vlmi_viid_instantiate(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/scale 
	ACTION: 	 POST
	DESCRIPTION: Scale a VNF instance incrementally. The resource scaling
				 depends on VNFM capacities, but in general it comprehends 
				 memory, disk, and virtualized CPU cores. 
	ARGUMENT: 	 vnfInstanceId (String), ScaleVnfRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_scale(self, vnfInstanceId, scaleVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/scale 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_scale(self):
		return "405"
	def put_vlmi_viid_scale(self):
		return "405"
	def patch_vlmi_viid_scale(self):
		return "405"
	def delete_vlmi_viid_scale(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/scale_to_level 
	ACTION: 	 POST
	DESCRIPTION: Scale a VNF instance to a target level. The levels availa-
				 ble depends on the VNFM platform.
	ARGUMENT: 	 vnfInstanceId (String), ScaleVnfToLevelRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_scaleToLevel(self, vnfInstanceId, scaleVnfToLevelRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/scale_to_level 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_scaleToLevel(self):
		return "405"
	def put_vlmi_viid_scaleToLevel(self):
		return "405"
	def patch_vlmi_viid_scaleToLevel(self):
		return "405"
	def delete_vlmi_viid_scaleToLevel(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_flavour 
	ACTION: 	 POST
	DESCRIPTION: Change the deployment flavour of a VNF instance. Here, we
				 consider that the flavour are previously defined in the VNF
				 descriptor.
	ARGUMENT: 	 vnfInstanceId (String), ChangeVnfFlavourRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_changeFlavour(self, vnfInstanceId, changeVnfFlavourRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_flavour 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_changeFlavour(self):
		return "405"
	def put_vlmi_viid_changeFlavour(self):
		return "405"
	def patch_vlmi_viid_changeFlavour(self):
		return "405"
	def delete_vlmi_viid_changeFlavour(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/terminate
	ACTION: 	 POST
	DESCRIPTION: Terminate a VNF instance. This method regards just to the
				 termination request to the VNFM. Here we do not threat the
				 management termination in the EMS.
	ARGUMENT: 	 vnfInstanceId (String), TerminateVnfRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_terminate(self, vnfInstanceId, terminateVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_flavour 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_terminate(self):
		return "405"
	def put_vlmi_viid_terminate(self):
		return "405"
	def patch_vlmi_viid_terminate(self):
		return "405"
	def delete_vlmi_viid_terminate(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/heal 
	ACTION: 	 POST
	DESCRIPTION: Heal a VNF instance. This method is typically used when the
				 VNF instance do not respond to the EMS or its users. However,
				 the VNFM is the component that decides if a healing process
				 should be really executed.
	ARGUMENT: 	 vnfInstanceId (String), HealVnfRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_heal(self, vnfInstanceId, healVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/heal
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_heal(self):
		return "405"
	def put_vlmi_viid_heal(self):
		return "405"
	def patch_vlmi_viid_heal(self):
		return "405"
	def delete_vlmi_viid_heal(self):
		return "405"

	'''
	PATH: 		 /vnf_instances/{vnfInstanceId}/operate 
	ACTION: 	 POST
	DESCRIPTION: Operate a VNF instance. There is no specific operation defined
				 for this method. Thus, we kept it the most generic as possible. 
	ARGUMENT: 	 vnfInstanceId (String), OperateVnfRequest (Class) 
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_operate(self, vnfInstanceId, operateVnfRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/operate
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_operate(self):
		return "405"
	def put_vlmi_viid_operate(self):
		return "405"
	def patch_vlmi_viid_operate(self):
		return "405"
	def delete_vlmi_viid_operate(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_ext_conn 
	ACTION: 	 POST
	DESCRIPTION: Change the external connectivity of a VNF instance. As it invol-
				 ves changing network parameters, we decided for receiving a mo-
				 fied VNFD as argument. If only few fields are used, they should
				 be filtered in the VNFM driver.
	ARGUMENT: 	 vnfInstanceId (String), ChangeExtVnfConnectivityRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_changeExtConn(self, vnfInstanceId, changeExtVnfConnectivityRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_ext_conn 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_changeExtConn(self):
		return "405"
	def put_vlmi_viid_changeExtConn(self):
		return "405"
	def patch_vlmi_viid_changeExtConn(self):
		return "405"
	def delete_vlmi_viid_changeExtConn(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_vnfpkg 
	ACTION: 	 POST
	DESCRIPTION: Change the current VNF package on which a VNF instance is ba-
				 sed. It do not redeploy a running VNF instance, but in the ne-
				 xt deployment the new package will be assumed.  
	ARGUMENT: 	 vnfInstanceId (String), ChangeCurrentVnfPkgRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_changeVnfPkg(self, vnfInstanceId, changeCurrentVnfPkgRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/change_vnfpkg
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_changeVnfPkg(self):
		return "405"
	def put_vlmi_viid_changeVnfPkg(self):
		return "405"
	def patch_vlmi_viid_changeVnfPkg(self):
		return "405"
	def delete_vlmi_viid_changeVnfPkg(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/create_snapshot 
	ACTION: 	 POST
	DESCRIPTION: Create a VNF snapshot. This snapshot copy all the configuration
				 files of VNF instances from a given VNF. Alternatively, it can
				 copy the virtual disks of these VNF instances. 
	ARGUMENT: 	 vnfInstanceId (String), CreateVnfSnapshotRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_createSnapshot(self, vnfInstanceId, createVnfSnapshotRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/create_snapshot 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_createSnapshot(self):
		return "405"
	def put_vlmi_viid_createSnapshot(self):
		return "405"
	def patch_vlmi_viid_createSnapshot(self):
		return "405"
	def delete_vlmi_viid_createSnapshot(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/revert_to_snapshot 
	ACTION: 	 POST
	DESCRIPTION: Revert a VNF instance to a previously created VNF snapshot.   
	ARGUMENT: 	 vnfInstanceId (String), RevertToVnfSnapshotRequest (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_viid_revertToSnapshot(self, vnfInstanceId, revertToVnfSnapshotRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_instances/{vnfInstanceId}/revert_to_snapshot 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_viid_revertToSnapshot(self):
		return "405"
	def put_vlmi_viid_revertToSnapshot(self):
		return "405"
	def patch_vlmi_viid_revertToSnapshot(self):
		return "405"
	def delete_vlmi_viid_revertToSnapshot(self):
		return "405"

	'''
	PATH: 	  	 /vnf_lcm_op_occs 
	ACTION: 	 GET
	DESCRIPTION: Query information about multiple VNF lifecycle management
				 operation occurrences. It is not clear which lcm operations
				 are considered in this method, probably it depends on the
				 management possibilities of the employed VNFM. However, in
				 summary, we consider operations regarding the management of
				 the virtualized instance of a VNF. A report of the execution
				 of the lcm operations is returned.
	ARGUMENT: 	 -- 
	RETURN: 	 - 202 (HTTP) + VnfLcmOpOcc (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vnfLcmOpOccs(self):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs 
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vlmi_vnfLcmOpOccs(self):
		return "405"
	def put_vlmi_vnfLcmOpOccs(self):
		return "405"
	def patch_vlmi_vnfLcmOpOccs(self):
		return "405"
	def delete_vlmi_vnfLcmOpOccs(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId} 
	ACTION: 	 GET
	DESCRIPTION: Read information about an individual VNF lifecycle manage-
				 ment operation occurrence. The same process as described 
				 for the "get_vnfLcmOpOccs" is done, but for a single and
				 defined lcm operation.
	ARGUMENT: 	 vnfLcmOpOccId (String)
	RETURN: 	 - 200 (HTTP) + VnfLcmOpOcc (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vloo_vnfOperationID(self, vnfLcmOpOccId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}  
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vlmi_vloo_vnfOperationID(self):
		return "405"
	def put_vlmi_vloo_vnfOperationID(self):
		return "405"
	def patch_vlmi_vloo_vnfOperationID(self):
		return "405"
	def delete_vlmi_vloo_vnfOperationID(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/retry 
	ACTION: 	 POST
	DESCRIPTION: Retry a VNF lifecycle management operation occurrence. This
				 method request to the VNFM to retry a lcm operation that is
				 marked as "FAILED_TEMP", i.e., an operation that failed for
				 an undetermined cause and can be executed again. 
	ARGUMENT:	 vnfLcmOpOccId (String)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vlooid_retry(self, vnfLcmOpOccId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/retry 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_vlooid_retry(self):
		return "405"
	def put_vlmi_vlooid_retry(self):
		return "405"
	def patch_vlmi_vlooid_retry(self):
		return "405"
	def delete_vlmi_vlooid_retry(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/rollback 
	ACTION: 	 POST
	DESCRIPTION: Rollback a VNF lifecycle management operation occurrence. 
				 This method request to the VNFM to retry a lcm operation 
				 that is marked as "FAILED_TEMP", i.e., an operation that
				 failed for an undetermined cause and can be aborted. 
	ARGUMENT: 	 vnfLcmOpOccId (String)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vlooid_rollback(self, vnfLcmOpOccId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/rollback 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_vlooid_rollback(self):
		return "405"
	def put_vlmi_vlooid_rollback(self):
		return "405"
	def patch_vlmi_vlooid_rollback(self):
		return "405"
	def delete_vlmi_vlooid_rollback(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/fail 
	ACTION: 	 POST
	DESCRIPTION: Mark a VNF lifecycle management operation occurrence as 
				 failed. This method request to the VNFM to mark a lcm op-
				 eration that is marked as "FAILED_TEMP" to "FINALLY_FAIL".
	ARGUMENT: 	 vnfLcmOpOccId (String)
	RETURN: 	 - 200 (HTTP) + VnfLcmOpOcc (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vlooid_fail(self, vnfLcmOpOccId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/fail 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_vlooid_fail(self):
		return "405"
	def put_vlmi_vlooid_fail(self):
		return "405"
	def patch_vlmi_vlooid_fail(self):
		return "405"
	def delete_vlmi_vlooid_fail(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/cancel 
	ACTION: 	 POST
	DESCRIPTION: Cancel a VNF lifecycle management operation occurrence.
				 This method executes a rollback to the previous state
				 of a VNF instance executing an operation marked as "STA-
				 RTED" (-> "ROLLED_BACK") and temporary fails lcm opera-
				 tions that are marked as "PROCESSING" or "ROLLING_BACK"
				 (-> "TEMPORARY_FAIL").
	ARGUMENT: 	 vnfLcmOpOccId (String), CancelMode (Class)
	RETURN: 	 - 202 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vlooid_cancel(self, vnfLcmOpOccId, cancelMode):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_lcm_op_occs/{vnfLcmOpOccId}/cancel 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlmi_vlooid_cancel(self):
		return "405"
	def put_vlmi_vlooid_cancel(self):
		return "405"
	def patch_vlmi_vlooid_cancel(self):
		return "405"
	def delete_vlmi_vlooid_cancel(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_snapshots
	ACTION: 	 GET
	DESCRIPTION: Query multiple VNF snapshots. Get information about 
				 all the available snapshots of the managed VNF ins-
				 tances.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + VnfSnapshotInfo (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vnfSnapshots(self):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_snapshots
	ACTION: 	 POST
	DESCRIPTION: Create an individual VNF snapshot resource. Save 
				 a new snapshot for all the managed VNF instances.
	ARGUMENT: 	 CreateVnfSnapshotInfoRequest (Class)
	RETURN: 	 - 201 (HTTP) + VnfSnapshotInfo (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_vnfSnapshots(self, createVnfSnapshotInfoRequest):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_snapshots
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vlmi_vnfSnapshots(self):
		return "405"
	def patch_vlmi_vnfSnapshots(self):
		return "405"
	def delete_vlmi_vnfSnapshots(self):
		return "405"

	'''
	PATH: 		 /vlmi/vnf_snapshots/{vnfSnapshotInfoId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual VNF snapshot resource. Get detailed
				 information about a particular snapshot.
	ARGUMENT: 	 vnfSnapshotInfoId (String)
	RETURN: 	 - 200 (HTTP) + VnfSnapshotInfo (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_vs_vnfSnapshotID(self, vnfSnapshotInfoId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_snapshots/{vnfSnapshotInfoId}
	ACTION: 	 DELETE
	DESCRIPTION: Delete VNF snapshot resource.
	ARGUMENT: 	 vnfSnapshotInfoId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def delete_vlmi_vs_vnfSnapshotID(self, vnfSnapshotInfoId):
		return "501"

	'''
	PATH: 		 /vlmi/vnf_snapshots/{vnfSnapshotInfoId}
	N/A ACTIONS: POST, PUT, PATCH
	**Do not change these methods**
	'''
	def post_vlmi_vs_vnfSnapshotID(self):
		return "405"
	def put_vlmi_vs_vnfSnapshotID(self):
		return "405"
	def patch_vlmi_vs_vnfSnapshotID(self):
		return "405"

	'''
	PATH: 		 /vlmi/subscriptions
	ACTION: 	 GET
	DESCRIPTION: Query multiple subscriptions (all the subscriptions, 
				 actually).
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + LccnSubscription (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_subscriptions(self):
		return "501"

	'''
	PATH: 		 /vlmi/subscriptions
	ACTION: 	 POST
	DESCRIPTION: Subscribe to VNF lifecycle change notifications. There
				 is no definition on which VNF instances will be subscribed.
				 Thus, we consider that it subscribes all the managed VNF
				 instances at the moment of the execution of this method.
	ARGUMENT: 	 LccnSubscriptionRequest (Class)
	RETURN: 	 - 201 (HTTP) + LccnSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_subscriptions(self, lccnSubscriptionRequest):
		return "501"

	'''
	PATH: 		 /vlmi/subscriptions
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vlmi_subscriptions(self):
		return "405"
	def patch_vlmi_subscriptions(self):
		return "405"
	def delete_vlmi_subscriptions(self):
		return "405"

	'''
	PATH: 		 /vlmi/subscriptions/{subscriptionId}
	ACTION: 	 GET
	DESCRIPTION: Read an "Individual subscription" resource. 
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 200 (HTTP) + LccnSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vlmi_s_subscriptionID(self, subscriptionId):
		return "501"

	'''
	PATH: 		 /vlmi/subscriptions/{subscriptionId}
	ACTION: 	 POST
	DESCRIPTION: Terminate a given subscription. The resource of "Individual
				 subscription" is removed and the monitoring stops.
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vlmi_s_subscriptionID(self, subscriptionId):
		return "501"

	'''
	PATH: 		 /vlmi/subscriptions/{subscriptionId}
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vlmi_s_subscriptionID(self):
		return "405"
	def patch_vlmi_s_subscriptionID(self):
		return "405"
	def delete_vlmi_s_subscriptionID(self):
		return "405"

	#######################################################################################################
	#######################################################################################################

	'''
	PATH: 		 /vpmi/pm_jobs
	ACTION: 	 GET
	DESCRIPTION: Get information of PM jobs. The API consumer can use this
				 method to retrieve information about PM jobs.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + PmJob (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vpmi_pm_jobs(self):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs
	ACTION: 	 POST
	DESCRIPTION: Create PM jobs. Create a new individual performance
				 monitoring job into the system to the available VNFs.
	ARGUMENT: 	 CreatePmJobRequest (Class)
	RETURN: 	 - 201 (HTTP) + PmJob (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vpmi_pm_jobs(self, createPmJobRequest):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vpmi_pm_jobs(self):
		return "405"
	def patch_vpmi_pm_jobs(self):
		return "405"
	def delete_vpmi_pm_jobs(self):
		return "405"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}
	ACTION: 	 GET
	DESCRIPTION: Get information of a single PM job. The API consumer can 
				 use this method for reading an individual performance mo-
				 nitoring job.
	ARGUMENT: 	 pmJobId (String)
	RETURN: 	 - 200 (HTTP) + PmJob (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vpmi_pmj_pmJobID(self, pmJobId):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}
	ACTION: 	 PATCH
	DESCRIPTION: Update PM job callback. This method allows to modify an
				 individual performance monitoring job resource.
	ARGUMENT: 	 pmJobId (string), PmJobModifications (Class)
	RETURN: 	 - 200 (HTTP) + PmJobModifications (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def patch_vpmi_pmj_pmJobID(self, pmJobId, pmJobModifications):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}
	ACTION: 	 DELETE
	DESCRIPTION: Delete a PM job. This method terminates an individual per-
				 formance monitoring job.
	ARGUMENT: 	 pmJobId (string)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def delete_vpmi_pmj_pmJobID(self, pmJobId):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}
	N/A ACTIONS: POST, PUT
	**Do not change these methods**
	'''
	def post_vpmi_pmj_pmJobID(self):
		return "405"
	def put_vpmi_pmj_pmJobID(self):
		return "405"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}/reports/{reportId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual performance report. The API consumer can
				 use this method for reading an individual performance report.
	ARGUMENT: 	 pmJobId (String), reportId (String)
	RETURN: 	 - 200 (HTTP) + PerformanceReport (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vpmi_pmjid_r_reportID(self, pmJobId, reportId):
		return "501"

	'''
	PATH: 		 /vpmi/pm_jobs/{pmJobId}/reports/{reportId}
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vpmi_pmjid_r_reportID(self):
		return "405"
	def put_vpmi_pmjid_r_reportID(self):
		return "405"
	def patch_vpmi_pmjid_r_reportID(self):
		return "405"
	def delete_vpmi_pmjid_r_reportID(self):
		return "405"

	'''
	PATH: 		 /vpmi/thresholds
	ACTION: 	 GET
	DESCRIPTION: Query thresholds. The API consumer can use this method to query
				 information about thresholds.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + Threshold (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vpmi_thresholds(self):
		return "501"

	'''
	PATH: 		 /vpmi/thresholds
	ACTION:		 POST
	DESCRIPTION: Create a threshold. Request parameters to create a new indi-
				 vidual threshold resource.
	ARGUMENT: 	 CreateThresholdRequest (Class)
	RETURN: 	 - 201 (HTTP) + Threshold (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def post_vpmi_thresholds(self, createThresholdRequest):
		return "501"

	'''
	PATH: 		 /vpmi/thresholds
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vpmi_thresholds(self):
		return "405"
	def patch_vpmi_thresholds(self):
		return "405"
	def delete_vpmi_thresholds(self):
		return "405"

	'''
	PATH: 		 /vpmi/thresholds/{thresholdId}
	ACTION: 	 GET
	DESCRIPTION: Read a single threshold. The API consumer can use this method
				 for reading an individual threshold.
	ARGUMENT: 	 thresholdId (String)
	RETURN: 	 - 200 (HTTP) + Threshold (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vpmi_t_thresholdID(self, thresholdId):
		return "501"

	'''
	PATH: 		 /vpmi/thresholds/{thresholdId}
	ACTION: 	 PATCH
	DESCRIPTION: Update threshold callback. This method allows to modify an indivi-
				 dual threshold resource.
	ARGUMENT: 	 thresholdId (String), ThresholdModifications (Class)
	RETURN: 	 - 200 (HTTP) + ThresholdModifications (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def patch_vpmi_t_thresholdID(self, thresholdId, thresholdModifications):
		return "501"

	'''
	PATH: 		 /vpmi/thresholds/{thresholdId}
	ACTION: 	 DELETE
	DESCRIPTION: Delete a threshold. This method allows to delete a threshold.
	ARGUMENT: 	 thresholdId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def delete_vpmi_t_thresholdID(self, thresholdId):
		return "501"

	'''
	PATH: 		 /vpmi/thresholds/{thresholdId}
	N/A ACTIONS: POST, PUT
	**Do not change these methods**
	'''
	def post_vpmi_t_thresholdID(self):
		return "405"
	def put_vpmi_t_thresholdID(self):
		return "405"

	#######################################################################################################
	#######################################################################################################

	'''
	PATH: 		 /vfmi/alarms
	ACTION: 	 GET
	DESCRIPTION: Query alarms related to VNF instances. The API consumer can
				 use this method to retrieve information about the alarm list.
	ARGUMENT: 	 --
	RETURN: 	 - 200 (HTTP) + Alarm (Class) [0..N]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vfmi_alarms(self):
		return "501"

	'''
	PATH: 		 /vfmi/alarms
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vfmi_alarms(self):
		return "405"
	def put_vfmi_alarms(self):
		return "405"
	def patch_vfmi_alarms(self):
		return "405"
	def delete_vfmi_alarms(self):
		return "405"

	'''
	PATH: 		 /vfmi/alarms/{alarmId}
	ACTION: 	 GET
	DESCRIPTION: Read individual alarm. The API consumer can use this
				 method to read an individual alarm.
	ARGUMENT: 	 alarmId (String)
	RETURN: 	 - 200 (HTTP) + Alarm (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vfmi_a_alarmID(self, alarmId):
		return "501"

	'''
	PATH: 		 /vfmi/alarms/{alarmId}
	ACTION: 	 PATCH
	DESCRIPTION: Acknowledge individual alarm. This method modifies an
				 individual alarm resource.
	ARGUMENT: 	 alarmId (String), AlarmModifications (Class)
	RETURN: 	 - 200 (HTTP) + AlarmModifications (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def patch_vfmi_a_alarmID(self, alarmId, alarmModifications):
		return "501"

	'''
	PATH: 		 /vfmi/alarms/{alarmId}
	N/A ACTIONS: POST, PUT, DELETE
	**Do not change these methods**
	'''
	def post_vfmi_a_alarmID(self):
		return "405"
	def put_vfmi_a_alarmID(self):
		return "405"
	def delete_vfmi_a_alarmID(self):
		return "405"

	'''
	PATH: 		 /vfmi/alarms/{alarmId}/escalate
	ACTION: 	 POST
	DESCRIPTION: Escalate the API consumer's view of perceived severity.
				 The POST method enables the API consumer to escalate the
				 perceived severity of an alarm that is represented by an
				 individual alarm resource.
	ARGUMENT: 	 alarmId (String), PerceivedSeverityRequest (Class)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def post_vfmi_aid_escalate(self, alarmId, perceivedSeverityRequest):
		return "501"

	'''
	PATH: 		 /vfmi/alarms/{alarmId}/escalate
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vfmi_aid_escalate(self):
		return "405"
	def put_vfmi_aid_escalate(self):
		return "405"
	def patch_vfmi_aid_escalate(self):
		return "405"
	def delete_vfmi_aid_escalate(self):
		return "405"

	'''
	PATH: 		 /vfmi/subscriptions
	ACTION: 	 GET
	DESCRIPTION: Query multiple subscriptions. The API consumer can use
				 this method to retrieve the list of active subscriptions
				 for VNF alarms subscribed by the API consumer. It can be
				 used e.g. for resynchronization after error situations.
	ARGUMENT: 	 --
	RETURN: 	- 200 (HTTP) + FmSubscription (Class) [0..N]
				- Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''	
	def get_vfmi_subscriptions(self):
		return "501"

	'''
	PATH: 		 /vfmi/subscriptions
	ACTION: 	 POST
	DESCRIPTION: Subscribe to VNF alarms. The POST method creates a new
				 subscription.
	ARGUMENT: 	 FmSubscriptionRequest (Class)
	RETURN: 	 - 201 (HTTP) + FmSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def post_vfmi_subscriptions(self, fmSubscriptionRequest):
		return "501"

	'''
	PATH: 		 /vfmi/subscriptions
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vfmi_subscriptions(self):
		return "405"
	def patch_vfmi_subscriptions(self):
		return "405"
	def delete_vfmi_subscriptions(self):
		return "405"

	'''
	PATH: 		 /vfmi/subscriptions/{subscriptionId}
	ACTION: 	 GET
	DESCRIPTION: Read an individual subscription. The API consumer can use
				 this method for reading an individual subscription for VNF
				 alarms subscribed by the API consumer.
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 200 (HTTP) + FmSubscription (Class) [1]
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def get_vfmi_s_subscriptionID(self, subscriptionId):
		return "501"

	'''
	PATH: 		 /vfmi/subscriptions/{subscriptionId}
	ACTION: 	 DELETE
	DESCRIPTION: Terminate a subscription. This method terminates an individu-
				 al subscription.
	ARGUMENT: 	 subscriptionId (String)
	RETURN: 	 - 204 (HTTP)
				 - Integer error code (HTTP)
	CALL: 		 EM -> VNFM
	'''
	def delete_vfmi_s_subscriptionID(self, subscriptionId):
		return "501"

	'''
	PATH: 		 /vfmi/subscriptions/{subscriptionId}
	N/A ACTIONS: POST, PUT, PATCH
	**Do not change these methods**
	'''
	def post_vfmi_s_subscriptionID(self):
		return "405"
	def put_vfmi_s_subscriptionID(self):
		return "405"
	def patch_vfmi_s_subscriptionID(self):
		return "405"