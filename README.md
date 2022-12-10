# FreeTAKServer [![Downloads](https://pepy.tech/badge/freetakserver)](https://pepy.tech/project/freetakserver) ![PyPI](https://img.shields.io/pypi/v/FreeTAKServer) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/FreeTAKTeam/FreeTakServer) ![Lines of code](https://img.shields.io/tokei/lines/github.com/FreeTAKTeam/FreeTakServer)

![the Parrot is not dead](https://github.com/FreeTAKTeam/FreeTAKServer-User-Docs/blob/a18a269fc1e425863ba5b3a76329e90645d751d1/docs/docs/FreeTakServerLogo.png)

Welcome to the FreeTakServer (FTS) git repository.

FTS is a Python3 implementation of the TAK Server for devices like [ATAK](https://play.google.com/store/apps/details?id=com.atakmap.app.civ), [WinTAK](https://1drv.ms/u/s!AtMVrrXVTu4YgSanKtSHIslxfRu5?e=ftVio7 ), and ITAK, it is cross-platform and runs from a multi node installation on AWS down to the Android edition. 
It's free and open source (released under the [Eclipse Public License](https://www.eclipse.org/legal/epl-2.0/).

## User Documentation
![FTS UI 1.8](https://user-images.githubusercontent.com/60719165/118400921-0731e180-b63a-11eb-976e-c38ee052a013.png)

For documentation on installation and usage visit our [FreeTAKServer Documentation page](https://freetakteam.github.io/FreeTAKServer-User-Docs/)

## Use Cases
FTS allows you to connect ATAK clients to share geo information, to chat with all the connected clients, exchange files and more.
It intends to support all the major use cases of the original TAK server.
- Web administration 
- Federation Service (Connecting two or more FTS instances)
- Data Package upload, share with all connected users  and retrieval
- Image transfer and storage
- COT recording in a database
- Execution of common task list (*using the ExCheck plugin for WinTAK; ATAK plugin only available to users with takmaps.com access*)
- SSL Encryption
- KML generation
- Command Line Interface
- [Extensive REST API](https://freetakteam.github.io/FreeTAKServer-User-Docs/API/REST_APIDoc/) for intgrations and extensions

![some use cases](https://github.com/Tapawingo/TAKlib/blob/master/docs/FreeTakServer%20specs/FreeTak%20Use%20Case%20model.png?raw=true)

## Project Status
This code is currently in *Production Stage*.
Check out our roadmap [@FreeTakServer#25](https://github.com/FreeTAKTeam/FreeTakServer/issues/25) to see what is planned
Also subscribe to this feed to be automatically informed about PIP new versions:
https://pypi.org/rss/project/freetakserver/releases.xml

### Public instance
We support a [public instance](https://www.reddit.com/r/ATAK/wiki/index/freetakserver) of FTS.
- download the configuration [here](https://drive.google.com/file/d/1IK1LfPN13EWikHaMyOuDDwIerNGz-Wli/view?usp=sharing)
- use the Import manager in ATAK to import the configuration
- [more details](https://freetakteam.github.io/FreeTAKServer-User-Docs/Usage/Connecting%20ATAK/)

### Tell us what you think!
To discuss with the developer team:
- Visit the ATAK subreddit 
https://www.reddit.com/r/ATAK/ 
- or join the Discord chat
https://discordapp.com/invite/XEPyhHA

## Architecture
TAKFreeServer uses a MVC pattern, the concept of a COT (Cursor On Target) is described in a set of Domain classes, generated from the UML model using a Model Driven Architecture approach.

## Documentation
See [user docs](https://freetakteam.github.io/FreeTAKServer-User-Docs/) for various information including an UML model of the Domain classes involved in a COT event.

## Requirements
- Python 3.8 
- Dependencies:
  - `flask`
  - `lxml`
  - `pathlib`
  - `tabulate`
  - `sqlalchemy`
  - `setuptools` 
  - `Flask-SQLAlchemy`

## Installing and using FreeTakServer
For installation [go here](https://freetakteam.github.io/FreeTAKServer-User-Docs/Installation/Linux/1_Install/).

##  Project Structure
- [FreeTakServer](./FreeTAKServer/)
  - **Controllers**: Contains FTS business Logic
  - **Models**: Contains all the FTS  object model
  - **Views**:   contains the access to FTS


## Community 
If you have any issues don't hesitate to [bring it up](https://github.com/Tapawingo/FreeTakServer/issues), as FreeTAKServer is in continuous development.
To discuss with the developer team you may use:
- The [subreddit](https://www.reddit.com/r/ATAK/)
- The [public ATAK Discord Server](https://discordapp.com/invite/XEPyhHA)

## Donate
The FTS team is working  daily on the development of an open and free solution. We plan to do more than simply replicate the functionalities of the legacy TAK server, our road map includes integration with open source systems like LORA's Meshtastic, porting it to Android, having an open API, and much more.

We are doing it for free because we believe that donating personal time to a cause is an endeavour that is worthy per-se, However, we are also spending our own time and money to:
- Maintain a Public server and a test server
- Invest in different technologies for R&D

If you feel that FTS is useful to you and you can donate in those challenging times please consider contributing here:
[DONATE](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=brothercorvo%40gmail.com&item_name=FreeTAKServer+R%26D&currency_code=CAD&source=url)

You can also support the project by buying one of our [t-shirts](http://tee.pub/lic/elARpZYCmaw).

***NOTE***:
> Not a big fan of Paypal, but that is the easiest way I found for an initial attempt. We may go to some more ethical system in future.
Finally you can help the project by spamming FTS information, starring our repositories in github and Pip and upvoting us.

## Open Source Notes
FTS was made possible by the following Open Source projects.
We'd like to thank the following individuals and organizations for providing crucial support and making FTS possible.
- [flask](https://flask.palletsprojects.com/en/2.0.x/)
- [lxml](https://lxml.de/)
- [pathlib](https://pathlib.readthedocs.io/en/pep428/)
- [tabulate](https://pypi.org/project/tabulate/)
- [sqlalchemy](https://www.sqlalchemy.org/)
- [setuptools](https://pypi.org/project/setuptools/)
- [eventlet](https://eventlet.net/)
- [random_word](https://pypi.org/project/Random-Word/)
- [Pip](https://pypi.org/project/pip/)
- [Bootstrap4](https://getbootstrap.com/)
- [pyopenssl](https://pypi.org/project/pyOpenSSL/)
- [Flask Dashboard Black by AppSeed](https://github.com/app-generator/flask-black-dashboard)
