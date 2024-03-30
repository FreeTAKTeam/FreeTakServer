import io
import json
from typing import List
import uuid
from flask import Blueprint, request, make_response, send_file
import qrcode

from FreeTAKServer.core.RestMessageControllers.RestEnumerations import RestEnumerations
from FreeTAKServer.core.util import certificate_generation
from ..controllers.authentication import auth
from geopy import Point, distance, Nominatim
import datetime as dt

from FreeTAKServer.core.util.time_utils import get_current_dtg
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.services.rest_api_service.controllers.rest_api_communication_controller import RestAPICommunicationController
from FreeTAKServer.core.configuration.LoggingConstants import LoggingConstants
from FreeTAKServer.core.configuration.CreateLoggerController import CreateLoggerController

config = MainConfig.instance()
page = Blueprint('user_management', __name__)

@page.route('/GenerateQR', methods=['GET'])
def generate_qr():
    datapackage_hash = request.args.get('datapackage_hash')
    resp = RestAPICommunicationController().make_request("GetEnterpriseSyncMetaData", "", {"objecthash": datapackage_hash})
    dp = resp.get_value("objectmetadata")
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=5)
    qr.add_data(f'http://{config.DataPackageServiceDefaultIP}:{8080}/Marti/api/sync/metadata/{dp.hash}/tool')
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img_io = io.BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

@page.route('/ManageSystemUser/postSystemUser', methods=['POST'])
def post_system_user():
    from ..controllers.persistency import dbController
    errors = []
    jsondata = request.get_json()
    for systemuser in jsondata['systemUsers']:
        try:
            user_id = str(uuid.uuid4())
            if systemuser["Certs"] == "true":

                # if certs are to be generated the certificate generation is called DP is created and CoT is sent to
                # client resulting in an automatic download of the certificate

                cert_name = systemuser["Name"] + user_id
                # create certs
                certificate_generation.AtakOfTheCerts().bake(common_name=cert_name)
                if systemuser["DeviceType"].lower() == "wintak":
                    certificate_generation.generate_wintak_zip(user_filename=cert_name + '.p12',  server_address=config.UserConnectionIP)
                elif systemuser["DeviceType"].lower() == "mobile":
                    certificate_generation.generate_standard_zip(user_filename=cert_name+'.p12',  server_address=config.UserConnectionIP)
                else:
                    raise Exception("invalid device type, must be either mobile or wintak")
                # add DP
                import string
                import random
                from pathlib import PurePath, Path
                import hashlib
                from defusedxml import ElementTree as etree
                import shutil
                import os
                dp_directory = str(PurePath(Path(config.DataPackageFilePath)))
                openfile = open(str(PurePath(Path(str(config.ClientPackages), cert_name + '.zip'))),
                                mode='rb')
                
                file_hash = str(hashlib.sha256(openfile.read()).hexdigest())
                openfile.seek(0)
                newDirectory = str(PurePath(Path(dp_directory), Path(file_hash)))
                os.mkdir(newDirectory)
                shutil.copy(str(PurePath(Path(str(config.ClientPackages), cert_name + '.zip'))),
                            str(PurePath(Path(newDirectory), Path(cert_name + '.zip'))))
                fileSize = Path(str(newDirectory), cert_name + '.zip').stat().st_size
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                token=systemuser["Token"], password=systemuser["Password"],
                                                uid=user_id,
                                                certificate_package_name=cert_name + '.zip', device_type = systemuser["DeviceType"])
                data = openfile.read()
                RestAPICommunicationController().make_request("SaveEnterpriseSyncData", "enterpriseSync", {"file_name":cert_name + '.zip',"objecthash": file_hash, "objectdata": data, "objkeywords": [cert_name + '.zip', user_id, "missionpackage"], "mime_type": "application/zip", "tool": "public", "synctype": "content", "objectuid": file_hash, "length": len(data), "privacy": 1}, None, True)
                
                DATETIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
                timer = dt.datetime
                now = timer.utcnow()
                zulu = now.strftime(DATETIME_FMT)
                add = dt.timedelta(seconds=600)
                stale_part = dt.datetime.strptime(zulu, DATETIME_FMT) + add
                stale = stale_part.strftime(DATETIME_FMT)
                timer = dt.datetime
                now = timer.utcnow()
                zulu = now.strftime(DATETIME_FMT)
                time = zulu
                #clientXML = f'<?xml version="1.0"?><event version="2.0" uid="{user_id}" type="b-f-t-r" time="{time}" start="{time}" stale="{stale}" how="h-e"><point lat="43.85570300" lon="-66.10801200" hae="19.55866360" ce="3.21600008" le="nan" /><detail><fileshare filename="{cert_name}" senderUrl="{DPIP}:8080/Marti/api/sync/metadata/{str(file_hash)}/tool" sizeInBytes="{fileSize}" sha256="{str(file_hash)}" senderUid="{"server-uid"}" senderCallsign="{"server"}" name="{cert_name + ".zip"}" /><ackrequest uid="{uuid.uuid4()}" ackrequested="true" tag="{cert_name + ".zip"}" /><marti><dest callsign="{systemuser["Name"]}" /></marti></detail></event>'

            else:
                # in the event no certificate is to be generated simply create a system user
                dbController.create_systemUser(name=systemuser["Name"], group=systemuser["Group"],
                                                token=systemuser["Token"], password=systemuser["Password"],
                                                uid=user_id, device_type = systemuser["DeviceType"])
        except Exception as e:
            if isinstance(systemuser, dict) and "Name" in systemuser:
                errors.append(f"operation failed for user {systemuser['Name']}")
            else:
                errors.append(f"operation failed for user. missing name parameter.")
            
    if len(errors) == 0:
        return {"message": "all users created"}, 201
    elif len(errors)<len(jsondata['systemUsers']):
        return {"message": ", ".join(errors)}, 201
    else:
        return {"message":"all users failed to create "+", ".join(errors)}, 500