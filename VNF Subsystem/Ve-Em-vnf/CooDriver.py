import VnfDriverTemplate

class CooDriver(VnfDriverTemplate.VnfDriverTemplate):

	def __init__(self):
		super().__init__("Click-On-OSv")

	def get_p_operations(self):
		return