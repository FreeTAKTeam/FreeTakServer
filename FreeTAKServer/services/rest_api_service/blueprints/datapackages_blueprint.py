"""
datapackages_blueprint.py

This module is part of a Flask web application and is responsible for defining a blueprint related to data packages. It includes routes and views for handling requests related to data packages.

It imports several modules and types for use within the file:
- TYPE_CHECKING from the typing module, which is used for conditional imports based on whether type checking is being performed.
- jsonify from flask.json, which is used to create a JSON response.
- EnterpriseSyncKeyword and EnterpriseSyncDataObject from FreeTAKServer.core.enterprise_sync.persistence.sqlalchemy, which are used for enterprise synchronization. These are imported conditionally if type checking is being performed.
- json module, which is used for handling JSON data.
- Blueprint and request from flask, which are used for creating modular, reusable components in a Flask application and handling requests, respectively.
- PurePath and Path from pathlib, which are used for handling filesystem paths in a platform-independent way.
"""
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
    """ This function handles the POST request for the DataPackageTable route. It is used to upload a data package to the server.
    """
    try:
        uid = str(uuid.uuid4())
        filename = request.args.get('filename')
        creatorUid = request.args.get('creatorUid')
        file = request.files.getlist('assetfile')[0].stream.read()
        metadata: EnterpriseSyncDataObject = RestAPICommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"objectuid": uid, "tool": "public", "objectdata": file, "objkeywords": [
            filename, creatorUid, "missionpackage"], "objstarttime": "", "synctype": "content", "mime_type": request.headers["Content-Type"], "file_name": filename}).get_value("objectmetadata")  # type: ignore

        return {"message": 'success', "id": str(metadata.id)}, 200
    except Exception as e:
        return {"message": "An error occurred accessing datapackage details: "+str(e)}, 500


@page.route('/DataPackageTable', methods=["PUT"])
@auth.login_required()
def put_DataPackageTable():
    """ This function handles the PUT request for the DataPackageTable route. It is used to update the metadata for a data package.
    """
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
        pk = RestAPICommunicationController().make_request("GetEnterpriseSyncMetaData", "",
                                                           {"file_name": dp["PrimaryKey"]}, None, True).get_value('objectmetadata').PrimaryKey
        RestAPICommunicationController().make_request("UpdateEnterpriseSyncMetaData", "", {
            "file_name": name, "keywords": keywords, "privacy": privacy, "objectuid": pk}, None, True)

    return {"message": "success"}, 200


@page.route('/DataPackageTable', methods=["GET"])
@auth.login_required()
def get_DataPackageTable():
    """ This function handles the GET request for the DataPackageTable route. It is used to retrieve the metadata for a data package.
    """
    return_vals = []
    output = RestAPICommunicationController().make_request("GetMultipleEnterpriseSyncMetaData",
                                                           "", {"keyword": "missionpackage"}, None, True).get_value("objectmetadata")
    for i in range(0, len(output)):
        updated_val = {}
        output[i] = output[i].__dict__
        updated_val['PrimaryKey'] = output[i]["keywords"][0].keyword
        updated_val['SubmissionUser'] = output[i]['submitter']
        updated_val['Size'] = output[i]['length']
        updated_val['Privacy'] = output[i]['private']
        updated_val['SubmissionDateTime'] = output[i]['start_time']
        updated_val["Name"] = output[i]["file_name"]
        updated_val["Hash"] = output[i]["hash"]
        return_vals.append(updated_val)
        del (output[i]['_sa_instance_state'])
        # del (output[i]['CreatorUid'])
        # del (output[i]['MIMEType'])
        # del (output[i]['uid'])
    print(return_vals)
    return jsonify(json_list=return_vals), 200


@page.route('/DataPackageTable', methods=["DELETE"])
@auth.login_required()
def delete_DataPackageTable():
    """ This function handles the DELETE request for the DataPackageTable route. It is used to delete a data package from the server.
    """
    jsondata = json.loads(request.data)
    Hashes = jsondata['DataPackages']
    for hash in Hashes:
        Hash = hash['hash']
        print(Hash)
        RestAPICommunicationController().make_request(
            "DeleteEnterpriseSyncData", "", {"object_hash": Hash}, None, True)
    return {"message": 'success'}, 200
