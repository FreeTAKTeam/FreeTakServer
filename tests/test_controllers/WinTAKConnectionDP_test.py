import unittest
import pytest
import os
import zipfile

from pathlib import PosixPath
from unittest import mock
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.util.certificate_generation import generate_wintak_zip

def test_generate_wintak_zip(tmpdir):
    # Set up test data and temporary directory
    server_filename = "server.p12"
    user_filename = "Client.p12"
    cert_password = "5Tr0ngP@ssw0rd!"
    ssl_port = "8089"
    server_address = "192.168.205.117"
    tmpdir_path = str(tmpdir)


    # Call MainConfig class instance method to initialize and populate the _values dictionary
    MainConfig.instance()

    # Mock the necessary functions for file operations
    with mock.patch("builtins.open", mock.mock_open()) as mock_open, \
        mock.patch("zipfile.ZipFile", spec=zipfile.ZipFile) as mock_zipfile, \
        mock.patch("os.remove") as mock_remove, \
        mock.patch("os.path.exists") as mock_path_exists, \
        mock.patch("shutil.rmtree") as mock_rmtree:
    
        # Call the function under test
        generate_wintak_zip(server_address=server_address, server_filename=server_filename,
                            user_filename=user_filename, cert_password=cert_password, ssl_port=ssl_port)

        # Mock the os.remove function to handle FileNotFoundError
        def remove_side_effect(*args, **kwargs):
            try:
                os.remove(*args, **kwargs)
            except FileNotFoundError:
                pass  # Handle the FileNotFoundError silently
    
        mock_remove.side_effect = remove_side_effect

        mock_path_exists.side_effect = lambda path: path.endswith(("fts.pref", "Client.zip", "MANIFEST"))

        # Mock the shutil.rmtree function to simulate the removal of the MANIFEST directory
        mock_rmtree.side_effect = lambda path, ignore_errors=False, onerror=None, dir_fd=None: None

        assert mock_open.called
        assert mock_open.call_args_list == [
            mock.call('./5c2bfcae3d98c9f4d262172df99ebac5/fts.pref', 'w'),
            mock.call('./MANIFEST/manifest.xml', 'w'),
            mock.call('/opt/fts/certs/server.p12', 'rb'),
            mock.call('./5c2bfcae3d98c9f4d262172df99ebac5/server.p12', 'wb'),
            mock.call(PosixPath('/opt/fts/certs/Client.p12'), 'rb'),
            mock.call(PosixPath('5c2bfcae3d98c9f4d262172df99ebac5/Client.p12'), 'wb'),
            mock.call('./MANIFEST/manifest.xml', 'w'),
            mock.call('Client.zip', 'rb'),
            mock.call(PosixPath('80b828699e074a239066d454a76284eb/Client.zip'), 'wb')
        ]
        assert mock_open.return_value.write.called

        assert mock_zipfile.called
        assert mock_zipfile.call_args_list == [
            mock.call('Client.zip', 'w', zipfile.ZIP_DEFLATED),
            mock.call('/opt/fts/certs/clientPackages/Client.zip', 'w', 8)
            ]
        assert mock_zipfile.return_value.write.called

        # Assert that the expected file operations were performed
        mock_copyfile.assert_called_with(server_filename, os.path.join(tmpdir_path, server_filename))
        mock_copyfile.assert_called_with(os.path.join("cert", user_filename),
                                         os.path.join(tmpdir_path, user_filename))

        # Assert that the ZIP file was created with the expected contents
        zip_file_path = os.path.join(tmpdir_path, f"{user_filename[:-4]}.zip")
        assert os.path.exists(zip_file_path)
        with zipfile.ZipFile(zip_file_path) as zipf:
            assert "5c2bfcae3d98c9f4d262172df99ebac5/fts.pref" in zipf.namelist()
            assert "5c2bfcae3d98c9f4d262172df99ebac5/server.p12" in zipf.namelist()
            assert "5c2bfcae3d98c9f4d262172df99ebac5/Client.p12" in zipf.namelist()
            assert "MANIFEST/manifest.xml" in zipf.namelist()
            assert f"80b828699e074a239066d454a76284eb/{user_filename[:-4]}.zip" in zipf.namelist()