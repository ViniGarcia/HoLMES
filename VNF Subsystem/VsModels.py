'''
GENERAL INFORMATION: 
NOTE:				 
VALIDATION ERROR CODES:
					 -1: 
'''

#######################################################################################################
#######################################################################################################

'''
CLASS: PlatformOperation
AUTHOR: Vinicius Fulber-Garcia
CREATION: 16 Nov. 2020
L. UPDATE: 16 Nov. 2020 (Fulber-Garcia; Class creation)
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
