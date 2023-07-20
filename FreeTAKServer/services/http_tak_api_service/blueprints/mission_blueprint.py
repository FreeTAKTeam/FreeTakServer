from flask import Blueprint, request
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.http_tak_api_service.controllers.http_tak_api_communication_controller import HTTPTakApiCommunicationController

page = Blueprint("mission", __name__)
config = MainConfig.instance()

@page.route('/Marti/api/missions', methods=['GET'])
def get_missions():
    out_data =  HTTPTakApiCommunicationController().make_request("GetMissions", "mission", {}, None, True).get_value("missions"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/invitations')
def get_invitations():
    return {
        "version": "3",
        "type": "MissionInvitation",
        "data": [],
        "nodeId": config.nodeID
    }

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
    out_data = HTTPTakApiCommunicationController().make_request("PutMission", "mission", {"mission_id": mission_id, "mission_data": request.data, "mission_data_args": request.args, "creatorUid": request.args.get("creatorUid")}, None, True).get_value("mission_subscription"), 200 # type: ignore
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>', methods=['GET'])
def get_mission(mission_id):
    from flask import request
    out_data = HTTPTakApiCommunicationController().make_request("GetMission", "mission", {"mission_id": mission_id}, None, True).get_value("mission"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>/cot', methods=['GET'])
def get_mission_cots(mission_id):
    """get all cots for a mission"""
    # TODO: implement this function
    return """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<events></events>""", 200

@page.route('/Marti/api/missions/<mission_id>/changes', methods=['POST'])
def get_mission_changes(mission_id):
    return {
        "version": "3",
        "type": "MissionChange",
        "data": [
        ],
        "nodeId": config.nodeID
    }

@page.route('/Marti/api/missions/<mission_id>/subscriptions/roles', methods=['GET'])
def get_all_mission_subscriptions(mission_id):
    """get all the subscriptions from a mission

    Args:
        mission_id (_type_): _description_
    """
    print("request made to get all mission subscriptions")
    out_data = HTTPTakApiCommunicationController().make_request("GetMissionSubscriptions", "mission", {"mission_id": mission_id}, None, True).get_value("mission_subscriptions"), 200
    print(out_data)
    return out_data

@page.route('/Marti/api/missions/<mission_id>/contents', methods=['PUT'])
def add_mission_contents(mission_id: str):
    """add contents to a mission

    Args:
        mission_id (str): the id of the mission to add contents to
    """
    request_json = request.get_json()
    return HTTPTakApiCommunicationController().make_request("AddMissionContents", "mission", {"mission_id": mission_id, "hashes": request_json["hashes"], "uids": request_json["uids"]}, None, True).get_value("mission"), 200

@page.route('/Marti/api/missions/logs/entries', methods=['POST'])
def add_log_entry():
    request_json = request.get_json()
    return HTTPTakApiCommunicationController().make_request("AddMissionLog", "mission", {"mission_log_data": request_json}, None, True).get_value("log"), 200

@page.route('/Marti/api/missions/logs/entries', methods=['PUT'])
def update_log_entry():
    request_json = request.get_json()
    return HTTPTakApiCommunicationController().make_request("UpdateMissionLog", "mission", {"mission_log_data": request_json}, None, True).get_value("log"), 200

@page.route('/Marti/api/missions/logs/entries/<id>', methods=['DELETE'])
def delete_log_entry(id):
    HTTPTakApiCommunicationController().make_request("DeleteMissionLog", "mission", {"log_id": id}, None, True)
    return "", 200

@page.route('/Marti/api/missions/logs/entries/<id>', methods=['GET'])
def get_log_entry():
    return HTTPTakApiCommunicationController().make_request("GetMissionLog", "mission", {"log_id": id}, None, True).get_value("log"), 200

@page.route('/Marti/api/missions/<missionID>/log', methods=['GET'])
def get_mission_logs(missionID):
    return HTTPTakApiCommunicationController().make_request("GetMissionLogs", "mission", {"mission_id": missionID, "seconds_ago": request.args.get("secago"), "start": request.args.get("start"), "end": request.args.get("end")}, None, True).get_value("logs"), 200

@page.route('/Marti/api/missions/all/logs', methods=['GET'])
def get_all_logs():
    return HTTPTakApiCommunicationController().make_request("GetAllLogs", "mission", {}, None, True).get_value("logs"), 200