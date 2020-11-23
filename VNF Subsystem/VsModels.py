'''
GENERAL INFORMATION: This file contains several classes that enable the
					 EMS to with the VNF instances.		 
VALIDATION ERROR CODES:
					 -1: Attribute type not satisfied
					 -2: Mandatory attribute not satisfied
					 -3: Invalid member in structure 
'''

#######################################################################################################
#######################################################################################################

'''
CLASS: PlatformOperation
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 17 Nov. 2020 (Fulber-Garcia; Methods implementation)
DESCRIPTION: This type represents an operation available
			 in a VNF platform. This operation must be
			 defined in the VNF driver. In that class,
			 arguments are define as name:type(). The
			 arguments object does not contain the ins-
			 tance class once it is a mandatory argument.
'''
class PlatformOperation:
	id = None					#Identifier (String), mandatory (1)
	method = None				#Method reference, mandatory (1)
	arguments = {}				#KeyValuePairs (Dictionary), optional (0..1)
	
	def validate(self):
	
		if self.id != None:
			if type(self.id) != str:
				return ("0", -1)
		else:
			return ("0", -2)

		if self.method != None:
			if not callable(self.method):
				return ("1", -1)
		else:
			return ("1", -2)

		if type(self.arguments) == dict:
			for key in self.arguments:
				if type(key) != str:
					return ("2." + str(key), -1)
		else:
			return ("2", -2)

		return ("3", 0)

	def fromData(self, id, method, arguments):
		self.id = id
		self.method = method
		self.arguments = arguments

		if self.validate()[1] == 0:
			return self
		else:
			return False

	def toDictionary(self):
		return {"id":self.id, "method":getattr(self.method, '__name__', None), "arguments":{key:getattr(self.arguments[key], '__name__', None) for key in self.arguments}}

	def fromDictionary(self, dictData, veEmVnf):
		self.id = dictData["id"]
		self.method = getattr(veEmVnf, dictData["method"]) 
		self.arguments = {key:eval(dictData["arguments"][key]) for key in dictData["arguments"]}
		return self