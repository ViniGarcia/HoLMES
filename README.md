HoLMES: Holistic Lightweight and Malleable EMS Solution
========================================================

*Status: Alfa -- Version: 0.1*

### What is HoLMES?
HoLMES is an Element Management System (EMS) platform designed to be fully compliant with the Network Function Virtualization (NFV) reference architecture from the ETSI. HoLMES can execute a myriad of EMS operations in the NFV environment by straightforward communicating with the Virtualized Network Functions (VNF) instances or exchanging information with the NFV Management and Orchestration (NFV-MANO) through the VNF Manager (VNFM). There are two possible communication agents in HoLMES: (i) users or generic external systems and (ii) VNFM. The communication from users or generic external systems, besides being able to access typical VNFM operations (if allowed), can configure the HoLMES platform itself by accessing its Internal Manager (IM) operations. The communication from VNFM platforms, in turn, follows the specification documents from the ETSI. HoLMES is holistic and malleable, being able to work with any VNFM and VNF platforms. This support comes from a driver system defined with templates. Within this driver system, the operators can implement simple drivers that enable HoLMES to communicate with particularly desired platforms.

The access interfaces of HoLMES works with HTTP protocol (execute CLI.py and run the "HELP" command to see the available operations). The exception is the interface with the VNF instances that, through the third-party drivers, can operate with any python-supported communication technology. HoLMES provides a complete set of EMS data models (AsModels) that can (and should) be used to implement VNFM drivers. Internal configuring is done through secondary data models (VibModels) used in the HoLMES configuring communication with users and generic external systems.

Regarding driver development, there are two template files available: VNFM (VnfmDriverTemplate) and VNF (VnfDriverTemplate). In the VNFM driver, the non-implemented methods will return and 501 HTTP error. On the other hand, all the template methods of VNF drivers are mandatory and must be implemented. Relevant data models used in the internal communication of HoLMES are located at the internal router folder (IrModels).

