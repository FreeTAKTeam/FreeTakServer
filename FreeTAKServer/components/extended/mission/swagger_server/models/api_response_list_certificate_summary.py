# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.certificate_summary import CertificateSummary  # noqa: F401,E501
from swagger_server import util


class ApiResponseListCertificateSummary(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, version: str=None, type: str=None, data: List[CertificateSummary]=None, messages: List[str]=None, node_id: str=None):  # noqa: E501
        """ApiResponseListCertificateSummary - a model defined in Swagger

        :param version: The version of this ApiResponseListCertificateSummary.  # noqa: E501
        :type version: str
        :param type: The type of this ApiResponseListCertificateSummary.  # noqa: E501
        :type type: str
        :param data: The data of this ApiResponseListCertificateSummary.  # noqa: E501
        :type data: List[CertificateSummary]
        :param messages: The messages of this ApiResponseListCertificateSummary.  # noqa: E501
        :type messages: List[str]
        :param node_id: The node_id of this ApiResponseListCertificateSummary.  # noqa: E501
        :type node_id: str
        """
        self.swagger_types = {
            'version': str,
            'type': str,
            'data': List[CertificateSummary],
            'messages': List[str],
            'node_id': str
        }

        self.attribute_map = {
            'version': 'version',
            'type': 'type',
            'data': 'data',
            'messages': 'messages',
            'node_id': 'nodeId'
        }
        self._version = version
        self._type = type
        self._data = data
        self._messages = messages
        self._node_id = node_id

    @classmethod
    def from_dict(cls, dikt) -> 'ApiResponseListCertificateSummary':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The ApiResponseListCertificateSummary of this ApiResponseListCertificateSummary.  # noqa: E501
        :rtype: ApiResponseListCertificateSummary
        """
        return util.deserialize_model(dikt, cls)

    @property
    def version(self) -> str:
        """Gets the version of this ApiResponseListCertificateSummary.


        :return: The version of this ApiResponseListCertificateSummary.
        :rtype: str
        """
        return self._version

    @version.setter
    def version(self, version: str):
        """Sets the version of this ApiResponseListCertificateSummary.


        :param version: The version of this ApiResponseListCertificateSummary.
        :type version: str
        """

        self._version = version

    @property
    def type(self) -> str:
        """Gets the type of this ApiResponseListCertificateSummary.


        :return: The type of this ApiResponseListCertificateSummary.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type: str):
        """Sets the type of this ApiResponseListCertificateSummary.


        :param type: The type of this ApiResponseListCertificateSummary.
        :type type: str
        """

        self._type = type

    @property
    def data(self) -> List[CertificateSummary]:
        """Gets the data of this ApiResponseListCertificateSummary.


        :return: The data of this ApiResponseListCertificateSummary.
        :rtype: List[CertificateSummary]
        """
        return self._data

    @data.setter
    def data(self, data: List[CertificateSummary]):
        """Sets the data of this ApiResponseListCertificateSummary.


        :param data: The data of this ApiResponseListCertificateSummary.
        :type data: List[CertificateSummary]
        """

        self._data = data

    @property
    def messages(self) -> List[str]:
        """Gets the messages of this ApiResponseListCertificateSummary.


        :return: The messages of this ApiResponseListCertificateSummary.
        :rtype: List[str]
        """
        return self._messages

    @messages.setter
    def messages(self, messages: List[str]):
        """Sets the messages of this ApiResponseListCertificateSummary.


        :param messages: The messages of this ApiResponseListCertificateSummary.
        :type messages: List[str]
        """

        self._messages = messages

    @property
    def node_id(self) -> str:
        """Gets the node_id of this ApiResponseListCertificateSummary.


        :return: The node_id of this ApiResponseListCertificateSummary.
        :rtype: str
        """
        return self._node_id

    @node_id.setter
    def node_id(self, node_id: str):
        """Sets the node_id of this ApiResponseListCertificateSummary.


        :param node_id: The node_id of this ApiResponseListCertificateSummary.
        :type node_id: str
        """

        self._node_id = node_id
