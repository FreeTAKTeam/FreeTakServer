import io
import json
from typing import List
import uuid
from flask import Blueprint, request, make_response, send_file
import qrcode

from FreeTAKServer.core.RestMessageControllers.RestEnumerations import RestEnumerations
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
    datapackage_id = request.args.get('datapackage_id')
    dp = RestAPICommunicationController().make_request("GetEnterpriseSyncMetaData", "", {"id": datapackage_id}).get_value("objectmetadata")
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