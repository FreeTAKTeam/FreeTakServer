import os
import sys
import re
import yaml
currentPath = os.path.dirname(os.path.abspath(__file__))

from pathlib import Path
from uuid import uuid4

# the version information of the server (recommended to leave as default)

FTS_VERSION = "FreeTAKServer-2.0.69.1"
API_VERSION = "3.0"
ROOTPATH = "/"
MAINPATH = Path(__file__).parent.parent.parent
USERPATH = rf"{ROOTPATH}usr/local/lib/"
PERSISTENCE_PATH = r'/opt/fts'

class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """

    _instance = None
    _values = {}

    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        _ip = s.getsockname()[0]
        s.close()
    except:
        _ip = "0.0.0.0"

    # create the persistence path if it doesn't exist
    if not os.path.exists(PERSISTENCE_PATH):
        try:
            os.mkdir(PERSISTENCE_PATH)
        except Exception as e:
            print(f"failed to create the fts persistence directory at {PERSISTENCE_PATH} with error: {e}")
            sys.exit(1)
    
    _node_id = str(uuid4())

    # All available config vars should be defined here
    #   currently only 'default', 'type' and 'readonly' are recognized
    _defaults = {
        "version": {"default": FTS_VERSION, "type": str, "readonly": True},
        "APIVersion": {"default": API_VERSION, "type": str, "readonly": True},
        "SecretKey": {"default": "vnkdjnfjknfl1232#", "type": str},
        "nodeID": {"default": f"FreeTAKServer-{_node_id}", "type": str},
        "OptimizeAPI": {"default": True, "type": bool},
        "DataReceptionBuffer": {"default": 1024, "type": int},
        "MaxReceptionTime": {"default": 4, "type": int},
        "LogLevel": {"default": "info", "type": str},
        "UserPersistencePath": {
            "default": Path("/opt/user_persistence.txt"),
            "type": str,
        },
        # number of milliseconds to wait between each iteration of main loop
        # decreasing will increase CPU usage and server performance
        # increasing will decrease CPU usage and server performance
        "MainLoopDelay": {"default": 100, "type": int},
        # this is the port to which clients will connect
        "CoTServicePort": {"default": 8087, "type": int},
        "SSLCoTServicePort": {"default": 8089, "type": int},
        # this needs to be changed for private data packages to work
        "DataPackageServiceDefaultIP": {"default": _ip, "type": str},
        # User Connection package IP needs to be set to the IP which is
        # used when creating the connection in your tak device
        "UserConnectionIP": {"default": _ip, "type": str},
        # api port
        "APIPort": {"default": 19023, "type": int},
        # Federation port
        "FederationPort": {"default": 9000, "type": int},
        # api IP
        "APIIP": {"default": "0.0.0.0", "type": str},
        # IP for CLI to access
        "CLIIP": {"default": "127.0.0.1", "type": str},
        "AllowCLIIPs": {"default": ["127.0.0.1"], "type": list},
        # whether or not to save CoT's to the DB
        "SaveCoTToDB": {"default": True, "type": bool},
        # this should be set before startup
        "DBFilePath": {"default": f"{PERSISTENCE_PATH}/FTSDataBase.db", "type": str},
        "MainPath": {"default": Path(MAINPATH), "type": str},
        "certsPath": {"default": Path(rf"{PERSISTENCE_PATH}/certs"), "type": str},
        "ExCheckMainPath": {"default": Path(rf"{PERSISTENCE_PATH}/ExCheck"), "type": str},
        "ExCheckFilePath": {
            "default": Path(rf"{PERSISTENCE_PATH}/ExCheck/template"),
            "type": str,
        },
        "ExCheckChecklistFilePath": {
            "default": Path(rf"{PERSISTENCE_PATH}/ExCheck/checklist"),
            "type": str,
        },
        "DataPackageFilePath": {
            "default": Path(rf"{PERSISTENCE_PATH}/FreeTAKServerDataPackageFolder"),
            "type": str,
        },
        "LogFilePath": {"default": Path(rf"{PERSISTENCE_PATH}/Logs"), "type": str},
        "federationKeyPassword": {"default": "defaultpass", "type": str},
        "keyDir": {"default": Path(rf"{PERSISTENCE_PATH}/certs/server.key"), "type": str},
        "pemDir": {"default": Path(rf"{PERSISTENCE_PATH}/certs/server.pem"), "type": str},
        "testPem": {"default": Path(rf"{PERSISTENCE_PATH}/certs/server.key"), "type": str},
        "testKey": {"default": Path(rf"{PERSISTENCE_PATH}/certs/server.pem"), "type": str},
        "unencryptedKey": {
            "default": Path(rf"{PERSISTENCE_PATH}/certs/server.key.unencrypted"),
            "type": str,
        },
        "p12Dir": {"default": Path(rf"{PERSISTENCE_PATH}/certs/server.p12"), "type": str},
        "CA": {"default": Path(rf"{PERSISTENCE_PATH}/certs/ca.pem"), "type": str},
        "CAkey": {"default": Path(rf"{PERSISTENCE_PATH}/certs/ca.key"), "type": str},
        "federationCert": {
            "default": Path(rf"{PERSISTENCE_PATH}/certs/server.pem"),
            "type": str,
        },
        "federationKey": {
            "default": Path(rf"{PERSISTENCE_PATH}/certs/server.key"),
            "type": str,
        },
        "password": {"default": "supersecret", "type": str},
        "websocketkey": {"default": "YourWebsocketKey", "type": str},
        "CRLFile": {"default": Path(rf"{PERSISTENCE_PATH}/certs/FTS_CRL.json"), "type": str},
        # set to None if you don't want a message sent
        "ConnectionMessage": {
            "default": f"Welcome to FreeTAKServer {FTS_VERSION}. The Parrot is not dead. It’s just resting",
            "type": str,
        },
        "DataBaseType": {"default": "SQLite", "type": str},
        # location to backup client packages
        "ClientPackages": {
            "default": Path(rf"{PERSISTENCE_PATH}/certs/clientPackages"),
            "type": str,
        },
        "CoreComponentsPath": {
            "default": Path(rf"{MAINPATH}/core"),
            "type": str,
        },
        "CoreComponentsImportRoot": {
            "default": "FreeTAKServer.core",
            "type": str,
        },
        "InternalComponentsPath": {
            "default": Path(rf"{MAINPATH}/components/core"),
            "type": str,
        },
        "InternalComponentsImportRoot": {
            "default": "FreeTAKServer.components.core",
            "type": str,
        },
        "ExternalComponentsPath": {
            "default": Path(rf"{MAINPATH}/components/extended"),
            "type": str,
        },
        "ExternalComponentsImportRoot": {
            "default": "FreeTAKServer.components.extended",
            "type": str,
        },
        # the number of routing workers to use
        "NumRoutingWorkers": {"default": 3, "type": int},
        # port to subscribe to requests by the routing proxy
        "RoutingProxySubscriberPort": {"default": 19030, "type": int},
        # port to publish responses by the routing proxy
        "RoutingProxyPublisherPort": {"default": 19032, "type": int},
        # port to send requests from the routing proxy to the routing workers
        "RoutingProxyRequestServerPort": {"default": 19031, "type": int},
        # ip to subscribe to requests by the routing proxy
        "RoutingProxySubscriberIP": {"default": "127.0.0.1", "type": str},
        # ip to publish responses by the routing proxy
        "RoutingProxyPublisherIP": {"default": "127.0.0.1", "type": str},
        # port to send requests from the routing proxy to the routing workers
        "RoutingProxyRequestServerIP": {"default": "127.0.0.1", "type": str},
        # port to receive worker responses by the integration manager
        "IntegrationManagerPullerPort": {"default": 19033, "type": int},
        # address to receive worker responses by the integration manager
        "IntegrationManagerPullerAddress": {"default": "127.0.0.1", "type": str},
        # port from which to publish messages by the integration manager
        "IntegrationManagerPublisherPort": {"default": 19034, "type": int},
        # address from which to publish messages by the integration manager
        "IntegrationManagerPublisherAddress": {"default": "127.0.0.1", "type": str},
        "yaml_path": {"default": f"{PERSISTENCE_PATH}/FTSConfig.yaml", "type": str},
        "ip": {"default": _ip, "type": str},
        # radius of emergency within-which users will receive it
        "EmergencyRadius": {"default": 10, "type": int},
        # set the persistence path
        "persistencePath": {"default": PERSISTENCE_PATH, "type": str}
    }

    # This structure maps environmental vars to config vars
    _env_vars = {
        "FTS_SECRET_KEY": "SecretKey",
        "FTS_NODE_ID": "nodeID",
        "FTS_OPTIMIZE_API": "OptimizeAPI",
        "FTS_DATA_RECEPTION_BUFFER": "DataReceptionBuffer",
        "FTS_MAX_RECEPTION_TIME": "MaxReceptionTime",
        "FTS_MAINLOOP_DELAY": "MainLoopDelay",
        "FTS_COT_PORT": "CoTServicePort",
        "FTS_SSLCOT_PORT": "SSLCoTServicePort",
        "FTS_DP_ADDRESS": "DataPackageServiceDefaultIP",
        "FTS_USER_ADDRESS": "UserConnectionIP",
        "FTS_API_PORT": "APIPort",
        "FTS_CLI_WHITELIST": "AllowCLIIPs",
        "FTS_FED_PORT": "FederationPort",
        "FTS_API_ADDRESS": "APIIP",
        "FTS_COT_TO_DB": "SaveCoTToDB",
        "FTS_DB_PATH": "DBFilePath",
        "FTS_MAINPATH": "MainPath",
        "FTS_CERTS_PATH": "certsPath",
        "FTS_EXCHECK_PATH": "ExCheckMainPath",
        "FTS_EXCHECK_TEMPLATE_PATH": "ExCheckFilePath",
        "FTS_EXCHECK_CHECKLIST_PATH": "ExCheckChecklistFilePath",
        "FTS_DATAPACKAGE_PATH": "DataPackageFilePath",
        "FTS_LOGFILE_PATH": "LogFilePath",
        "FTS_FED_PASSWORD": "federationKeyPassword",
        "FTS_SERVER_KEYDIR": "keyDir",
        "FTS_SERVER_PEMDIR": "pemDir",
        "FTS_TESTCLIENT_PEMDIR": "testPem",
        "FTS_TESTCLIENT_KEYDIR": "testKey",
        "FTS_UNENCRYPTED_KEYDIR": "unencryptedKey",
        "FTS_SERVER_P12DIR": "p12Dir",
        "FTS_CADIR": "CA",
        "FTS_CAKEYDIR": "CAkey",
        "FTS_FEDERATION_CERTDIR": "federationCert",
        "FTS_FEDERATION_KEYDIR": "federationKey",
        "FTS_FEDERATION_KEYPASS": "federationKeyPassword",
        "FTS_CLIENT_CERT_PASSWORD": "password",
        "FTS_WEBSOCKET_KEY": "websocketkey",
        "FTS_CRLDIR": "CRLFile",
        "FTS_CONNECTION_MESSAGE": "ConnectionMessage",
        "FTS_DATABASE_TYPE": "DataBaseType",
        "FTS_CLIENT_PACKAGES_PATH": "ClientPackages",
        "FTS_NUM_ROUTING_WORKERS": "NumRoutingWorkers",
        "FTS_ROUTING_PROXY_SUBSCRIBE_PORT": "RoutingProxySubscriberPort",
        "FTS_ROUTING_PROXY_SUBSCRIBE_IP": "RoutingProxySubscriberIP",
        "FTS_ROUTING_PROXY_PUBLISHER_PORT": "RoutingProxyPublisherPort",
        "FTS_ROUTING_PROXY_PUBLISHER_IP": "RoutingProxyPublisherIP",
        "FTS_ROUTING_PROXY_SERVER_PORT": "RoutingProxyRequestServerPort",
        "FTS_ROUTING_PROXY_SERVER_IP": "RoutingProxyRequestServerIP",
        "FTS_CORE_COMPONENTS_PATH": "CoreComponentsPath",
        "FTS_CORE_COMPONENTS_IMPORT_ROOT": "CoreComponentsImportRoot",
        "FTS_INTERNAL_COMPONENTS_PATH": "InternalComponentsPath",
        "FTS_INTERNAL_COMPONENTS_IMPORT_ROOT": "InternalComponentsImportRoot",
        "FTS_EXTERNAL_COMPONENTS_PATH": "ExternalComponentsPath",
        "FTS_EXTERNAL_COMPONENTS_IMPORT_ROOT": "ExternalComponentsImportRoot",
        # port to receive worker responses by the integration manager
        "FTS_INTEGRATION_MANAGER_PULLER_PORT": "IntegrationManagerPullerPort",
        # address to receive worker responses by the integration manager
        "FTS_INTEGRATION_MANAGER_PULLER_ADDRESS": "IntegrationManagerPullerAddress",
        # port from which to publish messages by the integration manager
        "FTS_INTEGRATION_MANAGER_PUBLISHER_PORT": "IntegrationManagerPublisherPort",
        # address from which to publish messages by the integration manager
        "FTS_INTEGRATION_MANAGER_PUBLISHER_ADDRESS": "IntegrationManagerPublisherAddress",
        # radius of emergency within-which users will receive it
        "FTS_EMERGENCY_RADIUS": "EmergencyRadius",
        "FTS_PERSISTENCE_PATH": "persistencePath",
        "FTS_LOG_LEVEL": "LogLevel"
    }

    # This is a simple representation of the YAML config schema with
    # mappings to config var
    _yaml_keys = {
        "System": {
            "FTS_NODE_ID": "nodeID",
            "FTS_MAINLOOP_DELAY": "MainLoopDelay",
            "FTS_CONNECTION_MESSAGE": "ConnectionMessage",
            "FTS_DATABASE_TYPE": "DataBaseType",
            "FTS_OPTIMIZE_API": "OptimizeAPI",
            "FTS_SECRET_KEY": "SecretKey",
            "FTS_DATA_RECEPTION_BUFFER": "DataReceptionBuffer",
            "FTS_MAX_RECEPTION_TIME": "MaxReceptionTime",
            "FTS_EMERGENCY_RADIUS": "EmergencyRadius"
        },
        "Addresses": {
            "FTS_COT_PORT": "CoTServicePort",
            "FTS_SSLCOT_PORT": "SSLCoTServicePort",
            "FTS_DP_ADDRESS": "DataPackageServiceDefaultIP",
            "FTS_USER_ADDRESS": "UserConnectionIP",
            "FTS_API_PORT": "APIPort",
            "FTS_FED_PORT": "FederationPort",
            "FTS_API_ADDRESS": "APIIP",
            "FTS_CLI_WHITELIST": "AllowCLIIPs",
            # the number of routing workers to use
            "NumRoutingWorkers": {"default": 3, "type": int},
            # port to subscribe to requests by the routing proxy
            "RoutingProxySubscriberPort": {"default": 19030, "type": int},
            # port to publish responses by the routing proxy
            "RoutingProxyPublisherPort": {"default": 19032, "type": int},
            # port to send requests from the routing proxy to the routing workers
            "RoutingProxyRequestServerPort": {"default": 19031, "type": int},
            # ip to subscribe to requests by the routing proxy
            "RoutingProxySubscriberIP": {"default": "127.0.0.1", "type": str},
            # ip to publish responses by the routing proxy
            "RoutingProxyPublisherIP": {"default": "127.0.0.1", "type": str},
            # port to send requests from the routing proxy to the routing workers
            "RoutingProxyRequestServerIP": {"default": "127.0.0.1", "type": str},
            # port to receive worker responses by the integration manager
            "FTS_INTEGRATION_MANAGER_PULLER_PORT": "IntegrationManagerPullerPort",
            # address to receive worker responses by the integration manager
            "FTS_INTEGRATION_MANAGER_PULLER_ADDRESS": "IntegrationManagerPullerAddress",
            # port from which to publish messages by the integration manager
            "FTS_INTEGRATION_MANAGER_PUBLISHER_PORT": "IntegrationManagerPublisherPort",
            # address from which to publish messages by the integration manager
            "FTS_INTEGRATION_MANAGER_PUBLISHER_ADDRESS": "IntegrationManagerPublisherAddress",

        },
        "Filesystem": {
            "FTS_PERSISTENCE_PATH": "persistencePath",
            "FTS_COT_TO_DB": "SaveCoTToDB",
            "FTS_DB_PATH": "DBFilePath",
            "FTS_MAINPATH": "MainPath",
            "FTS_CERTS_PATH": "certsPath",
            "FTS_EXCHECK_PATH": "ExCheckMainPath",
            "FTS_EXCHECK_TEMPLATE_PATH": "ExCheckFilePath",
            "FTS_EXCHECK_CHECKLIST_PATH": "ExCheckChecklistFilePath",
            "FTS_DATAPACKAGE_PATH": "DataPackageFilePath",
            "FTS_LOGFILE_PATH": "LogFilePath",
            "FTS_CLIENT_PACKAGES_PATH": "ClientPackages",
            "FTS_CORE_COMPONENTS_PATH": "CoreComponentsPath",
            "FTS_CORE_COMPONENTS_IMPORT_ROOT": "CoreComponentsImportRoot",
            "FTS_INTERNAL_COMPONENTS_PATH": "InternalComponentsPath",
            "FTS_INTERNAL_COMPONENTS_IMPORT_ROOT": "InternalComponentsImportRoot",
            "FTS_EXTERNAL_COMPONENTS_PATH": "ExternalComponentsPath",
            "FTS_EXTERNAL_COMPONENTS_IMPORT_ROOT": "ExternalComponentsImportRoot",
            "FTS_LOG_LEVEL": "LogLevel"
        },
        "Certs": {
            "FTS_SERVER_KEYDIR": "keyDir",
            "FTS_SERVER_PEMDIR": "pemDir",
            "FTS_TESTCLIENT_PEMDIR": "testPem",
            "FTS_TESTCLIENT_KEYDIR": "testKey",
            "FTS_UNENCRYPTED_KEYDIR": "unencryptedKey",
            "FTS_SERVER_P12DIR": "p12Dir",
            "FTS_CADIR": "CA",
            "FTS_CAKEYDIR": "CAkey",
            "FTS_FEDERATION_CERTDIR": "federationCert",
            "FTS_FEDERATION_KEYDIR": "federationKey",
            "FTS_FEDERATION_KEYPASS": "federationKeyPassword",
            "FTS_CLIENT_CERT_PASSWORD": "password",
            "FTS_WEBSOCKET_KEY": "websocketkey",
            "FTS_CRLDIR": "CRLFile",
        },
    }

    def __init__(self):
        raise RuntimeError("Call instance() instead")

    # instance() is the normal entry point to get access to config information.
    #
    # Generally it is called without arguments in the rest of the FTS code
    # and the return value is a config object where the config vars can be
    # read or written using the attribute syntax (e.g. config.var for read and
    # config.var = value for write), the dictionary syntax (e.g. config['var']
    # for read and config['var'] = value for write) or the get() and set() methods.
    #
    # The only time that instance() is called with a parameter is the first
    # time it is accessed so that the YAML config file can be read in and
    # parsed. Further calls to instance() with the YAML configuration param
    # may reset values of current config vars to their start values.
    @classmethod
    def instance(cls, config_file=None):
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
            # Put any initialization here.

            # preload the defaults into the _values table

            for var_name, metadata in cls._defaults.items():
                cls._instance.set(var_name, value=metadata["default"], override_ro=True)

            # if config_file not specified, check env or use default location
            if config_file == None:
                config_file = str(os.environ.get('FTS_CONFIG_PATH', MainConfig._defaults["yaml_path"]))

            # overlay the yaml config if found
            if os.path.exists(config_file):
                cls._instance.read_yaml_config(config_file)

            # finally overlay any configuration specified in the env
            cls._instance.import_env_config()

        return cls._instance

    # reset() is really only used for testing so that MainConfig can
    # be reinitialized between tests. It normally should not be used
    # by anything else.
    @classmethod
    def reset(cls):
        # here we need to reinitialze all the private vars
        cls._instance = None
        cls._values = {}
        cls._node_id = str(uuid4())

    def set(self, name, value=None, override_ro=False):
        # add the value to the values table using the correct type
        if not self._readonly(name) or override_ro:
            self._values[name] = self._var_type(name)(value)

    def get(self, name):
        if name in self._values:
            return self._values[name]
        else:
            raise RuntimeError(f'MainConfig unknown setting name: {name}')

    # read_yaml_config() will parse a YAML config and apply to the current
    # config vars. This should only be called from instance() and only
    # at the startup of the FTS server.
    def read_yaml_config(self, yaml_path):
        try:
            content = open(yaml_path).read()
            yamlConfig = yaml.safe_load(content)
        except OSError as e:
            raise e

        # walk through the _yaml_keys struct looking for values in yamlConfig
        for sect in MainConfig._yaml_keys:
            if sect in yamlConfig:
                for attr, var_name in MainConfig._yaml_keys[sect].items():
                    if yamlConfig[sect] is not None and attr in yamlConfig[sect]:
                        value = yamlConfig[sect][attr]
                        if attr.endswith(('PATH', 'DIR')):
                            value = self.validate_and_sanitize_path(value)
                        # found a setting we can update the config
                        self.set(var_name, value=value)

    def validate_and_sanitize_path(self, path):
        # sanitize and validate any path specified in config
        sanitized_path = ROOTPATH + os.path.relpath(os.path.normpath(os.path.join(os.sep, path)), os.sep)

        if not os.access(sanitized_path, os.F_OK) or not os.access(sanitized_path, os.W_OK):
            raise ValueError

        return sanitized_path

    # import_env_config() will inspect the current environment and detect
    # configuration values. Detected values will then be applied to the
    # current config vars. This should only be called from instance() and
    # only at the startup of the FTS server.
    def import_env_config(self):
        # Walk through all the registered env vars and check to see if the
        # env var is defined in the environment
        for env_var, config_var in self._env_vars.items():
            if env_var in os.environ:
                env_value = os.environ[env_var]

                # Handle boolean types
                if self._var_type(config_var) == bool:
                    # bools are actually specified as a string
                    if env_value.upper() in ('1', 'TRUE', 'YES', 'Y'):
                        env_value = True
                    else:
                        env_value = False
                # Handle lists and split the value apart
                elif self._var_type(config_var) == list:
                    env_value = re.split(r':|,', env_value)

                self[config_var] = env_value

    # dump_values() is used for debugging and inspecting the current
    # settings of config vars
    def dump_values(self):
        for var_name, value in self._values.items():
            print(f'{var_name} = {value}')

    # test if the config var should allow being set
    def _readonly(self, name):
        if (
            "readonly" in MainConfig._defaults[name]
            and MainConfig._defaults[name]["readonly"]
        ):
            return True
        return False

    # helper function to return the type of a config var
    def _var_type(self, name):
        return MainConfig._defaults[name]['type']

    # Attribute access magic methods
    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self.set(name, value)

    # Dictionary access magic methods
    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set(name, value)

    first_start = os.environ.get("FTS_FIRST_START", "true").lower() in ('true', 't', '1', 'yes', 'y') and not  os.path.exists(os.path.dirname(os.path.realpath(__file__))+os.sep+"installation.json")
