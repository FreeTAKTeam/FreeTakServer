# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.latest_sa import LatestSA  # noqa: F401,E501
from swagger_server.models.queue import Queue  # noqa: F401,E501
from swagger_server import util


class Buffer(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, latest_sa: LatestSA=None, queue: Queue=None, embedded_ignite: bool=None, ignite_multicast: bool=None, ignite_non_multicast_discovery_port: int=None, ignite_non_multicast_discovery_port_count: int=None, ignite_communication_port: int=None, ignite_communication_port_count: int=None, ignite_host: str=None, ignite_worker_timeout_milliseconds: int=None):  # noqa: E501
        """Buffer - a model defined in Swagger

        :param latest_sa: The latest_sa of this Buffer.  # noqa: E501
        :type latest_sa: LatestSA
        :param queue: The queue of this Buffer.  # noqa: E501
        :type queue: Queue
        :param embedded_ignite: The embedded_ignite of this Buffer.  # noqa: E501
        :type embedded_ignite: bool
        :param ignite_multicast: The ignite_multicast of this Buffer.  # noqa: E501
        :type ignite_multicast: bool
        :param ignite_non_multicast_discovery_port: The ignite_non_multicast_discovery_port of this Buffer.  # noqa: E501
        :type ignite_non_multicast_discovery_port: int
        :param ignite_non_multicast_discovery_port_count: The ignite_non_multicast_discovery_port_count of this Buffer.  # noqa: E501
        :type ignite_non_multicast_discovery_port_count: int
        :param ignite_communication_port: The ignite_communication_port of this Buffer.  # noqa: E501
        :type ignite_communication_port: int
        :param ignite_communication_port_count: The ignite_communication_port_count of this Buffer.  # noqa: E501
        :type ignite_communication_port_count: int
        :param ignite_host: The ignite_host of this Buffer.  # noqa: E501
        :type ignite_host: str
        :param ignite_worker_timeout_milliseconds: The ignite_worker_timeout_milliseconds of this Buffer.  # noqa: E501
        :type ignite_worker_timeout_milliseconds: int
        """
        self.swagger_types = {
            'latest_sa': LatestSA,
            'queue': Queue,
            'embedded_ignite': bool,
            'ignite_multicast': bool,
            'ignite_non_multicast_discovery_port': int,
            'ignite_non_multicast_discovery_port_count': int,
            'ignite_communication_port': int,
            'ignite_communication_port_count': int,
            'ignite_host': str,
            'ignite_worker_timeout_milliseconds': int
        }

        self.attribute_map = {
            'latest_sa': 'latestSA',
            'queue': 'queue',
            'embedded_ignite': 'embeddedIgnite',
            'ignite_multicast': 'igniteMulticast',
            'ignite_non_multicast_discovery_port': 'igniteNonMulticastDiscoveryPort',
            'ignite_non_multicast_discovery_port_count': 'igniteNonMulticastDiscoveryPortCount',
            'ignite_communication_port': 'igniteCommunicationPort',
            'ignite_communication_port_count': 'igniteCommunicationPortCount',
            'ignite_host': 'igniteHost',
            'ignite_worker_timeout_milliseconds': 'igniteWorkerTimeoutMilliseconds'
        }
        self._latest_sa = latest_sa
        self._queue = queue
        self._embedded_ignite = embedded_ignite
        self._ignite_multicast = ignite_multicast
        self._ignite_non_multicast_discovery_port = ignite_non_multicast_discovery_port
        self._ignite_non_multicast_discovery_port_count = ignite_non_multicast_discovery_port_count
        self._ignite_communication_port = ignite_communication_port
        self._ignite_communication_port_count = ignite_communication_port_count
        self._ignite_host = ignite_host
        self._ignite_worker_timeout_milliseconds = ignite_worker_timeout_milliseconds

    @classmethod
    def from_dict(cls, dikt) -> 'Buffer':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Buffer of this Buffer.  # noqa: E501
        :rtype: Buffer
        """
        return util.deserialize_model(dikt, cls)

    @property
    def latest_sa(self) -> LatestSA:
        """Gets the latest_sa of this Buffer.


        :return: The latest_sa of this Buffer.
        :rtype: LatestSA
        """
        return self._latest_sa

    @latest_sa.setter
    def latest_sa(self, latest_sa: LatestSA):
        """Sets the latest_sa of this Buffer.


        :param latest_sa: The latest_sa of this Buffer.
        :type latest_sa: LatestSA
        """
        if latest_sa is None:
            raise ValueError("Invalid value for `latest_sa`, must not be `None`")  # noqa: E501

        self._latest_sa = latest_sa

    @property
    def queue(self) -> Queue:
        """Gets the queue of this Buffer.


        :return: The queue of this Buffer.
        :rtype: Queue
        """
        return self._queue

    @queue.setter
    def queue(self, queue: Queue):
        """Sets the queue of this Buffer.


        :param queue: The queue of this Buffer.
        :type queue: Queue
        """
        if queue is None:
            raise ValueError("Invalid value for `queue`, must not be `None`")  # noqa: E501

        self._queue = queue

    @property
    def embedded_ignite(self) -> bool:
        """Gets the embedded_ignite of this Buffer.


        :return: The embedded_ignite of this Buffer.
        :rtype: bool
        """
        return self._embedded_ignite

    @embedded_ignite.setter
    def embedded_ignite(self, embedded_ignite: bool):
        """Sets the embedded_ignite of this Buffer.


        :param embedded_ignite: The embedded_ignite of this Buffer.
        :type embedded_ignite: bool
        """

        self._embedded_ignite = embedded_ignite

    @property
    def ignite_multicast(self) -> bool:
        """Gets the ignite_multicast of this Buffer.


        :return: The ignite_multicast of this Buffer.
        :rtype: bool
        """
        return self._ignite_multicast

    @ignite_multicast.setter
    def ignite_multicast(self, ignite_multicast: bool):
        """Sets the ignite_multicast of this Buffer.


        :param ignite_multicast: The ignite_multicast of this Buffer.
        :type ignite_multicast: bool
        """

        self._ignite_multicast = ignite_multicast

    @property
    def ignite_non_multicast_discovery_port(self) -> int:
        """Gets the ignite_non_multicast_discovery_port of this Buffer.


        :return: The ignite_non_multicast_discovery_port of this Buffer.
        :rtype: int
        """
        return self._ignite_non_multicast_discovery_port

    @ignite_non_multicast_discovery_port.setter
    def ignite_non_multicast_discovery_port(self, ignite_non_multicast_discovery_port: int):
        """Sets the ignite_non_multicast_discovery_port of this Buffer.


        :param ignite_non_multicast_discovery_port: The ignite_non_multicast_discovery_port of this Buffer.
        :type ignite_non_multicast_discovery_port: int
        """

        self._ignite_non_multicast_discovery_port = ignite_non_multicast_discovery_port

    @property
    def ignite_non_multicast_discovery_port_count(self) -> int:
        """Gets the ignite_non_multicast_discovery_port_count of this Buffer.


        :return: The ignite_non_multicast_discovery_port_count of this Buffer.
        :rtype: int
        """
        return self._ignite_non_multicast_discovery_port_count

    @ignite_non_multicast_discovery_port_count.setter
    def ignite_non_multicast_discovery_port_count(self, ignite_non_multicast_discovery_port_count: int):
        """Sets the ignite_non_multicast_discovery_port_count of this Buffer.


        :param ignite_non_multicast_discovery_port_count: The ignite_non_multicast_discovery_port_count of this Buffer.
        :type ignite_non_multicast_discovery_port_count: int
        """

        self._ignite_non_multicast_discovery_port_count = ignite_non_multicast_discovery_port_count

    @property
    def ignite_communication_port(self) -> int:
        """Gets the ignite_communication_port of this Buffer.


        :return: The ignite_communication_port of this Buffer.
        :rtype: int
        """
        return self._ignite_communication_port

    @ignite_communication_port.setter
    def ignite_communication_port(self, ignite_communication_port: int):
        """Sets the ignite_communication_port of this Buffer.


        :param ignite_communication_port: The ignite_communication_port of this Buffer.
        :type ignite_communication_port: int
        """

        self._ignite_communication_port = ignite_communication_port

    @property
    def ignite_communication_port_count(self) -> int:
        """Gets the ignite_communication_port_count of this Buffer.


        :return: The ignite_communication_port_count of this Buffer.
        :rtype: int
        """
        return self._ignite_communication_port_count

    @ignite_communication_port_count.setter
    def ignite_communication_port_count(self, ignite_communication_port_count: int):
        """Sets the ignite_communication_port_count of this Buffer.


        :param ignite_communication_port_count: The ignite_communication_port_count of this Buffer.
        :type ignite_communication_port_count: int
        """

        self._ignite_communication_port_count = ignite_communication_port_count

    @property
    def ignite_host(self) -> str:
        """Gets the ignite_host of this Buffer.


        :return: The ignite_host of this Buffer.
        :rtype: str
        """
        return self._ignite_host

    @ignite_host.setter
    def ignite_host(self, ignite_host: str):
        """Sets the ignite_host of this Buffer.


        :param ignite_host: The ignite_host of this Buffer.
        :type ignite_host: str
        """

        self._ignite_host = ignite_host

    @property
    def ignite_worker_timeout_milliseconds(self) -> int:
        """Gets the ignite_worker_timeout_milliseconds of this Buffer.


        :return: The ignite_worker_timeout_milliseconds of this Buffer.
        :rtype: int
        """
        return self._ignite_worker_timeout_milliseconds

    @ignite_worker_timeout_milliseconds.setter
    def ignite_worker_timeout_milliseconds(self, ignite_worker_timeout_milliseconds: int):
        """Sets the ignite_worker_timeout_milliseconds of this Buffer.


        :param ignite_worker_timeout_milliseconds: The ignite_worker_timeout_milliseconds of this Buffer.
        :type ignite_worker_timeout_milliseconds: int
        """

        self._ignite_worker_timeout_milliseconds = ignite_worker_timeout_milliseconds
