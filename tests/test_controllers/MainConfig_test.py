import unittest
import pytest
import os
import yaml

from FreeTAKServer.controllers.configuration.MainConfig import MainConfig, USERPATH, PYTHON_VERSION
from pathlib import PosixPath, WindowsPath
from unittest import mock

class Test_MainConfig(unittest.TestCase):

    # Need to re-initialize the singleton after each test
    def teardown_method(self, func):
        MainConfig.reset()

    def test_default_values(self):
        config = MainConfig.instance()

        for conf_var, metadata in config._defaults.items():
            if type(metadata['default']) in (PosixPath, WindowsPath):
                assert(config.get(conf_var) == str(metadata['default']))
            else:
                assert(config.get(conf_var) == metadata['default'])

    # we test only a couple of vars with env override assuming rest are OK
    @mock.patch.dict(os.environ, {'FTS_DATA_RECEPTION_BUFFER': '512'}) # int test
    def test_env_var_int_values(self):
        config = MainConfig.instance()
        assert(config.DataReceptionBuffer == 512)

    @mock.patch.dict(os.environ, {'FTS_OPTIMIZE_API': '0'})            # bool test
    def test_env_var_bool_values(self):
        config = MainConfig.instance()
        assert(config.OptimizeAPI == False)

    @mock.patch.dict(os.environ, {'FTS_SECRET_KEY': 'abc123'})         # str test
    def test_env_var_string_values(self):
        config = MainConfig.instance()
        assert(config.SecretKey == 'abc123')

    @mock.patch.dict(os.environ, {'FTS_CLI_WHITELIST': '127.0.0.1:10.10.10.10'})
    def test_env_var_list_values_with_colon(self):
        config = MainConfig.instance()
        assert all([a == b for a, b in zip(config.AllowCLIIPs, ['127.0.0.1', '10.10.10.10'])])

    @mock.patch.dict(os.environ, {'FTS_CLI_WHITELIST': '127.0.0.1,10.0.0.10'})
    def test_env_var_list_values_with_comma(self):
        config = MainConfig.instance()
        assert all([a == b for a, b in zip(config.AllowCLIIPs, ['127.0.0.1', '10.0.0.10'])])


    yaml_config = """
System:
    FTS_MAINLOOP_DELAY: 100
    FTS_CONNECTION_MESSAGE: ''
    FTS_DATABASE_TYPE: 'CouchDB'
    FTS_OPTIMIZE_API: false
    FTS_SECRET_KEY: 'SecretSquirel'
    FTS_DATA_RECEPTION_BUFFER: 256
    FTS_MAX_RECEPTION_TIME: 20
Addresses:
    FTS_COT_PORT: 2000
    FTS_SSLCOT_PORT: 2001
    FTS_DP_ADDRESS: '10.0.0.10'
    FTS_USER_ADDRESS: 'parrot.example.com'
    FTS_API_PORT: 2003
    FTS_FED_PORT: 2004
    FTS_API_ADDRESS: '192.168.10.20'
Filesystem:
    FTS_COT_TO_DB: false
    FTS_DB_PATH: '/db/store'
    FTS_MAINPATH: '/fts'
    FTS_CERTS_PATH: '/fts/certs'
    FTS_EXCHECK_PATH: '/fts/excheck'
    FTS_EXCHECK_TEMPLATE_PATH: '/fts/template'
    FTS_EXCHECK_CHECKLIST_PATH: '/fts/checklist'
    FTS_DATAPACKAGE_PATH: '/fts/package/data'
    FTS_LOGFILE_PATH: '/fts/logs'
    FTS_CLIENT_PACKAGES: '/fts/package/client'
Certs:
    FTS_SERVER_KEYDIR: '/fts/certs/private'
    FTS_SERVER_PEMDIR: '/fts/certs/public'
    FTS_TESTCLIENT_PEMDIR: '/fts/test/public'
    FTS_TESTCLIENT_KEYDIR: '/fts/test/private'
    FTS_UNENCRYPTED_KEYDIR: '/fts/certs/txt'
    FTS_SERVER_P12DIR: '/fts/certs/p12'
    FTS_CADIR: '/fts/certs/ca'
    FTS_CAKEYDIR: '/fts/certs/private'
    FTS_FEDERATION_CERTDIR: '/fts/certs/public'
    FTS_FEDERATION_KEYDIR: '/fts/certs/private'
    FTS_FEDERATION_KEYPASS: 'ringo-ranger'
    FTS_FED_PASSWORD: 'SuperMouse'
    FTS_CLIENT_CERT_PASSWORD: 'BooBoo'
    FTS_WEBSOCKET_KEY: 'flat_bread'
    FTS_CRLDIR: '/fts/certs/crl'
"""

    @mock.patch('builtins.open',
                create=True,
                new=mock.mock_open(read_data=yaml_config))
    def test_yaml_config(self):
        config = MainConfig.instance(config_file='/dev/null')

        expected = yaml.load(Test_MainConfig.yaml_config, Loader=yaml.SafeLoader)
        # Process each attribute of each YAML section
        for sect in MainConfig._yaml_keys:
            for var in MainConfig._yaml_keys[sect]:
                if var in expected[sect]:
                    assert(config.get(MainConfig._yaml_keys[sect][var]) == expected[sect][var])


    @mock.patch('builtins.open',
                create=True,
                new=mock.mock_open(read_data=yaml_config))
    @mock.patch.dict(os.environ, {'FTS_SSLCOT_PORT': '10000'}) # int test
    @mock.patch.dict(os.environ, {'FTS_COT_TO_DB': '1'})            # bool test
    @mock.patch.dict(os.environ, {'FTS_MAINPATH': '/tmp/fts'})         # str test
    def test_yaml_config_with_env_override(self):
        config = MainConfig.instance(config_file='/dev/null')

        assert(config.SSLCoTServicePort== 10000)
        assert(config.SaveCoTToDB == True)
        assert(config.MainPath == '/tmp/fts')

    def test_get_config_as_attribute(self):
        config = MainConfig.instance()
        assert(config.MainPath == fr'{USERPATH}{PYTHON_VERSION}/dist-packages/FreeTAKServer')
        assert(config.SaveCoTToDB == True)
        assert(config.FederationPort == 9000)

    def test_set_config_as_attribute(self):
        config = MainConfig.instance()
        config.OptimizeAPI = False
        assert(config.get('OptimizeAPI') == False)
        config.APIPort = 8088
        assert(config.get('APIPort') == 8088)
        config.LogFilePath = '/tmp/logs'
        assert(config.get('LogFilePath') == '/tmp/logs')

    def test_get_config_as_dictionary(self):
        config = MainConfig.instance()
        assert(config['MainPath'] == fr'{USERPATH}{PYTHON_VERSION}/dist-packages/FreeTAKServer')
        assert(config['SaveCoTToDB'] == True)
        assert(config['FederationPort'] == 9000)

    def test_set_config_as_dictionary(self):
        config = MainConfig.instance()
        config['OptimizeAPI'] = False
        assert(config.get('OptimizeAPI') == False)
        config['APIPort'] = 8088
        assert(config.get('APIPort') == 8088)
        config['LogFilePath'] = '/tmp/logs'
        assert(config.get('LogFilePath') == '/tmp/logs')