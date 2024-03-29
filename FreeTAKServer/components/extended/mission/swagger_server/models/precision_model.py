# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.type import Type  # noqa: F401,E501
from swagger_server import util


class PrecisionModel(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, scale: float=None, type: Type=None, floating: bool=None, maximum_significant_digits: int=None, offset_x: float=None, offset_y: float=None):  # noqa: E501
        """PrecisionModel - a model defined in Swagger

        :param scale: The scale of this PrecisionModel.  # noqa: E501
        :type scale: float
        :param type: The type of this PrecisionModel.  # noqa: E501
        :type type: Type
        :param floating: The floating of this PrecisionModel.  # noqa: E501
        :type floating: bool
        :param maximum_significant_digits: The maximum_significant_digits of this PrecisionModel.  # noqa: E501
        :type maximum_significant_digits: int
        :param offset_x: The offset_x of this PrecisionModel.  # noqa: E501
        :type offset_x: float
        :param offset_y: The offset_y of this PrecisionModel.  # noqa: E501
        :type offset_y: float
        """
        self.swagger_types = {
            'scale': float,
            'type': Type,
            'floating': bool,
            'maximum_significant_digits': int,
            'offset_x': float,
            'offset_y': float
        }

        self.attribute_map = {
            'scale': 'scale',
            'type': 'type',
            'floating': 'floating',
            'maximum_significant_digits': 'maximumSignificantDigits',
            'offset_x': 'offsetX',
            'offset_y': 'offsetY'
        }
        self._scale = scale
        self._type = type
        self._floating = floating
        self._maximum_significant_digits = maximum_significant_digits
        self._offset_x = offset_x
        self._offset_y = offset_y

    @classmethod
    def from_dict(cls, dikt) -> 'PrecisionModel':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The PrecisionModel of this PrecisionModel.  # noqa: E501
        :rtype: PrecisionModel
        """
        return util.deserialize_model(dikt, cls)

    @property
    def scale(self) -> float:
        """Gets the scale of this PrecisionModel.


        :return: The scale of this PrecisionModel.
        :rtype: float
        """
        return self._scale

    @scale.setter
    def scale(self, scale: float):
        """Sets the scale of this PrecisionModel.


        :param scale: The scale of this PrecisionModel.
        :type scale: float
        """

        self._scale = scale

    @property
    def type(self) -> Type:
        """Gets the type of this PrecisionModel.


        :return: The type of this PrecisionModel.
        :rtype: Type
        """
        return self._type

    @type.setter
    def type(self, type: Type):
        """Sets the type of this PrecisionModel.


        :param type: The type of this PrecisionModel.
        :type type: Type
        """

        self._type = type

    @property
    def floating(self) -> bool:
        """Gets the floating of this PrecisionModel.


        :return: The floating of this PrecisionModel.
        :rtype: bool
        """
        return self._floating

    @floating.setter
    def floating(self, floating: bool):
        """Sets the floating of this PrecisionModel.


        :param floating: The floating of this PrecisionModel.
        :type floating: bool
        """

        self._floating = floating

    @property
    def maximum_significant_digits(self) -> int:
        """Gets the maximum_significant_digits of this PrecisionModel.


        :return: The maximum_significant_digits of this PrecisionModel.
        :rtype: int
        """
        return self._maximum_significant_digits

    @maximum_significant_digits.setter
    def maximum_significant_digits(self, maximum_significant_digits: int):
        """Sets the maximum_significant_digits of this PrecisionModel.


        :param maximum_significant_digits: The maximum_significant_digits of this PrecisionModel.
        :type maximum_significant_digits: int
        """

        self._maximum_significant_digits = maximum_significant_digits

    @property
    def offset_x(self) -> float:
        """Gets the offset_x of this PrecisionModel.


        :return: The offset_x of this PrecisionModel.
        :rtype: float
        """
        return self._offset_x

    @offset_x.setter
    def offset_x(self, offset_x: float):
        """Sets the offset_x of this PrecisionModel.


        :param offset_x: The offset_x of this PrecisionModel.
        :type offset_x: float
        """

        self._offset_x = offset_x

    @property
    def offset_y(self) -> float:
        """Gets the offset_y of this PrecisionModel.


        :return: The offset_y of this PrecisionModel.
        :rtype: float
        """
        return self._offset_y

    @offset_y.setter
    def offset_y(self, offset_y: float):
        """Sets the offset_y of this PrecisionModel.


        :param offset_y: The offset_y of this PrecisionModel.
        :type offset_y: float
        """

        self._offset_y = offset_y
