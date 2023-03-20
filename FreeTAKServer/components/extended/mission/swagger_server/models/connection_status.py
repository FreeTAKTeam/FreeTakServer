# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.connection_info import ConnectionInfo  # noqa: F401,E501
from swagger_server.models.federate import Federate  # noqa: F401,E501
from swagger_server.models.group import Group  # noqa: F401,E501
from swagger_server.models.user import User  # noqa: F401,E501
from swagger_server import util


class ConnectionStatus(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, node_id: str=None, connection: ConnectionInfo=None, federate: Federate=None, last_error: str=None, connection_status_value: str=None, user: User=None, groups: List[Group]=None, federate_name: str=None):  # noqa: E501
        """ConnectionStatus - a model defined in Swagger

        :param node_id: The node_id of this ConnectionStatus.  # noqa: E501
        :type node_id: str
        :param connection: The connection of this ConnectionStatus.  # noqa: E501
        :type connection: ConnectionInfo
        :param federate: The federate of this ConnectionStatus.  # noqa: E501
        :type federate: Federate
        :param last_error: The last_error of this ConnectionStatus.  # noqa: E501
        :type last_error: str
        :param connection_status_value: The connection_status_value of this ConnectionStatus.  # noqa: E501
        :type connection_status_value: str
        :param user: The user of this ConnectionStatus.  # noqa: E501
        :type user: User
        :param groups: The groups of this ConnectionStatus.  # noqa: E501
        :type groups: List[Group]
        :param federate_name: The federate_name of this ConnectionStatus.  # noqa: E501
        :type federate_name: str
        """
        self.swagger_types = {
            'node_id': str,
            'connection': ConnectionInfo,
            'federate': Federate,
            'last_error': str,
            'connection_status_value': str,
            'user': User,
            'groups': List[Group],
            'federate_name': str
        }

        self.attribute_map = {
            'node_id': 'nodeId',
            'connection': 'connection',
            'federate': 'federate',
            'last_error': 'lastError',
            'connection_status_value': 'connectionStatusValue',
            'user': 'user',
            'groups': 'groups',
            'federate_name': 'federateName'
        }
        self._node_id = node_id
        self._connection = connection
        self._federate = federate
        self._last_error = last_error
        self._connection_status_value = connection_status_value
        self._user = user
        self._groups = groups
        self._federate_name = federate_name

    @classmethod
    def from_dict(cls, dikt) -> 'ConnectionStatus':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ConnectionStatus of this ConnectionStatus.  # noqa: E501
        :rtype: ConnectionStatus
        """
        return util.deserialize_model(dikt, cls)

    @property
    def node_id(self) -> str:
        """Gets the node_id of this ConnectionStatus.


        :return: The node_id of this ConnectionStatus.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id: str):
        """Sets the node_id of this ConnectionStatus.


        :param node_id: The node_id of this ConnectionStatus.
        :type node_id: str
        """

        self._node_id = node_id

    @property
    def connection(self) -> ConnectionInfo:
        """Gets the connection of this ConnectionStatus.


        :return: The connection of this ConnectionStatus.
        :rtype: ConnectionInfo
        """
        return self._connection

    @connection.setter
    def connection(self, connection: ConnectionInfo):
        """Sets the connection of this ConnectionStatus.


        :param connection: The connection of this ConnectionStatus.
        :type connection: ConnectionInfo
        """

        self._connection = connection

    @property
    def federate(self) -> Federate:
        """Gets the federate of this ConnectionStatus.


        :return: The federate of this ConnectionStatus.
        :rtype: Federate
        """
        return self._federate

    @federate.setter
    def federate(self, federate: Federate):
        """Sets the federate of this ConnectionStatus.


        :param federate: The federate of this ConnectionStatus.
        :type federate: Federate
        """

        self._federate = federate

    @property
    def last_error(self) -> str:
        """Gets the last_error of this ConnectionStatus.


        :return: The last_error of this ConnectionStatus.
        :rtype: str
        """
        return self._last_error

    @last_error.setter
    def last_error(self, last_error: str):
        """Sets the last_error of this ConnectionStatus.


        :param last_error: The last_error of this ConnectionStatus.
        :type last_error: str
        """

        self._last_error = last_error

    @property
    def connection_status_value(self) -> str:
        """Gets the connection_status_value of this ConnectionStatus.


        :return: The connection_status_value of this ConnectionStatus.
        :rtype: str
        """
        return self._connection_status_value

    @connection_status_value.setter
    def connection_status_value(self, connection_status_value: str):
        """Sets the connection_status_value of this ConnectionStatus.


        :param connection_status_value: The connection_status_value of this ConnectionStatus.
        :type connection_status_value: str
        """
        allowed_values = ["DISABLED", "CONNECTED", "CONNECTING", "WAITING_TO_RETRY", "RETRY_SCHEDULED"]  # noqa: E501
        if connection_status_value not in allowed_values:
            raise ValueError(
                "Invalid value for `connection_status_value` ({0}), must be one of {1}"
                .format(connection_status_value, allowed_values)
            )

        self._connection_status_value = connection_status_value

    @property
    def user(self) -> User:
        """Gets the user of this ConnectionStatus.


        :return: The user of this ConnectionStatus.
        :rtype: User
        """
        return self._user

    @user.setter
    def user(self, user: User):
        """Sets the user of this ConnectionStatus.


        :param user: The user of this ConnectionStatus.
        :type user: User
        """

        self._user = user

    @property
    def groups(self) -> List[Group]:
        """Gets the groups of this ConnectionStatus.


        :return: The groups of this ConnectionStatus.
        :rtype: List[Group]
        """
        return self._groups

    @groups.setter
    def groups(self, groups: List[Group]):
        """Sets the groups of this ConnectionStatus.


        :param groups: The groups of this ConnectionStatus.
        :type groups: List[Group]
        """

        self._groups = groups

    @property
    def federate_name(self) -> str:
        """Gets the federate_name of this ConnectionStatus.


        :return: The federate_name of this ConnectionStatus.
        :rtype: str
        """
        return self._federate_name

    @federate_name.setter
    def federate_name(self, federate_name: str):
        """Sets the federate_name of this ConnectionStatus.


        :param federate_name: The federate_name of this ConnectionStatus.
        :type federate_name: str
        """

        self._federate_name = federate_name