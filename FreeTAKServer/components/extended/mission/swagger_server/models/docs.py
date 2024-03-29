# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Docs(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, admin_only: bool=None):  # noqa: E501
        """Docs - a model defined in Swagger

        :param admin_only: The admin_only of this Docs.  # noqa: E501
        :type admin_only: bool
        """
        self.swagger_types = {
            'admin_only': bool
        }

        self.attribute_map = {
            'admin_only': 'adminOnly'
        }
        self._admin_only = admin_only

    @classmethod
    def from_dict(cls, dikt) -> 'Docs':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Docs of this Docs.  # noqa: E501
        :rtype: Docs
        """
        return util.deserialize_model(dikt, cls)

    @property
    def admin_only(self) -> bool:
        """Gets the admin_only of this Docs.


        :return: The admin_only of this Docs.
        :rtype: bool
        """
        return self._admin_only

    @admin_only.setter
    def admin_only(self, admin_only: bool):
        """Sets the admin_only of this Docs.


        :param admin_only: The admin_only of this Docs.
        :type admin_only: bool
        """

        self._admin_only = admin_only
