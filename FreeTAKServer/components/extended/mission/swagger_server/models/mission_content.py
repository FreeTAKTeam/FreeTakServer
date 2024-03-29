# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class MissionContent(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, hashes: List[str]=None, uids: List[str]=None):  # noqa: E501
        """MissionContent - a model defined in Swagger

        :param hashes: The hashes of this MissionContent.  # noqa: E501
        :type hashes: List[str]
        :param uids: The uids of this MissionContent.  # noqa: E501
        :type uids: List[str]
        """
        self.swagger_types = {
            'hashes': List[str],
            'uids': List[str]
        }

        self.attribute_map = {
            'hashes': 'hashes',
            'uids': 'uids'
        }
        self._hashes = hashes
        self._uids = uids

    @classmethod
    def from_dict(cls, dikt) -> 'MissionContent':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MissionContent of this MissionContent.  # noqa: E501
        :rtype: MissionContent
        """
        return util.deserialize_model(dikt, cls)

    @property
    def hashes(self) -> List[str]:
        """Gets the hashes of this MissionContent.


        :return: The hashes of this MissionContent.
        :rtype: List[str]
        """
        return self._hashes

    @hashes.setter
    def hashes(self, hashes: List[str]):
        """Sets the hashes of this MissionContent.


        :param hashes: The hashes of this MissionContent.
        :type hashes: List[str]
        """

        self._hashes = hashes

    @property
    def uids(self) -> List[str]:
        """Gets the uids of this MissionContent.


        :return: The uids of this MissionContent.
        :rtype: List[str]
        """
        return self._uids

    @uids.setter
    def uids(self, uids: List[str]):
        """Sets the uids of this MissionContent.


        :param uids: The uids of this MissionContent.
        :type uids: List[str]
        """

        self._uids = uids
