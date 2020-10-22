'''
CLASS: VnfmDriver
AUTHOR: Vinicius Fulber-Garcia
CREATION: 21 Oct. 2020
L. UPDATE: 22 Oct. 2020 (Fulber-Garcia; Inclusion of error 405 methods)
DESCRIPTION: Template for the implementation of VNFM drivers that run in the "Access Subsystem"
			 internal module. The drivers must inhert this class and overload the functions that
			 return the HTTP code 501 (Not Implemented).
'''
class VnfmDriver:
	className = None

	def __init__(self, className):
		self.className = className
	
	'''
	PATH: /vnfm/vnfInstances/ 
	ACTION: GET
	DESCRIPTION: Query multiple VNF instances, thus returning information 
				 from the VNFM of all the VNF instances managed by the EMS
	ARGUMENT: --
	RETURN: String data (according to the VNFM) or integer code (HTTP) 
	'''
	def get_vnfInstances(self):
		return 501

	'''
	PATH: /vnfm/vnfInstances/ 
	ACTION: POST
	DESCRIPTION: Create a new "Individual VNF instance" resource in the VNFM
				 and set it to be managed by the EMS as an idle instance (do 
				 not instantiate the VNF, just create the resource).
	ARGUMENT: Serialized VNF package (String)
	RETURN: Integer code (HTTP)
	'''
	def post_vnfInstances(self, vnfPackage):
		return 501

	'''
	PATH: /vnfm/vnfInstances/
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vnfInstances(self):
		return 405
	def patch_vnfInstances(self):
		return 405
	def delete_vnfInstances(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId} 
	ACTION: GET
	DESCRIPTION: Read an "Individual VNF instance" resource. Return the same
				 information than the "/vnfm/vnfInstances/" operation, but for
				 a single VNF instance.
	ARGUMENT: VNF instance ID (String)
	RETURN: String data (according to the VNFM) or integer code (HTTP)
	'''
	def get_vi_vnfInstanceID(self, vnfInstanceID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId} 
	ACTION: PATCH
	DESCRIPTION: Modify VNF instance information through the replacement of
				 its VNF descriptor. Note that it does not require an update
				 of the runnig instances (the modification occur only in in-
				 formational data).
	ARGUMENT: VNF instance ID (String), serialized VNF descriptor regarding
			  the requested instance (String)
	RETURN: Integer code (HTTP)
	'''
	def patch_vi_vnfInstanceID(self, vnfInstanceID, vnfDescriptor):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId} 
	ACTION: DELETE
	DESCRIPTION: Delete an "Individual VNF instance" resource. This opera-
				 tion must be used with caution. It is recommended that it
				 can be executed only in inactive VNF instances (avoiding
				 management errors and false alerts triggered by the EMS).
	ARGUMENT: VNF instance ID (String)
	RETURN: Integer code (HTTP)
	'''
	def delete_vi_vnfInstanceID(self, vnfInstanceID, vnfDescriptor):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId} 
	N/A ACTIONS: POST, PUT
	**Do not change these methods**
	'''
	def post_vi_vnfInstanceID(self):
		return 405
	def put_vi_vnfInstanceID(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/instantiate 
	ACTION: POST
	DESCRIPTION: Instantiate an already created and idle "Individual VNF
				 instance".
	ARGUMENT: VNF instance ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_instantiate(self, vnfInstanceID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/instantiate
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_instantiate(self):
		return 405
	def put_viid_instantiate(self):
		return 405
	def patch_viid_instantiate(self):
		return 405
	def delete_viid_instantiate(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/scale 
	ACTION: POST
	DESCRIPTION: Scale a VNF instance incrementally. The resource scaling
				 depends on VNFM capacities, but in general it comprehends 
				 memory, disk, and virtualized CPU cores. 
	ARGUMENT: VNF instance ID (String), serialized VNF descriptor regarding
			  the requested instance (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_scale(self, vnfInstanceID, vnfDescriptor):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/scale 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_scale(self):
		return 405
	def put_viid_scale(self):
		return 405
	def patch_viid_scale(self):
		return 405
	def delete_viid_scale(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/scale_to_level 
	ACTION: POST
	DESCRIPTION: Scale a VNF instance to a target level. The levels availa-
				 ble depends on the VNFM platform.
	ARGUMENT: VNF instance ID (String), level ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_scaleToLevel(self, vnfInstanceID, levelID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/scale_to_level 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_scaleToLevel(self):
		return 405
	def put_viid_scaleToLevel(self):
		return 405
	def patch_viid_scaleToLevel(self):
		return 405
	def delete_viid_scaleToLevel(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_flavour 
	ACTION: POST
	DESCRIPTION: Change the deployment flavour of a VNF instance. Here, we
				 consider that the flavour are previously defined in the VNF
				 descriptor.
	ARGUMENT: VNF instance ID (String), flavour ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_changeFlavour(self, vnfInstanceID, flavourID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_flavour 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_changeFlavour(self):
		return 405
	def put_viid_changeFlavour(self):
		return 405
	def patch_viid_changeFlavour(self):
		return 405
	def delete_viid_changeFlavour(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/terminate
	ACTION: POST
	DESCRIPTION: Terminate a VNF instance. This method regards just to the
				 termination request to the VNFM. Here we do not threat the
				 management termination in the EMS.
	ARGUMENT: VNF instance ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_terminate(self, vnfInstanceID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_flavour 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_terminate(self):
		return 405
	def put_viid_terminate(self):
		return 405
	def patch_viid_terminate(self):
		return 405
	def delete_viid_terminate(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/heal 
	ACTION: POST
	DESCRIPTION: Heal a VNF instance. This method is typically used when the
				 VNF instance do not respond to the EMS or its users. However,
				 the VNFM is the component that decides if a healing process
				 should be really executed.
	ARGUMENT: VNF instance ID (String) 
	RETURN: Integer code (HTTP)
	'''
	def post_viid_heal(self, vnfInstanceID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/heal
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_heal(self):
		return 405
	def put_viid_heal(self):
		return 405
	def patch_viid_heal(self):
		return 405
	def delete_viid_heal(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/operate 
	ACTION: POST
	DESCRIPTION: Operate a VNF instance. There is no specific operation defined
				 for this method. Thus, we kept it the most generic as possible. 
	ARGUMENT: VNF instance ID (String), VNF instance operation ID (String), seri-
			  alized operation arguments (String) 
	RETURN: Integer code (HTTP)
	'''
	def post_viid_operate(self, vnfInstanceID, vnfOperationID, vnfOperationArgs):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/operate
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_operate(self):
		return 405
	def put_viid_operate(self):
		return 405
	def patch_viid_operate(self):
		return 405
	def delete_viid_operate(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_ext_conn 
	ACTION: POST
	DESCRIPTION: Change the external connectivity of a VNF instance. As it invol-
				 ves changing network parameters, we decided for receiving a mo-
				 fied VNFD as argument. If only few fields are used, they should
				 be filtered in the VNFM driver.
	ARGUMENT: VNF instance ID (String), serialized VNF descriptor regarding
			  the requested instance (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_changeExtConn(self, vnfInstanceID, vnfDescriptor):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_ext_conn 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_changeExtConn(self):
		return 405
	def put_viid_changeExtConn(self):
		return 405
	def patch_viid_changeExtConn(self):
		return 405
	def delete_viid_changeExtConn(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_vnfpkg 
	ACTION: POST
	DESCRIPTION: Change the current VNF package on which a VNF instance is ba-
				 sed. It do not redeploy a running VNF instance, but in the ne-
				 xt deployment the new package will be assumed.  
	ARGUMENT: VNF instance ID (String), Serialized VNF package (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_changeVnfPkg(self, vnfInstanceID, vnfPackage):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/change_vnfpkg
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_changeVnfPkg(self):
		return 405
	def put_viid_changeVnfPkg(self):
		return 405
	def patch_viid_changeVnfPkg(self):
		return 405
	def delete_viid_changeVnfPkg(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/create_snapshot 
	ACTION: POST
	DESCRIPTION: Create a VNF snapshot. This snapshot copy all the configuration
				 files of VNF instances from a given VNF. Alternatively, it can
				 copy the virtual disks of these VNF instances. 
	ARGUMENT: VNF instance ID (String), snapshot ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_createSnapshot(self, vnfInstanceID, snapshotID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/create_snapshot 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_createSnapshot(self):
		return 405
	def put_viid_createSnapshot(self):
		return 405
	def patch_viid_createSnapshot(self):
		return 405
	def delete_viid_createSnapshot(self):
		return 405

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/revert_to_snapshot 
	ACTION: POST
	DESCRIPTION: Revert a VNF instance to a previously created VNF snapshot.   
	ARGUMENT: VNF instance ID (String), snapshot ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_viid_revertToSnapshot(self, vnfInstanceID, snapshotID):
		return 501

	'''
	PATH: /vnfm/vnf_instances/{vnfInstanceId}/revert_to_snapshot 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_viid_revertToSnapshot(self):
		return 405
	def put_viid_revertToSnapshot(self):
		return 405
	def patch_viid_revertToSnapshot(self):
		return 405
	def delete_viid_revertToSnapshot(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs 
	ACTION: GET
	DESCRIPTION: Query information about multiple VNF lifecycle management
				 operation occurrences. It is not clear which lcm operations
				 are considered in this method, probably it depends on the
				 management possibilities of the employed VNFM. However, in
				 summary, we consider operations regarding the management of
				 the virtualized instance of a VNF. A report of the execution
				 of the lcm operations is returned.
	ARGUMENT: --
	RETURN: String data (according to the VNFM) or integer code (HTTP) 
	'''
	def get_vnfLcmOpOccs(self):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs 
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vnfLcmOpOccs(self):
		return 405
	def put_vnfLcmOpOccs(self):
		return 405
	def patch_vnfLcmOpOccs(self):
		return 405
	def delete_vnfLcmOpOccs(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId} 
	ACTION: GET
	DESCRIPTION: Read information about an individual VNF lifecycle manage-
				 ment operation occurrence. The same process as described 
				 for the "get_vnfLcmOpOccs" is done, but for a single and
				 defined lcm operation.
	ARGUMENT: VNF operation ID (String)
	RETURN: String data (according to the VNFM) or integer code (HTTP) 
	'''
	def get_vloo_vnfOperationID(self, vnfOperationID):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}  
	N/A ACTIONS: POST, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def post_vloo_vnfOperationID(self):
		return 405
	def put_vloo_vnfOperationID(self):
		return 405
	def patch_vloo_vnfOperationID(self):
		return 405
	def delete_vloo_vnfOperationID(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/retry 
	ACTION: POST
	DESCRIPTION: Retry a VNF lifecycle management operation occurrence. This
				 method request to the VNFM to retry a lcm operation that is
				 marked as "FAILED_TEMP", i.e., an operation that failed for
				 an undetermined cause and can be executed again. 
	ARGUMENT: VNF operation ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_vlooid_retry(self, vnfOperationID):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/retry 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlooid_retry(self):
		return 405
	def put_vlooid_retry(self):
		return 405
	def patch_vlooid_retry(self):
		return 405
	def delete_vlooid_retry(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/rollback 
	ACTION: POST
	DESCRIPTION: Rollback a VNF lifecycle management operation occurrence. 
				 This method request to the VNFM to retry a lcm operation 
				 that is marked as "FAILED_TEMP", i.e., an operation that
				 failed for an undetermined cause and can be aborted. 
	ARGUMENT: VNF operation ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_vlooid_rollback(self, vnfOperationID):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/rollback 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlooid_rollback(self):
		return 405
	def put_vlooid_rollback(self):
		return 405
	def patch_vlooid_rollback(self):
		return 405
	def delete_vlooid_rollback(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/fail 
	ACTION: POST
	DESCRIPTION: Mark a VNF lifecycle management operation occurrence as 
				 failed. This method request to the VNFM to mark a lcm op-
				 eration that is marked as "FAILED_TEMP" to "FINALLY_FAIL".
	ARGUMENT: VNF operation ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_vlooid_fail(self, vnfOperationID):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/fail 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlooid_fail(self):
		return 405
	def put_vlooid_fail(self):
		return 405
	def patch_vlooid_fail(self):
		return 405
	def delete_vlooid_fail(self):
		return 405

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/cancel 
	ACTION: POST
	DESCRIPTION: Cancel a VNF lifecycle management operation occurrence.
				 This method executes a rollback to the previous state
				 of a VNF instance executing an operation marked as "STA-
				 RTED" (-> "ROLLED_BACK") and temporary fails lcm opera-
				 tions that are marked as "PROCESSING" or "ROLLING_BACK"
				 (-> "TEMPORARY_FAIL").
	ARGUMENT: VNF operation ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_vlooid_cancel(self, vnfOperationID):
		return 501

	'''
	PATH: /vnfm/vnf_lcm_op_occs/{vnfLcmOpOccId}/cancel 
	N/A ACTIONS: GET, PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def get_vlooid_cancel(self):
		return 405
	def put_vlooid_cancel(self):
		return 405
	def patch_vlooid_cancel(self):
		return 405
	def delete_vlooid_cancel(self):
		return 405

	'''
	PATH: /vnfm/vnf_snapshots
	ACTION: GET
	DESCRIPTION: Query multiple VNF snapshots. Get information about 
				 all the available snapshots of the managed VNF ins-
				 tances.
	ARGUMENT: --
	RETURN: Integer code (HTTP)
	'''
	def get_vnfSnapshots(self):
		return 501

	'''
	PATH: /vnfm/vnf_snapshots
	ACTION: POST
	DESCRIPTION: Create an individual VNF snapshot resource. Save 
				 a new snapshot for all the managed VNF instances.
	ARGUMENT: --
	RETURN: Integer code (HTTP)
	'''
	def post_vnfSnapshots(self):
		return 501

	'''
	PATH: /vnfm/vnf_snapshots
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_vnfSnapshots(self):
		return 405
	def patch_vnfSnapshots(self):
		return 405
	def delete_vnfSnapshots(self):
		return 405

	'''
	PATH: /vnfm/vnf_snapshots/{vnfSnapshotInfoId}
	ACTION: GET
	DESCRIPTION: Read an individual VNF snapshot resource. Get detailed
				 information about a particular snapshot.
	ARGUMENT: VNF snapshot ID (String)
	RETURN: Integer code (HTTP)
	'''
	def get_vs_vnfSnapshotID(self, vnfSnapshotID):
		return 501

	'''
	PATH: /vnfm/vnf_snapshots/{vnfSnapshotInfoId}
	ACTION: DELETE
	DESCRIPTION: Delete VNF snapshot resource.
	ARGUMENT: VNF snapshot ID (String)
	RETURN: Integer code (HTTP)
	'''
	def delete_vs_vnfSnapshotID(self, vnfSnapshotID):
		return 501

	'''
	PATH: /vnfm/vnf_snapshots/{vnfSnapshotInfoId}
	N/A ACTIONS: POST, PUT, PATCH
	**Do not change these methods**
	'''
	def post_vs_vnfSnapshotID(self):
		return 405
	def put_vs_vnfSnapshotID(self):
		return 405
	def patch_vs_vnfSnapshotID(self):
		return 405

	'''
	PATH: /vnfm/subscriptions
	ACTION: GET
	DESCRIPTION: Query multiple subscriptions (all the subscriptions, 
				 actually).
	ARGUMENT: --
	RETURN: Integer code (HTTP)
	'''
	def get_subscriptions(self):
		return 501

	'''
	PATH: /vnfm/subscriptions
	ACTION: POST
	DESCRIPTION: Subscribe to VNF lifecycle change notifications. There
				 is no definition on which VNF instances will be subscribed.
				 Thus, we consider that it subscribes all the managed VNF
				 instances at the moment of the execution of this method.
	ARGUMENT: --
	RETURN: String data (according to the VNFM) or integer code (HTTP)
	'''
	def post_subscriptions(self):
		return 501

	'''
	PATH: /vnfm/subscriptions
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_subscriptions(self):
		return 405
	def patch_subscriptions(self):
		return 405
	def post_subscriptions(self):
		return 405

	'''
	PATH: /vnfm/subscriptions/{subscriptionId}
	ACTION: GET
	DESCRIPTION: Read an "Individual subscription" resource. 
	ARGUMENT: Subscription ID (String)
	RETURN: String data (according to the VNFM) or integer code (HTTP)
	'''
	def get_s_subscriptionID(self):
		return 501

	'''
	PATH: /vnfm/subscriptions/{subscriptionId}
	ACTION: POST
	DESCRIPTION: Terminate a given subscription. The resource of "Individual
				 subscription" is removed and the monitoring stops.
	ARGUMENT: Subscription ID (String)
	RETURN: Integer code (HTTP)
	'''
	def post_s_subscriptionID(self):
		return 501

	'''
	PATH: /vnfm/subscriptions/{subscriptionId}
	N/A ACTIONS: PUT, PATCH, DELETE
	**Do not change these methods**
	'''
	def put_s_subscriptionID(self):
		return 405
	def patch_s_subscriptionID(self):
		return 405
	def post_s_subscriptionID(self):
		return 405



#TESTE
class TackerDriver(VNFMDriver):

	def __init__(self):
		super().__init__("Tacker")

	def barulho(self):
		print("grup grup")

tackito = TackerDriver()
tackito.barulho()