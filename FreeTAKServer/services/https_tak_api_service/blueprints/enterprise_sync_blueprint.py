import os
from pathlib import Path, PurePath
import random
import string
from flask import Blueprint, request, make_response
from FreeTAKServer.core.services.DataPackageServer import USINGSSL
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController
from werkzeug.utils import secure_filename
from FreeTAKServer.core.configuration.MainConfig import MainConfig

page = Blueprint("enterprise_sync", __name__)
config = MainConfig.instance()

@page.route('/Marti/sync/upload', methods=["POST"])
def enterprise_sync_upload_alt():
    """a new endpoint used by the enterprise sync tool to upload files"""
    return HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", None, { "objectdata": request.files.getlist('assetfile')[0], "objkeywords": [filename, creatorUid], "objstarttime": ""}, True).get_value("objectid"), 200 # type: ignore

@page.route('/Marti/sync/content', methods=["POST"])
def enterprise_sync_upload():
    return HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", None, {"objectuid": request.args.get('hash'), "objectdata": request.files.getlist('assetfile')[0], "objkeywords": [filename, creatorUid], "objstarttime": ""}, True).get_value("objectid"), 200 # type: ignore

@page.route('/Marti/sync/content', methods=["GET"])
def specificPackage():
    from defusedxml import ElementTree as etree
    from os import listdir
    try:
        if request.method == 'GET' and request.args.get('uid') != None: # type: ignore
            return HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", None, {"objectuid": request.args.get('uid')}, True).get_value("objectdata"), 200 # type: ignore
        else:
            return HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", None, {"objecthash": request.args.get('hash')}, True).get_value("objectdata"), 200 # type: ignore
    except Exception as ex:
        print(ex)
        return '', 500
    
@page.route('/Marti/sync/missionupload', methods=["PUT", "POST"])
def upload():
    file_hash = request.args.get('hash') # type: ignore
    letters = string.ascii_letters
    uid = ''.join(random.choice(letters) for i in range(4))
    uid = 'uid-' + str(uid)
    filename = secure_filename(request.args.get('filename')) # type: ignore
    creatorUid = request.args.get('creatorUid') # type: ignore
    HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "", {
        "objectuid": request.args.get('hash'), 
        "objectdata": request.files.getlist('assetfile')[0].stream.read(), 
        "objkeywords": [filename, creatorUid], 
        "objstarttime": "", 
        "synctype": "datapackage", 
        "file_name": filename,
        "tool": "public", 
        "mime_type": dict(request.headers)["Content-Type"].split(";")[0]}, None, True).get_value("objectid"), 200 # type: ignore
    return "https://" + config.DataPackageServiceDefaultIP + ':' + str(config.HTTPSTakAPIPort) + "/Marti/api/sync/metadata/" + file_hash + "/tool"
