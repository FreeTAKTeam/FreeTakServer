# FreeTAKServer [![Downloads](https://pepy.tech/badge/freetakserver)](https://pepy.tech/project/freetakserver) ![PyPI](https://img.shields.io/pypi/v/FreeTAKServer) ![GitHub release (latest by date)](https://img.shields.io/github/v/release/FreeTAKTeam/FreeTakServer) ![Lines of code](https://img.shields.io/tokei/lines/github.com/FreeTAKTeam/FreeTakServer)


![the Parrot is not dead](https://user-images.githubusercontent.com/60719165/226138056-a2b1076c-fd4c-4488-b330-55e57f9ecc78.png)

Ласкаво просимо до репозиторію git FreeTakServer (FTS).

FTS — це реалізація TAK-сервера на Python3 для таких пристроїв, як ATAK, WinTAK і ITAK, вона є кросплатформною та працює від інсталяції на кількох вузлах на AWS до версії Android. Він безкоштовний із відкритим вихідним кодом (випущений згідно з публічною ліцензією Eclipse.

## Документація користувача
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

## Статус проекту
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

## Вимоги
- Python 3.8 
- Dependencies:
  - `flask`
  - `lxml`
  - `pathlib`
  - `tabulate`
  - `sqlalchemy`
  - `setuptools` 
  - `Flask-SQLAlchemy`

## Встановлення та використання FreeTakServer
For installation [go here](https://freetakteam.github.io/FreeTAKServer-User-Docs/Installation/Linux/1_Install/).

##  Project Structure
- [FreeTakServer](./FreeTAKServer/)
  - **Controllers**: Contains FTS business Logic
  - **Models**: Contains all the FTS  object model
  - **Views**:   contains the access to FTS


## Спільнота 
If you have any issues don't hesitate to [bring it up](https://github.com/Tapawingo/FreeTakServer/issues), as FreeTAKServer is in continuous development.
To discuss with the developer team you may use:
- The [subreddit](https://www.reddit.com/r/ATAK/)
- The [public ATAK Discord Server](https://discordapp.com/invite/XEPyhHA)

## Пожертвуйте
Команда FTS щодня працює над розробкою відкритого та безкоштовного рішення. Ми плануємо зробити більше, ніж просто відтворити функції застарілого сервера TAK, наша дорожня карта включає інтеграцію з системами з відкритим кодом, як-от Meshtastic від LORA, перенесення його на Android, наявність відкритого API та багато іншого.

Ми робимо це безкоштовно, тому що вважаємо, що пожертвування особистого часу на справу є справою, яка сама по собі гідна. Однак ми також витрачаємо свій час і гроші на:
- Підтримувати публічний сервер і тестовий сервер
- Інвестуйте в різні технології для досліджень і розробок

Якщо ви вважаєте, що FTS корисний для вас і можете зробити пожертву в ці складні часи, зробіть внесок тут:
[Пожертвуйте](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=brothercorvo%40gmail.com&item_name=FreeTAKServer+R%26D&currency_code=CAD&source=url)

You can also support the project by buying one of our [t-shirts](http://tee.pub/lic/elARpZYCmaw).

***ПРИМІТКА***:
>Я не великий шанувальник Paypal, але це найпростіший спосіб, який я знайшов для першої спроби. У майбутньому ми можемо перейти до більш етичної системи.
Нарешті, ви можете допомогти проекту, розсилаючи спам із інформацією FTS, показуючи наші репозиторії на github і Pip і голосуючи за нас.
![star-history-2023123](https://user-images.githubusercontent.com/60719165/214117639-8bd41fd2-adea-4d41-a3b5-c75dca57b369.png)


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
