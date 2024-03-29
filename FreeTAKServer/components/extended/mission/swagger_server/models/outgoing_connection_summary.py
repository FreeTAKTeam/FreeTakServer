# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.connection_info_summary import ConnectionInfoSummary  # noqa: F401,E501
from swagger_server import util


class OutgoingConnectionSummary(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, connection_info_summary: ConnectionInfoSummary=None, address: str=None, port: int=None, display_name: str=None, enabled: bool=None, protocol_version: int=None, reconnect_interval: int=None, fallback: str=None, max_retries: int=None, unlimited_retries: bool=None):  # noqa: E501
        """OutgoingConnectionSummary - a model defined in Swagger

        :param connection_info_summary: The connection_info_summary of this OutgoingConnectionSummary.  # noqa: E501
        :type connection_info_summary: ConnectionInfoSummary
        :param address: The address of this OutgoingConnectionSummary.  # noqa: E501
        :type address: str
        :param port: The port of this OutgoingConnectionSummary.  # noqa: E501
        :type port: int
        :param display_name: The display_name of this OutgoingConnectionSummary.  # noqa: E501
        :type display_name: str
        :param enabled: The enabled of this OutgoingConnectionSummary.  # noqa: E501
        :type enabled: bool
        :param protocol_version: The protocol_version of this OutgoingConnectionSummary.  # noqa: E501
        :type protocol_version: int
        :param reconnect_interval: The reconnect_interval of this OutgoingConnectionSummary.  # noqa: E501
        :type reconnect_interval: int
        :param fallback: The fallback of this OutgoingConnectionSummary.  # noqa: E501
        :type fallback: str
        :param max_retries: The max_retries of this OutgoingConnectionSummary.  # noqa: E501
        :type max_retries: int
        :param unlimited_retries: The unlimited_retries of this OutgoingConnectionSummary.  # noqa: E501
        :type unlimited_retries: bool
        """
        self.swagger_types = {
            'connection_info_summary': ConnectionInfoSummary,
            'address': str,
            'port': int,
            'display_name': str,
            'enabled': bool,
            'protocol_version': int,
            'reconnect_interval': int,
            'fallback': str,
            'max_retries': int,
            'unlimited_retries': bool
        }

        self.attribute_map = {
            'connection_info_summary': 'connectionInfoSummary',
            'address': 'address',
            'port': 'port',
            'display_name': 'displayName',
            'enabled': 'enabled',
            'protocol_version': 'protocolVersion',
            'reconnect_interval': 'reconnectInterval',
            'fallback': 'fallback',
            'max_retries': 'maxRetries',
            'unlimited_retries': 'unlimitedRetries'
        }
        self._connection_info_summary = connection_info_summary
        self._address = address
        self._port = port
        self._display_name = display_name
        self._enabled = enabled
        self._protocol_version = protocol_version
        self._reconnect_interval = reconnect_interval
        self._fallback = fallback
        self._max_retries = max_retries
        self._unlimited_retries = unlimited_retries

    @classmethod
    def from_dict(cls, dikt) -> 'OutgoingConnectionSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The OutgoingConnectionSummary of this OutgoingConnectionSummary.  # noqa: E501
        :rtype: OutgoingConnectionSummary
        """
        return util.deserialize_model(dikt, cls)

    @property
    def connection_info_summary(self) -> ConnectionInfoSummary:
        """Gets the connection_info_summary of this OutgoingConnectionSummary.


        :return: The connection_info_summary of this OutgoingConnectionSummary.
        :rtype: ConnectionInfoSummary
        """
        return self._connection_info_summary

    @connection_info_summary.setter
    def connection_info_summary(self, connection_info_summary: ConnectionInfoSummary):
        """Sets the connection_info_summary of this OutgoingConnectionSummary.


        :param connection_info_summary: The connection_info_summary of this OutgoingConnectionSummary.
        :type connection_info_summary: ConnectionInfoSummary
        """

        self._connection_info_summary = connection_info_summary

    @property
    def address(self) -> str:
        """Gets the address of this OutgoingConnectionSummary.


        :return: The address of this OutgoingConnectionSummary.
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address: str):
        """Sets the address of this OutgoingConnectionSummary.


        :param address: The address of this OutgoingConnectionSummary.
        :type address: str
        """

        self._address = address

    @property
    def port(self) -> int:
        """Gets the port of this OutgoingConnectionSummary.


        :return: The port of this OutgoingConnectionSummary.
        :rtype: int
        """
        return self._port

    @port.setter
    def port(self, port: int):
        """Sets the port of this OutgoingConnectionSummary.


        :param port: The port of this OutgoingConnectionSummary.
        :type port: int
        """

        self._port = port

    @property
    def display_name(self) -> str:
        """Gets the display_name of this OutgoingConnectionSummary.


        :return: The display_name of this OutgoingConnectionSummary.
        :rtype: str
        """
        return self._display_name

    @display_name.setter
    def display_name(self, display_name: str):
        """Sets the display_name of this OutgoingConnectionSummary.


        :param display_name: The display_name of this OutgoingConnectionSummary.
        :type display_name: str
        """

        self._display_name = display_name

    @property
    def enabled(self) -> bool:
        """Gets the enabled of this OutgoingConnectionSummary.


        :return: The enabled of this OutgoingConnectionSummary.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        """Sets the enabled of this OutgoingConnectionSummary.


        :param enabled: The enabled of this OutgoingConnectionSummary.
        :type enabled: bool
        """

        self._enabled = enabled

    @property
    def protocol_version(self) -> int:
        """Gets the protocol_version of this OutgoingConnectionSummary.


        :return: The protocol_version of this OutgoingConnectionSummary.
        :rtype: int
        """
        return self._protocol_version

    @protocol_version.setter
    def protocol_version(self, protocol_version: int):
        """Sets the protocol_version of this OutgoingConnectionSummary.


        :param protocol_version: The protocol_version of this OutgoingConnectionSummary.
        :type protocol_version: int
        """

        self._protocol_version = protocol_version

    @property
    def reconnect_interval(self) -> int:
        """Gets the reconnect_interval of this OutgoingConnectionSummary.


        :return: The reconnect_interval of this OutgoingConnectionSummary.
        :rtype: int
        """
        return self._reconnect_interval

    @reconnect_interval.setter
    def reconnect_interval(self, reconnect_interval: int):
        """Sets the reconnect_interval of this OutgoingConnectionSummary.


        :param reconnect_interval: The reconnect_interval of this OutgoingConnectionSummary.
        :type reconnect_interval: int
        """

        self._reconnect_interval = reconnect_interval

    @property
    def fallback(self) -> str:
        """Gets the fallback of this OutgoingConnectionSummary.


        :return: The fallback of this OutgoingConnectionSummary.
        :rtype: str
        """
        return self._fallback

    @fallback.setter
    def fallback(self, fallback: str):
        """Sets the fallback of this OutgoingConnectionSummary.


        :param fallback: The fallback of this OutgoingConnectionSummary.
        :type fallback: str
        """

        self._fallback = fallback

    @property
    def max_retries(self) -> int:
        """Gets the max_retries of this OutgoingConnectionSummary.


        :return: The max_retries of this OutgoingConnectionSummary.
        :rtype: int
        """
        return self._max_retries

    @max_retries.setter
    def max_retries(self, max_retries: int):
        """Sets the max_retries of this OutgoingConnectionSummary.


        :param max_retries: The max_retries of this OutgoingConnectionSummary.
        :type max_retries: int
        """

        self._max_retries = max_retries

    @property
    def unlimited_retries(self) -> bool:
        """Gets the unlimited_retries of this OutgoingConnectionSummary.


        :return: The unlimited_retries of this OutgoingConnectionSummary.
        :rtype: bool
        """
        return self._unlimited_retries

    @unlimited_retries.setter
    def unlimited_retries(self, unlimited_retries: bool):
        """Sets the unlimited_retries of this OutgoingConnectionSummary.


        :param unlimited_retries: The unlimited_retries of this OutgoingConnectionSummary.
        :type unlimited_retries: bool
        """

        self._unlimited_retries = unlimited_retries
