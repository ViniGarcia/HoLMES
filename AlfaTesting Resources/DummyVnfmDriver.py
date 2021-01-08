import VnfmDriverTemplate

class DummyVnfmDriver(VnfmDriverTemplate.VnfmDriverTemplate):

	def __init__(self):
		
		super().__init__("DummyVnfmDriver")