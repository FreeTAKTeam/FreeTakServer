import json
from flask import Blueprint, request, make_response
from FreeTAKServer.core.configuration.MainConfig import MainConfig

config = MainConfig.instance()
page = Blueprint('misc', __name__)

@page.route("/Marti/api/groups/groupCacheEnabled")
def group_cache():
    return {
        "version": "3",
        "type": "java.lang.Boolean",
        "data": False,
        "nodeId": config.nodeID
    }

@page.route('/Marti/api/clientEndPoints', methods=["GET"])
def clientEndPoint():
    return {
        "version": "3",
        "type": "com.bbn.marti.remote.ClientEndpoint",
        "data": [
            {
                "callsign": "BOXER",
                "uid": "S-1-5-21-2351381107-139585266-151226405-1001",
                "username": "ghost",
                "lastEventTime": "2023-06-16T00:42:15.261Z",
                "lastStatus": "Connected"
            },
            {
                "callsign": "DOWNFALL",
                "uid": "ANDROID-199eeda473669973",
                "username": "ghost",
                "lastEventTime": "2023-06-16T15:20:55.871Z",
                "lastStatus": "Connected"
            }
        ],
        "nodeId": config.nodeID
    }