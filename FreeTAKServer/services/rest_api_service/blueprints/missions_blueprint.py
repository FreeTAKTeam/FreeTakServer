from typing import TYPE_CHECKING

from flask.json import jsonify

if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_keyword import EnterpriseSyncKeyword
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

import json
from flask import Blueprint, request
from pathlib import PurePath, Path
import hashlib
from zipfile import ZipFile
from defusedxml import ElementTree as etree
import uuid
from lxml.etree import SubElement, Element  # pylint: disable=no-name-in-module

from ..controllers.authentication import auth

from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.rest_api_service.controllers.rest_api_communication_controller import RestAPICommunicationController

config = MainConfig.instance()
page = Blueprint('mission', __name__)

@page.route("/MissionTable", methods=['GET'])
@auth.login_required()
def get_mission_table():
    try:
        out_data =  RestAPICommunicationController().make_request("GetMissions", "mission", {}, None, True).get_value("missions"), 200
        print(out_data)
        return out_data
    except Exception as e:
        logger.error(str(e))
        return {"message":"An error occurred accessing mission details."}, 500
