sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')

import VnfmDriverTemplate

class DummyVnfmDriver2(VnfmDriverTemplate.VnfmDriverTemplate):

	def __init__(self):
		
		super().__init__("DummyVnfmDriver2")