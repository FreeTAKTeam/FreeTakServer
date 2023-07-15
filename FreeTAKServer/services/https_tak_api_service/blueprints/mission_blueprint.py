import json
from flask import Blueprint, request
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController

page = Blueprint("mission", __name__)
config = MainConfig.instance()

@page.route('/Marti/api/missions', methods=['GET'])
def get_missions():
    return HTTPSTakApiCommunicationController().make_request("GetMissions", "mission", None, True).get_value("missions"), 200

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
    return HTTPSTakApiCommunicationController().make_request("PutMission", "mission", {"mission_id": mission_id, "mission_data": request.data}, None, True).get_value("mission_subscription"), 200
    return {
        "version": "3",
        "type": "Mission",
        "data": [],
        "nodeId": config.nodeID
    }
    
@page.route('/Marti/api/missions/<mission_id>/contents', methods=['PUT'])
def add_mission_content(mission_id):
    content_details = json.loads(request.data)
    return HTTPSTakApiCommunicationController().make_request("PutMission", "mission", {"mission_id": mission_id, "uids": content_details["uids"], "hashes": content_details["hashes"]}, None, True).get_value("mission_content"), 200
    return {
        "version": "3",
        "type": "Mission",
        "data": [],
        "nodeId": config.nodeID
    }