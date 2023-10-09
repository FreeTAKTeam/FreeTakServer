from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.services.rest_api_service.controllers.rest_api_communication_controller import RestAPICommunicationController

from flask import Blueprint, request

import json

config = MainConfig.instance()
page = Blueprint('excheck', __name__)
from ..controllers.authentication import auth

@page.route("/ExCheckTable", methods=["GET"])
@auth.login_required()
def excheck_table():
    return_data = RestAPICommunicationController().make_request("GetAllTemplates", "excheck", {}).get_value("template_info") # type: ignore
    if return_data:
        return return_data, 200
    else:
        return '{}'