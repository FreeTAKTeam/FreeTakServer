# TAKFreeServer
TAKFreeServer is a Python3 implemnentation of the TAK Server for devices like CivTAK , WinTak and ITak, it is cross-platform and is only dependent on python stdlib libraries. It intend to support all the major use cases of the original TAK server.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTak%20Use%20Case%20model.png?raw=true)

This code is currently in *ALPHA STAGE*
If you have any issues don't hesitate to bring it up as TAKFreeServer is still in the early stages of development.
use https://www.reddit.com/r/ATAK/

## Architecture
TAKFreeServer uses a MVC pattern, the concept of a COT is described in a set of Domain classes, generated  from the UML model using a Model Driven Architecture approach.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTAKServer%20Model.png?raw=true)
The target architecture supports also the ability to implement "plugins", thanks to a listener, that is decouple from the main server
![the FreeTakServer component model](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTakServerComponents.png?raw=true)


## Documentation
under docs, you can find various documents including an UMl model of the model classes involved in a COT event.

## Requirements
- Python 3

## Installing and using FreeTakServer
FreeTakServer  requires Python 3.0 or later to run. Once you’ve installed Python 3, install TAKLib using git:

```bash
git clone https://github.com/Tapawingo/TAKlib.git

cd TAKLib
```

It is available in 2 flavours:
- Windows service
- Linux Demon

### Linux Demon

run the following command in terminal in the directory where TAKDaemon.py is installed
```
python3 TAKDaemon.py
```

### Windows Service
To run this program you require admin priviliges

1. allow python.exe in firewall
2. open whichever port you will be using for connections in firewall
3. kill any program already running on whichever port you've decided to use
4. open CMD with admin
5. cd into whichever directory FreetakServer is located
```
Cd FreeTakServer/TakWinService
```
6. type the following 
```
beginProgramAsService.py install
```
7. type 
```
beginProgramAsService.py start
```

#### side note 
```
TAKFreeServer_running_as_service.py
```
can be run independently 

#### Troubleshooting
if you have this error Python windows service “Error starting service: The service did not respond to the start or control request in a timely fashion”

attempt to add python to the system path

##  Project Structure
- TakFreeServer
  - **Controllers**: Contains all the business Logic
  - **Models**: Contains all the COT object model
  - **TAKLinuxService**:   a demon for linux OS
  -  **TakWinService**: a service for the windows OS 
- Docs: Usefull documentation regarding COTS and different logs to understand how those are implemented
- Model: a UML model in Sparx EnterpriseArchitect format (see https://sparxsystems.com/products/ea/trial/request.html). 
- Old: Legacy versions

