from flask import Blueprint
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.http_tak_api_service.controllers.http_tak_api_communication_controller import HTTPTakApiCommunicationController

page = Blueprint("mission", __name__)
config = MainConfig.instance()

@page.route('/Marti/api/missions', methods=['GET'])
def get_missions():
    return HTTPTakApiCommunicationController().make_request("GetMissions", "mission", {}, None, True).get_value("missions"), 200

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
    return HTTPTakApiCommunicationController().make_request("PutMission", "mission", {"mission_id": mission_id, "mission_data": request.data, "mission_data_args": request.args}, None, True).get_value("mission_subscription"), 200

@page.route('/Marti/api/missions/<mission_id>', methods=['GET'])
def get_mission(mission_id):
    from flask import request
    return HTTPTakApiCommunicationController().make_request("GetMission", "mission", {"mission_id": mission_id}, None, True).get_value("mission"), 200

@page.route('/Marti/api/missions/<mission_id>/cot', methods=['GET'])
def get_mission_cots(mission_id):
    """get all cots for a mission"""
    # TODO: implement this function
    return """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<events></events>""", 200

@page.route('/Marti/api/missions/<mission_id>/log', methods=['GET'])
def get_mission_log(mission_id):
    """get the mission log"""
    return HTTPTakApiCommunicationController().make_request("GetMissionLogs", "mission", {"mission_id": mission_id}, None, True).get_value("mission_logs"), 200