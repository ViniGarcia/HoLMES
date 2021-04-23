import VibModels
import VibManager

'''
CLASS: TemplateAuthentication
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Jan. 2020 (Fulber-Garcia; Refactoring methods to
						 operate with the VibUserInstance; In-
						 cluded the "None" authenticator)
DESCRIPTION: This class is a template for the implementation of 
			 authentication models. In summary, there are four
			 methods: "fromAuthData", that decodes the authData
			 and authResource available in the VIB, returning a
			 string of authData and authResource; "toAuthData"
			 that receives a string authData and authResource,
			 and return a encoded string to be saved in the VIB;
			 "authUser" that receives an authentication string
			 of the operation request and returns the clientId.
			 "authCheck" receives an authentication string from
			 the operationrequest and do the authentication check.
AUTH MODEL: clientId + ";" + plainPassword
CODES: -1 -> Invalid data type of authData
	   -2 -> Invalid data type of authResource
	   -3 -> Invalid data type of requestAuth
	   -4 -> Invalid schema of requestAuth
	   -5 -> Invalid data type of authInstance
'''
class TemplateAuthentication:

	authenticatorId = "None"

	def __init__(self):
		return

	def fromAuthData(self, userAuth, userSecrets):
		return (userAuth, userSecrets)

	def toAuthData(self, userAuth, userSecrets):
		return (userAuth, userSecrets)

	def authUser(self, requestAuth):
		return None

	def authCheck(self, vibUserInstance, requestAuth):
		return True

'''
CLASS: PlainTextAuthentication
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 04 Nov. 2020 (Fulber-Garcia; Class creation)
DESCRIPTION: This class processes the plain text authentication.
			 "fromAuthData": just execute the type check and re-
			 turn the strings. "toAuthData": just executes the 
			 type check and returns the strings. "authUser":
			 executes the type check, clean the authentication 
			 model, and returns the clientId. "authCheck": 
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
		
		super().__init__()
		self.authenticatorId = "PlainText"

	def fromAuthData(self, userAuth, userSecrets):
		
		if type(userAuth) != str:
			return -1
		if userSecrets != None and type(userSecrets) != str:
			return -2

		return (userAuth, userSecrets)

	def toAuthData(self, userAuth, userSecrets):

		if type(userAuth) != str:
			return -1
		if userSecrets != None and type(userSecrets) != str:
			return -2

		return (userAuth, userSecrets)

	def authUser(self, requestAuth):

		if type(requestAuth) != str:
			return -3
		splitedAuth = requestAuth.split(";")
		if len(splitedAuth) != 2:
			return -4

		return splitedAuth[0]

	def authCheck(self, vibUserInstance, requestAuth):

		if type(vibUserInstance) != VibModels.VibUserInstance:
			return -5

		if type(requestAuth) != str:
			return -3
		splitedAuth = requestAuth.split(";")
		if len(splitedAuth) != 2:
			return -4

		vibAuth = self.fromAuthData(vibUserInstance.userAuthentication, vibUserInstance.userSecrets)
		if vibAuth[0] == splitedAuth[1]:
			return True
		return False

'''
CLASS: AuthenticationAgent
AUTHOR: Vinicius Fulber-Garcia
CREATION: 04 Nov. 2020
L. UPDATE: 07 Dez. 2020 (Fulber-Garcia; Implementation of "get" methods)
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

	def __init__(self, vibManager):
		
		if type(vibManager) != VibManager.VibManager:
			return

		self.__availableAuth = {"None":TemplateAuthentication, "PlainText":PlainTextAuthentication}
		self.__authModel = TemplateAuthentication()
		self.__vibManager = vibManager

	def getAuthenticators(self):

		return list(self.__availableAuth.keys())

	def getRunningAuthenticator(self):

		if self.__authModel != None:
			return self.__authModel.authenticatorId

		return None

	def setupAuthentication(self, authModel):
		
		if not authModel in self.__availableAuth:
			return -1
		self.__authModel = self.__availableAuth[authModel]()
		return 0

	def transformAuthentication(self, vibUserInstance):

		authTrasnform = self.__authModel.toAuthData(vibUserInstance.userAuthentication, vibUserInstance.userSecrets)
		vibUserInstance.userAuthentication = authTrasnform[0]
		vibUserInstance.userSecrets = authTrasnform[1]

		return vibUserInstance

	def authenticationCheck(self, userAuth):

		userId = self.__authModel.authUser(userAuth)
		if type(userId) == int:
			return -3

		vibUserInstance = self.__vibManager.queryVibDatabase("SELECT * FROM UserInstance WHERE userId = \"" + userId + "\";")
		if len(vibUserInstance) == 0:
			return -4

		vibUserInstance = VibModels.VibUserInstance().fromSql(vibUserInstance[0])
		authentication = self.__authModel.authCheck(vibUserInstance, userAuth)
		if type(authentication) == int:
			return -5

		if authentication:
			return vibUserInstance
		else:
			return False

	def credentialCheck(self, userId, vnfId):

		vibCredentialInstance = self.__vibManager.queryVibDatabase("SELECT * FROM CredentialInstance WHERE userId = \"" + userId + "\" AND vnfId = \"" + vnfId + "\";")
		if len(vibCredentialInstance) == 0:
			return False

		return VibModels.VibCredentialInstance().fromSql(vibCredentialInstance[0])