import json
from uuid import uuid4
from flask import Blueprint, request
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController

page = Blueprint("mission", __name__)
config = MainConfig.instance()

@page.route('/Marti/api/missions', methods=['GET'])
def get_missions():
    out_data =  HTTPSTakApiCommunicationController().make_request("GetMissions", "mission", {}, None, True).get_value("missions"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/invitations')
def get_invitations():
    client_uid = request.args.get("clientUid", None)
    if client_uid is None:
        return '', 400
    out_data = HTTPSTakApiCommunicationController().make_request("GetInvitations", "mission", {"client_uid": client_uid}, None, synchronous=True).get_value("mission_changes") # type: ignore
    return out_data, 200

@page.route('/Marti/api/groups/all')
def get_groups():
    return {
        "version": "3",
        "type": "com.bbn.marti.remote.groups.Group",
        "data": [
            {
                "name": "__ANON__",
                "direction": "OUT",
                "created": "2023-02-22",
                "type": "SYSTEM",
                "bitpos": 2,
                "active": True
            }
        ],
        "nodeId": config.nodeID
    }
    
@page.route('/Marti/api/missions/<mission_id>', methods=['PUT'])
def put_mission(mission_id):
    from flask import request
    out_data = HTTPSTakApiCommunicationController().make_request("PutMission", "mission", {"mission_id": mission_id, "mission_data": request.data, "mission_data_args": request.args, "creatorUid": request.args.get("creatorUid")}, None, True).get_value("mission_subscription"), 200 # type: ignore
    HTTPSTakApiCommunicationController().make_request("MissionCreatedNotification", "mission", {"mission_id": mission_id}, None, synchronous=False)
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>', methods=['GET'])
def get_mission(mission_id):
    from flask import request
    out_data = HTTPSTakApiCommunicationController().make_request("GetMission", "mission", {"mission_id": mission_id}, None, True).get_value("mission"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>/cot', methods=['GET'])
def get_mission_cots(mission_id):
    """get all cots for a mission"""
    return HTTPSTakApiCommunicationController().make_request("GetMissionCots", "mission", {"mission_id": mission_id}, None, True).get_value("cots"), 200

@page.route('/Marti/api/missions/<mission_id>/contents', methods=['PUT'])
def add_mission_contents(mission_id: str):
    """add contents to a mission

    Args:
        mission_id (str): the id of the mission to add contents to
    """
    request_json = request.get_json() # type: ignore
    return_data = HTTPSTakApiCommunicationController().make_request("AddMissionContents", "mission", {"mission_id": mission_id, "hashes": request_json.get("hashes", []), "uids": request_json.get("uids", [])}, None, True).get_value("mission")
    for hash in request_json.get("hashes", []):
        HTTPSTakApiCommunicationController().make_request("MissionContentCreatedNotification", "mission", {"content_id": hash}, None, synchronous=False)
        
    return return_data, 200

@page.route('/Marti/api/missions/logs/entries', methods=['POST'])
def add_log_entry():
    request_json = request.get_json() # type: ignore
    return_data =  HTTPSTakApiCommunicationController().make_request("AddMissionLog", "mission", {"mission_log_data": request_json}, None, True).get_value("log")
    HTTPSTakApiCommunicationController().make_request("MissionLogCreatedNotification", "mission", {"log_id": json.loads(return_data)["data"][0]["id"]}, None, synchronous=False)
    return return_data, 200

@page.route('/Marti/api/missions/logs/entries', methods=['PUT'])
def update_log_entry():
    request_json = request.get_json() # type: ignore
    return HTTPSTakApiCommunicationController().make_request("UpdateMissionLog", "mission", {"mission_log_data": request_json}, None, True).get_value("log"), 200

@page.route('/Marti/api/missions/logs/entries/<id>', methods=['DELETE'])
def delete_log_entry(id):
    HTTPSTakApiCommunicationController().make_request("DeleteMissionLog", "mission", {"log_id": id}, None, True)
    return "", 200

@page.route('/Marti/api/missions/logs/entries/<id>', methods=['GET'])
def get_log_entry():
    return HTTPSTakApiCommunicationController().make_request("GetMissionLog", "mission", {"log_id": id}, None, True).get_value("log"), 200

@page.route('/Marti/api/missions/<missionID>/log', methods=['GET'])
def get_mission_logs(missionID):
    return HTTPSTakApiCommunicationController().make_request("GetMissionLogs", "mission", {"mission_id": missionID, "seconds_ago": request.args.get("secago"), "start": request.args.get("start"), "end": request.args.get("end")}, None, True).get_value("logs"), 200

@page.route('/Marti/api/missions/all/logs', methods=['GET'])
def get_all_logs():
    return HTTPSTakApiCommunicationController().make_request("GetAllLogs", "mission", {}, None, True).get_value("logs"), 200

@page.route('/Marti/api/missions/<child_mission_id>/parent/<parent_mission_id>', methods=['PUT'])
def add_child_to_parent(child_mission_id, parent_mission_id):
    HTTPSTakApiCommunicationController().make_request("AddChildToParent", "mission", {"child_mission_id": child_mission_id, "parent_mission_id": parent_mission_id}, None, True)
    return '', 200

@page.route('/Marti/api/missions/<child_mission_id>/parent', methods=['DELETE'])
def delete_child(child_mission_id):
    return HTTPSTakApiCommunicationController().make_request("DeleteParent", "mission", {"child_mission_id": child_mission_id}, None, True).get_value("mission"), 200

@page.route('/Marti/api/missions/<parent_mission_id>/children', methods=['GET'])
def get_children(parent_mission_id):
    return HTTPSTakApiCommunicationController().make_request("GetChildren", "mission", {"parent_mission_id": parent_mission_id}, None, True).get_value("children"), 200

@page.route('/Marti/api/missions/<child_mission_id>/parent', methods=['GET'])
def get_parent(child_mission_id):
    return HTTPSTakApiCommunicationController().make_request("GetParent", "mission", {"child_mission_id": child_mission_id}, None, True).get_value("parent"), 200

@page.route('/Marti/api/missions/all/subscriptions', methods=['GET'])
def get_all_subscriptions():
    return HTTPSTakApiCommunicationController().make_request("GetAllSubscriptions", "mission", {}, None, True).get_value("mission_subscriptions"), 200

@page.route('/Marti/api/missions/<mission_id>/subscriptions', methods=['GET'])
def get_mission_subscriptions(mission_id):
    return HTTPSTakApiCommunicationController().make_request("GetMissionSubscriptions", "mission", {"mission_id": mission_id}, None, True).get_value("mission_subscriptions"), 200

@page.route('/Marti/api/missions/<mission_id>/subscription', methods=['PUT'])
def add_mission_subscription(mission_id):
    try:
        uid = request.args.get("uid") # type: ignore
        topic = request.args.get("topic") # type: ignore
        password = request.args.get("password") # type: ignore
        secago = request.args.get("secago") # type: ignore
        start = request.args.get("start") # type: ignore
        end = request.args.get("end") # type: ignore
        mission_subscription_data = HTTPSTakApiCommunicationController().make_request("AddMissionSubscription", "mission", {"mission_id": mission_id, 
                                                                                                    "client": uid, 
                                                                                                    "topic": topic, 
                                                                                                    "password": password, 
                                                                                                    "secago": secago,
                                                                                                    "start": start,
                                                                                                    "end": end},
                                                                None, True).get_value("mission_subscription")
        if mission_subscription_data is not None:
            return mission_subscription_data, 201
        else:
            return '', 404
    except Exception as e:
        print(e)
        return '', 500
@page.route('/Marti/api/missions/<mission_id>/subscription', methods=['DELETE'])
def delete_mission_subscription(mission_id):
    uid = request.args.get("uid") # type: ignore
    topic = request.args.get("topic") # type: ignore
    disconnectOnly = request.args.get("disconnectOnly") # type: ignore
    HTTPSTakApiCommunicationController().make_request("DeleteMissionSubscription", "mission", {"mission_id": mission_id, "client": uid, "topic": topic, "disconnect_only": disconnectOnly}, None, True)
    return '', 200

@page.route('/Marti/api/missions/<mission_id>/subscription', methods=['GET'])
def get_mission_subscription(mission_id):
    uid = request.args.get("uid") # type: ignore
    return HTTPSTakApiCommunicationController().make_request("GetMissionSubscription", "mission", {"mission_id": mission_id, "client": uid}, None, True).get_value("mission_subscription"), 200

@page.route('/Marti/api/missions/<mission_id>/subscriptions/roles', methods=['GET'])
def get_all_mission_subscriptions(mission_id):
    """get all the subscriptions from a mission

    Args:
        mission_id (_type_): _description_
    """
    print("request made to get all mission subscriptions")
    out_data = HTTPSTakApiCommunicationController().make_request("GetMissionSubscriptions", "mission", {"mission_id": mission_id}, None, True).get_value("mission_subscriptions"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>/externaldata', methods=['POST'])
def create_external_mission_data(mission_id):
    """create external mission data

    Args:
        mission_id (_type_): _description_
    """
    request_json = request.get_json() # type: ignore
    out_data = HTTPSTakApiCommunicationController().make_request("CreateExternalMissionData", "mission", {"mission_id": mission_id, "mission_external_data": request_json}, None, True).get_value("external_data"), 200 # type: ignore
    return out_data

@page.route('/Marti/api/missions/<mission_id>/changes', methods=['GET'])
def get_mission_changes(mission_id):
    """get mission changes

    Args:
        mission_id (_type_): _description_
    """
    out_data = HTTPSTakApiCommunicationController().make_request("GetMissionChanges", "mission", {"mission_id": mission_id}, None, True).get_value("mission_changes"), 200
    return out_data

@page.route('/Marti/api/missions/<mission_id>/contents/missionpackage', methods=["PUT"])
def add_mission_content_direct(mission_id):
    filename = request.args.get("filename")
    creatorUid = request.args.get("creatorUid")
    tool = request.args.get("tool", "public")
    if not request.data:
        data = request.files.getlist('assetfile')[0].stream.read()
    else:
        data = request.data

    if request.args.get("hash", None) == None:
        id = str(uuid4())
    else:
        id = request.args.get("hash")

    metadata = HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": id, "tool": tool, "objectdata": data, "objkeywords": [filename, creatorUid, "missionpackage"], "objstarttime": "", "synctype": "content", "mime_type": request.headers["Content-Type"]}, None, True).get_value("objectmetadata") # type: ignore

    HTTPSTakApiCommunicationController().make_request("AddMissionContents", "mission", {"mission_id": mission_id, "hashes": [metadata.hash], "uids": []}, None, True).get_value("mission"),200

    return {
        "version": "3",
        "type": "MissionChange",
        "data": [],
        "nodeId": config.nodeID
    }

@page.route('/Marti/api/missions/<mission_id>/invite/<type>/<invitee>', methods=["PUT"])
def put_mission_invitation(mission_id, type, invitee):
    """post the invitation for a mission"""
    author = request.args.get("creatorUid", "unknown")
    invitedContacts = invitee
    role = request.args.get("role", None)
    try:
        mission = HTTPSTakApiCommunicationController().make_request("GetMission", "mission", {"mission_id": mission_id}, None, True).get_value("mission")
        if mission == None:
            return '{"message": "mission not found"}', 404
        default_mission_role = json.loads(mission)["data"][0]["defaultRole"]["type"]
        if role is None or role == default_mission_role:
            HTTPSTakApiCommunicationController().make_request("SendInvitation", "mission", {"author_uid": author, "mission_id": mission_id, "client_uid": invitedContacts, "role": role}, None, False)
        else:
            return '{"message": "invalid role"}', 405
        return '', 200
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500
    
@page.route('/Marti/api/missions/<mission_id>/invite', methods=["POST"])
def post_mission_invitation(mission_id):
    """post the invitation for a mission"""
    author = request.args.get("creatorUid", "unknown")
    invitedContacts = request.args.get("contacts", None)
    if request.data != b'':
        invitedContacts = json.loads(request.data)[0]["invitee"]
        role = json.loads(request.data)[0]["role"]["type"]

    try:
        mission = HTTPSTakApiCommunicationController().make_request("GetMission", "mission", {"mission_id": mission_id}, None, True).get_value("mission")
        if mission == None:
            return '{"message": "mission not found"}', 404
        role = json.loads(mission)["data"][0]["defaultRole"]["type"]
        HTTPSTakApiCommunicationController().make_request("SendInvitation", "mission", {"author_uid": author, "mission_id": mission_id, "client_uid": invitedContacts, "role": role}, None, False)
        return '', 200
    except Exception as e:
        print(e)
        return {"message": str(e)}, 500