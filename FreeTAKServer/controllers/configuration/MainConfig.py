import os
import yaml
currentPath = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path


class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """

    #
    AlternateConfig = str(os.environ.get('FTS_CONFIG_PATH', '/opt/FTSConfig.yaml'))

    python_version = 'python3.8'

    userpath = '/usr/local/lib/'

    if os.path.exists(AlternateConfig):
        content = open(AlternateConfig).read()
        yamlConfig = yaml.safe_load(content)

        # this is the port to which clients will connect
        CoTServicePort = int(os.environ.get('FTS_COT_PORT', yamlConfig['CoTServicePort']))

        SSLCoTServicePort = int(os.environ.get('FTS_SSLCOT_PORT', yamlConfig['SSLCoTServicePort']))

        # this needs to be changed for private data packages to work
        DataPackageServiceDefaultIP = str(os.environ.get('FTS_DP_ADDRESS', yamlConfig['DataPackageServiceDefaultIP']))

        # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
        UserConnectionIP = str(os.environ.get('FTS_USER_ADDRESS', yamlConfig["UserConnectionIP"]))

        DBFilePath = str(os.environ.get('FTS_DB_PATH', yamlConfig["DBFilePath"]))

        # whether or not to save CoT's to the DB
        SaveCoTToDB = bool(os.environ.get('FTS_COT_TO_DB', yamlConfig["SaveCoTToDB"]))

        # api port
        APIPort = os.environ.get('FTS_API_PORT', yamlConfig["APIPort"])

        # Federation port
        FederationPort = os.environ.get('FTS_FED_PORT', yamlConfig["FederationPort"])

        # api IP
        APIIP = os.environ.get('FTS_API_ADDRESS', yamlConfig["APIIP"])

        if "MainPath" in yamlConfig.keys():
            MainPath = str(Path(yamlConfig["MainPath"]))
        else:
            MainPath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer'))

        if "CertsPath" in yamlConfig.keys():
            certsPath = os.environ.get('FTS_CERTS_PATH', yamlConfig["CertsPath"])
        else:
            certsPath = os.environ.get('FTS_CERTS_PATH', fr'{MainPath}/certs')

    else:
        # this is the port to which clients will connect
        CoTServicePort = int(os.environ.get('FTS_COT_PORT', 8087))

        SSLCoTServicePort = int(os.environ.get('FTS_SSLCOT_PORT', 8089))

        # this needs to be changed for private data packages to work
        DataPackageServiceDefaultIP = str(os.environ.get('FTS_DP_ADDRESS', "0.0.0.0"))

        # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
        UserConnectionIP = str(os.environ.get('FTS_USER_ADDRESS', "0.0.0.0"))

        # api port
        APIPort = os.environ.get('FTS_API_PORT', 19023)

        # Federation port
        FederationPort = os.environ.get('FTS_FED_PORT', 9000)

        # api IP
        APIIP = os.environ.get('FTS_API_ADDRESS', '0.0.0.0')

        # whether or not to save CoT's to the DB
        SaveCoTToDB = bool(os.environ.get('FTS_COT_TO_DB', True))

        # this should be set before startup
        DBFilePath = str(os.environ.get('FTS_DB_PATH', r'/root/FTSDataBase.db'))

        MainPath = str(Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer'))

        certsPath = os.environ.get('FTS_CERTS_PATH', fr'{MainPath}/certs')

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.8 RC 1 Public'

    # number of milliseconds to wait between each iteration of main loop
    # decreasing will increase CPU usage and server performance
    # increasing will decrease CPU usage and server performance
    MainLoopDelay = 1/1000

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    ExCheckMainPath = str(Path(fr'{MainPath}/ExCheck'))

    ExCheckFilePath = str(Path(fr'{MainPath}/ExCheck/template'))

    ExCheckChecklistFilePath = str(Path(fr'{MainPath}/ExCheck/checklist'))

    DataPackageFilePath = str(Path(fr'{MainPath}/FreeTAKServerDataPackageFolder'))

    # format of API message header should be {Authentication: Bearer 'TOKEN'}
    from uuid import uuid4
    id = str(uuid4())

    nodeID = os.environ.get('FTS_NODE_ID', f"FreeTAKServer-{id}")

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'



    keyDir = str(Path(fr'{certsPath}/pubserver.key'))

    pemDir = str(Path(fr'{certsPath}/pubserver.pem'))  # or crt

    unencryptedKey = str(Path(fr'{certsPath}/pubserver.key.unencrypted'))

    p12Dir = str(Path(fr'{certsPath}/pubserver.p12'))

    CA = str(Path(fr'{certsPath}/ca.pem'))
    CAkey = str(Path(fr'{certsPath}/ca.key'))

    federationCert = str(Path(fr'{certsPath}/pubserver.pem'))
    federationKey = str(Path(fr'{certsPath}/pubserver.key'))
    federationKeyPassword = str(os.environ.get('FTS_FED_PASSWORD','defaultpass'))

    # location to backup client packages
    clientPackages = str(Path(fr'{MainPath}/certs/ClientPackages'))

    password = str(os.environ.get('FTS_PASSWORD', 'defaultpass'))

    websocketkey = os.environ.get('FTS_WEBSOCKET_KEY', "YourWebsocketKey")
