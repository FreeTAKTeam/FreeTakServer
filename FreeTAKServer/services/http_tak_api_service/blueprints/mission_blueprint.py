from flask import Blueprint
from FreeTAKServer.core.configuration.MainConfig import MainConfig

page = Blueprint("mission", __name__)
config = MainConfig.instance()

@page.route('/Marti/api/missions')
def get_missions():
    return {
        "version": "3",
        "type": "Mission",
        "data": [],
        "nodeId": config.nodeID
    }

@page.route('/Marti/api/missions/invitations')
def get_invitations():
    return {
        "version": "3",
        "type": "MissionInvitation",
        "data": [],
        "nodeId": config.nodeID
    }