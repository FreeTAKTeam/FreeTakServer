import connexion
import six

from swagger_server.models.api_response_external_mission_data import ApiResponseExternalMissionData  # noqa: E501
from swagger_server.models.api_response_list_entry_string_string import ApiResponseListEntryStringString  # noqa: E501
from swagger_server.models.api_response_list_log_entry import ApiResponseListLogEntry  # noqa: E501
from swagger_server.models.api_response_list_mission import ApiResponseListMission  # noqa: E501
from swagger_server.models.api_response_list_mission_change import ApiResponseListMissionChange  # noqa: E501
from swagger_server.models.api_response_list_mission_invitation import ApiResponseListMissionInvitation  # noqa: E501
from swagger_server.models.api_response_list_mission_subscription import ApiResponseListMissionSubscription  # noqa: E501
from swagger_server.models.api_response_list_resource import ApiResponseListResource  # noqa: E501
from swagger_server.models.api_response_list_string import ApiResponseListString  # noqa: E501
from swagger_server.models.api_response_log_entry import ApiResponseLogEntry  # noqa: E501
from swagger_server.models.api_response_map_layer import ApiResponseMapLayer  # noqa: E501
from swagger_server.models.api_response_mission import ApiResponseMission  # noqa: E501
from swagger_server.models.api_response_mission_role import ApiResponseMissionRole  # noqa: E501
from swagger_server.models.api_response_mission_subscription import ApiResponseMissionSubscription  # noqa: E501
from swagger_server.models.api_response_navigable_set_resource import ApiResponseNavigableSetResource  # noqa: E501
from swagger_server.models.api_response_set_mission import ApiResponseSetMission  # noqa: E501
from swagger_server.models.api_response_set_mission_change import ApiResponseSetMissionChange  # noqa: E501
from swagger_server.models.api_response_set_mission_invitation import ApiResponseSetMissionInvitation  # noqa: E501
from swagger_server.models.api_response_set_string import ApiResponseSetString  # noqa: E501
from swagger_server.models.api_response_string import ApiResponseString  # noqa: E501
from swagger_server.models.contents_missionpackage_body import ContentsMissionpackageBody  # noqa: E501
from swagger_server.models.external_mission_data import ExternalMissionData  # noqa: E501
from swagger_server.models.log_entry import LogEntry  # noqa: E501
from swagger_server.models.map_layer import MapLayer  # noqa: E501
from swagger_server.models.mission_content import MissionContent  # noqa: E501
from swagger_server.models.mission_subscription import MissionSubscription  # noqa: E501
from swagger_server.models.missions_name_body import MissionsNameBody  # noqa: E501
from swagger_server.models.remote_subscription import RemoteSubscription  # noqa: E501
from swagger_server import util


def add_content_keyword(body, name, hash, creator_uid=None):  # noqa: E501
    """add_content_keyword

     # noqa: E501

    :param body: 
    :type body: List[]
    :param name: 
    :type name: str
    :param hash: 
    :type hash: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def add_feed(mission_name, creator_uid, data_feed_uid, filter_bbox=None, filter_type=None, filter_callsign=None):  # noqa: E501
    """add_feed

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param creator_uid: 
    :type creator_uid: str
    :param data_feed_uid: 
    :type data_feed_uid: str
    :param filter_bbox: 
    :type filter_bbox: str
    :param filter_type: 
    :type filter_type: str
    :param filter_callsign: 
    :type filter_callsign: str

    :rtype: None
    """
    return 'do some magic!'


def add_mission_content(body, name, creator_uid=None):  # noqa: E501
    """add_mission_content

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: ApiResponseSetMission
    """
    if connexion.request.is_json:
        body = MissionContent.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_mission_package(body, creator_uid, name):  # noqa: E501
    """add_mission_package

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param name: 
    :type name: str

    :rtype: ApiResponseListMissionChange
    """
    if connexion.request.is_json:
        body = ContentsMissionpackageBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def add_uid_keyword(body, name, uid, creator_uid=None):  # noqa: E501
    """add_uid_keyword

     # noqa: E501

    :param body: 
    :type body: List[]
    :param name: 
    :type name: str
    :param uid: 
    :type uid: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def clear_content_keywords(name, hash, creator_uid=None):  # noqa: E501
    """clear_content_keywords

     # noqa: E501

    :param name: 
    :type name: str
    :param hash: 
    :type hash: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def clear_keywords(name, creator_uid=None):  # noqa: E501
    """clear_keywords

     # noqa: E501

    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def clear_parent(child_name):  # noqa: E501
    """clear_parent

     # noqa: E501

    :param child_name: 
    :type child_name: str

    :rtype: None
    """
    return 'do some magic!'


def clear_uid_keywords(name, uid, creator_uid=None):  # noqa: E501
    """clear_uid_keywords

     # noqa: E501

    :param name: 
    :type name: str
    :param uid: 
    :type uid: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def copy_mission(mission_name, creator_uid, copy_name, copy_path=None, default_role=None, password=None):  # noqa: E501
    """copy_mission

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param creator_uid: 
    :type creator_uid: str
    :param copy_name: 
    :type copy_name: str
    :param copy_path: 
    :type copy_path: str
    :param default_role: 
    :type default_role: str
    :param password: 
    :type password: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def create_map_layer(body, creator_uid, mission_name):  # noqa: E501
    """create_map_layer

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseMapLayer
    """
    if connexion.request.is_json:
        body = MapLayer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_mission(name, body=None, creator_uid=None, group=None, description=None, chat_room=None, base_layer=None, bbox=None, bounding_polygon=None, path=None, classification=None, tool=None, password=None, default_role=None, expiration=None):  # noqa: E501
    """create_mission

     # noqa: E501

    :param name: 
    :type name: str
    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param group: 
    :type group: List[str]
    :param description: 
    :type description: str
    :param chat_room: 
    :type chat_room: str
    :param base_layer: 
    :type base_layer: str
    :param bbox: 
    :type bbox: str
    :param bounding_polygon: 
    :type bounding_polygon: List[str]
    :param path: 
    :type path: str
    :param classification: 
    :type classification: str
    :param tool: 
    :type tool: str
    :param password: 
    :type password: str
    :param default_role: 
    :type default_role: str
    :param expiration: 
    :type expiration: int

    :rtype: ApiResponseSetMission
    """
    if connexion.request.is_json:
        body = MissionsNameBody.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def create_mission_subscription(mission_name, uid=None, topic=None, password=None, secago=None, start=None, end=None):  # noqa: E501
    """create_mission_subscription

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param uid: 
    :type uid: str
    :param topic: 
    :type topic: str
    :param password: 
    :type password: str
    :param secago: 
    :type secago: int
    :param start: 
    :type start: str
    :param end: 
    :type end: str

    :rtype: ApiResponseMissionSubscription
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'


def delete_external_mission_data(name, id, notes, creator_uid):  # noqa: E501
    """delete_external_mission_data

     # noqa: E501

    :param name: 
    :type name: str
    :param id: 
    :type id: str
    :param notes: 
    :type notes: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def delete_log_entry(id):  # noqa: E501
    """delete_log_entry

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: None
    """
    return 'do some magic!'


def delete_map_layer(mission_name, creator_uid, uid):  # noqa: E501
    """delete_map_layer

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param creator_uid: 
    :type creator_uid: str
    :param uid: 
    :type uid: str

    :rtype: None
    """
    return 'do some magic!'


def delete_mission(name, creator_uid=None, deep_delete=None):  # noqa: E501
    """delete_mission

     # noqa: E501

    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str
    :param deep_delete: 
    :type deep_delete: bool

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def delete_mission_subscription(mission_name, uid=None, topic=None, disconnect_only=None):  # noqa: E501
    """delete_mission_subscription

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param uid: 
    :type uid: str
    :param topic: 
    :type topic: str
    :param disconnect_only: 
    :type disconnect_only: bool

    :rtype: None
    """
    return 'do some magic!'


def get_all_log_entries():  # noqa: E501
    """get_all_log_entries

     # noqa: E501


    :rtype: ApiResponseListLogEntry
    """
    return 'do some magic!'


def get_all_mission_invitations(client_uid=None):  # noqa: E501
    """get_all_mission_invitations

     # noqa: E501

    :param client_uid: 
    :type client_uid: str

    :rtype: ApiResponseSetString
    """
    return 'do some magic!'


def get_all_mission_invitations_with_passwords(client_uid):  # noqa: E501
    """get_all_mission_invitations_with_passwords

     # noqa: E501

    :param client_uid: 
    :type client_uid: str

    :rtype: ApiResponseSetMissionInvitation
    """
    return 'do some magic!'


def get_all_mission_subscriptions():  # noqa: E501
    """get_all_mission_subscriptions

     # noqa: E501


    :rtype: ApiResponseListEntryStringString
    """
    return 'do some magic!'


def get_all_missions(password_protected=None, default_role=None, tool=None):  # noqa: E501
    """get_all_missions

     # noqa: E501

    :param password_protected: 
    :type password_protected: bool
    :param default_role: 
    :type default_role: bool
    :param tool: 
    :type tool: str

    :rtype: ApiResponseListMission
    """
    return 'do some magic!'


def get_children(name):  # noqa: E501
    """get_children

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def get_kml(name, download=None):  # noqa: E501
    """get_kml

     # noqa: E501

    :param name: 
    :type name: str
    :param download: 
    :type download: bool

    :rtype: str
    """
    return 'do some magic!'


def get_latest_mission_cot_events(name):  # noqa: E501
    """get_latest_mission_cot_events

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: str
    """
    return 'do some magic!'


def get_log_entry(mission_name, secago=None, start=None, end=None):  # noqa: E501
    """get_log_entry

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param secago: 
    :type secago: int
    :param start: 
    :type start: str
    :param end: 
    :type end: str

    :rtype: ApiResponseListLogEntry
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'


def get_mission(name, password=None, changes=None, logs=None, secago=None, start=None, end=None):  # noqa: E501
    """get_mission

     # noqa: E501

    :param name: 
    :type name: str
    :param password: 
    :type password: str
    :param changes: 
    :type changes: bool
    :param logs: 
    :type logs: bool
    :param secago: 
    :type secago: int
    :param start: 
    :type start: str
    :param end: 
    :type end: str

    :rtype: ApiResponseSetMission
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'


def get_mission_archive(name):  # noqa: E501
    """get_mission_archive

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: List[bytearray]
    """
    return 'do some magic!'


def get_mission_changes(name, secago=None, start=None, end=None, squashed=None):  # noqa: E501
    """get_mission_changes

     # noqa: E501

    :param name: 
    :type name: str
    :param secago: 
    :type secago: int
    :param start: 
    :type start: str
    :param end: 
    :type end: str
    :param squashed: 
    :type squashed: bool

    :rtype: ApiResponseSetMissionChange
    """
    start = util.deserialize_datetime(start)
    end = util.deserialize_datetime(end)
    return 'do some magic!'


def get_mission_invitations(mission_name):  # noqa: E501
    """get_mission_invitations

     # noqa: E501

    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseListMissionInvitation
    """
    return 'do some magic!'


def get_mission_role_from_token(mission_name):  # noqa: E501
    """get_mission_role_from_token

     # noqa: E501

    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseMissionRole
    """
    return 'do some magic!'


def get_mission_subscription_roles(mission_name):  # noqa: E501
    """get_mission_subscription_roles

     # noqa: E501

    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseListMissionSubscription
    """
    return 'do some magic!'


def get_mission_subscriptions(mission_name):  # noqa: E501
    """get_mission_subscriptions

     # noqa: E501

    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseListString
    """
    return 'do some magic!'


def get_one_log_entry(id):  # noqa: E501
    """get_one_log_entry

     # noqa: E501

    :param id: 
    :type id: str

    :rtype: ApiResponseListLogEntry
    """
    return 'do some magic!'


def get_parent(name):  # noqa: E501
    """get_parent

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseMission
    """
    return 'do some magic!'


def get_read_only_access_token(mission_name, password=None):  # noqa: E501
    """get_read_only_access_token

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param password: 
    :type password: str

    :rtype: ApiResponseString
    """
    return 'do some magic!'


def get_resource(hash):  # noqa: E501
    """get_resource

     # noqa: E501

    :param hash: 
    :type hash: str

    :rtype: ApiResponseListResource
    """
    return 'do some magic!'


def get_subscription_for_user(mission_name, uid=None):  # noqa: E501
    """get_subscription_for_user

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param uid: 
    :type uid: str

    :rtype: ApiResponseMissionSubscription
    """
    return 'do some magic!'


def invite_to_mission(name, type, invitee, creator_uid, role=None):  # noqa: E501
    """invite_to_mission

     # noqa: E501

    :param name: 
    :type name: str
    :param type: 
    :type type: str
    :param invitee: 
    :type invitee: str
    :param creator_uid: 
    :type creator_uid: str
    :param role: 
    :type role: str

    :rtype: None
    """
    return 'do some magic!'


def notify_external_data_changed(body, creator_uid, notes, name, id):  # noqa: E501
    """notify_external_data_changed

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param notes: 
    :type notes: str
    :param name: 
    :type name: str
    :param id: 
    :type id: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = str.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def post_log_entry(body):  # noqa: E501
    """post_log_entry

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseLogEntry
    """
    if connexion.request.is_json:
        body = LogEntry.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def remove_feed(mission_name, uid, creator_uid):  # noqa: E501
    """remove_feed

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param uid: 
    :type uid: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def remove_keyword(name, keyword, creator_uid=None):  # noqa: E501
    """remove_keyword

     # noqa: E501

    :param name: 
    :type name: str
    :param keyword: 
    :type keyword: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def remove_mission_content(name, hash=None, uid=None, creator_uid=None):  # noqa: E501
    """remove_mission_content

     # noqa: E501

    :param name: 
    :type name: str
    :param hash: 
    :type hash: str
    :param uid: 
    :type uid: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def remove_password(name, creator_uid=None):  # noqa: E501
    """remove_password

     # noqa: E501

    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def results(name):  # noqa: E501
    """results

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: List[RemoteSubscription]
    """
    return 'do some magic!'


def search_sync(box=None, circle=None, start_time=None, end_time=None, min_altitude=None, max_altitude=None, filename=None, keyword=None, mimetype=None, name=None, uid=None, hash=None, mission=None, tool=None):  # noqa: E501
    """search_sync

     # noqa: E501

    :param box: 
    :type box: str
    :param circle: 
    :type circle: str
    :param start_time: 
    :type start_time: str
    :param end_time: 
    :type end_time: str
    :param min_altitude: 
    :type min_altitude: float
    :param max_altitude: 
    :type max_altitude: float
    :param filename: 
    :type filename: str
    :param keyword: 
    :type keyword: List[str]
    :param mimetype: 
    :type mimetype: str
    :param name: 
    :type name: str
    :param uid: 
    :type uid: str
    :param hash: 
    :type hash: str
    :param mission: 
    :type mission: str
    :param tool: 
    :type tool: str

    :rtype: ApiResponseNavigableSetResource
    """
    start_time = util.deserialize_datetime(start_time)
    end_time = util.deserialize_datetime(end_time)
    return 'do some magic!'


def send_mission_archive(name):  # noqa: E501
    """send_mission_archive

     # noqa: E501

    :param name: 
    :type name: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def send_mission_invites(name, creator_uid=None):  # noqa: E501
    """send_mission_invites

     # noqa: E501

    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def set_expiration1(name, expiration=None):  # noqa: E501
    """set_expiration1

     # noqa: E501

    :param name: 
    :type name: str
    :param expiration: 
    :type expiration: int

    :rtype: None
    """
    return 'do some magic!'


def set_external_mission_data(body, creator_uid, name):  # noqa: E501
    """set_external_mission_data

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param name: 
    :type name: str

    :rtype: ApiResponseExternalMissionData
    """
    if connexion.request.is_json:
        body = ExternalMissionData.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def set_keywords(body, name, creator_uid=None):  # noqa: E501
    """set_keywords

     # noqa: E501

    :param body: 
    :type body: List[]
    :param name: 
    :type name: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: ApiResponseSetMission
    """
    return 'do some magic!'


def set_mission_role(mission_name, client_uid=None, username=None, role=None):  # noqa: E501
    """set_mission_role

     # noqa: E501

    :param mission_name: 
    :type mission_name: str
    :param client_uid: 
    :type client_uid: str
    :param username: 
    :type username: str
    :param role: 
    :type role: str

    :rtype: None
    """
    return 'do some magic!'


def set_parent(child_name, parent_name):  # noqa: E501
    """set_parent

     # noqa: E501

    :param child_name: 
    :type child_name: str
    :param parent_name: 
    :type parent_name: str

    :rtype: None
    """
    return 'do some magic!'


def set_password(name, password=None, creator_uid=None):  # noqa: E501
    """set_password

     # noqa: E501

    :param name: 
    :type name: str
    :param password: 
    :type password: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def set_subscription_role(body, creator_uid, mission_name):  # noqa: E501
    """set_subscription_role

     # noqa: E501

    :param body: 
    :type body: list | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param mission_name: 
    :type mission_name: str

    :rtype: None
    """
    if connexion.request.is_json:
        body = [MissionSubscription.from_dict(d) for d in connexion.request.get_json()]  # noqa: E501
    return 'do some magic!'


def uninvite_from_mission(name, type, invitee, creator_uid):  # noqa: E501
    """uninvite_from_mission

     # noqa: E501

    :param name: 
    :type name: str
    :param type: 
    :type type: str
    :param invitee: 
    :type invitee: str
    :param creator_uid: 
    :type creator_uid: str

    :rtype: None
    """
    return 'do some magic!'


def update_log_entry(body):  # noqa: E501
    """update_log_entry

     # noqa: E501

    :param body: 
    :type body: dict | bytes

    :rtype: ApiResponseLogEntry
    """
    if connexion.request.is_json:
        body = LogEntry.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'


def update_map_layer(body, creator_uid, mission_name):  # noqa: E501
    """update_map_layer

     # noqa: E501

    :param body: 
    :type body: dict | bytes
    :param creator_uid: 
    :type creator_uid: str
    :param mission_name: 
    :type mission_name: str

    :rtype: ApiResponseMapLayer
    """
    if connexion.request.is_json:
        body = MapLayer.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
