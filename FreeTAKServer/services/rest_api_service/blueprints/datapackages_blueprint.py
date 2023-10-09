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
page = Blueprint('datapackage', __name__)

@page.route('/DataPackageTable', methods=["POST"])
@auth.login_required()
def post_DataPackageTable():
    try:            
        uid = str(uuid.uuid4())
        filename = request.args.get('filename')
        creatorUid = request.args.get('creatorUid')
        file = request.files.getlist('assetfile')[0]
        metadata: EnterpriseSyncDataObject = RestAPICommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": uid, "tool": "public", "objectdata": file, "objkeywords": [filename, creatorUid, "missionpackage"], "objstarttime": "", "synctype": "content", "mime_type": request.headers["Content-Type"], "file_name": filename}).get_value("objectmetadata") # type: ignore

        return {"message":'success', "id": str(metadata.id)}, 200
    except Exception as e:
        return {"message":"An error occurred accessing datapackage details."}, 500

@page.route('/DataPackageTable', methods=["PUT"])
@auth.login_required()
def put_DataPackageTable():
    updatedata = json.loads(request.data)
    DataPackages = updatedata['DataPackages']
    for dp in DataPackages:
        updateDict = {}
        if 'Privacy' in dp:
            privacy = int(dp["Privacy"])
        else:
            privacy = None
        if "Keywords" in dp:
            keywords = dp["Keywords"]
        else:
            keywords = None
        if "Name" in dp:
            name = dp["Name"]
        else:
            name = None
        RestAPICommunicationController().make_request("UpdateEnterpriseSyncMetaData", "", {"file_name": name, "keywords": keywords, "private": privacy, "id": dp["PrimaryKey"]}, None, True)
    
    return {"message":"success"}, 200

@page.route('/DataPackageTable', methods=["GET"])
@auth.login_required()
def get_DataPackageTable():
    return_vals = []
    output = RestAPICommunicationController().make_request("GetAllEnterpriseSyncMetaData", "", {}, None, True).get_value("objectmetadata")
    for i in range(0, len(output)):
        updated_val = {}
        output[i] = output[i].__dict__
        updated_val['PrimaryKey'] = output[i]["keywords"][0].keyword
        updated_val['SubmissionUser'] = output[i]['submitter']
        updated_val['Size'] = output[i]['length']
        updated_val['Privacy'] = output[i]['private']
        updated_val['SubmissionDateTime'] = output[i]['start_time']
        updated_val["Name"] = output[i]["file_name"]
        return_vals.append(updated_val)
        del (output[i]['_sa_instance_state'])
        #del (output[i]['CreatorUid'])
        #del (output[i]['MIMEType'])
        #del (output[i]['uid'])
    print(return_vals)
    return jsonify(json_list=return_vals), 200

@page.route('/DataPackageTable', methods=["DELETE"])
@auth.login_required()
def delete_DataPackageTable():
    jsondata = json.loads(request.data)
    Hashes = jsondata['DataPackages']
    for hash in Hashes:
        Hash = hash['hash']
        print(Hash)
        RestAPICommunicationController().make_request("DeleteEnterpriseSyncData", "", {"objecthash": Hash}, None, True)
    return {"message":'success'}, 200        
    