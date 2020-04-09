# TAKlib
TAKFreeServer is a Python3 implemnentation of the TAK Server for devices like CivTAK , WinTak and Itak, it is cross-platform and is only dependant on python stdlib libraries. 

## Documentation
under docs, you can find various documents including an UMl model of the model classes involved in a COT event.

## Requirements
- Python 3

## Installing and using FreeTakServer
FreeTakServer is available in 2 flavours:
- Windows service
- Linux Service

requires Python 3.0 or later to run. Once you’ve installed Python 3, install TAKLib using git:
```bash
git clone https://github.com/Tapawingo/TAKlib.git
cd TAKLib
```
<h1>run the following command in terminal in the directory where TAKDaemon.py is installed</h1>
<code>python3 TAKDaemon.py</code>


<h1>To run this program you require admin priviliges</h1>

#1 allow python.exe in firewall
<br>
#2 open whichever port you will be using for connections in firewall
<br>
#3 kill any program already running on whichever port you've decided to use
<br>
#4 open CMD with admin(advisable to have green text on black background)
<br>
#5 cd into whichever directory this file is located
<br>
#6 type the following "beginProgramAsService.py install"
<br>
#7 type "beginProgramAsService.py start"
<br>
if you have any issues don't hesitate to bring it up as this program is still in development
<br>
<br>
if you have this error Python windows service “Error starting service: The service did not respond to the start or control request in a timely fashion”
<br>
<br>
attempt to add python to the system path
<br>
side note TAKFreeServer_running_as_service.py can be run independently without being run as service 


