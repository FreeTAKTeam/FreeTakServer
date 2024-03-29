# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.group import Group  # noqa: F401,E501
from swagger_server.models.remote_subscription_metrics import RemoteSubscriptionMetrics  # noqa: F401,E501
from swagger_server import util


class SubscriptionInfo(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    def __init__(self, dn: str=None, callsign: str=None, client_uid: str=None, last_report_milliseconds: int=None, tak_client: str=None, tak_version: str=None, username: str=None, groups: List[Group]=None, role: str=None, team: str=None, ip_address: str=None, port: str=None, pending_writes: int=None, num_processed: int=None, protocol: str=None, xpath: str=None, subscription_uid: str=None, app_framerate: str=None, battery: str=None, battery_status: str=None, battery_temp: str=None, device_data_rx: str=None, device_data_tx: str=None, heap_current_size: str=None, heap_free_size: str=None, heap_max_size: str=None, device_ip_address: str=None, storage_available: str=None, storage_total: str=None, incognito: bool=None, handler_type: str=None, last_report_diff_milliseconds: int=None, metrics: RemoteSubscriptionMetrics=None):  # noqa: E501
        """SubscriptionInfo - a model defined in Swagger

        :param dn: The dn of this SubscriptionInfo.  # noqa: E501
        :type dn: str
        :param callsign: The callsign of this SubscriptionInfo.  # noqa: E501
        :type callsign: str
        :param client_uid: The client_uid of this SubscriptionInfo.  # noqa: E501
        :type client_uid: str
        :param last_report_milliseconds: The last_report_milliseconds of this SubscriptionInfo.  # noqa: E501
        :type last_report_milliseconds: int
        :param tak_client: The tak_client of this SubscriptionInfo.  # noqa: E501
        :type tak_client: str
        :param tak_version: The tak_version of this SubscriptionInfo.  # noqa: E501
        :type tak_version: str
        :param username: The username of this SubscriptionInfo.  # noqa: E501
        :type username: str
        :param groups: The groups of this SubscriptionInfo.  # noqa: E501
        :type groups: List[Group]
        :param role: The role of this SubscriptionInfo.  # noqa: E501
        :type role: str
        :param team: The team of this SubscriptionInfo.  # noqa: E501
        :type team: str
        :param ip_address: The ip_address of this SubscriptionInfo.  # noqa: E501
        :type ip_address: str
        :param port: The port of this SubscriptionInfo.  # noqa: E501
        :type port: str
        :param pending_writes: The pending_writes of this SubscriptionInfo.  # noqa: E501
        :type pending_writes: int
        :param num_processed: The num_processed of this SubscriptionInfo.  # noqa: E501
        :type num_processed: int
        :param protocol: The protocol of this SubscriptionInfo.  # noqa: E501
        :type protocol: str
        :param xpath: The xpath of this SubscriptionInfo.  # noqa: E501
        :type xpath: str
        :param subscription_uid: The subscription_uid of this SubscriptionInfo.  # noqa: E501
        :type subscription_uid: str
        :param app_framerate: The app_framerate of this SubscriptionInfo.  # noqa: E501
        :type app_framerate: str
        :param battery: The battery of this SubscriptionInfo.  # noqa: E501
        :type battery: str
        :param battery_status: The battery_status of this SubscriptionInfo.  # noqa: E501
        :type battery_status: str
        :param battery_temp: The battery_temp of this SubscriptionInfo.  # noqa: E501
        :type battery_temp: str
        :param device_data_rx: The device_data_rx of this SubscriptionInfo.  # noqa: E501
        :type device_data_rx: str
        :param device_data_tx: The device_data_tx of this SubscriptionInfo.  # noqa: E501
        :type device_data_tx: str
        :param heap_current_size: The heap_current_size of this SubscriptionInfo.  # noqa: E501
        :type heap_current_size: str
        :param heap_free_size: The heap_free_size of this SubscriptionInfo.  # noqa: E501
        :type heap_free_size: str
        :param heap_max_size: The heap_max_size of this SubscriptionInfo.  # noqa: E501
        :type heap_max_size: str
        :param device_ip_address: The device_ip_address of this SubscriptionInfo.  # noqa: E501
        :type device_ip_address: str
        :param storage_available: The storage_available of this SubscriptionInfo.  # noqa: E501
        :type storage_available: str
        :param storage_total: The storage_total of this SubscriptionInfo.  # noqa: E501
        :type storage_total: str
        :param incognito: The incognito of this SubscriptionInfo.  # noqa: E501
        :type incognito: bool
        :param handler_type: The handler_type of this SubscriptionInfo.  # noqa: E501
        :type handler_type: str
        :param last_report_diff_milliseconds: The last_report_diff_milliseconds of this SubscriptionInfo.  # noqa: E501
        :type last_report_diff_milliseconds: int
        :param metrics: The metrics of this SubscriptionInfo.  # noqa: E501
        :type metrics: RemoteSubscriptionMetrics
        """
        self.swagger_types = {
            'dn': str,
            'callsign': str,
            'client_uid': str,
            'last_report_milliseconds': int,
            'tak_client': str,
            'tak_version': str,
            'username': str,
            'groups': List[Group],
            'role': str,
            'team': str,
            'ip_address': str,
            'port': str,
            'pending_writes': int,
            'num_processed': int,
            'protocol': str,
            'xpath': str,
            'subscription_uid': str,
            'app_framerate': str,
            'battery': str,
            'battery_status': str,
            'battery_temp': str,
            'device_data_rx': str,
            'device_data_tx': str,
            'heap_current_size': str,
            'heap_free_size': str,
            'heap_max_size': str,
            'device_ip_address': str,
            'storage_available': str,
            'storage_total': str,
            'incognito': bool,
            'handler_type': str,
            'last_report_diff_milliseconds': int,
            'metrics': RemoteSubscriptionMetrics
        }

        self.attribute_map = {
            'dn': 'dn',
            'callsign': 'callsign',
            'client_uid': 'clientUid',
            'last_report_milliseconds': 'lastReportMilliseconds',
            'tak_client': 'takClient',
            'tak_version': 'takVersion',
            'username': 'username',
            'groups': 'groups',
            'role': 'role',
            'team': 'team',
            'ip_address': 'ipAddress',
            'port': 'port',
            'pending_writes': 'pendingWrites',
            'num_processed': 'numProcessed',
            'protocol': 'protocol',
            'xpath': 'xpath',
            'subscription_uid': 'subscriptionUid',
            'app_framerate': 'appFramerate',
            'battery': 'battery',
            'battery_status': 'batteryStatus',
            'battery_temp': 'batteryTemp',
            'device_data_rx': 'deviceDataRx',
            'device_data_tx': 'deviceDataTx',
            'heap_current_size': 'heapCurrentSize',
            'heap_free_size': 'heapFreeSize',
            'heap_max_size': 'heapMaxSize',
            'device_ip_address': 'deviceIPAddress',
            'storage_available': 'storageAvailable',
            'storage_total': 'storageTotal',
            'incognito': 'incognito',
            'handler_type': 'handlerType',
            'last_report_diff_milliseconds': 'lastReportDiffMilliseconds',
            'metrics': 'metrics'
        }
        self._dn = dn
        self._callsign = callsign
        self._client_uid = client_uid
        self._last_report_milliseconds = last_report_milliseconds
        self._tak_client = tak_client
        self._tak_version = tak_version
        self._username = username
        self._groups = groups
        self._role = role
        self._team = team
        self._ip_address = ip_address
        self._port = port
        self._pending_writes = pending_writes
        self._num_processed = num_processed
        self._protocol = protocol
        self._xpath = xpath
        self._subscription_uid = subscription_uid
        self._app_framerate = app_framerate
        self._battery = battery
        self._battery_status = battery_status
        self._battery_temp = battery_temp
        self._device_data_rx = device_data_rx
        self._device_data_tx = device_data_tx
        self._heap_current_size = heap_current_size
        self._heap_free_size = heap_free_size
        self._heap_max_size = heap_max_size
        self._device_ip_address = device_ip_address
        self._storage_available = storage_available
        self._storage_total = storage_total
        self._incognito = incognito
        self._handler_type = handler_type
        self._last_report_diff_milliseconds = last_report_diff_milliseconds
        self._metrics = metrics

    @classmethod
    def from_dict(cls, dikt) -> 'SubscriptionInfo':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The SubscriptionInfo of this SubscriptionInfo.  # noqa: E501
        :rtype: SubscriptionInfo
        """
        return util.deserialize_model(dikt, cls)

    @property
    def dn(self) -> str:
        """Gets the dn of this SubscriptionInfo.


        :return: The dn of this SubscriptionInfo.
        :rtype: str
        """
        return self._dn

    @dn.setter
    def dn(self, dn: str):
        """Sets the dn of this SubscriptionInfo.


        :param dn: The dn of this SubscriptionInfo.
        :type dn: str
        """

        self._dn = dn

    @property
    def callsign(self) -> str:
        """Gets the callsign of this SubscriptionInfo.


        :return: The callsign of this SubscriptionInfo.
        :rtype: str
        """
        return self._callsign

    @callsign.setter
    def callsign(self, callsign: str):
        """Sets the callsign of this SubscriptionInfo.


        :param callsign: The callsign of this SubscriptionInfo.
        :type callsign: str
        """

        self._callsign = callsign

    @property
    def client_uid(self) -> str:
        """Gets the client_uid of this SubscriptionInfo.


        :return: The client_uid of this SubscriptionInfo.
        :rtype: str
        """
        return self._client_uid

    @client_uid.setter
    def client_uid(self, client_uid: str):
        """Sets the client_uid of this SubscriptionInfo.


        :param client_uid: The client_uid of this SubscriptionInfo.
        :type client_uid: str
        """

        self._client_uid = client_uid

    @property
    def last_report_milliseconds(self) -> int:
        """Gets the last_report_milliseconds of this SubscriptionInfo.


        :return: The last_report_milliseconds of this SubscriptionInfo.
        :rtype: int
        """
        return self._last_report_milliseconds

    @last_report_milliseconds.setter
    def last_report_milliseconds(self, last_report_milliseconds: int):
        """Sets the last_report_milliseconds of this SubscriptionInfo.


        :param last_report_milliseconds: The last_report_milliseconds of this SubscriptionInfo.
        :type last_report_milliseconds: int
        """

        self._last_report_milliseconds = last_report_milliseconds

    @property
    def tak_client(self) -> str:
        """Gets the tak_client of this SubscriptionInfo.


        :return: The tak_client of this SubscriptionInfo.
        :rtype: str
        """
        return self._tak_client

    @tak_client.setter
    def tak_client(self, tak_client: str):
        """Sets the tak_client of this SubscriptionInfo.


        :param tak_client: The tak_client of this SubscriptionInfo.
        :type tak_client: str
        """

        self._tak_client = tak_client

    @property
    def tak_version(self) -> str:
        """Gets the tak_version of this SubscriptionInfo.


        :return: The tak_version of this SubscriptionInfo.
        :rtype: str
        """
        return self._tak_version

    @tak_version.setter
    def tak_version(self, tak_version: str):
        """Sets the tak_version of this SubscriptionInfo.


        :param tak_version: The tak_version of this SubscriptionInfo.
        :type tak_version: str
        """

        self._tak_version = tak_version

    @property
    def username(self) -> str:
        """Gets the username of this SubscriptionInfo.


        :return: The username of this SubscriptionInfo.
        :rtype: str
        """
        return self._username

    @username.setter
    def username(self, username: str):
        """Sets the username of this SubscriptionInfo.


        :param username: The username of this SubscriptionInfo.
        :type username: str
        """

        self._username = username

    @property
    def groups(self) -> List[Group]:
        """Gets the groups of this SubscriptionInfo.


        :return: The groups of this SubscriptionInfo.
        :rtype: List[Group]
        """
        return self._groups

    @groups.setter
    def groups(self, groups: List[Group]):
        """Sets the groups of this SubscriptionInfo.


        :param groups: The groups of this SubscriptionInfo.
        :type groups: List[Group]
        """

        self._groups = groups

    @property
    def role(self) -> str:
        """Gets the role of this SubscriptionInfo.


        :return: The role of this SubscriptionInfo.
        :rtype: str
        """
        return self._role

    @role.setter
    def role(self, role: str):
        """Sets the role of this SubscriptionInfo.


        :param role: The role of this SubscriptionInfo.
        :type role: str
        """

        self._role = role

    @property
    def team(self) -> str:
        """Gets the team of this SubscriptionInfo.


        :return: The team of this SubscriptionInfo.
        :rtype: str
        """
        return self._team

    @team.setter
    def team(self, team: str):
        """Sets the team of this SubscriptionInfo.


        :param team: The team of this SubscriptionInfo.
        :type team: str
        """

        self._team = team

    @property
    def ip_address(self) -> str:
        """Gets the ip_address of this SubscriptionInfo.


        :return: The ip_address of this SubscriptionInfo.
        :rtype: str
        """
        return self._ip_address

    @ip_address.setter
    def ip_address(self, ip_address: str):
        """Sets the ip_address of this SubscriptionInfo.


        :param ip_address: The ip_address of this SubscriptionInfo.
        :type ip_address: str
        """

        self._ip_address = ip_address

    @property
    def port(self) -> str:
        """Gets the port of this SubscriptionInfo.


        :return: The port of this SubscriptionInfo.
        :rtype: str
        """
        return self._port

    @port.setter
    def port(self, port: str):
        """Sets the port of this SubscriptionInfo.


        :param port: The port of this SubscriptionInfo.
        :type port: str
        """

        self._port = port

    @property
    def pending_writes(self) -> int:
        """Gets the pending_writes of this SubscriptionInfo.


        :return: The pending_writes of this SubscriptionInfo.
        :rtype: int
        """
        return self._pending_writes

    @pending_writes.setter
    def pending_writes(self, pending_writes: int):
        """Sets the pending_writes of this SubscriptionInfo.


        :param pending_writes: The pending_writes of this SubscriptionInfo.
        :type pending_writes: int
        """

        self._pending_writes = pending_writes

    @property
    def num_processed(self) -> int:
        """Gets the num_processed of this SubscriptionInfo.


        :return: The num_processed of this SubscriptionInfo.
        :rtype: int
        """
        return self._num_processed

    @num_processed.setter
    def num_processed(self, num_processed: int):
        """Sets the num_processed of this SubscriptionInfo.


        :param num_processed: The num_processed of this SubscriptionInfo.
        :type num_processed: int
        """

        self._num_processed = num_processed

    @property
    def protocol(self) -> str:
        """Gets the protocol of this SubscriptionInfo.


        :return: The protocol of this SubscriptionInfo.
        :rtype: str
        """
        return self._protocol

    @protocol.setter
    def protocol(self, protocol: str):
        """Sets the protocol of this SubscriptionInfo.


        :param protocol: The protocol of this SubscriptionInfo.
        :type protocol: str
        """

        self._protocol = protocol

    @property
    def xpath(self) -> str:
        """Gets the xpath of this SubscriptionInfo.


        :return: The xpath of this SubscriptionInfo.
        :rtype: str
        """
        return self._xpath

    @xpath.setter
    def xpath(self, xpath: str):
        """Sets the xpath of this SubscriptionInfo.


        :param xpath: The xpath of this SubscriptionInfo.
        :type xpath: str
        """

        self._xpath = xpath

    @property
    def subscription_uid(self) -> str:
        """Gets the subscription_uid of this SubscriptionInfo.


        :return: The subscription_uid of this SubscriptionInfo.
        :rtype: str
        """
        return self._subscription_uid

    @subscription_uid.setter
    def subscription_uid(self, subscription_uid: str):
        """Sets the subscription_uid of this SubscriptionInfo.


        :param subscription_uid: The subscription_uid of this SubscriptionInfo.
        :type subscription_uid: str
        """

        self._subscription_uid = subscription_uid

    @property
    def app_framerate(self) -> str:
        """Gets the app_framerate of this SubscriptionInfo.


        :return: The app_framerate of this SubscriptionInfo.
        :rtype: str
        """
        return self._app_framerate

    @app_framerate.setter
    def app_framerate(self, app_framerate: str):
        """Sets the app_framerate of this SubscriptionInfo.


        :param app_framerate: The app_framerate of this SubscriptionInfo.
        :type app_framerate: str
        """

        self._app_framerate = app_framerate

    @property
    def battery(self) -> str:
        """Gets the battery of this SubscriptionInfo.


        :return: The battery of this SubscriptionInfo.
        :rtype: str
        """
        return self._battery

    @battery.setter
    def battery(self, battery: str):
        """Sets the battery of this SubscriptionInfo.


        :param battery: The battery of this SubscriptionInfo.
        :type battery: str
        """

        self._battery = battery

    @property
    def battery_status(self) -> str:
        """Gets the battery_status of this SubscriptionInfo.


        :return: The battery_status of this SubscriptionInfo.
        :rtype: str
        """
        return self._battery_status

    @battery_status.setter
    def battery_status(self, battery_status: str):
        """Sets the battery_status of this SubscriptionInfo.


        :param battery_status: The battery_status of this SubscriptionInfo.
        :type battery_status: str
        """

        self._battery_status = battery_status

    @property
    def battery_temp(self) -> str:
        """Gets the battery_temp of this SubscriptionInfo.


        :return: The battery_temp of this SubscriptionInfo.
        :rtype: str
        """
        return self._battery_temp

    @battery_temp.setter
    def battery_temp(self, battery_temp: str):
        """Sets the battery_temp of this SubscriptionInfo.


        :param battery_temp: The battery_temp of this SubscriptionInfo.
        :type battery_temp: str
        """

        self._battery_temp = battery_temp

    @property
    def device_data_rx(self) -> str:
        """Gets the device_data_rx of this SubscriptionInfo.


        :return: The device_data_rx of this SubscriptionInfo.
        :rtype: str
        """
        return self._device_data_rx

    @device_data_rx.setter
    def device_data_rx(self, device_data_rx: str):
        """Sets the device_data_rx of this SubscriptionInfo.


        :param device_data_rx: The device_data_rx of this SubscriptionInfo.
        :type device_data_rx: str
        """

        self._device_data_rx = device_data_rx

    @property
    def device_data_tx(self) -> str:
        """Gets the device_data_tx of this SubscriptionInfo.


        :return: The device_data_tx of this SubscriptionInfo.
        :rtype: str
        """
        return self._device_data_tx

    @device_data_tx.setter
    def device_data_tx(self, device_data_tx: str):
        """Sets the device_data_tx of this SubscriptionInfo.


        :param device_data_tx: The device_data_tx of this SubscriptionInfo.
        :type device_data_tx: str
        """

        self._device_data_tx = device_data_tx

    @property
    def heap_current_size(self) -> str:
        """Gets the heap_current_size of this SubscriptionInfo.


        :return: The heap_current_size of this SubscriptionInfo.
        :rtype: str
        """
        return self._heap_current_size

    @heap_current_size.setter
    def heap_current_size(self, heap_current_size: str):
        """Sets the heap_current_size of this SubscriptionInfo.


        :param heap_current_size: The heap_current_size of this SubscriptionInfo.
        :type heap_current_size: str
        """

        self._heap_current_size = heap_current_size

    @property
    def heap_free_size(self) -> str:
        """Gets the heap_free_size of this SubscriptionInfo.


        :return: The heap_free_size of this SubscriptionInfo.
        :rtype: str
        """
        return self._heap_free_size

    @heap_free_size.setter
    def heap_free_size(self, heap_free_size: str):
        """Sets the heap_free_size of this SubscriptionInfo.


        :param heap_free_size: The heap_free_size of this SubscriptionInfo.
        :type heap_free_size: str
        """

        self._heap_free_size = heap_free_size

    @property
    def heap_max_size(self) -> str:
        """Gets the heap_max_size of this SubscriptionInfo.


        :return: The heap_max_size of this SubscriptionInfo.
        :rtype: str
        """
        return self._heap_max_size

    @heap_max_size.setter
    def heap_max_size(self, heap_max_size: str):
        """Sets the heap_max_size of this SubscriptionInfo.


        :param heap_max_size: The heap_max_size of this SubscriptionInfo.
        :type heap_max_size: str
        """

        self._heap_max_size = heap_max_size

    @property
    def device_ip_address(self) -> str:
        """Gets the device_ip_address of this SubscriptionInfo.


        :return: The device_ip_address of this SubscriptionInfo.
        :rtype: str
        """
        return self._device_ip_address

    @device_ip_address.setter
    def device_ip_address(self, device_ip_address: str):
        """Sets the device_ip_address of this SubscriptionInfo.


        :param device_ip_address: The device_ip_address of this SubscriptionInfo.
        :type device_ip_address: str
        """

        self._device_ip_address = device_ip_address

    @property
    def storage_available(self) -> str:
        """Gets the storage_available of this SubscriptionInfo.


        :return: The storage_available of this SubscriptionInfo.
        :rtype: str
        """
        return self._storage_available

    @storage_available.setter
    def storage_available(self, storage_available: str):
        """Sets the storage_available of this SubscriptionInfo.


        :param storage_available: The storage_available of this SubscriptionInfo.
        :type storage_available: str
        """

        self._storage_available = storage_available

    @property
    def storage_total(self) -> str:
        """Gets the storage_total of this SubscriptionInfo.


        :return: The storage_total of this SubscriptionInfo.
        :rtype: str
        """
        return self._storage_total

    @storage_total.setter
    def storage_total(self, storage_total: str):
        """Sets the storage_total of this SubscriptionInfo.


        :param storage_total: The storage_total of this SubscriptionInfo.
        :type storage_total: str
        """

        self._storage_total = storage_total

    @property
    def incognito(self) -> bool:
        """Gets the incognito of this SubscriptionInfo.


        :return: The incognito of this SubscriptionInfo.
        :rtype: bool
        """
        return self._incognito

    @incognito.setter
    def incognito(self, incognito: bool):
        """Sets the incognito of this SubscriptionInfo.


        :param incognito: The incognito of this SubscriptionInfo.
        :type incognito: bool
        """

        self._incognito = incognito

    @property
    def handler_type(self) -> str:
        """Gets the handler_type of this SubscriptionInfo.


        :return: The handler_type of this SubscriptionInfo.
        :rtype: str
        """
        return self._handler_type

    @handler_type.setter
    def handler_type(self, handler_type: str):
        """Sets the handler_type of this SubscriptionInfo.


        :param handler_type: The handler_type of this SubscriptionInfo.
        :type handler_type: str
        """

        self._handler_type = handler_type

    @property
    def last_report_diff_milliseconds(self) -> int:
        """Gets the last_report_diff_milliseconds of this SubscriptionInfo.


        :return: The last_report_diff_milliseconds of this SubscriptionInfo.
        :rtype: int
        """
        return self._last_report_diff_milliseconds

    @last_report_diff_milliseconds.setter
    def last_report_diff_milliseconds(self, last_report_diff_milliseconds: int):
        """Sets the last_report_diff_milliseconds of this SubscriptionInfo.


        :param last_report_diff_milliseconds: The last_report_diff_milliseconds of this SubscriptionInfo.
        :type last_report_diff_milliseconds: int
        """

        self._last_report_diff_milliseconds = last_report_diff_milliseconds

    @property
    def metrics(self) -> RemoteSubscriptionMetrics:
        """Gets the metrics of this SubscriptionInfo.


        :return: The metrics of this SubscriptionInfo.
        :rtype: RemoteSubscriptionMetrics
        """
        return self._metrics

    @metrics.setter
    def metrics(self, metrics: RemoteSubscriptionMetrics):
        """Sets the metrics of this SubscriptionInfo.


        :param metrics: The metrics of this SubscriptionInfo.
        :type metrics: RemoteSubscriptionMetrics
        """

        self._metrics = metrics
