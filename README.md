HoLMES: Holistic, Lightweight and Malleable EMS Solution
========================================================

*Status: Alfa -- Version: 0.1*

### What is HoLMES?
<p align="justify"> HoLMES is an Element Management System (EMS) platform designed to be fully compliant with the Network Function Virtualization (NFV) reference architecture from the ETSI. HoLMES can execute a myriad of EMS operations in the NFV environment by straightforward communicating with the Virtualized Network Functions (VNF) instances or exchanging information with the NFV Management and Orchestration (NFV-MANO) through the VNF Manager (VNFM). There are two possible communication agents in HoLMES: (i) users or generic external systems and (ii) VNFM. The communication from users or generic external systems, besides being able to access typical VNFM operations (if allowed), can configure the HoLMES platform itself by accessing its Internal Manager (IM) operations. The communication from VNFM platforms, in turn, follows the specification documents from the ETSI. HoLMES is holistic and malleable, being able to work with any VNFM and VNF platforms. This support comes from a driver system defined with templates. Within this driver system, the operators can implement simple drivers that enable HoLMES to communicate with particularly desired platforms. </p>

<p align="justify"> The access interfaces of HoLMES works with HTTP protocol (execute CLI.py and run the "HELP" command to see the available operations). The exception is the interface with the VNF instances that, through the third-party drivers, can operate with any python-supported communication technology. HoLMES provides a complete set of EMS data models (AsModels) that can (and should) be used to implement VNFM drivers. Internal configuring is done through secondary data models (VibModels) used in the HoLMES configuring communication with users and generic external systems. </p>

<p align="justify"> Regarding driver development, there are two template files available: VNFM (VnfmDriverTemplate) and VNF (VnfDriverTemplate). In the VNFM driver, the non-implemented methods will return and 501 HTTP error. On the other hand, all the template methods of VNF drivers are mandatory and must be implemented. Relevant data models used in the internal communication of HoLMES are located at the internal router folder (IrModels). </p>

<p align="justify"> HoLMES requires a previous installation of the Python 3 programming language. We provide a shell script and a batch file with installation commands of all the required libraries. These scripts use python-pip to install the dependencies. After the installation, you can run the AlfaTesting program to check if HoLMES is running correctly. AlfaTesting executes a myriad of tests into all HoLMES operational elements. A correct execution must return the HTTP code 200 for available operations, and the HTTP code 405 for non-available operations. </p>

<p align="justify"> HoLMES is composed of six operational elements, a brief description of each element is provided next: </p>

1. Access Subsystem: this element provides the communication interfaces with the agents that request operations. Besides processing the requests, it is also responsible for authenticating users and checking their operation credentials.<br/>
2. VNF Subsystem: this element executes the requested VNF operations. The VNF subsystem has a straightforward communication interface with the VNF instances.<br/>
3. Monitoring Subsystem: this element manages the monitoring agents of the VNF instances. It also keeps all the monitoring scripts available internally.<br/>
4. EMS Information Base: this element is a centralized database that mantain all the management information regarding the other operational elements.<br/>
5. Internal Manager: this element is responsible for managing all the other operational elements of HoLMES. All the configuring operations are implemented in the Internal Manager.<br/>
6. Internal Router: this element enables the internal communication between two different operational elements.

<p align="justify"> HoLMES can be operated by other systems, such as VNFM and OSS/BSS, through its HTTP interface. Furthermore, it is possible to straightforward access the EMS through HoLMES CLI (please, run the "list" command to see all the available operations). See next some examples of how doing that: </p>

<p align="center">
  <img src="https://www.inf.ufpr.br/vfgarcia/hosting/VNFInserting.png">
  <b>VNF Instance Insertion Through the HoLMES CLI</b>
</p>

<p align="justify"> You can execute HoLMES through its CLI (CLI.py). The standard HoLMES login is "admin", as well as the standard password ("admin"). </p>

### HoLMES Platform

<p align="justify"> HoLMES is also provided as a platform on the Ubuntu Cloud operating system. You can download the platform version [HERE](https://drive.google.com/file/d/1b8ya-mVo1myf90v1uYmiNLHUvkrcCbBt/view?usp=sharing). The virtual machine standard credentials are "user" for the username and "holmes" for the password. </p>

### How does it was created?

<p align="justify"> The NIEP platform was developed using python 3.9 language and a number of libraries and applications: </p>

1. Python<br/>
1.1 Python 3.9.1 (apt-get install python3.9)<br/>
1.2 Pip (apt-get install python-pip)<br/>
2. Non-native Python libraries <br/>
2.1 Flask (pip install flask)<br/>
2.2 PsUtil (pip install psutil)<br/>
2.1 Requests (pip install requests)<br/>
3. SQLite<br/>
3.1 SQLite 3 (apt-get install sqlite3)

### Next Steps

1. Implementation of new authentication methods (Authentication Agent)<br/>
2. Implementation of native VNF drivers for well known platforms (VNS Subsystem)<br/>
3. Implentation of a debug mechanism (Access Subsystem and Internal Manager)<br/>
4. Creation of a development environment for VNF and VNFM drivers (Entire platform)<br/>
5. General refactoring and new error threatment (Entire platform)<br/>
6. Graphical interface (Entire platform)

### Support

<p align="justify"> Contact us towards git issues requests or by the e-mail vfulber@inf.ufsm.br. </p>

### HoLMES Research Group

Vinícius Fülber Garcia (UFPR - Brazil)<br/>
José Wilson Vieira Flauzino (UFPR - Brazil)<br/>
Elias Procópio Duarte Junior (UFPR - Brazil)