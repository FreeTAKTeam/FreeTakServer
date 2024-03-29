# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.repeatable_type import RepeatableType  # noqa: F401,E501
from swagger_server import util


class Repeater(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, repeatable_type: List[RepeatableType]=None, enable: bool=None, period_millis: int=None, stale_delay_millis: int=None, max_allowed_repeatables: int=None):  # noqa: E501
        """Repeater - a model defined in Swagger

        :param repeatable_type: The repeatable_type of this Repeater.  # noqa: E501
        :type repeatable_type: List[RepeatableType]
        :param enable: The enable of this Repeater.  # noqa: E501
        :type enable: bool
        :param period_millis: The period_millis of this Repeater.  # noqa: E501
        :type period_millis: int
        :param stale_delay_millis: The stale_delay_millis of this Repeater.  # noqa: E501
        :type stale_delay_millis: int
        :param max_allowed_repeatables: The max_allowed_repeatables of this Repeater.  # noqa: E501
        :type max_allowed_repeatables: int
        """
        self.swagger_types = {
            'repeatable_type': List[RepeatableType],
            'enable': bool,
            'period_millis': int,
            'stale_delay_millis': int,
            'max_allowed_repeatables': int
        }

        self.attribute_map = {
            'repeatable_type': 'repeatableType',
            'enable': 'enable',
            'period_millis': 'periodMillis',
            'stale_delay_millis': 'staleDelayMillis',
            'max_allowed_repeatables': 'maxAllowedRepeatables'
        }
        self._repeatable_type = repeatable_type
        self._enable = enable
        self._period_millis = period_millis
        self._stale_delay_millis = stale_delay_millis
        self._max_allowed_repeatables = max_allowed_repeatables

    @classmethod
    def from_dict(cls, dikt) -> 'Repeater':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Repeater of this Repeater.  # noqa: E501
        :rtype: Repeater
        """
        return util.deserialize_model(dikt, cls)

    @property
    def repeatable_type(self) -> List[RepeatableType]:
        """Gets the repeatable_type of this Repeater.


        :return: The repeatable_type of this Repeater.
        :rtype: List[RepeatableType]
        """
        return self._repeatable_type

    @repeatable_type.setter
    def repeatable_type(self, repeatable_type: List[RepeatableType]):
        """Sets the repeatable_type of this Repeater.


        :param repeatable_type: The repeatable_type of this Repeater.
        :type repeatable_type: List[RepeatableType]
        """

        self._repeatable_type = repeatable_type

    @property
    def enable(self) -> bool:
        """Gets the enable of this Repeater.


        :return: The enable of this Repeater.
        :rtype: bool
        """
        return self._enable

    @enable.setter
    def enable(self, enable: bool):
        """Sets the enable of this Repeater.


        :param enable: The enable of this Repeater.
        :type enable: bool
        """

        self._enable = enable

    @property
    def period_millis(self) -> int:
        """Gets the period_millis of this Repeater.


        :return: The period_millis of this Repeater.
        :rtype: int
        """
        return self._period_millis

    @period_millis.setter
    def period_millis(self, period_millis: int):
        """Sets the period_millis of this Repeater.


        :param period_millis: The period_millis of this Repeater.
        :type period_millis: int
        """

        self._period_millis = period_millis

    @property
    def stale_delay_millis(self) -> int:
        """Gets the stale_delay_millis of this Repeater.


        :return: The stale_delay_millis of this Repeater.
        :rtype: int
        """
        return self._stale_delay_millis

    @stale_delay_millis.setter
    def stale_delay_millis(self, stale_delay_millis: int):
        """Sets the stale_delay_millis of this Repeater.


        :param stale_delay_millis: The stale_delay_millis of this Repeater.
        :type stale_delay_millis: int
        """

        self._stale_delay_millis = stale_delay_millis

    @property
    def max_allowed_repeatables(self) -> int:
        """Gets the max_allowed_repeatables of this Repeater.


        :return: The max_allowed_repeatables of this Repeater.
        :rtype: int
        """
        return self._max_allowed_repeatables

    @max_allowed_repeatables.setter
    def max_allowed_repeatables(self, max_allowed_repeatables: int):
        """Sets the max_allowed_repeatables of this Repeater.


        :param max_allowed_repeatables: The max_allowed_repeatables of this Repeater.
        :type max_allowed_repeatables: int
        """

        self._max_allowed_repeatables = max_allowed_repeatables
