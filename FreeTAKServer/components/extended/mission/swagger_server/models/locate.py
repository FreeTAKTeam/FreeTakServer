# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Locate(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, enabled: bool=None, require_login: bool=None, cot_type: str=None, group: str=None, broadcast: bool=None, add_to_mission: bool=None, mission: str=None):  # noqa: E501
        """Locate - a model defined in Swagger

        :param enabled: The enabled of this Locate.  # noqa: E501
        :type enabled: bool
        :param require_login: The require_login of this Locate.  # noqa: E501
        :type require_login: bool
        :param cot_type: The cot_type of this Locate.  # noqa: E501
        :type cot_type: str
        :param group: The group of this Locate.  # noqa: E501
        :type group: str
        :param broadcast: The broadcast of this Locate.  # noqa: E501
        :type broadcast: bool
        :param add_to_mission: The add_to_mission of this Locate.  # noqa: E501
        :type add_to_mission: bool
        :param mission: The mission of this Locate.  # noqa: E501
        :type mission: str
        """
        self.swagger_types = {
            'enabled': bool,
            'require_login': bool,
            'cot_type': str,
            'group': str,
            'broadcast': bool,
            'add_to_mission': bool,
            'mission': str
        }

        self.attribute_map = {
            'enabled': 'enabled',
            'require_login': 'requireLogin',
            'cot_type': 'cotType',
            'group': 'group',
            'broadcast': 'broadcast',
            'add_to_mission': 'addToMission',
            'mission': 'mission'
        }
        self._enabled = enabled
        self._require_login = require_login
        self._cot_type = cot_type
        self._group = group
        self._broadcast = broadcast
        self._add_to_mission = add_to_mission
        self._mission = mission

    @classmethod
    def from_dict(cls, dikt) -> 'Locate':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Locate of this Locate.  # noqa: E501
        :rtype: Locate
        """
        return util.deserialize_model(dikt, cls)

    @property
    def enabled(self) -> bool:
        """Gets the enabled of this Locate.


        :return: The enabled of this Locate.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled: bool):
        """Sets the enabled of this Locate.


        :param enabled: The enabled of this Locate.
        :type enabled: bool
        """

        self._enabled = enabled

    @property
    def require_login(self) -> bool:
        """Gets the require_login of this Locate.


        :return: The require_login of this Locate.
        :rtype: bool
        """
        return self._require_login

    @require_login.setter
    def require_login(self, require_login: bool):
        """Sets the require_login of this Locate.


        :param require_login: The require_login of this Locate.
        :type require_login: bool
        """

        self._require_login = require_login

    @property
    def cot_type(self) -> str:
        """Gets the cot_type of this Locate.


        :return: The cot_type of this Locate.
        :rtype: str
        """
        return self._cot_type

    @cot_type.setter
    def cot_type(self, cot_type: str):
        """Sets the cot_type of this Locate.


        :param cot_type: The cot_type of this Locate.
        :type cot_type: str
        """

        self._cot_type = cot_type

    @property
    def group(self) -> str:
        """Gets the group of this Locate.


        :return: The group of this Locate.
        :rtype: str
        """
        return self._group

    @group.setter
    def group(self, group: str):
        """Sets the group of this Locate.


        :param group: The group of this Locate.
        :type group: str
        """

        self._group = group

    @property
    def broadcast(self) -> bool:
        """Gets the broadcast of this Locate.


        :return: The broadcast of this Locate.
        :rtype: bool
        """
        return self._broadcast

    @broadcast.setter
    def broadcast(self, broadcast: bool):
        """Sets the broadcast of this Locate.


        :param broadcast: The broadcast of this Locate.
        :type broadcast: bool
        """

        self._broadcast = broadcast

    @property
    def add_to_mission(self) -> bool:
        """Gets the add_to_mission of this Locate.


        :return: The add_to_mission of this Locate.
        :rtype: bool
        """
        return self._add_to_mission

    @add_to_mission.setter
    def add_to_mission(self, add_to_mission: bool):
        """Sets the add_to_mission of this Locate.


        :param add_to_mission: The add_to_mission of this Locate.
        :type add_to_mission: bool
        """

        self._add_to_mission = add_to_mission

    @property
    def mission(self) -> str:
        """Gets the mission of this Locate.


        :return: The mission of this Locate.
        :rtype: str
        """
        return self._mission

    @mission.setter
    def mission(self, mission: str):
        """Sets the mission of this Locate.


        :param mission: The mission of this Locate.
        :type mission: str
        """

        self._mission = mission