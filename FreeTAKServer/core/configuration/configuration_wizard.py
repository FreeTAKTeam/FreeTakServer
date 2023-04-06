import os
from typing import List

from FreeTAKServer.core.configuration.MainConfig import MainConfig
from ruamel.yaml import YAML
from pathlib import Path
yaml = YAML()

# TODO  This code may have problems with the rewrite of MainConfig
# Make a connection to the MainConfig object for all routines below
config = MainConfig.instance()

# TODO: refactor this
def get_user_input(*, question: str, default: str = None, options: list = None):
    input_string = question
    if default:
        input_string += f" [{default}]: "
        choice = input(input_string)
        if not choice:
            return default
        else:
            return choice
    """else:
        print(question+f" [{default}]: "+"\n")
        for option in range(0, len(options)):
            print(option)"""

def add_to_config(path: List[str], data: str, source: dict):
    for index in range(0, len(path)):
        entry = path[index]
        if index == len(path) - 1:
            source[entry] = data
            break
        if source.get(entry):
            source = source[entry]
        else:
            source[entry] = {}
            source = source[entry]

def get_yaml_config(yaml_path):
    # if the path doesnt exist create a new file
    if not os.path.exists(yaml_path):
        open(yaml_path, 'w+').close()
        return {}
    # otherwise load the existing file
    else:
        with open(yaml_path, "r+") as fp:
            return yaml.load(fp)
    

def ask_user_for_config():
    use_yaml = get_user_input(question="would you like to use a yaml config file, \n if yes you will be prompted for further configuration options", default="yes")
    if use_yaml != "yes":
        return

    yaml_path = get_user_input(question="where would you like to save the yaml config", default=config.yaml_path)
    
    yaml_config = get_yaml_config(yaml_path)

    ip = get_user_input(question="enter ip", default=config.UserConnectionIP)
    add_to_config(data=ip, path=["Addresses", "FTS_DP_ADDRESS"], source=yaml_config)
    add_to_config(data=ip, path=["Addresses", "FTS_USER_ADDRESS"], source=yaml_config)
    while True:
        database = get_user_input(question="enter the preferred database type (MySQL is highly experimental if you're not sure leave default)", default="SQLite")

        if database == "SQLite":
            database_path = get_user_input(question="enter the preferred database path", default=config.DBFilePath)

            while not valid_and_safe_path(database_path):
                print("Invalid path. Path does not exist or insufficient permissions exist.")
                database_path = get_user_input(question="enter the preferred database path", default=config.DBFilePath)
            break
        elif database == "MySQL":
            username = get_user_input(question="please enter MySQL username")
            password = get_user_input(question="please enter MySQL password")
            db_ip = get_user_input(question="please enter MySQL server IP")
            db_name = get_user_input(question="please enter MySQL DataBase name")
            database_path = f"{username}:{password}@{db_ip}/{db_name}"
            config.DataBaseType = "MySQL"
            add_to_config(data=database, path=["System", "FTS_DATABASE_TYPE"], source=yaml_config)
            break
        else:
            print('invalid database type')
    config.DBFilePath = database_path
    add_to_config(data=database_path, path=["FileSystem", "FTS_DB_PATH"], source=yaml_config)

    main_path = get_user_input(question="enter the preferred main path", default=config.MainPath)
    while not valid_and_safe_path(main_path):
        print("Invalid path. Path does not exist or insufficient permissions exist.")
        main_path = get_user_input(question="enter the preferred main path", default=config.MainPath)

    config.MainPath = main_path
    add_to_config(path=["FileSystem", "FTS_MAINPATH"], data= main_path, source= yaml_config)

    log_path = get_user_input(question="enter the preferred log file path", default=config.LogFilePath)
    while not valid_and_safe_path(log_path):
        print("Invalid path. Path does not exist or insufficient permissions exist.")
        log_path = get_user_input(question="enter the preferred log file path", default=config.LogFilePath)

    add_to_config(path=["FileSystem", "FTS_LOGFILE_PATH"], data=log_path, source=yaml_config)
    config.yaml_path = yaml_path
    file = open(yaml_path, mode="w+")
    yaml.dump(yaml_config, file)
    file.close()
    create_installation_file()

    """ip = get_user_input(question="enter ip", default=MainConfig.ip)
    MainConfig.ip = ip
    """

def create_installation_file():
    """create an installation.json file in the directory to inform the application on startup that
    the installation process has completed"""
    f = open(f"{config.persistencePath}/installation.json", "w+")
    f.close()

def valid_and_safe_path(path):
    """Method that sanitized path and determines if it exists and writable
    """
    # Check if the input is a string
    if not isinstance(path, str):
        raise ValueError("Input must be a string")
    
    # Check if the input is an absolute path
    path = Path(path).resolve()
    if not path.is_absolute():
        raise ValueError("Input must be an absolute path")
    sanitized_path = path.relative_to(path.parent)
    sanitized_parent = path.parent.relative_to(path.parent)
    return (
        (
            sanitized_path.exists()
            and os.access(sanitized_path, os.F_OK)
            and os.access(sanitized_path, os.W_OK)
            and os.access(sanitized_path, os.R_OK)
        ) or
        (
            not sanitized_path.exists()
            and sanitized_parent.exists()
            and os.access(sanitized_parent, os.F_OK)
            and os.access(sanitized_parent, os.W_OK)
            and os.access(sanitized_parent, os.R_OK)
        )
    )

default_yaml_file = f"""
System:
  #FTS_DATABASE_TYPE: SQLite
  FTS_CONNECTION_MESSAGE: Welcome to FreeTAKServer {config.version}. The Parrot is not dead. It’s just resting
  #FTS_OPTIMIZE_API: True
  #FTS_MAINLOOP_DELAY: 1
Addresses:
  #FTS_COT_PORT: 8087
  #FTS_SSLCOT_PORT: 8089
  FTS_DP_ADDRESS: 0.0.0.0
  FTS_USER_ADDRESS: 0.0.0.0
  #FTS_API_PORT: 19023
  #FTS_FED_PORT: 9000
  #FTS_API_ADDRESS: 0.0.0.0
FileSystem:
  FTS_DB_PATH: /opt/fts/FreeTAKServer.db
  #FTS_COT_TO_DB: True
  FTS_PERSISTENCE_PATH: /opt/fts/
  #FTS_CERTS_PATH: /opt/fts/certs
  #FTS_EXCHECK_PATH: /opt/fts/ExCheck
  #FTS_EXCHECK_TEMPLATE_PATH: /opt/fts/ExCheck/template
  #FTS_EXCHECK_CHECKLIST_PATH: /opt/fts/ExCheck/checklist
  #FTS_DATAPACKAGE_PATH: /opt/fts/FreeTAKServerDataPackageFolder
  #FTS_LOGFILE_PATH: /opt/fts/Logs
Certs:
  #FTS_SERVER_KEYDIR: /opt/fts/certs/server.key
  #FTS_SERVER_PEMDIR: /opt/fts/certs/server.pem
  #FTS_TESTCLIENT_PEMDIR: /opt/fts/certs/Client.pem
  #FTS_TESTCLIENT_KEYDIR: /opt/fts/certs/Client.key
  #FTS_UNENCRYPTED_KEYDIR: /opt/fts/certs/server.key.unencrypted
  #FTS_SERVER_P12DIR: /opt/fts/certs/server.p12
  #FTS_CADIR: /opt/fts/certs/ca.pem
  #FTS_CAKEYDIR: /opt/fts/certs/ca.key
  #FTS_FEDERATION_CERTDIR: /opt/fts/certs/server.pem
  #FTS_FEDERATION_KEYDIR: /opt/fts/certs/server.key
  #FTS_CRLDIR: /opt/fts/certs/FTS_CRL.json
  #FTS_FEDERATION_KEYPASS: demopassfed
  #FTS_CLIENT_CERT_PASSWORD: demopasscert
  #FTS_WEBSOCKET_KEY: YourWebsocketKey
"""