import os
currentPath = os.path.dirname(os.path.abspath(__file__))

class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """
    # this is the port to which clients will connect
    CoTServicePort = int(8087)

    # this needs to be changed for private data packages to work
    DataPackageServiceDefaultIP = str("0.0.0.0")

    # api port
    APIPort = 19023

    # api IP
    APIIP = '0.0.0.0'

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    # whether or not to save CoT's to the DB
    SaveCoTToDB = bool(False)

    # this should be set before startup
    DBFilePath = str(r'/root/FTSDataBase.db')

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.2 RC 2'

    # set to None if you don't want a message sent
    ConnectionMessage = f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting'