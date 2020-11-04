import sys
sys.path.insert(0,'../VNF Information Base/')

import CommunicationModels
import VibManager
import VibTableModels

'''
CLASS: TemplateAuthentication
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class is a template for the implementation of 
			 authentication models. In summary, there are four
			 methods: "fromAuthData", that decodes the authData
			 and authResource available in the VIB, returning a
			 string of authData and authResource; "toAuthData"
			 that receives a string authData and authResource,
			 and return a encoded string to be saved in the VIB;
			 "authClient" that receives an authentication string
			 of the operation request and returns the clientId.
			 "authRequest" receives an authentication string from
			 the operationrequest and do the authentication check.
AUTH MODEL: clientId + ";" + plainPassword
CODES: -1 -> Invalid data type of authData
	   -2 -> Invalid data type of authResource
	   -3 -> Invalid data type of requestAuth
	   -4 -> Invalid schema of requestAuth
	   -5 -> Invalid data type of authInstance
'''
class TemplateAuthentication:

	def __init__(self):
		return

	def fromAuthData(self, authData, authResource):
		return

	def toAuthData(self, authData, authResource):
		return

	def authClient(self, requestAuth):
		return

	def authRequest(self, authInstance, requestAuth):
		return

'''
CLASS: PlainTextAuthentication
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class processes the plain text authentication.
			 "fromAuthData": just execute the type check and re-
			 turn the strings. "toAuthData": just executes the 
			 type check and returns the strings. "authClient":
			 executes the type check, clean the authentication 
			 model, and returns the clientId. "authRequest": 
			 executes the type check and the comparision of
			 passwords.
AUTH MODEL: clientId + ";" + plainPassword
CODES: -1 -> Invalid data type of authData
	   -2 -> Invalid data type of authResource
	   -3 -> Invalid data type of requestAuth
	   -4 -> Invalid schema of requestAuth
	   -5 -> Invalid data type of authInstance
'''
class PlainTextAuthentication(TemplateAuthentication):

	def __init__(self):
		return

	def fromAuthData(self, authData, authResource):
		
		if type(authData) != str:
			return -1
		if authResource != None and type(authResource) != str:
			return -2

		return (authData, authResource)

	def toAuthData(self, authData, authResource):

		if type(authData) != str:
			return -1
		if authResource != None and type(authResource) != str:
			return -2

		return (authData, authResource)

	def authClient(self, requestAuth):

		if type(requestAuth) != str:
			return -3
		splitedAuth = requestAuth.split(";")
		if len(splitedAuth) != 2:
			return -4

		return splitedAuth[0]

	def authRequest(self, authInstance, requestAuth):

		if type(authInstance) != VibTableModels.VibAuthInstance:
			return -5

		if type(requestAuth) != str:
			return -3
		splitedAuth = requestAuth.split(";")
		if len(splitedAuth) != 2:
			return -4

		vibAuth = self.fromAuthData(authInstance.authData, authInstance.authResource)
		if vibAuth[0] == splitedAuth[1]:
			return True
		return False

'''
CLASS: AuthenticationAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: Authentication agent implementation. This class
			 is configured with the EMS authentication model.
			 Thus, this class is responsible for athutenti-
			 cating the operational requests received in the
			 access subsytem.
CODES: -1 -> Invalid authentication model
	   -2 -> Invalid data type of vibManager
	   -3 -> Error code on authClient retrievering
	   -4 -> Error code on authInstance retrievering
	   -5 -> Error code on authentication check
'''
class AuthenticationAgent:
	__availableAuth = None
	__authModel = None
	__vibManager = None	

	def __init__(self, authModel, vibManager):

		self.__availableAuth = {"PlainText":PlainTextAuthentication}
		if not authModel in self.__availableAuth:
			return
		if type(vibManager) != VibManager.VibManager:
			return

		self.__authModel = self.__availableAuth[authModel]()
		self.__vibManager = vibManager

	def __changeAuthentication(self, authModel):
		
		if not authModel in self.__availableAuth:
			return -1
		self.__authModel = self.__availableAuth[authModel]()
		return 0

	def __updateVibManager(self, vibManager):
		
		if type(vibManager) != VibManager.VibManager:
			return -2
		self.__vibManager = vibManager
		return 0

	def authRequest(self, requestAuth):

		authClient = self.__authModel.authClient(requestAuth)
		if type(authClient) == int:
			return -3

		authSql = self.__vibManager.queryVibDatabase("SELECT * FROM AuthInstance WHERE userId = \"" + authClient + "\";")
		if len(authSql) == 0:
			return -4

		authInstance = VibTableModels.VibAuthInstance(authSql[0][0], authSql[0][1], authSql[0][2], authSql[0][3])
		authentication = self.__authModel.authRequest(authInstance, requestAuth)
		if type(authentication) == int:
			return -5

		return authentication

'''#TEMPORARY
vibTester = VibManager.VibManager()
authTester = AuthenticationAgent("PlainText", vibTester)
authentication = authTester.authRequest("USER01;BatataFrita")
print(authentication)'''