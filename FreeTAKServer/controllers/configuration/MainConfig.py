import os
import yaml
import random
from string import ascii_letters, digits, punctuation
from pathlib import Path
from uuid import uuid4

class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.9.9.6 Public'

    yaml_path = str(os.environ.get('FTS_CONFIG_PATH', '/opt/FTSConfig.yaml'))
    python_version = 'python3.8'
    userpath = '/usr/local/lib/'
    first_start = True

    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "0.0.0.0"

    ## The following are *all* the attributes supported by this class
    ## and their default values

    ## Network settings ##
    # Client ports
    CoTServicePort = 8087
    SSLCoTServicePort = 8089

    # this needs to be changed for private data packages to work
    DataPackageServiceDefaultIP = ip

    # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
    UserConnectionIP = ip

    # API IP and port
    APIIP = '0.0.0.0'
    APIPort = 19023

    # Federation port
    FederationPort = 9000

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    ## API Settings ##
    APIVersion = "1.9.5"
    nodeID = f"FreeTAKServer-{uuid4()}"
    OptimizeAPI = True
    DataReceptionBuffer = 1024
    MaxReceptionTime = 4

    # number of milliseconds to wait between each iteration of main loop
    # decreasing will increase CPU usage and server performance
    # increasing will decrease CPU usage and server performance
    MainLoopDelay = 100

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'

    ## Database Settings ##
    # whether or not to save CoT's to the DB
    SaveCoTToDB = True

    # this should be set before startup
    DBFilePath = '/opt/FTSDataBase.db'
    DataBaseType = 'SQLite'

    ## Paths ##
    MainPath = Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer')
    ExCheckMainPath = Path(fr'{MainPath}/ExCheck')
    ExCheckFilePath = Path(fr'{MainPath}/ExCheck/template')
    ExCheckChecklistFilePath = Path(fr'{MainPath}/ExCheck/checklist')
    DataPackageFilePath = Path(fr'{MainPath}/FreeTAKServerDataPackageFolder')
    LogFilePath = Path(fr'{MainPath}/Logs')
    certsPath = Path(fr'{MainPath}/certs')
    # location to backup client packages
    clientPackages = str(Path(fr'{MainPath}/certs/ClientPackages'))

    ## Certificate Settings ##
    keyDir = Path(fr'{certsPath}/server.key')
    pemDir = Path(fr'{certsPath}/server.pem') # or crt
    testPem = ''
    testKey = ''
    unencryptedKey = Path(fr'certsPath}/server.key.unencrypted')
    p12Dir = Path(fr'{certsPath}/server.p12')
    CA = Path(fr'{certsPath}/ca.pem')
    CAkey = Path(fr'{certsPath}/ca.key')
    CRLFile = Path(fr"{certsPath}/FTS_CRL.json")

    ## Federation Settings ##
    federationCert = Path(fr'{certsPath}/server.pem')
    federationKey = Path(fr'{certsPath}/server.key')
    federationKeyPassword = 'defaultpass'

    ## Secrets ##
    password = 'supersecret'
    websocketkey = "YourWebsocketKey"
    SecretKey = ''.join(random.choice(ascii_letters + digits + punctuation) for i in range(18))

    # Overlay the settings from the YAML config if it exists
    if os.path.exists(yaml_path):
        try:
            yamlConfig = yaml.safe_load(open(yaml_path).read())
        except OSError as e:
            raise RuntimeError(f"{yaml_path} exists, but can not be read")

        if yamlConfig.get("System"):
            MainLoopDelay = int(yamlConfig["System"].get("FTS_MAINLOOP_DELAY", MainLoopDelay))
            ConnectionMessage = yamlConfig["System"].get("FTS_CONNECTION_MESSAGE", ConnectionMessage)
            DataBaseType = yamlConfig["System"].get("FTS_DATABASE_TYPE", DataBaseType)
            OptimizeAPI = bool(yamlConfig["System"].get("FTS_OPTIMIZE_API", OptimizeAPI))
            SecretKey = yamlConfig["System"].get("FTS_SECRET_KEY", SecretKey)
            DataReceptionBuffer = int(yamlConfig["System"].get("FTS_DATA_RECEPTION_BUFFER", DataReceptionBuffer))
            MaxReceptionTime = int(yamlConfig["System"].get("FTS_MAX_RECEPTION_TIME", MaxReceptionTime))
            nodeID = yamlConfig["System"].get("FTS_NODE_ID", nodeID)

        if yamlConfig.get("Addresses"):
            CoTServicePort = int(yamlConfig["Addresses"].get('FTS_COT_PORT', CoTServicePort))
            SSLCoTServicePort = int(yamlConfig["Addresses"].get('FTS_SSLCOT_PORT', SSLCoTServicePort))
            DataPackageServiceDefaultIP = yamlConfig["Addresses"].get('FTS_DP_ADDRESS', DataPackageServiceDefaultIP)
            UserConnectionIP = yamlConfig["Addresses"].get("FTS_USER_ADDRESS", UserConnectionIP)
            APIPort = int(yamlConfig["Addresses"].get("FTS_API_PORT", APIPort))
            APIIP = yamlConfig["Addresses"].get("FTS_API_ADDRESS", APIIP)
            FederationPort = int(yamlConfig["Addresses"].get("FTS_FED_PORT", FederationPort))
            AllowedCLIIPs = yamlConfig["Addresses"].get("FTS_CLI_WHITELIST", AllowedCLIIPs)
            CLIIP = yamlConfig["Addresses"].get("FTS_CLI_IP", CLIIP)

        if yamlConfig.get("FileSystem"):
            DBFilePath = yamlConfig["FileSystem"].get("FTS_DB_PATH", DBFilePath)
            SaveCoTToDB = bool(yamlConfig["FileSystem"].get("FTS_COT_TO_DB", SaveCoTToDB))
            MainPath = yamlConfig["FileSystem"].get("FTS_MAINPATH", MainPath)
            certsPath = yamlConfig["FileSystem"].get("FTS_CERTS_PATH", certsPath)
            ExCheckMainPath = yamlConfig["FileSystem"].get("FTS_EXCHECK_PATH", ExCheckMainPath)
            ExCheckFilePath = yamlConfig["FileSystem"].get("FTS_EXCHECK_TEMPLATE_PATH", ExCheckFilePath)
            ExCheckChecklistFilePath = yamlConfig["FileSystem"].get("FTS_EXCHECK_CHECKLIST_PATH", ExCheckChecklistFilePath)
            DataPackageFilePath = yamlConfig["FileSystem"].get("FTS_DATAPACKAGE_PATH", DataPackageFilePath)
            LogFilePath = yamlConfig["FileSystem"].get("FTS_LOGFILE_PATH", LogFilePath)

        if yamlConfig.get("Certs"):
            keyDir = yamlConfig["Certs"].get("FTS_SERVER_KEYDIR", keyDir)
            pemDir = yamlConfig["Certs"].get("FTS_SERVER_PEMDIR", pemDir)
            testPem = yamlConfig["Certs"].get("FTS_TESTCLIENT_PEMDIR", testPem)
            testKey = yamlConfig["Certs"].get("FTS_TESTCLIENT_KEYDIR", testKey)
            unencryptedKey = yamlConfig["Certs"].get("FTS_UNENCRYPTED_KEYDIR", unencryptedKey)
            p12Dir = yamlConfig["Certs"].get("FTS_SERVER_P12DIR", p12Dir)
            CA = yamlConfig["Certs"].get("FTS_CADIR", CA)
            CAkey = yamlConfig["Certs"].get("FTS_CAKEYDIR", CAkey)
            federationCert = yamlConfig["Certs"].get("FTS_FEDERATION_CERTDIR", federationCert)
            federationKey = yamlConfig["Certs"].get("FTS_FEDERATION_KEYDIR", federationKey)
            federationKeyPassword = yamlConfig["Certs"].get("FTS_FEDERATION_KEYPASS", federationKeyPassword)
            password = yamlConfig["Certs"].get("FTS_CLIENT_CERT_PASSWORD", password)
            websocketkey = yamlConfig["Certs"].get("FTS_WEBSOCKET_KEY", websocketkey)
            CRLFile = yamlConfig["Certs"].get("FTS_CRLDIR", CRLFile)

    # Allow env vars to modify configuration
    MainLoopDelay = int(os.environ.get('FTS_MAINLOOP_DELAY', MainLoopDelay))
    ConnectionMessage = os.environ.get("FTS_CONNECTION_MESSAGE", ConnectionMessage)
    DataBaseType = os.environ.get("FTS_DATABASE_TYPE", DataBaseType)
    OptimizeAPI = bool(os.environ.get("FTS_OPTIMIZE_API", OptimizeAPI))
    SecretKey = os.environ.get("FTS_SECRET_KEY", SecretKey)
    DataReceptionBuffer = int(os.environ.get("FTS_DATA_RECEPTION_BUFFER", DataReceptionBuffer))
    MaxReceptionTime = int(os.environ.get("FTS_MAX_RECEPTION_TIME", MaxReceptionTime))
    nodeID = os.environ.get("FTS_NODE_ID", nodeID)
    CoTServicePort = int(os.environ.get('FTS_COT_PORT', CoTServicePort))
    SSLCoTServicePort = int(os.environ.get('FTS_SSLCOT_PORT', SSLCoTServicePort))
    DataPackageServiceDefaultIP = os.environ.get('FTS_DP_ADDRESS', DataPackageServiceDefaultIP)
    UserConnectionIP = os.environ.get("FTS_USER_ADDRESS", UserConnectionIP)
    APIPort = int(os.environ.get("FTS_API_PORT", APIPort))
    APIIP = os.environ.get("FTS_API_ADDRESS", APIIP)
    FederationPort = int(os.environ.get("FTS_FED_PORT", FederationPort))
    AllowedCLIIPs = re.split(r'[,:]', os.environ.get("FTS_CLI_WHITELIST")) or AllowedCLIIPs
    CLIIP = os.environ.get("FTS_CLI_IP", CLIIP)
    DBFilePath = os.environ.get("FTS_DB_PATH", DBFilePath)
    SaveCoTToDB = bool(os.environ.get("FTS_COT_TO_DB", SaveCoTToDB))
    MainPath = os.environ.get("FTS_MAINPATH", MainPath)
    certsPath = os.environ.get("FTS_CERTS_PATH", certsPath)
    ExCheckMainPath = os.environ.get("FTS_EXCHECK_PATH", ExCheckMainPath)
    ExCheckFilePath = os.environ.get("FTS_EXCHECK_TEMPLATE_PATH", ExCheckFilePath)
    ExCheckChecklistFilePath = os.environ.get("FTS_EXCHECK_CHECKLIST_PATH", ExCheckChecklistFilePath)
    DataPackageFilePath = os.environ.get("FTS_DATAPACKAGE_PATH", DataPackageFilePath)
    LogFilePath = os.environ.get("FTS_LOGFILE_PATH", LogFilePath)
    keyDir = os.environ.get("FTS_SERVER_KEYDIR", keyDir)
    pemDir = os.environ.get("FTS_SERVER_PEMDIR", pemDir)
    testPem = os.environ.get("FTS_TESTCLIENT_PEMDIR", testPem)
    testKey = os.environ.get("FTS_TESTCLIENT_KEYDIR", testKey)
    unencryptedKey = os.environ.get("FTS_UNENCRYPTED_KEYDIR", unencryptedKey)
    p12Dir = os.environ.get("FTS_SERVER_P12DIR", p12Dir)
    CA = os.environ.get("FTS_CADIR", CA)
    CAkey = os.environ.get("FTS_CAKEYDIR", CAkey)
    federationCert = os.environ.get("FTS_FEDERATION_CERTDIR", federationCert)
    federationKey = os.environ.get("FTS_FEDERATION_KEYDIR", federationKey)
    federationKeyPassword = os.environ.get("FTS_FEDERATION_KEYPASS", federationKeyPassword)
    password = os.environ.get("FTS_CLIENT_CERT_PASSWORD", password)
    websocketkey = os.environ.get("FTS_WEBSOCKET_KEY", websocketkey)
    CRLFile = os.environ.get("FTS_CRLDIR", CRLFile)
