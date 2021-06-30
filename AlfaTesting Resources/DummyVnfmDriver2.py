import sys
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')

import VnfmDriverTemplate

class DummyVnfmDriver2(VnfmDriverTemplate.VnfmDriverTemplate):

	def __init__(self, vnfmId, vnfmCredentials):
		
		super().__init__(vnfmId, vnfmCredentials)