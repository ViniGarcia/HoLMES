import VsAgent
import AsOpAgent
import MsManager
import VibManager
import AsAuthAgent
import AsOpAgent

import VibModels
import IrModels
import AsModels

import sqlite3
import shutil
import json
import os

'''
CLASS: ImAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 01 Dez. 2020
L. UPDATE: 08 Dez. 2020 (Fulber-Garcia; Refactoring operations)
DESCRIPTION: Implementation of the internal manager agent of the EMS.
			 This class provides the configuration ans mantaining o-
			 perations of the other internal modules of the EMS.
ERROR CODES: 
			-1: Invalid vibManager received
			-2: Invalid msManager received
			-3: Invalid asAuthAgent received
			-4: Invalid asOpAgent received
			-5: Invalid vsAgent received
			-6: Invalid irManagement received
			-7: Invalid module requested
			-8: Invalid operation requested
OPERATION STR ERROR CODES:
			1: Invalid operation arguments
			2: SQL error during some operation
			3: Redundant data requested
			4: Missing required data
			5: Element is present in another table
			6: External error code
'''	
class ImAgent:

	vibManager = None
	msManager = None
	asAuthAgent = None
	asOpAgent = None
	vsAgent = None
	
	def __init__(self):
		return

	def setupAgent(self, vibManager, msManager, asAuthAgent, asOpAgent, vsAgent):

		if type(vibManager) != VibManager.VibManager:
			return -1
		if type(msManager) != MsManager.MsManager:
			return -2
		if type(asAuthAgent) != AsAuthAgent.AuthenticationAgent:
			return -3	
		if type(asOpAgent) != AsOpAgent.OperationAgent:
			return -4
		if type(vsAgent) != VsAgent.VsAgent:
			return -5
		
		self.vibManager = vibManager
		self.msManager = msManager
		self.asAuthAgent = asAuthAgent
		self.asOpAgent = asOpAgent
		self.vsAgent = vsAgent
		
		return self

	def requestOperation(self, irManagement):

		if type(irManagement) != IrModels.IrManagement:
			return -6

		if irManagement.moduleId == "VIB":
			return self.__executeVibOperation(irManagement)
		elif irManagement.moduleId == "MS":
			return self.__executeMsOperation(irManagement)
		elif irManagement.moduleId == "AS":
			return self.__executeAsOperation(irManagement)
		elif irManagement.moduleId == "VS":
			return self.__executeVsOperation(irManagement)
		else:
			return -7

	def __executeVibOperation(self, irManagement):

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
				return -8
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
				return -8
		elif irManagement.operationId.endswith("m_agents") or irManagement.operationId.endswith("ma_agentId"):
			if irManagement.operationId == "get_vib_m_agents":
				return self.__get_vib_m_agents(irManagement)
			elif irManagement.operationId == "post_vib_m_agents":
				return self.__post_vib_m_agents(irManagement)
			elif irManagement.operationId == "get_vib_ma_agentId":
				return self.__get_vib_ma_agentId(irManagement)
			elif irManagement.operationId == "patch_vib_ma_agentId":
				return self.__patch_vib_ma_agentId(irManagement)
			elif irManagement.operationId == "delete_vib_ma_agentId":
				return self.__delete_vib_ma_agentId(irManagement)
			else:
				return -8
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
				return -8
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
				return -8
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
				return -8
		else:
			return -8

	def __executeMsOperation(self, irManagement):

		if irManagement.operationId.endswith("subscription") or irManagement.operationId.endswith("subscriptionId"):
			if irManagement.operationId == "get_ms_running_subscription":
				return self.__get_ms_running_subscription(irManagement)
			elif irManagement.operationId == "post_ms_running_subscription":
				return self.__post_ms_running_subscription(irManagement)
			elif irManagement.operationId == "get_msrs_subscriptionId":
				return self.__get_msrs_subscriptionId(irManagement)
			elif irManagement.operationId == "patch_msrs_subscriptionId":
				return self.__patch_msrs_subscriptionId(irManagement)
			elif irManagement.operationId == "delete_msrs_subscriptionId":
				return self.__delete_msrs_subscriptionId(irManagement)
			elif irManagement.operationId == "get_ms_subscription":
				return self.__get_ms_subscription(irManagement)
			elif irManagement.operationId == "post_ms_subscription":
				return self.__post_ms_subscription(irManagement)
			elif irManagement.operationId == "get_mss_subscriptionId":
				return self.__get_mss_subscriptionId(irManagement)
			elif irManagement.operationId == "patch_mss_subscriptionId":
				return self.__patch_mss_subscriptionId(irManagement)
			elif irManagement.operationId == "delete_mss_subscriptionId":
				return self.__delete_mss_subscriptionId(irManagement)
			else:
				return -8
		elif irManagement.operationId.endswith("agent") or irManagement.operationId.endswith("agentId"):
			if irManagement.operationId == "get_ms_agent":
				return self.__get_ms_agent(irManagement)
			elif irManagement.operationId == "post_ms_agent":
				return self.__post_ms_agent(irManagement)
			elif irManagement.operationId == "get_msa_agentId":
				return self.__get_msa_agentId(irManagement)
			elif irManagement.operationId == "patch_msa_agentId":
				return self.__patch_msa_agentId(irManagement)
			elif irManagement.operationId == "delete_msa_agentId":
				return self.__delete_msa_agentId(irManagement)
			else:
				return -8
		else:
			return -8

	def __executeAsOperation(self, irManagement):

		if irManagement.operationId.endswith("auth") or irManagement.operationId.endswith("authId"):
			if irManagement.operationId == "get_as_auth":
				return self.__get_as_auth(irManagement)
			elif irManagement.operationId == "get_as_a_authId":
				return self.__get_as_a_authId(irManagement)
			elif irManagement.operationId == "get_as_running_auth":
				return self.__get_as_running_auth(irManagement)
			elif irManagement.operationId == "post_as_running_auth":
				return self.__post_as_running_auth(irManagement)
			elif irManagement.operationId == "get_as_ra_authId":
				return self.__get_as_ra_authId(irManagement)
			else:
				return -8
		elif irManagement.operationId.endswith("credential") or irManagement.operationId.endswith("credentialId"):
			if irManagement.operationId == "get_as_credential":
				return self.__get_as_credential(irManagement)
			elif irManagement.operationId == "post_as_credential":
				return self.__post_as_credential(irManagement)
			elif irManagement.operationId == "get_as_c_credentialId":
				return self.__get_as_c_credentialId(irManagement)
			elif irManagement.operationId == "patch_as_c_credentialId":
				return self.__patch_as_c_credentialId(irManagement)
			elif irManagement.operationId == "delete_as_c_credentialId":
				return self.__delete_as_c_credentialId(irManagement)
			else:
				return -8
		elif irManagement.operationId.endswith("driver") or irManagement.operationId.endswith("driverId"):
			if irManagement.operationId == "get_as_vnfm_running_driver":
				return self.__get_as_vnfm_running_driver(irManagement)
			elif irManagement.operationId == "post_as_vnfm_running_driver":
				return self.__post_as_vnfm_running_driver(irManagement)
			elif irManagement.operationId == "get_as_vrd_driverId":
				return self.__get_as_vrd_driverId(irManagement)
			elif irManagement.operationId == "get_as_vnfm_driver":
				return self.__get_as_vnfm_driver(irManagement)
			elif irManagement.operationId == "post_as_vnfm_driver":
				return self.__post_as_vnfm_driver(irManagement)
			elif irManagement.operationId == "get_as_vd_driverId":
				return self.__get_as_vd_driverId(irManagement)
			elif irManagement.operationId == "patch_as_vd_driverId":
				return self.__patch_as_vd_driverId(irManagement)
			elif irManagement.operationId == "delete_as_vd_driverId":
				return self.__delete_as_vd_driverId(irManagement)
			else:
				return -8
		else:
			return -8

	def __executeVsOperation(self, irManagement):

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
		elif irManagement.operationId == "get_vs_driver":
			return self.__get_vs_driver(irManagement)
		elif irManagement.operationId == "post_vs_driver":
			return self.__post_vs_driver(irManagement)
		elif irManagement.operationId == "get_vsd_driverId":
			return self.__get_vsd_driverId(irManagement)
		elif irManagement.operationId == "patch_vsd_driverId":
			return self.__patch_vsd_driverId(irManagement)
		elif irManagement.operationId == "delete_vsd_driverId":
			return self.__delete_vsd_driverId(irManagement)
		else:
			return -8

################################################################################################################################################################
################################################################################################################################################################

	def __get_vib_credentials(self, irManagement):

		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		credentials = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance;")
		if type(credentials) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING", 2)

		return [VibModels.VibCredentialInstance().fromSql(c) for c in credentials]

	def __post_vib_credentials(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs.userId +"\" AND vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED CREDENTIAL ALREADY EXISTS", 3)

		existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(existence) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
		if len(existence) == 0:
			return ("ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST", 4)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIAL INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)", 1)
		if type(irManagement.operationArgs[0]) != str or type(irManagement.operationArgs[1]) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)", 1)

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs[0] +"\" AND vnfId = \"" + irManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING", 2)
		if len(credential) == 0:
			return ("ERROR CODE #4: THE REQUIRED CREDENTIAL DOES NOT EXIST", 4)

		return VibModels.VibCredentialInstance().fromSql(credential[0])

	def __patch_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)", 1)

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs.userId +"\" AND vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(credential) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING", 2)
		if len(credential) == 0:
			return ("ERROR CODE #4: THE REQUIRED CREDENTIAL DOES NOT EXIST", 4)

		update = self.vibManager.operateVibDatabase(("UPDATE CredentialInstance SET authData = ?, authResource = ? WHERE userId = ? AND vnfId = ?;", (irManagement.operationArgs.authData, irManagement.operationArgs.authResource, irManagement.operationArgs.userId, irManagement.operationArgs.vnfId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING", 2)

		return VibModels.VibCredentialInstance().fromSql(credential[0])

	def __delete_vib_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)", 1)
		if type(irManagement.operationArgs[0]) != str or type(irManagement.operationArgs[1]) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)", 1)

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + irManagement.operationArgs[0] +"\" AND vnfId = \"" + irManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING", 2)
		if len(credential) == 0:
			return ("ERROR CODE #4: THE REQUIRED CREDENTIAL DOES NOT EXIST", 4)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM CredentialInstance WHERE userId = ? AND vnfId = ?;", (irManagement.operationArgs[0], irManagement.operationArgs[1])))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIAL DELETING", 2)

		return VibModels.VibCredentialInstance().fromSql(credential[0])

	#----

	def __get_vib_subscriptions(self, irManagement):

		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		if type(subscriptions) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING", 2)

		return [VibModels.VibSubscriptionInstance().fromSql(s) for s in subscriptions]

	def __post_vib_subscriptions(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs.visId +"\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED SUBSCRIPTION ALREADY EXISTS", 3)

		if irManagement.operationArgs.visFilter != None:
			if irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter != None:
				for vnfId in irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
					if len(existence) == 0:
						return ("ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST", 4)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)", 1)

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs +"\";")
		if type(subscription) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION CONSULTING", 2)
		if len(subscription) == 0:
			return ("ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST", 4)

		return VibModels.VibSubscriptionInstance().fromSql(subscription[0])

	def __patch_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)", 1)

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs.visId + "\";")
		if type(subscription) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING", 2)
		if len(subscription) == 0:
			return ("ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST", 4)

		if irManagement.operationArgs.visFilter != None:
			if irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter != None:
				for vnfId in irManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
					if len(existence) == 0:
						return ("ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST", 4)

		if irManagement.operationArgs.visFilter == None:
			update = self.vibManager.operateVibDatabase(("UPDATE SubscriptionInstance SET visFilter = ?, visCallback = ?, visLinks = ? WHERE visId = ?;", (irManagement.operationArgs.visFilter, irManagement.operationArgs.visCallback, json.dumps(irManagement.operationArgs.visLinks), irManagement.operationArgs.visId)))
		else:
			update = self.vibManager.operateVibDatabase(("UPDATE SubscriptionInstance SET visFilter = ?, visCallback = ?, visLinks = ? WHERE visId = ?;", (json.dumps(irManagement.operationArgs.visFilter.toDictionary()), irManagement.operationArgs.visCallback, json.dumps(irManagement.operationArgs.visLinks), irManagement.operationArgs.visId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING", 2)

		return VibModels.VibSubscriptionInstance().fromSql(subscription[0])

	def __delete_vib_s_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)", 1)

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + irManagement.operationArgs + "\";")
		if type(subscription) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING", 2)
		if len(subscription) == 0:
			return ("ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST", 4)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM SubscriptionInstance WHERE visId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING CREDENTIAL DELETING", 2)

		return VibModels.VibSubscriptionInstance().fromSql(subscription[0])

	#----

	def __get_vib_m_agents(self, irManagement):
		
		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		agents = self.vibManager.queryVibDatabase("SELECT * FROM MaInstance;")
		if type(agents) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENTS CONSULTING", 2)

		return [VibModels.VibMaInstance().fromSql(a) for a in agents]

	def __post_vib_m_agents(self, irManagement):
		
		if type(irManagement.operationArgs) != VibModels.VibMaInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibMaInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"" + irManagement.operationArgs.maId + "\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENTS CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED MONITORING AGENT ALREADY EXISTS", 3)

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.maPlatform + "\";")
		if type(platform) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(platform) == 0:
			return ("ERROR CODE #4: THE REQUIRED PLATFORM INSTANCE DOES NOT EXIST", 4)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENT INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_ma_agentId(self, irManagement):
		
		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (maId is expected)", 1)

		agent = self.vibManager.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"" + irManagement.operationArgs +"\";")
		if type(agent) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENT CONSULTING", 2)
		if len(agent) == 0:
			return ("ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST", 4)

		return VibModels.VibMaInstance().fromSql(agent[0])

	def __patch_vib_ma_agentId(self, irManagement):
		
		if type(irManagement.operationArgs) != VibModels.VibMaInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibMaInstance is expected)", 1)

		agent = self.vibManager.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"" + irManagement.operationArgs.maId + "\";")
		if type(agent) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENTS CONSULTING", 2)
		if len(agent) == 0:
			return ("ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST", 4)

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.maPlatform + "\";")
		if type(platform) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(platform) == 0:
			return ("ERROR CODE #4: THE REQUIRED PLATFORM INSTANCE DOES NOT EXIST", 4)

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		for element in subscriptions:
			element = VibModels.VibSubscriptionInstance().fromSql(element)
			if irManagement.operationArgs in element.visFilter.indicatorIds:
				return ("ERROR CODE #5: THE REQUIRED MONITORING AGENT INSTANCE IS BEING USED IN THE SUBSCRIPTION TABLE", 5)

		update = self.vibManager.operateVibDatabase(("UPDATE MaInstance SET maSource = ?, maPlatform = ? WHERE maId = ?;", (irManagement.operationArgs.maSource, irManagement.operationArgs.maPlatform, irManagement.operationArgs.maId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENT UPDATING", 2)

		return VibModels.VibMaInstance().fromSql(agent[0])

	def __delete_vib_ma_agentId(self, irManagement):
		
		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (maId is expected)", 1)

		agent = self.vibManager.queryVibDatabase("SELECT * FROM MaInstance WHERE maId = \"" + irManagement.operationArgs + "\";")
		if type(agent) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENTS CONSULTING", 2)
		if len(agent) == 0:
			return ("ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST", 4)

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		for element in subscriptions:
			element = VibModels.VibSubscriptionInstance().fromSql(element)
			if irManagement.operationArgs in element.visFilter.indicatorIds:
				return ("ERROR CODE #5: THE REQUIRED MONITORING AGENT INSTANCE IS BEING USED IN THE SUBSCRIPTION TABLE", 5)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM MaInstance WHERE maId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING MONITORING AGENT DELETING", 2)

		return VibModels.VibMaInstance().fromSql(agent[0])

	#----

	def __get_vib_instances(self, irManagement):

		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		instances = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")
		if type(instances) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)

		return [VibModels.VibVnfInstance().fromSql(i) for i in instances]

	def __post_vib_instances(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED VNF INSTANCE ALREADY EXISTS", 3)

		existence = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.vnfPlatform + "\";")
		if type(existence) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(existence) == 0:
			return ("ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST", 4)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCE INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfId is expected)", 1)

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs +"\";")
		if type(instance) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
		if len(instance) == 0:
			return ("ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST", 4)

		return VibModels.VibVnfInstance().fromSql(instance[0])

	def __patch_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfInstance is expected)", 1)

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs.vnfId + "\";")
		if type(instance) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
		if len(instance) == 0:
			return ("ERROR CODE #4: THE REQUIRED INSTANCE DOES NOT EXIST", 4)

		if instance[0][2] != irManagement.operationArgs.vnfPlatform:
			existence = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.vnfPlatform + "\";")
			if type(existence) == sqlite3.Error:
				return ("ERROR CODE #2: SQL ERROR DURING VNF PLATFORMS CONSULTING", 2)
			if len(existence) == 0:
				return ("ERROR CODE #4: THE REQUIRED VNF PLATFORM DOES NOT EXIST", 4)

		update = self.vibManager.operateVibDatabase(("UPDATE VnfInstance SET vnfAddress = ?, vnfPlatform = ?, vnfExtAgents = ?, vnfAuth = ? WHERE vnfId = ?;", (irManagement.operationArgs.vnfAddress, irManagement.operationArgs.vnfPlatform, json.dumps(irManagement.operationArgs.vnfExtAgents), irManagement.operationArgs.vnfAuth, irManagement.operationArgs.vnfId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCE UPDATING", 2)

		return VibModels.VibVnfInstance().fromSql(instance[0])

	def __delete_vib_i_instanceId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfId is expected)", 1)

		instance = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + irManagement.operationArgs + "\";")
		if type(instance) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING", 2)
		if len(instance) == 0:
			return ("ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST", 4)

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		for element in subscriptions:
			if element[1] != None:
				element = json.loads(element[1])
				if element["vnfInstanceSubscriptionFilter"] != None:
					 if irManagement.operationArgs in element["vnfInstanceSubscriptionFilter"]["vnfInstanceIds"]:
					 	return ("ERROR CODE #5: THE REQUIRED VNF INSTANCE IS BEING USED IN THE SUBSCRIPTION TABLE", 5)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM VnfInstance WHERE vnfId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF INSTANCE DELETING", 2)

		return VibModels.VibVnfInstance().fromSql(instance[0])

	#----

	def __get_vib_platforms(self, irManagement):

		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		platforms = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance;")
		if type(platforms) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)

		return [VibModels.VibPlatformInstance().fromSql(p) for p in platforms]

	def __post_vib_platforms(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.platformId + "\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED PLATFORM ALREADY EXISTS", 3)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORM INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)", 1)

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs +"\";")
		if type(platform) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORM CONSULTING", 2)
		if len(platform) == 0:
			return ("ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST", 4)

		return VibModels.VibPlatformInstance().fromSql(platform[0])

	def __patch_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibPlatformInstance is expected)", 1)

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs.platformId + "\";")
		if type(platform) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(platform) == 0:
			return ("ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST", 4)

		update = self.vibManager.operateVibDatabase(("UPDATE PlatformInstance SET platformDriver = ? WHERE platformId = ?;", (irManagement.operationArgs.platformDriver, irManagement.operationArgs.platformId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORM UPDATING", 2)

		return VibModels.VibPlatformInstance().fromSql(platform[0])

	def __delete_vib_p_platformId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)", 1)

		platform = self.vibManager.queryVibDatabase("SELECT * FROM PlatformInstance WHERE platformId = \"" + irManagement.operationArgs + "\";")
		if type(platform) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORMS CONSULTING", 2)
		if len(platform) == 0:
			return ("ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST", 4)

		instances = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance;")
		for element in instances:
			if irManagement.operationArgs == element[2]:
				return ("ERROR CODE #5: THE REQUIRED PLATFORM INSTANCE IS BEING USED IN THE VNF INSTANCE TABLE", 5)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM PlatformInstance WHERE platformId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING PLATFORM DELETING", 2)

		return VibModels.VibPlatformInstance().fromSql(platform[0])

	#----

	def __get_vib_vnf_managers(self, irManagement):

		if irManagement.operationArgs != None:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)", 1)

		managers = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance;")
		if type(managers) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING", 2)

		return [VibModels.VibVnfmInstance().fromSql(m) for m in managers]

	def __post_vib_vnf_managers(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)", 1)

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs.vnfmId + "\";")
		if type(redundancy) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING", 2)
		if len(redundancy) != 0:
			return ("ERROR CODE #3: THE REQUIRED VNF MANAGER ALREADY EXISTS", 3)

		insertion = self.vibManager.operateVibDatabase(irManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGER INSERTION", 2)

		return irManagement.operationArgs

	def __get_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)", 1)

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs +"\";")
		if type(manager) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING", 2)
		if len(manager) == 0:
			return ("ERROR CODE #4: THE REQUIRED VNF MANAGER DOES NOT EXIST", 4)

		return VibModels.VibVnfmInstance().fromSql(manager[0])

	def __patch_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs.vnfmId + "\";")
		if type(manager) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGERS CONSULTING", 2)
		if len(manager) == 0:
			return ("ERROR CODE #4: THE REQUIRED VNF MANAGER DOES NOT EXIST", 4)

		update = self.vibManager.operateVibDatabase(("UPDATE VnfmInstance SET vnfmDriver = ? WHERE vnfmId = ?;", (irManagement.operationArgs.vnfmDriver, irManagement.operationArgs.vnfmId)))
		if type(update) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNF MANAGER UPDATING", 2)

		return VibModels.VibVnfmInstance().fromSql(manager[0])

	def __delete_vib_vnfm_managerId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return ("ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)", 1)

		manager = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmId = \"" + irManagement.operationArgs + "\";")
		if type(manager) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNFM MANAGERS CONSULTING", 2)
		if len(manager) == 0:
			return ("ERROR CODE #4: THE REQUIRED VNFM MANAGER DOES NOT EXIST", 4)

		delete = self.vibManager.operateVibDatabase(("DELETE FROM VnfmInstance WHERE vnfmId = ?;", (irManagement.operationArgs, )))
		if type(delete) == sqlite3.Error:
			return ("ERROR CODE #2: SQL ERROR DURING VNFM MANAGER DELETING", 2)

		return VibModels.VibVnfmInstance().fromSql(manager[0])

################################################################################################################################################################
################################################################################################################################################################

	def __get_as_auth(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.asAuthAgent.getAuthenticators()

	def __get_as_a_authId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (authId is expected)"

		if irManagement.operationArgs in self.asAuthAgent.getAuthenticators():
			return True

		return False

	def __get_as_running_auth(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.asAuthAgent.getRunningAuthenticator()

	def __post_as_running_auth(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (authId is expected)"

		result = self.asAuthAgent.setupAuthentication(irManagement.operationArgs)
		if result < 0:
			return "ERROR CODE #6: AN ERROR OCCURED WHEN SETUPING THE AUTHENTICATION AGENT (" + str(result) + ")"

		return 1

	def __get_as_ra_authId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (authId is expected)"

		if self.asAuthAgent.getRunningAuthenticator() == irManagement.operationArgs:
			return True

		return False

	def __get_as_credential(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.__get_vib_credentials(irManagement)

	def __post_as_credential(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibCredentialInstance PROVIDED"

		return self.__post_vib_credentials(irManagement)

	def __get_as_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"

		return self.__get_vib_c_credentialId(irManagement)

	def __patch_as_c_credentialId(self, irManagement):
		
		if type(irManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibCredentialInstance PROVIDED"

		return self.__patch_vib_c_credentialId(irManagement)

	def __delete_as_c_credentialId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"

		return self.__delete_vib_c_credentialId(irManagement)

	def __get_as_vnfm_running_driver(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.asOpAgent.getRunningDriver()

	def __post_as_vnfm_running_driver(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"

		result = self.asOpAgent.setupDriver(irManagement.operationArgs)
		if result < 0:
			return "ERROR CODE #6: AN ERROR OCCURED WHEN SETUPING THE VNFM RUNNING DRIVER (" + str(result) + ")"

		return True
	
	def __get_as_vrd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)"

		if self.asOpAgent.getRunningDriver() == irManagement.operationArgs:
			return True

		return False

	def __get_as_vnfm_driver(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.__get_vib_vnf_managers(irManagement)

	def __post_as_vnfm_driver(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibVnfmInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.vnfmDriver) or not irManagement.operationArgs.vnfmDriver.endswith(".py"):
			return "ERROR CODE #1: INVALID VibVnfmInstance.vnfmDriver PROVIDED"

		original = irManagement.operationArgs.vnfmDriver
		irManagement.operationArgs.vnfmDriver = irManagement.operationArgs.vnfmDriver.replace("\\", "/").split("/")[-1][:-3]

		result = self.__post_vib_vnf_managers(irManagement)
		if type(result) == str:
			return result

		shutil.copyfile(original, "Access Subsystem/Ve-Vnfm-em/" + irManagement.operationArgs.vnfmDriver + ".py")

		return 1

	def __get_as_vd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)"

		return self.__get_vib_vnfm_managerId(irManagement)

	def __patch_as_vd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibVnfmInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibVnfmInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibVnfmInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.vnfmDriver) or not irManagement.operationArgs.vnfmDriver.endswith(".py"):
			return "ERROR CODE #1: INVALID VibVnfmInstance.vnfmDriver PROVIDED"
		if self.__get_as_vrd_driverId(IrModels.IrManagement().fromData("AS", "get_as_vrd_driverId", irManagement.operationArgs.vnfmId)):
			return "ERROR CODE #1: VibVnfmInstance.vnfmId IS THE RUNNING DRIVER"
		
		original = irManagement.operationArgs.vnfmDriver
		irManagement.operationArgs.vnfmDriver = irManagement.operationArgs.vnfmDriver.replace("\\", "/").split("/")[-1][:-3]

		result = self.__patch_vib_vnfm_managerId(irManagement)
		if type(result) == str:
			return result

		if result[0][1] != irManagement.operationArgs.vnfmDriver:
			delete = self.vibManager.queryVibDatabase("SELECT * FROM VnfmInstance WHERE vnfmDriver = \"" + result[0][1] + "\";")
			if len(delete) == 0:
				os.remove("VNF Subsystem/Ve-Em-vnf/" + result.vnfmDriver + ".py")

		shutil.copyfile(original, "Access Subsystem/Ve-Vnfm-em/" + irManagement.operationArgs.vnfmDriver + ".py")

		return 1

	def __delete_as_vd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (vnfmId is expected)"
		if self.__get_as_vrd_driverId(IrModels.IrManagement().fromData("AS", "get_as_vrd_driverId", irManagement.operationArgs)):
			return "ERROR CODE #1: VibVnfmInstance.vnfmId IS THE RUNNING DRIVER"

		result = self.__delete_vib_vnfm_managerId(irManagement)
		if type(result) == str:
			return result

		os.remove("Access Subsystem/Ve-Vnfm-em/" + result[0][1] + ".py")

		return 1

################################################################################################################################################################
################################################################################################################################################################

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

		return list(self.vsAgent.get_p_operations().keys())

	def __get_vs_rdo_monitoring(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return list(self.vsAgent.get_po_monitoring().keys())

	def __get_vs_rdo_modification(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return list(self.vsAgent.get_po_modification().keys())

	def __get_vs_rdo_other(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return list(self.vsAgent.get_po_other().keys())

	def __get_vs_driver(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.__get_vib_platforms(irManagement)

	def __post_vs_driver(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
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
		shutil.copyfile(original, "VNF Subsystem/Ve-Em-vnf/" + irManagement.operationArgs.platformDriver + ".py")

		return 1

	def __get_vsd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"

		return self.__get_vib_p_platformId(irManagement)

	def __patch_vsd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibPlatformInstance:
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

		if self.vsAgent.get_p_id() == irManagement.operationArgs:
			self.vsAgent.detach()

		if result[0][1] != irManagement.operationArgs.platformDriver:
			delete = self.vibManager.queryVibDatabase("SELECT * FROM PlatformINstance WHERE platformDriver = \"" + result.platformDriver + "\";")
			if len(delete) == 0:
				os.remove("VNF Subsystem/Ve-Em-vnf/" + result.platformDriver + ".py")

		shutil.copyfile(original, "VNF Subsystem/Ve-Em-vnf/" + irManagement.operationArgs.platformDriver + ".py")

		return 1

	def __delete_vsd_driverId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (platformId is expected)"	

		result = self.__delete_vib_p_platformId(irManagement)
		if type(result) == str:
			return result

		if self.vsAgent.get_p_id() == result[0][1]:
			self.vsAgent.detach()

		os.remove("VNF Subsystem/Ve-Em-vnf/" + result[0][1] + ".py")

		return 1

################################################################################################################################################################
################################################################################################################################################################

	def __get_ms_running_subscription(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.msManager.getAgents()

	def __post_ms_running_subscription(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (subscriptionId is expected)"

		subscription = self.__get_vib_s_subscriptionId(irManagement)
		if type(subscription) == str:
			return subscription
		if len(subscription) == 0:
			return "ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"
		subscription = VibModels.VibSubscriptionInstance().fromSql(subscription[0])

		if subscription.visFilter == None or subscription.visFilter.vnfInstanceSubscriptionFilter == None:
			return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"

		vnfInstances = []
		for instanceId in subscription.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
			instance = self.__get_vib_i_instanceId(IrModels.IrManagement().fromData("VIB", "get_vib_i_instanceId", instanceId))
			if type(instance) == str:
				return instance
			if len(instance) == 0:
				return "ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST"
			vnfInstances.append(VibModels.VibVnfInstance().fromSql(instance[0]))

		platformInstance = self.__get_vib_p_platformId(IrModels.IrManagement().fromData("VIB", "get_vib_p_platformId", vnfInstances[0].vnfPlatform))
		if type(platformInstance) == str:
			return platformInstance
		if len(platformInstance) == 0:
			return "ERROR CODE #4: THE REQUIRED PLATFORM DOES NOT EXIST"

		result = self.msManager.setupAgent(subscription, vnfInstances, VibModels.VibPlatformInstance().fromSql(platformInstance[0]))
		if type(result) == int:
			return "ERROR CODE #6: AN ERROR OCCURED WHILE SETUPING THE SUBSCRIPTION AGENT (" + str(result) + ")"

		return result

	def __get_msrs_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (subscriptionId is expected)"

		if not irManagement.operationArgs in self.msManager.getAgents():
			return False

		return True

	def __patch_msrs_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((subscriptionId, ) or (subscriptionId, resourcesData) is expected)"
		if type(irManagement.operationArgs[0]) != str:
			return "ERROR CODE #1: INVALID subscriptionId PROVIDED (str is expected)" 

		subscription = self.__get_vib_s_subscriptionId(IrModels.IrManagement().fromData("VIB", "get_vib_s_subscriptionId", irManagement.operationArgs[0]))
		if type(subscription) == str:
			return subscription
		if len(subscription) == 0:
			return "ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"
		subscription = VibModels.VibSubscriptionInstance().fromSql(subscription[0])

		if len(irManagement.operationArgs) == 1:
			result = self.msManager.stopAgent(subscription)
			if result != 0:
				return "ERROR CODE #6: AN ERROR OCCURED WHILE STOPPING THE SUBSCRIPTION AGENT (" + str(result) + ")"
		else:
			result = self.msManager.startAgent(subscription, irManagement.operationArgs[1])
			if result != 0:
				return "ERROR CODE #6: AN ERROR OCCURED WHILE STARTING THE SUBSCRIPTION AGENT (" + str(result) + ")"

		return 1

	def __delete_msrs_subscriptionId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (subscriptionId is expected)"

		subscription = self.__get_vib_s_subscriptionId(irManagement)
		if type(subscription) == str:
			return subscription
		if len(subscription) == 0:
			return "ERROR CODE #4: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"

		result = self.msManager.removeAgent(VibModels.VibSubscriptionInstance().fromSql(subscription[0]))
		if result != 0:
			return "ERROR CODE #6: AN ERROR OCCURED WHILE DELETING THE SUBSCRIPTION AGENT (" + str(result) + ")"

		return subscription

	def __get_ms_subscription(self, irManagement):
		
		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.__get_vib_subscriptions(irManagement)

	def __post_ms_subscription(self, irManagement):
		
		if type(irManagement.operationArgs) != AsModels.VnfIndicatorSubscriptionRequest:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VnfIndicatorSubscriptionRequest is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VnfIndicatorSubscriptionRequest PROVIDED"
		if irManagement.operationArgs.filter == None or irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter == None:
			return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"
		if len(irManagement.operationArgs.filter.indicatorIds) == 0 or len(irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter.vnfInstanceIds) == 0:
			return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"

		platform = None
		for instanceId in irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
			instance = self.__get_vib_i_instanceId(IrModels.IrManagement().fromData("VIB", "get_vib_i_instanceId", instanceId))
			if type(instance) == str:
				return instance
			if len(instance) == 0:
				return "ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST"
			if platform != None:
				if platform != instance[0][2]:
					return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"
			else:
				platform = instance[0][2]

		for monitoringAgent in irManagement.operationArgs.filter.indicatorIds:
			if not os.path.isfile("Monitoring Subsystem/Monitoring Agents/" + monitoringAgent + ".py"):
				return "ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST"

		result = self.msManager.requestAgent(irManagement.operationArgs)
		if type(result) == int:
			return "ERROR CODE #6: AN ERROR OCCURED WHILE CREATING THE SUBSCRIPTION AGENT (" + str(result) + ")"

		self.vibManager.operateVibDatabase(VibModels.VibSubscriptionInstance().fromData(result.id, result.filter, result.callbackUri, result.links).toSql())
		
		return result

	def __get_mss_subscriptionId(self, irManagement):
		
		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (subscriptionId is expected)"

		return self.__get_vib_s_subscriptionId(irManagement)

	def __patch_mss_subscriptionId(self, irManagement):
		
		if type(irManagement.operationArgs) != AsModels.VnfIndicatorSubscription:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VnfIndicatorSubscription is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VnfIndicatorSubscription PROVIDED"
		if self.__get_msrs_subscriptionId(IrModels.IrManagement().fromData("MS", "get_msra_agentId", irManagement.operationArgs.id)):
			return "ERROR CODE #1: PROVIDED VnfIndicatorSubscription IS A RUNNING SUBSCRIPTION AGENT"
		if irManagement.operationArgs.filter == None or irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter == None:
			return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"
		if len(irManagement.operationArgs.filter.indicatorIds) == 0 or len(irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter.vnfInstanceIds) == 0:
			return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"

		platform = None
		for instanceId in irManagement.operationArgs.filter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
			instance = self.__get_vib_i_instanceId(IrModels.IrManagement().fromData("VIB", "get_vib_i_instanceId", instanceId))
			if type(instance) == str:
				return instance
			if len(instance) == 0:
				return "ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST"
			if platform != None:
				if platform != instance[0][2]:
					return "ERROR CODE #1: THE REQUIRED SUBSCRIPTION IS NOT SUPPORTED BY THE MONITORING SUBSYSTEM"
			else:
				platform = instance[0][2]

		for monitoringAgent in irManagement.operationArgs.filter.indicatorIds:
			if not os.path.isfile("Monitoring Subsystem/Monitoring Agents/" + monitoringAgent + ".py"):
				return "ERROR CODE #4: THE REQUIRED MONITORING AGENT DOES NOT EXIST"

		subscription = VibModels.VibSubscriptionInstance().fromData(irManagement.operationArgs.id, irManagement.operationArgs.filter, irManagement.operationArgs.callbackUri, irManagement.operationArgs.links)
		result = self.__patch_vib_s_subscriptionId(IrModels.IrManagement().fromData("VIB", "patch_vib_s_subscriptionId", subscription))

		return result

	def __delete_mss_subscriptionId(self, irManagement):
		
		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (subscriptionId is expected)"
		if self.__get_msrs_subscriptionId(irManagement):
			return "ERROR CODE #1: PROVIDED subscriptionId IS A RUNNING AGENT"

		subscription = self.__delete_vib_s_subscriptionId(irManagement)
		if type(subscription) == str:
			return subscription

		return 1

	def __get_ms_agent(self, irManagement):

		if irManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		return self.__get_vib_m_agents(irManagement)

	def __post_ms_agent(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibMaInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibMaInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibMaInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.maSource) or not irManagement.operationArgs.maSource.endswith(".py"):
			return "ERROR CODE #1: INVALID VibMaInstance.maSource PROVIDED"

		original = irManagement.operationArgs.maSource
		irManagement.operationArgs.maSource = irManagement.operationArgs.maSource.replace("\\", "/").split("/")[-1][:-3]

		result = self.__post_vib_m_agents(irManagement)
		if type(result) == str:
			return result
		shutil.copyfile(original, "Monitoring Subsystem/Monitoring Agents/" + irManagement.operationArgs.maSource + ".py")

		return 1

	def __get_msa_agentId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (maId is expected)"

		return self.__get_vib_ma_agentId(irManagement)

	def __patch_msa_agentId(self, irManagement):

		if type(irManagement.operationArgs) != VibModels.VibMaInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibMaInstance is expected)"
		if irManagement.operationArgs.validate()[1] != 0:
			return "ERROR CODE #1: INVALID VibMaInstance PROVIDED"
		if not os.path.isfile(irManagement.operationArgs.maSource) or not irManagement.operationArgs.maSource.endswith(".py"):
			return "ERROR CODE #1: INVALID VibMaInstance.maSource PROVIDED"

		original = irManagement.operationArgs.maSource
		irManagement.operationArgs.maSource = irManagement.operationArgs.maSource.replace("\\", "/").split("/")[-1][:-3]

		result = self.__patch_vib_ma_agentId(irManagement)
		if type(result) == str:
			return result

		shutil.copyfile(original, "Monitoring Subsystem/Monitoring Agents/" + irManagement.operationArgs.maSource + ".py")

		return 1

	def __delete_msa_agentId(self, irManagement):

		if type(irManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (maId is expected)"

		result = self.__delete_vib_ma_agentId(irManagement)
		if type(result) == str:
			return result

		os.remove("Monitoring Subsystem/Monitoring Agents/" + result[0][1] + ".py")

		return 1