from io import BytesIO
import json
import os
from pathlib import Path, PurePath
import random
import string
from typing import List, TYPE_CHECKING

from flask import Blueprint, request, make_response, send_file
from flask_cors import cross_origin
if TYPE_CHECKING:
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_keyword import EnterpriseSyncKeyword
    from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy.enterprise_sync_data_object import EnterpriseSyncDataObject

from FreeTAKServer.core.services.DataPackageServer import USINGSSL
from FreeTAKServer.services.http_tak_api_service.controllers.http_tak_api_communication_controller import HTTPTakApiCommunicationController
from werkzeug.utils import secure_filename
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.util.time_utils import get_dtg

page = Blueprint('enterprise_sync', __name__)
config = MainConfig.instance()

@page.route('/Marti/sync/upload', methods=["POST"])
def enterprise_sync_upload_alt():
    """a new endpoint used by the enterprise sync tool to upload files"""
    filename = request.args.get("filename") or request.args.get("name")
    creatorUid = request.args.get("creatorUid")
    tool = request.args.get("tool", "public")
    if not request.data:
        data = request.files.getlist('assetfile')[0].stream.read()
    else:
        data = request.data
    metadata: EnterpriseSyncDataObject = HTTPTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": request.args.get('hash'), "tool": tool, "objectdata": data, "objkeywords": [filename, creatorUid, "missionpackage"], "objstarttime": "", "synctype": "content", "mime_type": request.headers["Content-Type"], "file_name": filename}).get_value("objectmetadata") # type: ignore
    return {
        "UID": metadata.id,
        "SubmissionDateTime": get_dtg(metadata.start_time),
        "MIMEType": metadata.mime_type,
        "SubmissionUser": metadata.submitter,
        "PrimaryKey": metadata.PrimaryKey,
        "Hash": metadata.hash,
    }

@page.route('/Marti/sync/search', methods=["GET"])
def retrieveData():
    keyword = request.args.get('keyword', "missionpackage")
    tool = request.args.get('tool', "public")
    packages: List[EnterpriseSyncDataObject] = HTTPTakApiCommunicationController().make_request("GetMultipleEnterpriseSyncMetaData", "", {"tool": tool, "keyword": keyword}, None, True).get_value("objectmetadata") # type: ignore
    public_packages = [package for package in packages if package.private == 0]
    package_dict = {
                "resultCount": len(public_packages),
                "results": []
            }
    for pack in public_packages:
        package_dict["results"].append({
            "UID": str(pack.PrimaryKey),
            "Name": pack.keywords[0].keyword,
            "Hash": pack.PrimaryKey,
            "PrimaryKey": str(pack.id),
            "SubmissionDateTime": str(pack.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            "SubmissionUser": pack.submitter,
            "CreatorUid": pack.creator_uid,
            "Keywords": [keyword.keyword for keyword in pack.keywords],
            "MIMEType": pack.mime_type,
            "Size": pack.length
        })
    print(str(package_dict))
    return json.dumps(package_dict)

@page.route('/Marti/sync/content', methods=["HEAD"])
def enterprise_sync_head():
    contents = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objecthash": request.args.get('hash')}, None, True).get_value("objectdata")# type: ignore
    if contents == None:
        return '', 404
    else:
        return '', 200
    
@page.route('/Marti/sync/content', methods=["PUT", "POST"])
def enterprise_sync_upload():
    filename = request.args.get("filename")
    creatorUid = request.args.get("creatorUid")
    tool = request.args.get("tool", "public")
    return HTTPTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "", {"objecthash": request.args.get('hash'), "objectdata": request.files.getlist('assetfile')[0], "objkeywords": [filename, creatorUid, "missionpackage"], "objstarttime": "", "tool": tool}, True).get_value("objectid"), 200 # type: ignore

@page.route('/Marti/sync/content', methods=["GET"])
def specificPackage():
    from defusedxml import ElementTree as etree
    from os import listdir
    try:
        if request.method == 'GET' and request.args.get('uid') != None: # type: ignore
            return_data = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objectuid": request.args.get('uid'), "use_bytes": True}, None, True).get_value("objectdata") # type: ignore
        else:
            return_data = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objecthash": request.args.get('hash'), "use_bytes": True}, None, True).get_value("objectdata") # type: ignore
        if return_data != None:
            return return_data, 200
        else:
            return "", 404
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
    tool: str = request.args.get('tool', "public") # type: ignore
    HTTPTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": request.args.get('hash'), "tool": tool, "objectdata": request.files.getlist('assetfile')[0].stream.read(), "objkeywords": [filename, creatorUid, "missionpackage"], "objstarttime": "", "synctype": "content", "mime_type": request.files.getlist('assetfile')[0].headers["Content-Type"]}).get_value("objectid"), 200 # type: ignore
    return "http://" + config.DataPackageServiceDefaultIP + ':' + str(config.HTTPTakAPIPort) + "/Marti/api/sync/metadata/" + file_hash + "/tool"

@page.route('/Marti/sync/missionquery', methods=["GET"])
def get_mission():
    hash = request.args.get("hash") # type: ignore
    data: bytes = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncData", "enterpriseSync", {"objecthash": hash, "use_bytes": True}).get_value("objectdata") # type: ignore
    metadata: EnterpriseSyncDataObject = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncMetaData", "enterpriseSync", {"objecthash": hash}).get_value("objectmetadata") # type: ignore
    if data != None and metadata !=None:
        file = BytesIO(data)
        return send_file(file, as_attachment=True, mimetype=metadata.mime_type, attachment_filename=metadata.file_name)
    else:
        return '404', 404
@page.route('/Marti/api/sync/metadata/<hash>/tool', methods=["PUT"])
def putDataPackageTool(hash):
    if request.data == b'private':
        privacy = 1
    else:
        privacy = 0
    HTTPTakApiCommunicationController().make_request("UpdateEnterpriseSyncMetaData", "enterpriseSync", {"objecthash": hash, "privacy": privacy})
    return "Okay", 200


@page.route('/Marti/api/sync/metadata/<hash>/tool', methods=["GET"])
@cross_origin(send_wildcard=True)
def getDataPackageTool(hash):
    data: bytes = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objecthash": hash, "use_bytes": True}, None, True).get_value("objectdata") # type: ignore
    if data == None:
        return "", 404
    metadata: EnterpriseSyncDataObject = HTTPTakApiCommunicationController().make_request("GetEnterpriseSyncMetaData", "", {"objecthash": hash}, None, True).get_value("objectmetadata") # type: ignore
    file = BytesIO()
    file.write(data)
    file.seek(0)
    return send_file(file, as_attachment=True, mimetype=metadata.mime_type, download_name=metadata.file_name)