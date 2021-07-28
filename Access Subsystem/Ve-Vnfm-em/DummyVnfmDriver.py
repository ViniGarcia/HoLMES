import sys
sys.path.insert(0,'Access Subsystem/Ve-Vnfm-em')

import VnfmDriverTemplate

class DummyVnfmDriver(VnfmDriverTemplate.VnfmDriverTemplate):

	def __init__(self, vnfmId, vnfmAddress, vnfmCredentials):
		
		super().__init__(vnfmId, vnfmAddress, vnfmCredentials)