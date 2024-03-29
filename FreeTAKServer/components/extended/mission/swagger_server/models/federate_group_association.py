# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class FederateGroupAssociation(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, group: str=None, direction: str=None, federate_id: str=None):  # noqa: E501
        """FederateGroupAssociation - a model defined in Swagger

        :param group: The group of this FederateGroupAssociation.  # noqa: E501
        :type group: str
        :param direction: The direction of this FederateGroupAssociation.  # noqa: E501
        :type direction: str
        :param federate_id: The federate_id of this FederateGroupAssociation.  # noqa: E501
        :type federate_id: str
        """
        self.swagger_types = {
            'group': str,
            'direction': str,
            'federate_id': str
        }

        self.attribute_map = {
            'group': 'group',
            'direction': 'direction',
            'federate_id': 'federateId'
        }
        self._group = group
        self._direction = direction
        self._federate_id = federate_id

    @classmethod
    def from_dict(cls, dikt) -> 'FederateGroupAssociation':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The FederateGroupAssociation of this FederateGroupAssociation.  # noqa: E501
        :rtype: FederateGroupAssociation
        """
        return util.deserialize_model(dikt, cls)

    @property
    def group(self) -> str:
        """Gets the group of this FederateGroupAssociation.


        :return: The group of this FederateGroupAssociation.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group: str):
        """Sets the group of this FederateGroupAssociation.


        :param group: The group of this FederateGroupAssociation.
        :type group: str
        """

        self._group = group

    @property
    def direction(self) -> str:
        """Gets the direction of this FederateGroupAssociation.


        :return: The direction of this FederateGroupAssociation.
        :rtype: str
        """
        return self._direction

    @direction.setter
    def direction(self, direction: str):
        """Sets the direction of this FederateGroupAssociation.


        :param direction: The direction of this FederateGroupAssociation.
        :type direction: str
        """
        allowed_values = ["INBOUND", "OUTBOUND", "BOTH"]  # noqa: E501
        if direction not in allowed_values:
            raise ValueError(
                "Invalid value for `direction` ({0}), must be one of {1}"
                .format(direction, allowed_values)
            )

        self._direction = direction

    @property
    def federate_id(self) -> str:
        """Gets the federate_id of this FederateGroupAssociation.


        :return: The federate_id of this FederateGroupAssociation.
        :rtype: str
        """
        return self._federate_id

    @federate_id.setter
    def federate_id(self, federate_id: str):
        """Sets the federate_id of this FederateGroupAssociation.


        :param federate_id: The federate_id of this FederateGroupAssociation.
        :type federate_id: str
        """

        self._federate_id = federate_id
