from typing import List

from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from ruamel.yaml import YAML
yaml = YAML()
import pathlib

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

    print(data)

def ask_user_for_config():
    use_yaml = get_user_input(question="would you like to use a yaml config file, \n if yes you will be prompted for further configuration options", default="yes")
    if use_yaml == "yes":
        yaml_path = get_user_input(question="where would you like to save the yaml config", default=MainConfig.yaml_path)
        yaml_config = yaml.load(default_yaml_file)
        ip = get_user_input(question="enter ip", default= MainConfig.ip)
        add_to_config(data=ip, path=["Addresses", "FTS_DP_ADDRESS"], source=yaml_config)
        add_to_config(data=ip, path=["Addresses", "FTS_USER_ADDRESS"], source=yaml_config)
        while True:
            database = get_user_input(question="enter the preferred database type (MySQL is highly experimental if you're not sure leave default)", default="SQLite")

            if database == "SQLite":
                database_path = get_user_input(question="enter the preferred database path", default=MainConfig.DBFilePath)
                break
            elif database == "MySQL":
                username = get_user_input(question="please enter MySQL username")
                password = get_user_input(question="please enter MySQL password")
                db_ip = get_user_input(question="please enter MySQL server IP")
                db_name = get_user_input(question="please enter MySQL DataBase name")
                database_path = f"{username}:{password}@{db_ip}/{db_name}"
                MainConfig.DataBaseType = "MySQL"
                add_to_config(data=database, path=["System", "FTS_DATABASE_TYPE"], source=yaml_config)
                break
            else:
                print('invalid database type')
        MainConfig.DBFilePath = database_path
        add_to_config(data=database_path, path=["FileSystem", "FTS_DB_PATH"], source=yaml_config)
        main_path = get_user_input(question="enter the preferred main_path", default=MainConfig.MainPath)
        MainConfig.MainPath = main_path
        add_to_config(path=["FileSystem", "FTS_MAINPATH"], data= main_path, source= yaml_config)
        log_path = get_user_input(question="enter the preferred log file path", default=MainConfig.LogFilePath)
        add_to_config(path=["FileSystem", "FTS_LOGFILE_PATH"], data=log_path, source=yaml_config)
        with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent,
                                   pathlib.Path("controllers/configuration/MainConfig.py")), mode="r+") as file:
            data = file.readlines()
            data[-1] = "    first_start = False"

        with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent,
                                   pathlib.Path("controllers/configuration/MainConfig.py")), mode="w+") as file:
            file.writelines(data)
        if yaml_path != MainConfig.yaml_path:
            file_path = (pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent, pathlib.Path("controllers/configuration/MainConfig.py")))
            file = open(file_path, mode="r+")
            data = file.readlines()
            data[13] = f'    yaml_path = "{yaml_path}"'
            file.close()
        MainConfig.yaml_path = yaml_path
        file = open(yaml_path, mode="w+")
        yaml.dump(yaml_config, file)
        file.close()
    else:
        with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent,
                                   pathlib.Path("controllers/configuration/MainConfig.py")), mode="r+") as file:
            data = file.readlines()
            data[-1] = "    first_start = False"

        with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent,
                                   pathlib.Path("controllers/configuration/MainConfig.py")), mode="w+") as file:
            file.writelines(data)
        """ip = get_user_input(question="enter ip", default=MainConfig.ip)
        MainConfig.ip = ip
        database_path = get_user_input(question="enter the preferred database path", default=MainConfig.DBFilePath)
        MainConfig.DBFilePath = database_path
        main_path = get_user_input(question="enter the preferred main_path", default=MainConfig.MainPath)
        MainConfig.MainPath = main_path
        log_path = get_user_input(question="enter the preferred log file path", default=MainConfig.LogFilePath)
        MainConfig.LogFilePath = log_path"""

default_yaml_file = """
Addresses:
  #FTS_COT_PORT: 8087
  #FTS_SSLCOT_PORT: 8089
  FTS_DP_ADDRESS: 0.0.0.0
  FTS_USER_ADDRESS: 0.0.0.0
  #FTS_API_PORT: 19023
  #FTS_FED_PORT: 9000
  #FTS_API_ADDRESS: 0.0.0.0
FileSystem:
  FTS_DB_PATH: /opt/FreeTAKServer.db
  #FTS_COT_TO_DB: True
  FTS_MAINPATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer
  #FTS_CERTS_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs
  #FTS_EXCHECK_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/ExCheck
  #FTS_EXCHECK_TEMPLATE_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/ExCheck/template
  #FTS_EXCHECK_CHECKLIST_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/ExCheck/checklist
  #FTS_DATAPACKAGE_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/FreeTAKServerDataPackageFolder
  #FTS_LOGFILE_PATH: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/Logs
Certs:
  #FTS_SERVER_KEYDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.key
  #FTS_SERVER_PEMDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.pem
  #FTS_TESTCLIENT_PEMDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/Client.pem
  #FTS_TESTCLIENT_KEYDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/Client.key
  #FTS_UNENCRYPTED_KEYDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.key.unencrypted
  #FTS_SERVER_P12DIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.p12
  #FTS_CADIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/ca.pem
  #FTS_CAKEYDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/ca.key
  #FTS_FEDERATION_CERTDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.pem
  #FTS_FEDERATION_KEYDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/server.key
  #FTS_CRLDIR: /usr/local/lib/python3.8/dist-packages/FreeTAKServer/certs/FTS_CRL.json
  #FTS_FEDERATION_KEYPASS: demopassfed
  #FTS_CLIENT_CERT_PASSWORD: demopasscert
  #FTS_WEBSOCKET_KEY: YourWebsocketKey
"""