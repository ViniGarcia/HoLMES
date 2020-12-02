import VsAgent
import AsOpAgent
import MsManager
import VibManager

import VibModels
import IrModels

import sqlite3
import shutil
import json
import os

'''
CLASS: ImAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 01 Dez. 2020
L. UPDATE: 02 Dez. 2020 (Fulber-Garcia; Subscription table methods adjustments; VNF instance table
						 management implementation; platform table management implementation; VNF 
						 managers table management implementation; entire VNF subsystem management
						 implementation (not tested yet))
DESCRIPTION: Implementation of the internal manager agent of the EMS.
			 This class provides the configuration ans mantaining o-
			 perations of the other internal modules of the EMS.
ERROR CODES: 
			-1: Invalid asAgent received
			-2: Invalid vsAgent received
			-3: Invalid msManager received
			-4: Invalid vibManager received
			-5: Invalid operation received
			-6: Invalid irManagement received
OPERATION STR ERROR CODES:
			1: Invalid operation arguments
			2: SQL error during some operation
			3: Redundant data requested
			4: Missing required data
			5: Element is present in another table
			6: External error code
'''	
class ImAgent:

	asAgent = None
	vsAgent = None
	msManager = None
	vibManager = None

	def __init__(self):
		return

	def setupAgent(self, asAgent, vsAgent, msManager, vibManager):

		#if type(asAgent) != AsOpAgent.AsOpAgent:
		#	return -1
		if type(vsAgent) != VsAgent.VsAgent:
			return -2
		#if type(msManager) != MsManager.MsManager:
		#	return -3
		if type(vibManager) != VibManager.VibManager:
			return -4

		self.asAgent = asAgent
		self.vsAgent = vsAgent
		self.msManager = msManager
		self.vibManager = vibManager

		return self

	def executeVsOperation(self, irManagement):

		if type(irManagement) != IrModels.IrManagement:
			return -6

		if irManagement.operationId == "get_vs_running_driver":
			return self.__get_vs_running_driver(irManagement)
		elif irManagement.operationId == "post_vs_running_driver":
			return self.__post_vs_running_driver(irManagement)
		elif irManagement.operationId == "get_vs_rd_operations":
			return self.__get_vs_rd_operations(irManagement)
		elif irManagement.operationId == "get_vs_rdo_monitoring":
			return self.__get_vs_rdo_monitoring(irManagement)
		elif irManagement.operationId == "get_vs_rdo_modification":
			return self.__get_vs_rdo_modification(irManagement)
		elif irManagement.operationId == "get_vs_rdo_other":
			return self.__get_vs_rdo_other(irManagement)
		elif irManagement.operationId == "post_vs_driver":
			return self.__post_vs_driver(irManagement)
		elif irManagement.operationId == "patch_vs_driver":
			return self.__patch_vs_driver(irManagement)
		elif irManagement.operationId == "delete_vs_driver":
			return self.__delete_vs_driver(irManagement)

	def executeVibOperation(self, irManagement):

		if type(irManagement) != IrModels.IrManagement:
			return -6

		if irManagement.operationId.endswith("credentials") or irManagement.operationId.endswith("credentialId"):
			if irManagement.operationId == "get_vib_credentials":
				return self.__get_vib_credentials(irManagement)
			elif irManagement.operationId == "post_vib_credentials":
				return self.__post_vib_credentials(irManagement)
			elif irManagement.operationId == "get_vib_c_credentialId":
				return self.__get_vib_c_credentialId(irManagement)
			elif irManagement.operationId == "patch_vib_c_credentialId":
				return self.__patch_vib_c_credentialId(irManagement)
			elif irManagement.operationId == "delete_vib_c_credentialId":
				return self.__delete_vib_c_credentialId(irManagement)
			else:
				return -5

		elif irManagement.operationId.endswith("subscriptions") or irManagement.operationId.endswith("subscriptionId"):
			if irManagement.operationId == "get_vib_subscriptions":
				return self.__get_vib_subscriptions(irManagement)
			elif irManagement.operationId == "post_vib_subscriptions":
				return self.__post_vib_subscriptions(irManagement)
			elif irManagement.operationId == "get_vib_s_subscriptionId":
				return self.__get_vib_s_subscriptionId(irManagement)
			elif irManagement.operationId == "patch_vib_s_subscriptionId":
				return self.__patch_vib_s_subscriptionId(irManagement)
			elif irManagement.operationId == "delete_vib_s_subscriptionId":
				return self.__delete_vib_s_subscriptionId(irManagement)
			else:
				return -5

		elif irManagement.operationId.endswith("instances") or irManagement.operationId.endswith("instanceId"):
			if irManagement.operationId == "get_vib_instances":
				return self.__get_vib_instances(irManagement)
			elif irManagement.operationId == "post_vib_instances":
				return self.__post_vib_instances(irManagement)
			elif irManagement.operationId == "get_vib_i_instanceId":
				return self.__get_vib_i_instanceId(irManagement)
			elif irManagement.operationId == "patch_vib_i_instanceId":
				return self.__patch_vib_i_instanceId(irManagement)
			elif irManagement.operationId == "delete_vib_i_instanceId":
				return self.__delete_vib_i_instanceId(irManagement)
			else:
				return -5

		elif irManagement.operationId.endswith("platforms") or irManagement.operationId.endswith("platformId"):
			if irManagement.operationId == "get_vib_platforms":
				return self.__get_vib_platforms(irManagement)
			elif irManagement.operationId == "post_vib_platforms":
				return self.__post_vib_platforms(irManagement)
			elif irManagement.operationId == "get_vib_p_platformId":
				return self.__get_vib_p_platformId(irManagement)
			elif irManagement.operationId == "patch_vib_p_platformId":
				return self.__patch_vib_p_platformId(irManagement)
			elif irManagement.operationId == "delete_vib_p_platformId":
				return self.__delete_vib_p_platformId(irManagement)
			else:
				return -5

		elif irManagement.operationId.endswith("vnf_managers") or irManagement.operationId.endswith("vnfm_managerId"):
			if irManagement.operationId == "get_vib_vnf_managers":
				return self.__get_vib_vnf_managers(irManagement)
			elif irManagement.operationId == "post_vib_vnf_managers":
				return self.__post_vib_vnf_managers(irManagement)
			elif irManagement.operationId == "get_vib_vnfm_managerId":
				return self.__get_vib_vnfm_managerId(irManagement)
			elif irManagement.operationId == "patch_vib_vnfm_managerId":
				return self.__patch_vib_vnfm_managerId(irManagement)
			elif irManagement.operationId == "delete_vib_vnfm_managerId":
				return self.__delete_vib_vnfm_managerId(irManagement)
			else:
				return -5

		else:
			return -5





	def __get_vs_running_driver(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.vsAgent.get_p_id()

	def __post_vs_running_driver(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"

		platform = self.__get_vib_p_platformId(irManagement)
		if type(platform) == str:
			return platform
		if len(platform) == 0:
			return "ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST"
		platform = VibModels.VibPlatformInstance().fromSql(platform[0])

		result = self.vsAgent.setup(platform)
		if type(result) == int:
			return "ERROR CODE #6: AN ERROR OCCURED WHEN SETUPING THE PLATFORM DRIVER (" + str(result) + ")"

		return 1

	def __get_vs_rd_operations(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.vsAgent.get_p_operations()

	def __get_vs_rdo_monitoring(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.vsAgent.get_po_monitoring()

	def __get_vs_rdo_modification(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.vsAgent.get_po_modification()

	def __get_vs_rdo_other(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.vsAgent.get_po_other()

	def __post_vs_driver(self, irManagement):

		if type(irManagement.operationArgs) != VibPlatformInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibPlatformInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.platformDriver) or not irManagement.operationArgs.platformDriver.endswith(".py"):
			return "ERROR CODE #1: INVALID VibPlatformInstance.platformDriver PROVIDED"

		original = irManagement.operationArgs.platformDriver
		irManagement.operationArgs.platformDriver = irManagement.operationArgs.platformDriver.replace("\\", "/").split("/")[-1][:-3]

		result = self.__post_vib_platforms(irManagement)
		if type(result) == str:
			return result
		shutil.copyfile(irManagement.operationArgs.platformDriver, "VNF Subsystem/Ve-Em-vnf/" + kernel + ".py")

		return 1

	def __patch_vs_driver(self, irManagement):

		if type(irManagement.operationArgs) != VibPlatformInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibPlatformInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.platformDriver) or not irManagement.operationArgs.platformDriver.endswith(".py"):
			return "ERROR CODE #1: INVALID VibPlatformInstance.platformDriver PROVIDED"

		original = irManagement.operationArgs.platformDriver
		irManagement.operationArgs.platformDriver = irManagement.operationArgs.platformDriver.replace("\\", "/").split("/")[-1][:-3]
		
		result = self.__patch_vib_p_platformId(irManagement)
		if type(result) == str:
			return result
		shutil.copyfile(irManagement.operationArgs.platformDriver, "VNF Subsystem/Ve-Em-vnf/" + kernel + ".py")

		return 1

	def __delete_vs_driver(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"

		result = self.__delete_vib_p_platformId(irManagement)
		if type(result) == str:
			return result

		if self.vsAgent.get_p_id() == irManagement.operationArgs:
			self.vsAgent.detach()

		os.remove("VNF Subsystem/Ve-Em-vnf/" + irManagement.operationArgs + ".py")

	############################################################################################################################################################

	def __get_vib_credentials(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		credentials = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance;")
		if type(credentials) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"

		return credentials

	def __post_vib_credentials(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs.userId +"\" AND vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL ALREADY EXISTS"

		existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(existence) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(existence) == 0:
			return "ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST"

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL INSERTION"

		return insertion.lastrowid

	def __get_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"
		if type(irManagement.operationArgs[0]) != str or type(irManagement.operationArgs[1]) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs[0] +"\" AND vnfId = \"" + irManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"

		return credential

	def __patch_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs.userId +"\" AND vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"
		if len(credential) == 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL DOES NOT EXIST"

		update = self.vibManager.operateVibDatabase(("UPDATE CredentialInstance SET authData = ?, authResource = ? WHERE userId = ? AND vnfId = ?;", (irManagement.operationArgs.authData, irManagement.operationArgs.authResource, irManagement.operationArgs.userId, irManagement.operationArgs.vnfId)))
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING"

		return update.rowcount

	def __delete_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"
		if type(irManagement.operationArgs[0]) != str or type(irManagement.operationArgs[1]) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs[0] +"\" AND vnfId = \"" + irManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"
		if len(credential) == 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL DOES NOT EXIST"

		delete = self.vibManager.operateVibDatabase(("DELETE FROM CredentialInstance WHERE userId = ? AND vnfId = ?;", (irManagement.operationArgs[0], irManagement.operationArgs[1])))
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL DELETING"

		return delete.rowcount

	def __get_vib_subscriptions(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		if type(subscriptions) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"

		return subscriptions

	def __post_vib_subscriptions(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs.visId +"\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION ALREADY EXISTS"

		if irManagement.operationArgs.visFilter != None:
			if irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter != None:
				for vnfId in irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
					if len(existence) == 0:
						return "ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST"

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION INSERTION"

		return insertion.rowcount

	def __get_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs +"\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION CONSULTING"

		return subscription

	def __patch_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs.visId + "\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(subscription) == 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"

		if irManagement.operationArgs.visFilter != None:
			if irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter != None:
				for vnfId in irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
					if len(existence) == 0:
						return "ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST"

		if irManagement.operationArgs.visFilter == None:
			update = self.vibManager.operateVibDatabase(("UPDATE SubscriptionInstance SET visFilter = ?, visCallback = ?, visLinks = ? WHERE visId = ?;", (irManagement.operationArgs.visFilter, irManagement.operationArgs.visCallback, json.dumps(irManagement.operationArgs.visLinks), irManagement.operationArgs.visId)))
		else:
			update = self.vibManager.operateVibDatabase(("UPDATE SubscriptionInstance SET visFilter = ?, visCallback = ?, visLinks = ? WHERE visId = ?;", (json.dumps(irManagement.operationArgs.visFilter.toDictionary()), irManagement.operationArgs.visCallback, json.dumps(irManagement.operationArgs.visLinks), irManagement.operationArgs.visId)))
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING"

		return update.rowcount

	def __delete_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs + "\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(subscription) == 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"

		delete = self.vibManager.operateVibDatabase(("DELETE FROM SubscriptionInstance WHERE visId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL DELETING"

		return delete.rowcount

	def __get_vib_instances(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		instances = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")
		if type(instances) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"

		return instances

	def __post_vib_instances(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED VNF INSTANCE ALREADY EXISTS"

		existence = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.vnfPlatform + "\";")
		if type(existence) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(existence) == 0:
			return "ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST"

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCE INSERTION"

		return insertion.lastrowid

	def __get_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfId is expected)"

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs +"\";")
		if type(instance) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"

		return instance

	def __patch_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfInstance is expected)"

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(instance) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(instance) == 0:
			return "ERROR CODE #3: THE REQUIRED INSTANCE DOES NOT EXIST"

		if instance[0][2] != irManagement.operationArgs.vnfPlatform:
			existence = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.vnfPlatform + "\";")
			if type(existence) == sqlite3.Error:
				return "ERROR CODE #2: SQL ERROR DURING VNF PLATFORMS CONSULTING"
			if len(existence) == 0:
				return "ERROR CODE #4: THE REQUIRED VNF PLATFORM DOES NOT EXIST"

		update = self.vibManager.operateVibDatabase(("UPDATE VnfInstance SET vnfAddress = ?, vnfPlatform = ?, vnfExtAgents = ?, vnfAuth = ? WHERE vnfId = ?;", (irManagement.operationArgs.vnfAddress, irManagement.operationArgs.vnfPlatform, json.dumps(irManagement.operationArgs.vnfExtAgents), irManagement.operationArgs.vnfAuth, irManagement.operationArgs.vnfId)))
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCE UPDATING"

		return update.rowcount

	def __delete_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfId is expected)"

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs + "\";")
		if type(instance) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(instance) == 0:
			return "ERROR CODE #3: THE REQUIRED VNF INSTANCE DOES NOT EXIST"

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		for element in subscriptions:
			if element[1] != None:
				element = json.loads(element[1])
				if element["vnfInstanceSubscriptionFilter"] != None:
					 if irManagement.operationArgs in element["vnfInstanceSubscriptionFilter"]["vnfInstanceIds"]:
					 	return "ERROR CODE #5: THE REQUIRED VNF INSTANCE IS BEING USED IN THE SUBSCRIPTION TABLE"

		delete = self.vibManager.operateVibDatabase(("DELETE FROM VnfInstance WHERE vnfId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCE DELETING"

		return delete.rowcount

	def __get_vib_platforms(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		platforms = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance;")
		if type(platforms) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING"

		return platforms

	def __post_vib_platforms(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.platformId + "\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED PLATFORM ALREADY EXISTS"

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORM INSERTION"

		return insertion.lastrowid

	def __get_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs +"\";")
		if type(platform) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORM CONSULTING"

		return platform

	def __patch_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)"

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.platformId + "\";")
		if type(platform) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING"
		if len(platform) == 0:
			return "ERROR CODE #3: THE REQUIRED PLATFORM DOES NOT EXIST"

		update = self.vibManager.operateVibDatabase(("UPDATE PlatformInstance SET platformDriver = ? WHERE platformId = ?;", (irManagement.operationArgs.platformDriver, irManagement.operationArgs.platformId)))
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORM UPDATING"

		return update.rowcount

	def __delete_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs + "\";")
		if type(platform) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING"
		if len(platform) == 0:
			return "ERROR CODE #3: THE REQUIRED PLATFORM DOES NOT EXIST"

		instances = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")
		for element in instances:
			if irManagement.operationArgs == element[2]:
				return "ERROR CODE #5: THE REQUIRED PLATFORM INSTANCE IS BEING USED IN THE VNF INSTANCE TABLE"

		delete = self.vibManager.operateVibDatabase(("DELETE FROM PlatformInstance WHERE platformId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING PLATFORM DELETING"

		return platform

	def __get_vib_vnf_managers(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		managers = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance;")
		if type(managers) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING"

		return managers

	def __post_vib_vnf_managers(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs.vnfmId + "\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED VNF MANAGER ALREADY EXISTS"

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGER INSERTION"

		return insertion.lastrowid

	def __get_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)"

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs +"\";")
		if type(manager) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING"

		return manager

	def __patch_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs.vnfmId + "\";")
		if type(manager) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING"
		if len(manager) == 0:
			return "ERROR CODE #3: THE REQUIRED VNF MANAGER DOES NOT EXIST"

		update = self.vibManager.operateVibDatabase(("UPDATE VnfmInstance SET vnfmDriver = ? WHERE vnfmId = ?;", (irManagement.operationArgs.vnfmDriver, irManagement.operationArgs.vnfmId)))
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF MANAGER UPDATING"

		return update.rowcount

	def __delete_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)"

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs + "\";")
		if type(manager) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNFM MANAGERS CONSULTING"
		if len(manager) == 0:
			return "ERROR CODE #3: THE REQUIRED VNFM MANAGER DOES NOT EXIST"

		delete = self.vibManager.operateVibDatabase(("DELETE FROM VnfmInstance WHERE vnfmId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNFM MANAGER DELETING"

		return delete.rowcount

