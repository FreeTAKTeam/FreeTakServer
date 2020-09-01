# FreeTAKServer

![the Parrot is not dead](https://github.com/Tapawingo/FreeTakServer/blob/master/docs/FreeTakServer%20specs/FreeTakServerLogo.png?raw=true)

Welcome to the FreeTakServer (FTS) git repository.

FTS  is a Python3 implementation of the TAK Server for devices like CivTAK , WinTAK and ITAK, it is cross-platform and is only dependent on python stdlib libraries. We use the Flask framework for web services. 
it's free and open source  (released under the Eclipse Public License).

## Use cases
FTS allows you to connect ATAK clients to share geo information, to chat with all the connected clients, exchange files and more.
It intends to support all the major use cases of the original TAK server.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTak%20Use%20Case%20model.png?raw=true)

## Community 
This code is currently in *BETA STAGE*
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
- Python  3.6 (or better)

## Installing and using FreeTakServer
### Prerequisites
- Install Python3
```
  sudo apt update && sudo apt install python3 && sudo apt install pip3` (Ubuntu)```
 ```
### install FreeTakServer
Since version 0.8, FTS supports Pip installation, manual installation can be done with some modifications of the import paths, however we don't support it

```
  pip install FreeTAKServer
```

Optional: check if installation is correctly executed
```
pip check FreeTakServer 
```

note under windows it's installed under
```
C:\Users\user.name\AppData\Local\Programs\Python\PythonXX\Lib\site-packages
```

## Run FreeTakServer

### Linux

#### Configuration

it is recomended to edit the maximum number of open connections with the following
```
vim /etc/sysctl.conf
fs.file-max = 200000
sysctl -p
```

#### Run Server in console

```
sudo  python3 -m FreeTAKServer.controllers.FTS -AutoStart (weather the full server start or just the RestAPI, must be True or False) -CoTIP (your IP) -DataPackageIP(your IP) -CoTPort (the port you want atak to connect to) -DataPackagePort (the port you want datapackages to be sent and received on)
```

```
defaults:

AutoStart = True

CoTIP = 0.0.0.0

DataPackageIP = 0.0.0.0

DataPackagePort = 8080

CoTPort = 8087
```

this will start the program in an emulated terminal like enviroment

### Run CLI in console

```
sudo  python3 -m FreeTAKServer.views.CLI
``` 
to start the commandline

```
help
```

to get a list of other supported commands run the above command

it is recommended to start the server with start_all

### Windows
go to the start menu and type cmd to start a command prompt
open a console with admin rights
```
python3 -m FreeTAKServer.controllers.FTS
```

### Troubleshooting
if, trying to start FTS you get an error 'package not found'
```
'package not found'
```
navigate to the physical location where the controllers are installed and start the server from there

## Update FreeTakServer
if you already installed FTS with pip you can use
```
pip install FreeTAKServer --upgrade
```

##  Project Structure
- TakFreeServer
  - **Controllers**: Contains all the business Logic
  - **Models**: Contains all the COT object model
  - **configuration**: Contains constants and configuration files for FTS
- Docs: Usefull documentation regarding COTS and different logs to understand how those are implemented
- Model: a UML model in Sparx EnterpriseArchitect format (see https://sparxsystems.com/products/ea/trial/request.html).
- Old: Legacy versions
