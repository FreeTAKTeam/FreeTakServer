import os
import re
import yaml
currentPath = os.path.dirname(os.path.abspath(__file__))
from os.path import expanduser
from pathlib import Path
from string import ascii_letters, digits, punctuation
from uuid import uuid4

# the version information of the server (recommended to leave as default)
FTS_VERSION = 'FreeTAKServer-1.9.9.7 Public'
API_VERSION = '1.9.5'
# TODO Need to find a better way to determine python version at runtime
PYTHON_VERSION = 'python3.8'
USERPATH = '/usr/local/lib/'
MAINPATH = Path(expanduser("~"), '.fts')

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

    _node_id = str(uuid4())

    # All available config vars should be defined here
    #   currently only 'default', 'type' and 'readonly' are recognized
    _defaults = {
        'version': {'default': FTS_VERSION, 'type': str, 'readonly': True},
        'APIVersion': {'default': API_VERSION, 'type': str, 'readonly': True},
        'SecretKey': {'default': 'vnkdjnfjknfl1232#', 'type': str},
        'nodeID': {'default': f'FreeTAKServer-{_node_id}', 'type': str},
        'OptimizeAPI': {'default': True, 'type': bool},
        'DataReceptionBuffer': {'default': 1024, 'type': int},
        'MaxReceptionTime': {'default': 4, 'type': int},
        # number of milliseconds to wait between each iteration of main loop
        # decreasing will increase CPU usage and server performance
        # increasing will decrease CPU usage and server performance
        'MainLoopDelay': {'default': 100, 'type': int},
        # this is the port to which clients will connect
        'CoTServicePort': {'default': 8087, 'type': int},
        'SSLCoTServicePort': {'default': 8089, 'type': int},
        # this needs to be changed for private data packages to work
        'DataPackageServiceDefaultIP': {'default': _ip, 'type': str},
        # User Connection package IP needs to be set to the IP which is 
        # used when creating the connection in your tak device
        'UserConnectionIP': {'default': _ip, 'type': str},
        # api port
        'APIPort': {'default': 19023, 'type': int},
        # Federation port
        'FederationPort': {'default': 9000, 'type': int},
        # api IP
        'APIIP': {'default': '0.0.0.0', 'type': str},
        # IP for CLI to access
        'CLIIP': {'default': '127.0.0.1', 'type': str},
        'AllowCLIIPs': {'default': ['127.0.0.1'], 'type': list},
        # whether or not to save CoT's to the DB
        'SaveCoTToDB': {'default': True, 'type': bool},
        # this should be set before startup
        'DBFilePath': {'default': r'/opt/FTSDataBase.db', 'type': str},
        'MainPath': {'default': Path(MAINPATH), 'type': str},
        'certsPath': {'default': Path(fr'{MAINPATH}/certs'), 'type': str},
        'ExCheckMainPath': {'default': Path(fr'{MAINPATH}/ExCheck'), 'type': str},
        'ExCheckFilePath': {'default': Path(fr'{MAINPATH}/ExCheck/template'), 'type': str},
        'ExCheckChecklistFilePath': {'default': Path(fr'{MAINPATH}/ExCheck/checklist'), 'type': str},
        'DataPackageFilePath': {'default': Path(fr'{MAINPATH}/FreeTAKServerDataPackageFolder'), 'type': str},
        'LogFilePath': {'default': Path(fr"{MAINPATH}/Logs"), 'type': str},
        'federationKeyPassword': {'default': 'defaultpass', 'type': str},
        'keyDir': {'default': Path(fr'{MAINPATH}/certs/server.key'), 'type': str},
        'pemDir': {'default': Path(fr'{MAINPATH}/certs/server.pem'), 'type': str},
        'testPem': {'default': Path(fr'{MAINPATH}/certs/server.key'), 'type': str},
        'testKey': {'default': Path(fr'{MAINPATH}/certs/server.pem'), 'type': str},
        'unencryptedKey': {'default': Path(fr'{MAINPATH}/certs/server.key.unencrypted'), 'type': str},
        'p12Dir': {'default': Path(fr'{MAINPATH}/certs/server.p12'), 'type': str},
        'CA': {'default': Path(fr'{MAINPATH}/certs/ca.pem'), 'type': str},
        'CAkey': {'default': Path(fr'{MAINPATH}/certs/ca.key'), 'type': str},
        'federationCert': {'default': Path(fr'{MAINPATH}/certs/server.pem'), 'type': str},
        'federationKey': {'default': Path(fr'{MAINPATH}/certs/server.key'), 'type': str},
        'federationKeyPassword': {'default': 'defaultpass', 'type': str},
        'password': {'default': 'supersecret', 'type': str},
        'websocketkey': {'default': "YourWebsocketKey", 'type': str},
        'CRLFile': {'default': Path(fr"{MAINPATH}/certs/FTS_CRL.json"), 'type': str},
        # set to None if you don't want a message sent
        'ConnectionMessage': {'default': f'Welcome to FreeTAKServer {FTS_VERSION}. The Parrot is not dead. It’s just resting', 'type': str},
        'DataBaseType': {'default': "SQLite", 'type': str},
        # location to backup client packages
        'clientPackages': {'default': Path(fr'{MAINPATH}/certs/clientPackages'), 'type': str},
    }

    # This structure maps environmental vars to config vars
    _env_vars = {
        'FTS_SECRET_KEY': 'SecretKey',
        'FTS_NODE_ID': 'nodeID',
        'FTS_OPTIMIZE_API': 'OptimizeAPI',
        'FTS_DATA_RECEPTION_BUFFER': 'DataReceptionBuffer',
        'FTS_MAX_RECEPTION_TIME': 'MaxReceptionTime',
        'FTS_MAINLOOP_DELAY': 'MainLoopDelay',
        'FTS_COT_PORT': 'CoTServicePort',
        'FTS_SSLCOT_PORT': 'SSLCoTServicePort',
        'FTS_DP_ADDRESS': 'DataPackageServiceDefaultIP',
        'FTS_USER_ADDRESS': 'UserConnectionIP',
        'FTS_API_PORT': 'APIPort',
        'FTS_CLI_WHITELIST': 'AllowCLIIPs',
        'FTS_FED_PORT': 'FederationPort',
        'FTS_API_ADDRESS': 'APIIP',
        'FTS_COT_TO_DB': 'SaveCoTToDB',
        'FTS_DB_PATH': 'DBFilePath',
        'FTS_MAINPATH': 'MainPath',
        'FTS_CERTS_PATH': 'certsPath',
        'FTS_EXCHECK_PATH': 'ExCheckMainPath',
        'FTS_EXCHECK_TEMPLATE_PATH': 'ExCheckFilePath',
        'FTS_EXCHECK_CHECKLIST_PATH': 'ExCheckChecklistFilePath',
        'FTS_DATAPACKAGE_PATH': 'DataPackageFilePath',
        'FTS_LOGFILE_PATH': 'LogFilePath',
        'FTS_FED_PASSWORD': 'federationKeyPassword',
        'FTS_SERVER_KEYDIR': 'keyDir',
        'FTS_SERVER_PEMDIR': 'pemDir',
        'FTS_TESTCLIENT_PEMDIR': 'testPem',
        'FTS_TESTCLIENT_KEYDIR': 'testKey',
        'FTS_UNENCRYPTED_KEYDIR': 'unencryptedKey',
        'FTS_SERVER_P12DIR': 'p12Dir',
        'FTS_CADIR': 'CA',
        'FTS_CAKEYDIR': 'CAkey',
        'FTS_FEDERATION_CERTDIR': 'federationCert',
        'FTS_FEDERATION_KEYDIR': 'federationKey',
        'FTS_FEDERATION_KEYPASS': 'federationKeyPassword',
        'FTS_CLIENT_CERT_PASSWORD': 'password',
        'FTS_WEBSOCKET_KEY': 'websocketkey',
        'FTS_CRLDIR': 'CRLFile',
        'FTS_CONNECTION_MESSAGE': 'ConnectionMessage',
        'FTS_DATABASE_TYPE': 'DataBaseType',
        'FTS_CLIENT_PACKAGES': 'clientPackages',
    }

    # This is a simple representation of the YAML config schema with
    # mappings to config var
    _yaml_keys = {
        'System': {
            'FTS_NODE_ID': 'nodeID',
            'FTS_MAINLOOP_DELAY': 'MainLoopDelay',
            'FTS_CONNECTION_MESSAGE': 'ConnectionMessage',
            'FTS_DATABASE_TYPE': 'DataBaseType',
            'FTS_OPTIMIZE_API': 'OptimizeAPI',
            'FTS_SECRET_KEY': 'SecretKey',
            'FTS_DATA_RECEPTION_BUFFER': 'DataReceptionBuffer',
            'FTS_MAX_RECEPTION_TIME': 'MaxReceptionTime',
        },
        'Addresses': {
            'FTS_COT_PORT': 'CoTServicePort',
            'FTS_SSLCOT_PORT': 'SSLCoTServicePort',
            'FTS_DP_ADDRESS': 'DataPackageServiceDefaultIP',
            'FTS_USER_ADDRESS': 'UserConnectionIP',
            'FTS_API_PORT': 'APIPort',
            'FTS_FED_PORT': 'FederationPort',
            'FTS_API_ADDRESS': 'APIIP',
            'FTS_CLI_WHITELIST': 'AllowCLIIPs',
        },
        'Filesystem': {
            'FTS_COT_TO_DB': 'SaveCoTToDB',
            'FTS_DB_PATH': 'DBFilePath',
            'FTS_MAINPATH': 'MainPath',
            'FTS_CERTS_PATH': 'certsPath',
            'FTS_EXCHECK_PATH': 'ExCheckMainPath',
            'FTS_EXCHECK_TEMPLATE_PATH': 'ExCheckFilePath',
            'FTS_EXCHECK_CHECKLIST_PATH': 'ExCheckChecklistFilePath',
            'FTS_DATAPACKAGE_PATH': 'DataPackageFilePath',
            'FTS_LOGFILE_PATH': 'LogFilePath',
            'FTS_CLIENT_PACKAGES': 'clientPackages',
        },
        'Certs': {
            'FTS_SERVER_KEYDIR': 'keyDir',
            'FTS_SERVER_PEMDIR': 'pemDir',
            'FTS_TESTCLIENT_PEMDIR': 'testPem',
            'FTS_TESTCLIENT_KEYDIR': 'testKey',
            'FTS_UNENCRYPTED_KEYDIR': 'unencryptedKey',
            'FTS_SERVER_P12DIR': 'p12Dir',
            'FTS_CADIR': 'CA',
            'FTS_CAKEYDIR': 'CAkey',
            'FTS_FEDERATION_CERTDIR': 'federationCert',
            'FTS_FEDERATION_KEYDIR': 'federationKey',
            'FTS_FEDERATION_KEYPASS': 'federationKeyPassword',
            'FTS_CLIENT_CERT_PASSWORD': 'password',
            'FTS_WEBSOCKET_KEY': 'websocketkey',
            'FTS_CRLDIR': 'CRLFile',
        }
    }

    def __init__(self):
        raise RuntimeError('Call instance() instead')

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
                cls._instance.set(var_name, value=metadata['default'],
                                  override_ro=True)

            # if config_file not specified, check env or use default location
            if config_file == None:
                config_file = str(os.environ.get('FTS_CONFIG_PATH', '/opt/FTSConfig.yaml'))

            # overlay the yaml config if found
            if  os.path.exists(config_file):
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
                    if attr in yamlConfig[sect]:
                        # found a setting we can update the config
                        self.set(var_name, value=yamlConfig[sect][attr])

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
        if 'readonly' in MainConfig._defaults[name] and MainConfig._defaults[name]['readonly']:
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

    first_start = True
