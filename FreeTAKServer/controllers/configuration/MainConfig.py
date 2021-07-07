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
    yaml_path = str(os.environ.get('FTS_CONFIG_PATH', '/opt/FTSConfig.yaml'))

    python_version = 'python3.8'

    userpath = '/usr/local/lib/'

    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "0.0.0.0"

    if not os.path.exists(yaml_path):
        MainLoopDelay = int(os.environ.get('FTS_MAINLOOP_DELAY', 1))

        # this is the port to which clients will connect
        CoTServicePort = int(os.environ.get('FTS_COT_PORT', 8087))

        SSLCoTServicePort = int(os.environ.get('FTS_SSLCOT_PORT', 8089))

        # this needs to be changed for private data packages to work
        DataPackageServiceDefaultIP = str(os.environ.get('FTS_DP_ADDRESS', ip))

        # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
        UserConnectionIP = str(os.environ.get('FTS_USER_ADDRESS', ip))

        # api port
        APIPort = os.environ.get('FTS_API_PORT', 19023)

        # Federation port
        FederationPort = os.environ.get('FTS_FED_PORT', 9000)

        # api IP
        APIIP = os.environ.get('FTS_API_ADDRESS', '0.0.0.0')

        # whether or not to save CoT's to the DB
        SaveCoTToDB = bool(os.environ.get('FTS_COT_TO_DB', True))

        # this should be set before startup
        DBFilePath = str(os.environ.get('FTS_DB_PATH', r'/opt/FTSDataBase.db'))

        MainPath = str(os.environ.get("FTS_MAINPATH", Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer')))

        certsPath = str(os.environ.get('FTS_CERTS_PATH', fr'{MainPath}/certs'))

        ExCheckMainPath = str(os.environ.get('FTS_EXCHECK_PATH', Path(fr'{MainPath}/ExCheck')))

        ExCheckFilePath = str(os.environ.get('FTS_EXCHECK_TEMPLATE_PATH', Path(fr'{MainPath}/ExCheck/template')))

        ExCheckChecklistFilePath = str(
            os.environ.get("FTS_EXCHECK_CHECKLIST_PATH", Path(fr'{MainPath}/ExCheck/checklist')))

        DataPackageFilePath = str(
            os.environ.get("FTS_DATAPACKAGE_PATH", Path(fr'{MainPath}/FreeTAKServerDataPackageFolder')))

        LogFilePath = str(os.environ.get("FTS_LOGFILE_PATH", Path(fr"{MainPath}/Logs")))

        federationKeyPassword = str(os.environ.get('FTS_FED_PASSWORD', 'defaultpass'))

        keyDir = str(os.environ.get("FTS_SERVER_KEYDIR", Path(fr'{certsPath}/server.key')))

        pemDir = str(os.environ.get("FTS_SERVER_PEMDIR", Path(fr'{certsPath}/server.pem')))  # or crt

        testPem = str(os.environ.get("FTS_TESTCLIENT_PEMDIR", pemDir))

        testKey = str(os.environ.get("FTS_TESTCLIENT_KEYDIR", keyDir))

        unencryptedKey = str(os.environ.get("FTS_UNENCRYPTED_KEYDIR", Path(fr'{certsPath}/server.key.unencrypted')))

        p12Dir = str(os.environ.get("FTS_SERVER_P12DIR", Path(fr'{certsPath}/server.p12')))

        CA = str(os.environ.get("FTS_CADIR", Path(fr'{certsPath}/ca.pem')))

        CAkey = str(os.environ.get("FTS_CAKEYDIR", Path(fr'{certsPath}/ca.key')))

        federationCert = str(os.environ.get("FTS_FEDERATION_CERTDIR", Path(fr'{certsPath}/server.pem')))

        federationKey = str(os.environ.get("FTS_FEDERATION_KEYDIR", Path(fr'{certsPath}/server.key')))

        federationKeyPassword = str(os.environ.get("FTS_FEDERATION_KEYPASS", 'defaultpass'))

        password = str(os.environ.get('FTS_CLIENT_CERT_PASSWORD', 'supersecret'))

        websocketkey = str(os.environ.get('FTS_WEBSOCKET_KEY', "YourWebsocketKey"))

        CRLFile = str(os.environ.get('FTS_CRLDIR', fr"{certsPath}/FTS_CRL.json"))

    else:
        content = open(yaml_path).read()
        yamlConfig = yaml.safe_load(content)

        # number of milliseconds to wait between each iteration of main loop
        # decreasing will increase CPU usage and server performance
        # increasing will decrease CPU usage and server performance
        if yamlConfig.get("System"):
            MainLoopDelay = int(os.environ.get('FTS_MAINLOOP_DELAY', yamlConfig["System"].get("MainLoopDelay", 1)))
        else:
            MainLoopDelay = int(os.environ.get('FTS_MAINLOOP_DELAY',  1))
        if yamlConfig.get("Addresses"):
            # this is the port to which clients will connect
            CoTServicePort = int(os.environ.get('FTS_COT_PORT', yamlConfig["Addresses"].get('CoTServicePort', 8087)))

            SSLCoTServicePort = int(os.environ.get('FTS_SSLCOT_PORT', yamlConfig["Addresses"].get('SSLCoTServicePort', 8089)))

            # this needs to be changed for private data packages to work
            DataPackageServiceDefaultIP = str(os.environ.get('FTS_DP_ADDRESS', yamlConfig["Addresses"].get('DataPackageServiceDefaultIP', ip)))

            # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
            UserConnectionIP = str(os.environ.get('FTS_USER_ADDRESS', yamlConfig["Addresses"].get("UserConnectionIP", ip)))

            # api port
            APIPort = int(os.environ.get('FTS_API_PORT', yamlConfig["Addresses"].get("APIPort", 19023)))

            # Federation port
            FederationPort = int(os.environ.get('FTS_FED_PORT', yamlConfig["Addresses"].get("FederationPort", 9000)))

            # api IP
            APIIP = str(os.environ.get('FTS_API_ADDRESS', yamlConfig["Addresses"].get("APIIP", "0.0.0.0")))
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

        if yamlConfig.get("FileSystem"):

            DBFilePath = str(os.environ.get('FTS_DB_PATH', yamlConfig["FileSystem"].get("DBFilePath", "/opt/FreeTAKServer")))

            # whether or not to save CoT's to the DB
            SaveCoTToDB = bool(os.environ.get('FTS_COT_TO_DB', yamlConfig["FileSystem"].get("SaveCoTToDB")))

            MainPath = str(os.environ.get("FTS_MAINPATH", yamlConfig["FileSystem"].get("MainPath", Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer'))))

            certsPath = str(os.environ.get('FTS_CERTS_PATH', yamlConfig["FileSystem"].get("CertsPath", fr'{MainPath}/certs')))

            ExCheckMainPath = str(os.environ.get('FTS_EXCHECK_PATH', yamlConfig["FileSystem"].get("ExCheckPath",Path(fr'{MainPath}/ExCheck'))))

            ExCheckFilePath = str(os.environ.get('FTS_EXCHECK_TEMPLATE_PATH', yamlConfig["FileSystem"].get("ExCheckTemplatePath", Path(fr'{MainPath}/ExCheck/template'))))

            ExCheckChecklistFilePath = str(os.environ.get("FTS_EXCHECK_CHECKLIST_PATH", yamlConfig["FileSystem"].get("ExCheckChecklistPath", Path(fr'{MainPath}/ExCheck/checklist'))))

            DataPackageFilePath = str(os.environ.get("FTS_DATAPACKAGE_PATH", yamlConfig["FileSystem"].get("DataPackageFilePath", Path(fr'{MainPath}/FreeTAKServerDataPackageFolder'))))

            LogFilePath = str(os.environ.get("FTS_LOGFILE_PATH", yamlConfig["FileSystem"].get("LogFilePath", Path(fr"{MainPath}/Logs"))))

        else:
            # whether or not to save CoT's to the DB
            SaveCoTToDB = bool(os.environ.get('FTS_COT_TO_DB', True))

            # this should be set before startup
            DBFilePath = str(os.environ.get('FTS_DB_PATH', r'/root/FTSDataBase.db'))

            MainPath = str(
                os.environ.get("FTS_MAINPATH", Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer')))

            certsPath = str(os.environ.get('FTS_CERTS_PATH', fr'{MainPath}/certs'))

            ExCheckMainPath = str(os.environ.get('FTS_EXCHECK_PATH', Path(fr'{MainPath}/ExCheck')))

            ExCheckFilePath = str(os.environ.get('FTS_EXCHECK_TEMPLATE_PATH', Path(fr'{MainPath}/ExCheck/template')))

            ExCheckChecklistFilePath = str(
                os.environ.get("FTS_EXCHECK_CHECKLIST_PATH", Path(fr'{MainPath}/ExCheck/checklist')))

            DataPackageFilePath = str(
                os.environ.get("FTS_DATAPACKAGE_PATH", Path(fr'{MainPath}/FreeTAKServerDataPackageFolder')))

            LogFilePath = str(os.environ.get("FTS_LOGFILE_PATH", Path(fr"{MainPath}/Logs")))


        if yamlConfig.get("Certs"):
            keyDir = str(os.environ.get("FTS_SERVER_KEYDIR", yamlConfig["Certs"].get("ServerKeyDir", Path(fr'{certsPath}/server.key'))))

            pemDir = str(os.environ.get("FTS_SERVER_PEMDIR",yamlConfig["Certs"].get("ServerPemDir", Path(fr'{certsPath}/server.pem')))) # or crt

            testPem = str(os.environ.get("FTS_TESTCLIENT_PEMDIR",yamlConfig["Certs"].get("TestPemDir", fr'{certsPath}/Client.pem')))

            testKey = str(os.environ.get("FTS_TESTCLIENT_KEYDIR",yamlConfig["Certs"].get("TestKeyDir", fr'{certsPath}/Client.key')))

            unencryptedKey = str(os.environ.get("FTS_UNENCRYPTED_KEYDIR", yamlConfig["Certs"].get("UnencryptedKeyDir", Path(fr'{certsPath}/server.key.unencrypted'))))

            p12Dir = str(os.environ.get("FTS_SERVER_P12DIR", yamlConfig["Certs"].get("ServerP12Dir", Path(fr'{certsPath}/server.p12'))))

            CA = str(os.environ.get("FTS_CADIR", yamlConfig["Certs"].get("CAPemDir",Path(fr'{certsPath}/ca.pem'))))

            CAkey = str(os.environ.get("FTS_CAKEYDIR", yamlConfig["Certs"].get("CAKeyDir",Path(fr'{certsPath}/ca.key'))))

            federationCert = str(os.environ.get("FTS_FEDERATION_CERTDIR", yamlConfig["Certs"].get("FederationPemDir", Path(fr'{certsPath}/server.pem'))))

            federationKey = str(os.environ.get("FTS_FEDERATION_KEYDIR", yamlConfig["Certs"].get("FederationKeyDir", Path(fr'{certsPath}/server.key'))))

            federationKeyPassword = str(os.environ.get("FTS_FEDERATION_KEYPASS", yamlConfig["Certs"].get("FederationKeyPassword", None)))

            password = str(os.environ.get('FTS_CLIENT_CERT_PASSWORD', yamlConfig["Certs"].get("ClientCertPassword", 'defaultpass')))

            websocketkey = str(os.environ.get('FTS_WEBSOCKET_KEY', yamlConfig["Certs"].get("WebsocketKey", "YourWebsocketKey")))

            CRLFile = str(os.environ.get('FTS_CRLDIR', yamlConfig["Certs"].get("CRLDir", fr"{certsPath}/FTS_CRL.json")))
        else:
            federationKeyPassword = str(os.environ.get('FTS_FED_PASSWORD', 'defaultpass'))

            keyDir = str(os.environ.get("FTS_SERVER_KEYDIR", Path(fr'{certsPath}/server.key')))

            pemDir = str(os.environ.get("FTS_SERVER_PEMDIR", Path(fr'{certsPath}/server.pem')))  # or crt

            testPem = str(os.environ.get("FTS_TESTCLIENT_PEMDIR", pemDir))

            testKey = str(os.environ.get("FTS_TESTCLIENT_KEYDIR", keyDir))

            unencryptedKey = str(os.environ.get("FTS_UNENCRYPTED_KEYDIR", Path(fr'{certsPath}/server.key.unencrypted')))

            p12Dir = str(os.environ.get("FTS_SERVER_P12DIR", Path(fr'{certsPath}/server.p12')))

            CA = str(os.environ.get("FTS_CADIR", Path(fr'{certsPath}/ca.pem')))

            CAkey = str(os.environ.get("FTS_CAKEYDIR", Path(fr'{certsPath}/ca.key')))

            federationCert = str(os.environ.get("FTS_FEDERATION_CERTDIR", Path(fr'{certsPath}/server.pem')))

            federationKey = str(os.environ.get("FTS_FEDERATION_KEYDIR", Path(fr'{certsPath}/server.key')))

            federationKeyPassword = str(os.environ.get("FTS_FEDERATION_KEYPASS", 'defaultpass'))

            password = str(os.environ.get('FTS_CLIENT_CERT_PASSWORD', 'defaultpass'))

            websocketkey = str(os.environ.get('FTS_WEBSOCKET_KEY', "YourWebsocketKey"))

            CRLFile = str(os.environ.get('FTS_CRLDIR', fr"{certsPath}/FTS_CRL.json"))


    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.9 Alpha RC 2'

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    # format of API message header should be {Authentication: Bearer 'TOKEN'}
    from uuid import uuid4
    id = str(uuid4())

    nodeID = os.environ.get('FTS_NODE_ID', f"FreeTAKServer-{id}")

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'


    # location to backup client packages
    clientPackages = str(Path(fr'{MainPath}/certs/ClientPackages'))

    first_start = True