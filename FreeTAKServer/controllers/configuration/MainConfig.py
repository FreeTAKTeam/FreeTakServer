import os
import yaml
currentPath = os.path.dirname(os.path.abspath(__file__))
from pathlib import Path

class MainConfig:
    """
    this is the main configuration file and is the only one which
    should need to be changed
    """

    _instance = None
    _values = {}

    # the version information of the server (recommended to leave as default)
    version = 'FreeTAKServer-1.9.9.6 Public'
    #

    python_version = 'python3.8'

    userpath = '/usr/local/lib/'

    # allowed ip's to access CLI commands
    AllowedCLIIPs = ['127.0.0.1']

    # IP for CLI to access
    CLIIP = '127.0.0.1'

    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
    except:
        ip = "0.0.0.0"

    # format of API message header should be {Authentication: Bearer 'TOKEN'}
    from uuid import uuid4
    id = str(uuid4())

    nodeID = os.environ.get('FTS_NODE_ID', f"FreeTAKServer-{id}")

    MainPath = '/tmp'
    certsPath = '/tmp/certs'

    # We do not specify a type for values that should not ever be updated at runtime
    _defaults = {
        'APIVersion': {'default': '1.9.5', 'type': str, 'readonly': True},
        'SecretKey': {'default': 'vnkdjnfjknfl1232#', 'type': str},
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
        'DataPackageServiceDefaultIP': {'default': ip, 'type': str},
        # User Connection package IP needs to be set to the IP which is used when creating the connection in your tak device
        'UserConnectionIP': {'default': ip, 'type': str},
        # api port
        'APIPort': {'default': 19023, 'type': int},
        # Federation port
        'FederationPort': {'default': 9000, 'type': int},
        # api IP
        'APIIP': {'default': '0.0.0.0', 'type': str},
        # whether or not to save CoT's to the DB
        'SaveCoTToDB': {'default': True, 'type': bool},
        # this should be set before startup
        'DBFilePath': {'default': r'/opt/FTSDataBase.db', 'type': str},
        'MainPath': {'default': Path(fr'{userpath}{python_version}/dist-packages/FreeTAKServer'), 'type': str},
        'certsPath': {'default': Path(fr'{MainPath}/certs'), 'type': str},
        'ExCheckMainPath': {'default': Path(fr'{MainPath}/ExCheck'), 'type': str},
        'ExCheckFilePath': {'default': Path(fr'{MainPath}/ExCheck/template'), 'type': str},
        'ExCheckChecklistFilePath': {'default': Path(fr'{MainPath}/ExCheck/checklist'), 'type': str},
        'DataPackageFilePath': {'default': Path(fr'{MainPath}/FreeTAKServerDataPackageFolder'), 'type': str},
        'LogFilePath': {'default': Path(fr"{MainPath}/Logs"), 'type': str},
        'federationKeyPassword': {'default': 'defaultpass', 'type': str},
        'keyDir': {'default': Path(fr'{certsPath}/server.key'), 'type': str},
        'pemDir': {'default': Path(fr'{certsPath}/server.pem'), 'type': str},
        'testPem': {'default': Path(fr'{certsPath}/server.key'), 'type': str},
        'testKey': {'default': Path(fr'{certsPath}/server.pem'), 'type': str},
        'unencryptedKey': {'default': Path(fr'{certsPath}/server.key.unencrypted'), 'type': str},
        'p12Dir': {'default': Path(fr'{certsPath}/server.p12'), 'type': str},
        'CA': {'default': Path(fr'{certsPath}/ca.pem'), 'type': str},
        'CAkey': {'default': Path(fr'{certsPath}/ca.key'), 'type': str},
        'federationCert': {'default': Path(fr'{certsPath}/server.pem'), 'type': str},
        'federationKey': {'default': Path(fr'{certsPath}/server.key'), 'type': str},
        'federationKeyPassword': {'default': 'defaultpass', 'type': str},
        'password': {'default': 'supersecret', 'type': str},
        'websocketkey': {'default': "YourWebsocketKey", 'type': str},
        'CRLFile': {'default': Path(fr"{certsPath}/FTS_CRL.json"), 'type': str},
        # set to None if you don't want a message sent
        'ConnectionMessage': {'default': f'Welcome to FreeTAKServer {version}. The Parrot is not dead. It’s just resting', 'type': str},
        'DataBaseType': {'default': "SQLite", 'type': str},
        # location to backup client packages
        'clientPackages': {'default': Path(fr'{MainPath}/certs/clientPackages'), 'type': str},
    }

    _env_vars = {
        'FTS_SECRET_KEY': 'SecretKey',
        'FTS_OPTIMIZE_API': 'OptimizeAPI',
        'FTS_DATA_RECEPTION_BUFFER': 'DataReceptionBuffer',
        'FTS_MAX_RECEPTION_TIME': 'MaxReceptionTime',
        'FTS_MAINLOOP_DELAY': 'MainLoopDelay',
        'FTS_COT_PORT': 'CoTServicePort',
        'FTS_SSLCOT_PORT': 'SSLCoTServicePort',
        'FTS_DP_ADDRESS': 'DataPackageServiceDefaultIP',
        'FTS_USER_ADDRESS': 'UserConnectionIP',
        'FTS_API_PORT': 'APIPort',
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

    _yaml_keys = {
        'System': {
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

    def set(self, name, value=None, override_ro=False):
        # add the value to the values table using the correct type
        if not self._readonly(name) or override_ro:
            self._values[name] = self._var_type(name)(value)

    def get(self, name):
        if name in self._values:
            return self._values[name]
        else:
            raise RuntimeError(f'MainConfig unknown setting name: {name}')

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

    def import_env_config(self):
        for env_var, config_var in self._env_vars.items():
            if env_var in os.environ:
                value = os.environ[env_var]
                if self._var_type(config_var) == bool:
                    # bools are actually specified as a string
                    if value.upper() in ('1', 'TRUE', 'YES', 'Y'):
                        value = True
                    else:
                        value = False
                self[config_var] = value

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

    def __getattr__(self, name):
        return self.get(name)

    def __setattr__(self, name, value):
        self.set(name, value)

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, value):
        self.set(name, value)

    first_start = True
