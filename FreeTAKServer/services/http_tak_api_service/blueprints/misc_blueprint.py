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
                "callsign": "DOWN",
                "uid": "ANDROID-199eeda473669973",
                "username": "ghost",
                "lastEventTime": "2023-06-16T15:20:55.871Z",
                "lastStatus": "Connected"
            }
        ],
        "nodeId": config.nodeID
    }

# TODO remove?
@page.route('/Marti/api/missions/exchecktemplates/subscription', methods=['PUT'])
def request_subscription():
    try:
        # this endpoint allows for the client to request a new subscription
        # possibly the uid of the client db also contains create_time and mission_id
        print(request.args.get('uid'))

        return ('', 200)
    except Exception as e:
        print('exception in request_subscription' + str(e))