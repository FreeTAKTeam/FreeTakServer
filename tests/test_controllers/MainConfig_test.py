import unittest
import pytest
import os

from FreeTAKServer.controllers.configuration.MainConfig import MainConfig
from pathlib import PosixPath, WindowsPath
from unittest import mock

class Test_MainConfig(unittest.TestCase):

    # Need to re-initialize the singleton after each test
    def teardown_method(self, func):
        MainConfig._instance = None

    def test_default_values(self):
        config = MainConfig.instance()

        for conf_var, metadata in config._defaults.items():
            if type(metadata['default']) in (PosixPath, WindowsPath):
                assert(config.get(conf_var) == str(metadata['default']))
            else:
                assert(config.get(conf_var) == metadata['default'])


    # we test only a couple of vars with env override assuming rest are OK
    @mock.patch.dict(os.environ, {'FTS_DATA_RECEPTION_BUFFER': '512'}) # int test
    @mock.patch.dict(os.environ, {'FTS_OPTIMIZE_API': '0'})            # bool test
    @mock.patch.dict(os.environ, {'FTS_SECRET_KEY': 'abc123'})         # str test
    def test_env_var_values(self):
        config = MainConfig.instance()

        assert(config.DataReceptionBuffer == 512)
        #assert(config.OptimizeAPI == False)
        assert(config.SecretKey == 'abc123')