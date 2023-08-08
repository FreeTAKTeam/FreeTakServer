import os
from pathlib import Path, PurePath
import random
import string
from flask import Blueprint, request, make_response
from FreeTAKServer.core.services.DataPackageServer import USINGSSL
from FreeTAKServer.services.https_tak_api_service.controllers.https_tak_api_communication_controller import HTTPSTakApiCommunicationController
from werkzeug.utils import secure_filename
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from io import BytesIO
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

page = Blueprint("enterprise_sync", __name__)
config = MainConfig.instance()
@page.route('/Marti/sync/upload', methods=["POST"])
def enterprise_sync_upload_alt():
    """a new endpoint used by the enterprise sync tool to upload files"""
    return HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "", { "objectdata": request.files.getlist('assetfile')[0], "objkeywords": [filename, creatorUid], "objstarttime": ""}, True).get_value("objectid"), 200 # type: ignore

@page.route('/Marti/sync/search', methods=["GET"])
def retrieveData():
    keyword = request.args.get('keyword', "missionpackage")
    tool = request.args.get('tool', "public")
    packages: List[EnterpriseSyncDataObject] = HTTPSTakApiCommunicationController().make_request("GetMultipleEnterpriseSyncMetaData", "", {"tool": tool, "keyword": keyword}, None, True).get_value("objectmetadata") # type: ignore
    package_dict = {
                "resultCount": len(packages),
                "results": []
            }
    for pack in packages:
        package_dict["results"].append({
            "UID": pack.id,
            "Name": pack.keywords[0].keyword,
            "Hash": pack.PrimaryKey,
            "PrimaryKey": pack.id,
            "SubmissionDateTime": str(pack.start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")),
            "SubmissionUser": pack.submitter,
            "CreatorUid": pack.creator_uid,
            "Keywords": [keyword.keyword for keyword in pack.keywords],
            "MIMEType": pack.mime_type,
            "Size": pack.length
        })
    print(str(package_dict))
    return str(package_dict)

@page.route('/Marti/sync/content', methods=["HEAD"])
def enterprise_sync_head():
    contents = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", None, {"objecthash": request.args.get('hash')}, True).get_value("objectdata"), 200 # type: ignore
    if contents == None:
        return '', 404
    else:
        return '', 200
@page.route('/Marti/sync/content', methods=["PUT", "POST"])
def enterprise_sync_upload():
    filename = request.args.get("filename")
    creatorUid = request.args.get("creatorUid")
    return HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", None, {"objecthash": request.args.get('hash'), "objectdata": request.files.getlist('assetfile')[0], "objkeywords": [filename, creatorUid], "objstarttime": ""}, True).get_value("objectid"), 200 # type: ignore

@page.route('/Marti/sync/content', methods=["GET"])
def specificPackage():
    from defusedxml import ElementTree as etree
    from os import listdir
    try:
        if request.method == 'GET' and request.args.get('uid') != None: # type: ignore
            return HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objectuid": request.args.get('uid'), "use_bytes": True}, None, True).get_value("objectdata"), 200 # type: ignore
        else:
            out_data = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", "", {"objecthash": request.args.get('hash'), "use_bytes": True}, None, True).get_value("objectdata"), 200 # type: ignore
            return out_data
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
    HTTPSTakApiCommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": request.args.get('hash'), "objectdata": request.files.getlist('assetfile')[0].stream._file.getvalue(), "objkeywords": [filename, creatorUid], "objstarttime": "", "synctype": "content", "tool": "enterprise_sync", "mime_type": request.files.getlist('assetfile')[0].headers["Content-Type"]}).get_value("objectid"), 200 # type: ignore
    return "http://" + config.DataPackageServiceDefaultIP + ':' + str(config.HTTPTakAPIPort) + "/Marti/api/sync/metadata/" + file_hash + "/tool"

@page.route('/Marti/sync/missionquery', methods=["GET"])
def get_mission():
    hash = request.args.get("hash") # type: ignore
    data: bytes = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", "enterpriseSync", {"objecthash": hash, "use_bytes": True}).get_value("objectdata") # type: ignore
    metadata: EnterpriseSyncDataObject = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncMetaData", "enterpriseSync", {"objecthash": hash}).get_value("objectmetadata") # type: ignore
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
    HTTPSTakApiCommunicationController().make_request("UpdateEnterpriseSyncMetaData", "enterpriseSync", {"objecthash": hash, "privacy": privacy})
    return "Okay", 200


@page.route('/Marti/api/sync/metadata/<hash>/tool', methods=["GET"])
@cross_origin(send_wildcard=True)
def getDataPackageTool(hash):
    data: bytes = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncData", None, {"objecthash": hash}, True).get_value("objectdata") # type: ignore
    metadata: EnterpriseSyncDataObject = HTTPSTakApiCommunicationController().make_request("GetEnterpriseSyncMetaData", None, {"objecthash": hash}, True).get_value("objectmetadata") # type: ignore
    with BytesIO() as file:
        file.write(data)
        file.seek(0)
        return send_file(file, as_attachment=True, mimetype=metadata.mime_type, attachment_filename=metadata.filename)