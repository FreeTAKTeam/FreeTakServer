from typing import List

from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
import yaml
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
        if source.get(entry):
            source = source[entry]
        else:
            source[entry] = {}
            source = source[entry]

    print(data)

def ask_user_for_config():
    with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent, pathlib.Path("controllers/configuration/MainConfig.py")), mode="r+") as file:
        data = file.readlines()
        data[-1] = "    first_start = False"

    with open(pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent,
                               pathlib.Path("controllers/configuration/MainConfig.py")), mode="w+") as file:
        file.writelines(data)
    use_yaml = get_user_input(question="would you like to use a yaml config file, \n if yes you will be prompted for further configuration options", default="yes")
    if use_yaml == "yes":
        yaml_path = get_user_input(question="where would you like to save the yaml config", default=MainConfig.yaml_path)
        if yaml_path != MainConfig.yaml_path:
            file_path = (pathlib.PurePath(pathlib.Path(__file__).parent.resolve().parent, pathlib.Path("controllers/configuration/MainConfig.py")))
            file = open(file_path, mode="r+")
            data = file.readlines()
            data[13] = f'    yaml_path = "{yaml_path}"'
            file.close()
        MainConfig.yaml_path = yaml_path
        content = open(yaml_path, mode="w+").read()
        yaml_config = yaml.safe_load(content)
        if not yaml_config:
            yaml_config = {}
        ip = get_user_input(question="enter ip", default= MainConfig.ip)
        add_to_config(data=ip, path=["Address", "FTS_MAIN_IP"], source=yaml_config)
        database_path = get_user_input(question="enter the preferred database path", default=MainConfig.DBFilePath)
        MainConfig.DBFilePath = database_path
        add_to_config(data = database_path, path=["FileSystem", "FTS_DB_PATH"], source=yaml_config)
        main_path = get_user_input(question="enter the preferred main_path", default=MainConfig.MainPath)
        MainConfig.MainPath = main_path
        add_to_config(path=["FileSystem", "FTS_MAINPATH"], data= main_path, source= yaml_config)
        log_path = get_user_input(question="enter the preferred log file path", default=MainConfig.LogFilePath)
        add_to_config(path=["FileSystem", "FTS_LOGFILE_PATH"], data=log_path, source=yaml_config)
        file = open(yaml_path, mode="w+")
        file.write(yaml.dump(yaml_config))
        file.close()
    else:
        pass
        """ip = get_user_input(question="enter ip", default=MainConfig.ip)
        MainConfig.ip = ip
        database_path = get_user_input(question="enter the preferred database path", default=MainConfig.DBFilePath)
        MainConfig.DBFilePath = database_path
        main_path = get_user_input(question="enter the preferred main_path", default=MainConfig.MainPath)
        MainConfig.MainPath = main_path
        log_path = get_user_input(question="enter the preferred log file path", default=MainConfig.LogFilePath)
        MainConfig.LogFilePath = log_path"""