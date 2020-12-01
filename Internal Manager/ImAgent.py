import VsAgent
import AsOpAgent
import MsManager
import VibManager

import VibModels
import IrModels

import sqlite3
import json

'''
CLASS: ImAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 01 Dez. 2020
L. UPDATE: 01 Dez. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Implementation of the internal manager agent of the EMS.
			 This class provides the configuration ans mantaining o-
			 perations of the other internal modules of the EMS.
ERROR CODES: 
			-1: Invalid asAgent received
			-2: Invalid vsAgent received
			-3: Invalid msManager received
			-4: Invalid vibManager received
			-5: Invalid operation received
			-6: Invalid vibManagement received
OPERATION STR ERROR CODES:
			1: Invalid operation arguments
			2: SQL error during some operation
			3: Redundant data requested
			4: Missing required data
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
		#if type(vsAgent) != VsAgent.VsAgent:
		#	return -2
		#if type(msManager) != MsManager.MsManager:
		#	return -3
		if type(vibManager) != VibManager.VibManager:
			return -4

		self.asAgent = asAgent
		self.vsAgent = vsAgent
		self.msManager = msManager
		self.vibManager = vibManager

		return self

	def executeVibOperation(self, vibManagement):

		if type(vibManagement) != IrModels.VibManagement:
			return -6

		if vibManagement.operationId.endswith("credentials") or vibManagement.operationId.endswith("credentialId"):
			if vibManagement.operationId == "get_vib_credentials":
				return self.__get_vib_credentials(vibManagement)
			elif vibManagement.operationId == "post_vib_credentials":
				return self.__post_vib_credentials(vibManagement)
			elif vibManagement.operationId == "get_vib_c_credentialId":
				return self.__get_vib_c_credentialId(vibManagement)
			elif vibManagement.operationId == "patch_vib_c_credentialId":
				return self.__patch_vib_c_credentialId(vibManagement)
			elif vibManagement.operationId == "delete_vib_c_credentialId":
				return self.__delete_vib_c_credentialId(vibManagement)
			else:
				return -5

		elif vibManagement.operationId.endswith("subscriptions") or vibManagement.operationId.endswith("subscriptionId"):
			if vibManagement.operationId == "get_vib_subscriptions":
				return self.__get_vib_subscriptions(vibManagement)
			elif vibManagement.operationId == "post_vib_subscriptions":
				return self.__post_vib_subscriptions(vibManagement)
			elif vibManagement.operationId == "get_vib_s_subscriptionId":
				return self.__get_vib_s_subscriptionId(vibManagement)
			elif vibManagement.operationId == "patch_vib_s_subscriptionId":
				return self.__patch_vib_s_subscriptionId(vibManagement)
			elif vibManagement.operationId == "delete_vib_s_subscriptionId":
				return self.__delete_vib_s_subscriptionId(vibManagement)
			else:
				return -5

		elif vibManagement.operationId.endswith("platforms") or vibManagement.operationId.endswith("platformId"):
			if vibManagement.operationId == "get_vib_platforms":
				return
			elif vibManagement.operationId == "post_vib_platforms":
				return
			elif vibManagement.operationId == "get_vib_p_platformId":
				return
			elif vibManagement.operationId == "patch_vib_p_platformId":
				return
			elif vibManagement.operationId == "delete_vib_p_platformId":
				return
			else:
				return -5

		elif vibManagement.operationId.endswith("instances") or vibManagement.operationId.endswith("instanceId"):
			if vibManagement.operationId == "get_vib_instances":
				return
			elif vibManagement.operationId == "post_vib_instances":
				return
			elif vibManagement.operationId == "get_vib_i_instanceId":
				return
			elif vibManagement.operationId == "patch_vib_i_instanceId":
				return
			elif vibManagement.operationId == "delete_vib_i_instanceId":
				return
			else:
				return -5

		elif vibManagement.operationId.endswith("vnf_managers") or vibManagement.operationId.endswith("vnfm_managerId"):
			if vibManagement.operationId == "get_vib_vnf_managers":
				return
			elif vibManagement.operationId == "post_vib_vnf_managers":
				return
			elif vibManagement.operationId == "get_vib_vnfm_managerId":
				return
			elif vibManagement.operationId == "patch_vib_vnfm_managerId":
				return
			elif vibManagement.operationId == "delete_vib_vnfm_managerId":
				return
			else:
				return -5

		else:
			return -5

		
	def __get_vib_credentials(self, vibManagement):

		if vibManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		credentials = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance;")
		if type(credentials) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"

		return credentials

	def __post_vib_credentials(self, vibManagement):

		if type(vibManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + vibManagement.operationArgs.userId +"\" AND vnfId = \"" + vibManagement.operationArgs.vnfId + "\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL ALREADY EXISTS"

		existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vibManagement.operationArgs.vnfId + "\";")
		if type(existence) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
		if len(existence) == 0:
			return "ERROR CODE #4: THE REQUIRED VNF INSTANCE DOES NOT EXIST"

		insertion = self.vibManager.insertVibDatabase(vibManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL INSERTION"

		return insertion

	def __get_vib_c_credentialId(self, vibManagement):

		if type(vibManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"
		if type(vibManagement.operationArgs[0]) != str or type(vibManagement.operationArgs[1]) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + vibManagement.operationArgs[0] +"\" AND vnfId = \"" + vibManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"

		return credential

	def __patch_vib_c_credentialId(self, vibManagement):

		if type(vibManagement.operationArgs) != VibModels.VibCredentialInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibCredentialInstance is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + vibManagement.operationArgs.userId +"\" AND vnfId = \"" + vibManagement.operationArgs.vnfId + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS CONSULTING"
		if len(credential) == 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL DOES NOT EXIST"

		update = self.vibManager.operateVibDatabase("UPDATE CredentialInstance SET authData = \"" + vibManagement.operationArgs.authData + "\", authResource = \"" + vibManagement.operationArgs.authResource + "\" WHERE userId = \"" + vibManagement.operationArgs.userId +"\" AND vnfId = \"" + vibManagement.operationArgs.vnfId + "\";")
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING"

		return update

	def __delete_vib_c_credentialId(self, vibManagement):

		if type(vibManagement.operationArgs) != tuple:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((userId, vnfId) is expected)"
		if type(vibManagement.operationArgs[0]) != str or type(vibManagement.operationArgs[1]) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED ((str, str) is expected)"

		credential = self.vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + vibManagement.operationArgs[0] +"\" AND vnfId = \"" + vibManagement.operationArgs[1] + "\";")
		if type(credential) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"
		if len(credential) == 0:
			return "ERROR CODE #3: THE REQUIRED CREDENTIAL DOES NOT EXIST"

		delete = self.vibManager.operateVibDatabase("DELETE FROM CredentialInstance WHERE userId = \"" + vibManagement.operationArgs[0] +"\" AND vnfId = \"" + vibManagement.operationArgs[1] + "\";")
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"

		return delete

	def __get_vib_subscriptions(self, vibManagement):

		if vibManagement.operationArgs != None:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (None is expected)"

		subscriptions = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance;")
		if type(subscriptions) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"

		return subscriptions

	def __post_vib_subscriptions(self, vibManagement):

		if type(vibManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)"

		redundancy = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + vibManagement.operationArgs.visId +"\";")
		if type(redundancy) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(redundancy) != 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION ALREADY EXISTS"

		if vibManagement.operationArgs.visFilter != None:
			if vibManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter != None:
				for vnfId in vibManagement.operationArgs.visFilter.vnfInstanceSubscriptionFilter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
					if len(existence) == 0:
						return "ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST"

		insertion = self.vibManager.insertVibDatabase(vibManagement.operationArgs.toSql())
		if type(insertion) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION INSERTION"

		return insertion

	def __get_vib_s_subscriptionId(self, vibManagement):

		if type(vibManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + vibManagement.operationArgs +"\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTION CONSULTING"

		return subscription

	def __patch_vib_s_subscriptionId(self, vibManagement):

		if type(vibManagement.operationArgs) != VibModels.VibSubscriptionInstance:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (VibSubscriptionInstance is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + vibManagement.operationArgs.visId + "\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(subscription) == 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"

		if vibManagement.operationArgs.visFilter != None:
			if vibManagement.operationArgs.visFilter.filter != None:
				for vnfId in vibManagement.operationArgs.visFilter.filter.vnfInstanceIds:
					existence = self.vibManager.queryVibDatabase("SELECT * FROM VnfInstance WHERE vnfId = \"" + vnfId + "\";")
					if type(existence) == sqlite3.Error:
						return "ERROR CODE #2: SQL ERROR DURING VNF INSTANCES CONSULTING"
					if len(existence) == 0:
						return "ERROR CODE #4: A REQUIRED VNF INSTANCE DOES NOT EXIST"

		if vibManagement.operationArgs.visFilter == None:
			update = self.vibManager.operateVibDatabase("UPDATE CredentialInstance SET visFilter = \"" + vibManagement.operationArgs.visFilter + "\", visCallback = \"" + vibManagement.operationArgs.visCallback + "\", visLinks = \"" + json.dumps(vibManagement.operationArgs.visLinks) + "\" WHERE visId = \"" + vibManagement.operationArgs.visId + "\";")
		else:
			update = self.vibManager.operateVibDatabase("UPDATE CredentialInstance SET visFilter = \"" + json.dumps(vibManagement.operationArgs.visFilter.toDictionary()) + "\", visCallback = \"" + vibManagement.operationArgs.visCallback + "\", visLinks = \"" + json.dumps(vibManagement.operationArgs.visLinks) + "\" WHERE visId = \"" + vibManagement.operationArgs.visId + "\";")
		if type(update) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIALS UPDATING"

	def __delete_vib_s_subscriptionId(self, vibManagement):

		if type(vibManagement.operationArgs) != str:
			return "ERROR CODE #1: INVALID ARGUMENTS PROVIDED (visId is expected)"

		subscription = self.vibManager.queryVibDatabase("SELECT * FROM SubscriptionInstance WHERE visId = \"" + vibManagement.operationArgs + "\";")
		if type(subscription) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING SUBSCRIPTIONS CONSULTING"
		if len(subscription) == 0:
			return "ERROR CODE #3: THE REQUIRED SUBSCRIPTION DOES NOT EXIST"

		delete = self.vibManager.operateVibDatabase("DELETE FROM SubscriptionInstance WHERE visId = \"" + vibManagement.operationArgs + "\";")
		if type(delete) == sqlite3.Error:
			return "ERROR CODE #2: SQL ERROR DURING CREDENTIAL CONSULTING"

		return delete