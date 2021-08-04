import sys
import hmac
import json
import base64
import urllib
import hashlib

import urllib.parse
import urllib.request

sys.path.insert(0,'Access Subsystem')
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')
import VnfmDriverTemplate
import AsModels

class VinesVnfmDriver(VnfmDriverTemplate.VnfmDriverTemplate):
	apiKey = None
	secretKey = None

	def __generate_url(self, request):
		baseUrl = "http://" + self.vnfmAddress + "/client/api?"
		requestUrl = '&'.join(['='.join([k,urllib.parse.quote_plus(request[k])]) for k in request.keys()])
		signatureStr = '&'.join(['='.join([k.lower(),urllib.parse.quote_plus(request[k].lower().replace('+','%20'))])for k in sorted(request.keys())])
		signatureUrl = urllib.parse.quote_plus(base64.encodestring(hmac.new(self.secretKey.encode("utf-8"),signatureStr.encode("utf-8"),hashlib.sha1).digest()).strip())

		return baseUrl + requestUrl + '&signature=' + signatureUrl

	def __init__(self, vnfmId, vnfmAddress, vnfmCredentials):
		
		super().__init__(vnfmId, vnfmAddress, vnfmCredentials)

		if vnfmCredentials.count(";") != 1:
			return
		vinesKeys = vnfmCredentials.split(";")
		if len(vinesKeys[0]) != 86 or len(vinesKeys[1]) != 86:
			return

		self.apiKey = vinesKeys[0]
		self.secretKey = vinesKeys[1]

	def get_vlmi_vnfInstances(self):

		requestUrl = self.__generate_url({"command":"listVnfs", "response":"json", "apikey":self.apiKey})
		try:
			requestResponse = urllib.request.urlopen(requestUrl)
		except Exception as e:
			if type(e) == urllib.error.HTTPError:
				return str(e.code)
			else:
				return "500"

		instanceResults = json.loads(requestResponse.read().decode())
		instanceClass = AsModels.VnfInstance()
		veVnfmEmResults = []
		for ir in instanceResults["listvnfsresponse"]["vnf"]:
			instanceClass.id = ir["id"]
			instanceClass.vnfInstanceName = ir["name"]
			instanceClass.vnfdId = ir["vnfpid"]
			instanceClass.metadata = {"creationDate":ir["created"], "vinesEmsId":ir["emsid"]}
			veVnfmEmResults.append(instanceClass.toDictionary())

		return json.dumps([requestResponse.getcode(), veVnfmEmResults])
	
	def get_vlmi_vi_vnfInstanceID(self, vnfInstanceId):

		requestUrl = self.__generate_url({"command":"listVnfs", "response":"json", "vnfid":vnfInstanceId, "apikey":self.apiKey})
		try:
			requestResponse = urllib.request.urlopen(requestUrl)
		except Exception as e:
			if type(e) == urllib.error.HTTPError:
				return str(e.code)
			else:
				return "500"

		instanceResults = json.loads(requestResponse.read().decode())
		instanceClass = AsModels.VnfInstance()
		veVnfmEmResults = []
		for ir in instanceResults["listvnfsresponse"]["vnf"]:
			instanceClass.id = ir["id"]
			instanceClass.vnfInstanceName = ir["name"]
			instanceClass.vnfdId = ir["vnfpid"]
			instanceClass.metadata = {"creationDate":ir["created"], "vinesEmsId":ir["emsid"]}
			veVnfmEmResults.append(instanceClass.toDictionary())

		return json.dumps([requestResponse.getcode(), veVnfmEmResults])

	def post_vlmi_viid_operate(self, vnfInstanceId, operateVnfRequest):

		try:
			operateVnfRequest = AsModels.OperateVnfRequest().fromDictionary(json.loads(operateVnfRequest))
		except Exception as e:
			return "400"

		if operateVnfRequest.changeStateTo == None:
			return "400"

		if operateVnfRequest.changeStateTo.value == 0:
			requestUrl = self.__generate_url({"command":"startVirtualMachine", "response":"json", "id":vnfInstanceId, "apikey":self.apiKey})
		else:
			if operateVnfRequest.stopType == None or operateVnfRequest.stopType.value == 1:
				forcedOperation = "false"
			else:
				forcedOperation = "true"
			requestUrl = self.__generate_url({"command":"stopVirtualMachine", "response":"json", "id":vnfInstanceId, "forced":forcedOperation, "apikey":self.apiKey})
		try:
			requestResponse = urllib.request.urlopen(requestUrl)
		except Exception as e:
			if type(e) == urllib.error.HTTPError:
				return str(e.code)
			else:
				return "500"

		return "202"