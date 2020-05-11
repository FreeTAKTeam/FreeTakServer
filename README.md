# FreeTAKServer

![the Parrot is not dead](https://github.com/Tapawingo/FreeTakServer/blob/master/docs/FreeTakServer%20specs/FreeTakServerLogo.png?raw=true)

Welcome to the FreeTakServer (FTS) git repository.

FTS  is a Python3 implemnentation of the TAK Server for devices like CivTAK , WinTAK and ITAK, it is cross-platform and is only dependent on python stdlib libraries. 
it's free and open source  (released under the Eclipse Public License).

## Use cases
FTS allows you to connect ATAK clients to share geo information, to chat with all the connected clients, exchange files and more.
It intends to support all the major use cases of the original TAK server.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTak%20Use%20Case%20model.png?raw=true)

## Community 
This code is currently in *ALPHA STAGE*
Check out our roadmap @ FreeTakServer#25 to see what is planned
If you have any issues don't hesitate to bring it up https://github.com/Tapawingo/FreeTakServer/issues,  as TAKFreeServer is still in the early stages of development.

### Public instance
we support a public instance of FTS.
- download the configuration here
https://drive.google.com/open?id=1IK1LfPN13EWikHaMyOuDDwIerNGz-Wli
- use the Import manager in ATAK to import the configuration

### Tell us what you think!
to discuss with the developer team
Use the reddit server 
https://www.reddit.com/r/ATAK/ 
and the Discord chat
https://discordapp.com/invite/XEPyhHA


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
### Prerequisites
- Install Python3

  `sudo apt update && sudo apt install python3` (Ubuntu)
  - install Flask

  `pip install flask

- Clone TAKLib repository

  `git clone https://github.com/Tapawingo/TAKlib.git`

### Linux

#### Run Server in console

```
cd TAKlib/TAKfreeServer/

python3 server.py
```

#### Run Server as Demon
see also https://github.com/Tapawingo/FreeTakServer/tree/master/TAKfreeServer/TAKLinuxService
```
cd TAKlib/TAKfreeServer/TAKLinuxService

sudo python3 beginServerFromLinux.py
```

### Windows

#### Windows Service
see also https://github.com/Tapawingo/FreeTakServer/tree/master/TAKfreeServer/TAKWinService
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

### side note
```
TAKFreeServer_running_as_service.py
```
can be run independently

### Troubleshooting
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
