# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class MessagingConfigInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, latest_sa: bool=None, num_db_connections: int=None, num_auto_db_connections: int=None, connection_pool_auto_size: bool=None, archive: bool=None, db_username: str=None, db_password: str=None, db_url: str=None):  # noqa: E501
        """MessagingConfigInfo - a model defined in Swagger

        :param latest_sa: The latest_sa of this MessagingConfigInfo.  # noqa: E501
        :type latest_sa: bool
        :param num_db_connections: The num_db_connections of this MessagingConfigInfo.  # noqa: E501
        :type num_db_connections: int
        :param num_auto_db_connections: The num_auto_db_connections of this MessagingConfigInfo.  # noqa: E501
        :type num_auto_db_connections: int
        :param connection_pool_auto_size: The connection_pool_auto_size of this MessagingConfigInfo.  # noqa: E501
        :type connection_pool_auto_size: bool
        :param archive: The archive of this MessagingConfigInfo.  # noqa: E501
        :type archive: bool
        :param db_username: The db_username of this MessagingConfigInfo.  # noqa: E501
        :type db_username: str
        :param db_password: The db_password of this MessagingConfigInfo.  # noqa: E501
        :type db_password: str
        :param db_url: The db_url of this MessagingConfigInfo.  # noqa: E501
        :type db_url: str
        """
        self.swagger_types = {
            'latest_sa': bool,
            'num_db_connections': int,
            'num_auto_db_connections': int,
            'connection_pool_auto_size': bool,
            'archive': bool,
            'db_username': str,
            'db_password': str,
            'db_url': str
        }

        self.attribute_map = {
            'latest_sa': 'latestSA',
            'num_db_connections': 'numDbConnections',
            'num_auto_db_connections': 'numAutoDbConnections',
            'connection_pool_auto_size': 'connectionPoolAutoSize',
            'archive': 'archive',
            'db_username': 'dbUsername',
            'db_password': 'dbPassword',
            'db_url': 'dbUrl'
        }
        self._latest_sa = latest_sa
        self._num_db_connections = num_db_connections
        self._num_auto_db_connections = num_auto_db_connections
        self._connection_pool_auto_size = connection_pool_auto_size
        self._archive = archive
        self._db_username = db_username
        self._db_password = db_password
        self._db_url = db_url

    @classmethod
    def from_dict(cls, dikt) -> 'MessagingConfigInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MessagingConfigInfo of this MessagingConfigInfo.  # noqa: E501
        :rtype: MessagingConfigInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def latest_sa(self) -> bool:
        """Gets the latest_sa of this MessagingConfigInfo.


        :return: The latest_sa of this MessagingConfigInfo.
        :rtype: bool
        """
        return self._latest_sa

    @latest_sa.setter
    def latest_sa(self, latest_sa: bool):
        """Sets the latest_sa of this MessagingConfigInfo.


        :param latest_sa: The latest_sa of this MessagingConfigInfo.
        :type latest_sa: bool
        """

        self._latest_sa = latest_sa

    @property
    def num_db_connections(self) -> int:
        """Gets the num_db_connections of this MessagingConfigInfo.


        :return: The num_db_connections of this MessagingConfigInfo.
        :rtype: int
        """
        return self._num_db_connections

    @num_db_connections.setter
    def num_db_connections(self, num_db_connections: int):
        """Sets the num_db_connections of this MessagingConfigInfo.


        :param num_db_connections: The num_db_connections of this MessagingConfigInfo.
        :type num_db_connections: int
        """

        self._num_db_connections = num_db_connections

    @property
    def num_auto_db_connections(self) -> int:
        """Gets the num_auto_db_connections of this MessagingConfigInfo.


        :return: The num_auto_db_connections of this MessagingConfigInfo.
        :rtype: int
        """
        return self._num_auto_db_connections

    @num_auto_db_connections.setter
    def num_auto_db_connections(self, num_auto_db_connections: int):
        """Sets the num_auto_db_connections of this MessagingConfigInfo.


        :param num_auto_db_connections: The num_auto_db_connections of this MessagingConfigInfo.
        :type num_auto_db_connections: int
        """

        self._num_auto_db_connections = num_auto_db_connections

    @property
    def connection_pool_auto_size(self) -> bool:
        """Gets the connection_pool_auto_size of this MessagingConfigInfo.


        :return: The connection_pool_auto_size of this MessagingConfigInfo.
        :rtype: bool
        """
        return self._connection_pool_auto_size

    @connection_pool_auto_size.setter
    def connection_pool_auto_size(self, connection_pool_auto_size: bool):
        """Sets the connection_pool_auto_size of this MessagingConfigInfo.


        :param connection_pool_auto_size: The connection_pool_auto_size of this MessagingConfigInfo.
        :type connection_pool_auto_size: bool
        """

        self._connection_pool_auto_size = connection_pool_auto_size

    @property
    def archive(self) -> bool:
        """Gets the archive of this MessagingConfigInfo.


        :return: The archive of this MessagingConfigInfo.
        :rtype: bool
        """
        return self._archive

    @archive.setter
    def archive(self, archive: bool):
        """Sets the archive of this MessagingConfigInfo.


        :param archive: The archive of this MessagingConfigInfo.
        :type archive: bool
        """

        self._archive = archive

    @property
    def db_username(self) -> str:
        """Gets the db_username of this MessagingConfigInfo.


        :return: The db_username of this MessagingConfigInfo.
        :rtype: str
        """
        return self._db_username

    @db_username.setter
    def db_username(self, db_username: str):
        """Sets the db_username of this MessagingConfigInfo.


        :param db_username: The db_username of this MessagingConfigInfo.
        :type db_username: str
        """

        self._db_username = db_username

    @property
    def db_password(self) -> str:
        """Gets the db_password of this MessagingConfigInfo.


        :return: The db_password of this MessagingConfigInfo.
        :rtype: str
        """
        return self._db_password

    @db_password.setter
    def db_password(self, db_password: str):
        """Sets the db_password of this MessagingConfigInfo.


        :param db_password: The db_password of this MessagingConfigInfo.
        :type db_password: str
        """

        self._db_password = db_password

    @property
    def db_url(self) -> str:
        """Gets the db_url of this MessagingConfigInfo.


        :return: The db_url of this MessagingConfigInfo.
        :rtype: str
        """
        return self._db_url

    @db_url.setter
    def db_url(self, db_url: str):
        """Sets the db_url of this MessagingConfigInfo.


        :param db_url: The db_url of this MessagingConfigInfo.
        :type db_url: str
        """

        self._db_url = db_url
