# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Connection(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, url: str=None, username: str=None, password: str=None):  # noqa: E501
        """Connection - a model defined in Swagger

        :param url: The url of this Connection.  # noqa: E501
        :type url: str
        :param username: The username of this Connection.  # noqa: E501
        :type username: str
        :param password: The password of this Connection.  # noqa: E501
        :type password: str
        """
        self.swagger_types = {
            'url': str,
            'username': str,
            'password': str
        }

        self.attribute_map = {
            'url': 'url',
            'username': 'username',
            'password': 'password'
        }
        self._url = url
        self._username = username
        self._password = password

    @classmethod
    def from_dict(cls, dikt) -> 'Connection':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Connection of this Connection.  # noqa: E501
        :rtype: Connection
        """
        return util.deserialize_model(dikt, cls)

    @property
    def url(self) -> str:
        """Gets the url of this Connection.


        :return: The url of this Connection.
        :rtype: str
        """
        return self._url

    @url.setter
    def url(self, url: str):
        """Sets the url of this Connection.


        :param url: The url of this Connection.
        :type url: str
        """

        self._url = url

    @property
    def username(self) -> str:
        """Gets the username of this Connection.


        :return: The username of this Connection.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this Connection.


        :param username: The username of this Connection.
        :type username: str
        """

        self._username = username

    @property
    def password(self) -> str:
        """Gets the password of this Connection.


        :return: The password of this Connection.
        :rtype: str
        """
        return self._password

    @password.setter
    def password(self, password: str):
        """Sets the password of this Connection.


        :param password: The password of this Connection.
        :type password: str
        """

        self._password = password
