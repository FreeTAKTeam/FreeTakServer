import os
currentPath = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path


class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """
    # this is the port to which clients will connect
    CoTServicePort = int(8087)

    SSLCoTServicePort = int(8089)

    # this needs to be changed for private data packages to work
    DataPackageServiceDefaultIP = str("0.0.0.0")

    # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
    UserConnectionIP = str("0.0.0.0")

    python_version = 'python3.8'

    userpath = '/usr/local/lib/'

    # api port
    APIPort = 19023

    # Federation port
    FederationPort = 9000

    # api IP
    APIIP = '0.0.0.0'

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    # whether or not to save CoT's to the DB
    SaveCoTToDB = bool(True)

    # this should be set before startup
    DBFilePath = str(r'/root/FTSDataBase.db')

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.5.10 RC 1'

    MainPath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer'))

    ExCheckMainPath = str(Path(fr'{MainPath}/ExCheck'))

    ExCheckFilePath = str(Path(fr'{MainPath}/ExCheck/template'))

    ExCheckChecklistFilePath = str(Path(fr'{MainPath}/ExCheck/checklist'))

    DataPackageFilePath = str(Path(fr'{MainPath}/FreeTAKServerDataPackageFolder'))

    # format of API message header should be {Authentication: Bearer 'TOKEN'}
    from uuid import uuid4
    id = str(uuid4())

    nodeID = f"FreeTAKServer-{id}"

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'

    keyDir = str(Path(fr'{MainPath}/certs/pubserver.key'))

    pemDir = str(Path(fr'{MainPath}/certs/pubserver.pem')) # or crt

    unencryptedKey = str(Path(fr'{MainPath}/certs/pubserver.key.unencrypted'))

    p12Dir = str(Path(fr'{MainPath}/certs/pubserver.p12'))

    CA = str(Path(fr'{MainPath}/certs/ca.pem'))
    CAkey = str(Path(fr'{MainPath}/certs/ca.key'))

    federationCert = str(Path(fr'{MainPath}/certs/pubserver.pem'))
    federationKey = str(Path(fr'{MainPath}/certs/pubserver.key'))
    federationKeyPassword = str('defaultpass')
    
    # location to backup client packages
    clientPackages = str(Path(fr'{MainPath}/certs/ClientPackages'))

    password = str('defaultpass')

    websocketkey = "YourWebsocketKey"