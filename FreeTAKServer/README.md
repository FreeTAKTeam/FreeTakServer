# FreeTAKServer

![the Parrot is not dead](https://github.com/Tapawingo/FreeTakServer/blob/master/docs/FreeTakServer%20specs/FreeTakServerLogo.png?raw=true)

Welcome to the FreeTakServer (FTS) git repository.

FTS  is a Python3 implementation of the TAK Server for devices like CivTAK , WinTAK and ITAK, it is cross-platform. We use the Flask framework for web services. 
it's free and open source  (released under the Eclipse Public License).

## User Documentation
For documentation on installation and usage visit https://freetakteam.github.io/FreeTAKServer-User-Docs/

## Supported Use cases
FTS allows you to connect ATAK clients to share geo information, to chat with all the connected clients, exchange files and more.
It intends to support all the major use cases of the original TAK server.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTak%20Use%20Case%20model.png?raw=true)
[Live version](http://pldemo.sparxsystems.us/TVHOG)

## Community 
This code is currently in *Early Production Stage*.
Check out our roadmap [@FreeTakServer#25](https://github.com/FreeTAKTeam/FreeTakServer/issues/25) to see what is planned
If you have any issues don't hesitate to [bring it up](https://github.com/Tapawingo/FreeTakServer/issues),  as TAKFreeServer is in contionous development.

### Donate back
the FTS team is working  daily on the development of a open and free solution. We plan to do more that simply replicate the functionalities of the legacy TAK server, our road map includes integration with open source systems like LORA's Meshtastic, porting it to Android, having an open API and much more.

We are doing it for free because we believe that donating personal time to a cause its a endeavour that is worthy per-se, However, a part time, we are also spending our own money  to:
- Maintain a Public server and a test server
- Investing in different technologies for R&D

if you feel that FTS is useful to you and you can donate in those challenging times please consider to send you contribution here:
[DONATE](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=brothercorvo%40gmail.com&item_name=FreeTAKServer+R%26D&currency_code=CAD&source=url)

You can also support the project by buying one of our [t-shirts](http://tee.pub/lic/elARpZYCmaw)

NOTE:
not a big fan of Paypal, but that is the easier way I found for an initial attempt. We may go to some more ethical system in future.

### Public instance
we support a [public instance](https://www.reddit.com/r/ATAK/wiki/index/freetakserver) of FTS.
- download the configuration [here](https://drive.google.com/file/d/1IK1LfPN13EWikHaMyOuDDwIerNGz-Wli/view?usp=sharing)
- use the Import manager in ATAK to import the configuration

### Tell us what you think!
to discuss with the developer team
Use the reddit server 
https://www.reddit.com/r/ATAK/ 
and the Discord chat
https://discordapp.com/invite/XEPyhHA

## Architecture
TAKFreeServer uses a MVC pattern, the concept of a COT is described in a set of Domain classes, generated  from the UML model using a Model Driven Architecture approach.
![the domain model with all the know objects used by CIVTAK/ wintak](https://github.com/FreeTAKTeam/FreeTakServer/blob/master/docs/FreeTAKServer%20Model.png) [Live version](http://pldemo.sparxsystems.us/Ldsd4T)
[generated documentation of the COT description](https://github.com/FreeTAKTeam/FreeTakServer/blob/master/docs/FreeTakServer%20specs/COTDomainModel.pdf)

## Documentation
under /docs, you can find various documents including an UML model of the Domain classes involved in a COT event.

## Requirements
- Python  3.6 (or better)
following Python libraries are required and will be installed automatically by Pip: flask, lxml, pathlib, tabulate, sqlalchemy, setuptools, Flask-SQLAlchemy

## Installing and using FreeTakServer
For documentation on installation and usage visit https://freetakteam.github.io/FreeTAKServer-User-Docs/Installation/PyPi/Linux/Install/

### Windows
go to the start menu and type ```cmd``` to start a command prompt

open a console with admin rights
Powershell has issues so do not use it
```
python3 -m FreeTAKServer.controllers.services.FTS -DataPackageIP [YourIP]
```

### Troubleshooting
#### package not found'
if, trying to start FTS you get an error 'package not found'
```
'package not found'
```
navigate to the physical location where the controllers are installed and start the server from there.

You may also check for missing libraries and install then using Pip

#### issue connecting in WinTAK
if you have issues connecting winTAK to FTS, try to deactivate the TAKChat plugin, under the plugin section

## Update FreeTakServer
if you already installed FTS with pip you can use
```
pip install FreeTAKServer --upgrade
```
subscribe to this feed to be automatically informed about new versions:
https://pypi.org/rss/project/freetakserver/releases.xml

### client2client datapackages

If you have issues sending datapackages directly to clients via FTS, make sure -IP you specified can be reached from your device.  
A quick way to test if it works is to take a picture with Quick Pic in ATAK and send it to another client. Please also note that for that test ATAK clients needs to be on different network (ie one on mobile and one on wifi), because if you run them in same network (wifi, vpn, etc) they will just use same multicast group, bypassing FTS completely.  
When you post package to specific contact in ATAK, following happens:  

  1) Datapackage is uploaded to server, recorded in database and stored in FTS directory  
  2) Client receives payload with URL pointing to datapackage so ATAK can download it   

Assuming you want to run open-to-everyone FTS instance, and you have server hosted somewhere, you need to specify _public_ IP address in -IP argument. And just in case, -IP also accepts domain names.   
If you run it at home and port forward on router doesn't work, check if you receive actual IP address and not being NATed and ports 8080 and 8087 are not filtered - you can ask your ISP about that.

## Additional Documentation
  * Since version 1.2 FTS supports a[REST API](https://github.com/FreeTAKTeam/FreeTakServer/blob/master/REST_APIDoc.md)

##  Project Structure
- TakFreeServer
  - **Controllers**: Contains all the business Logic
  - **Models**: Contains all the COT object model
  - **TAKLinuxService**:   a demon for linux OS
  -  **TakWinService**: a service for the windows OS
- Docs: Useful documentation regarding COTS and different logs to understand how those are implemented
- Model: a UML model in Sparx EnterpriseArchitect format (see https://sparxsystems.com/products/ea/trial/request.html).
- Old: Legacy versions
