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
