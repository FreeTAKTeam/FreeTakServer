import json
from typing import List
import uuid
from flask import Blueprint, request, make_response

from FreeTAKServer.core.RestMessageControllers.RestEnumerations import RestEnumerations
from ..controllers.authentication import auth
from geopy import Point, distance, Nominatim
import datetime as dt

from FreeTAKServer.core.util.time_utils import get_current_dtg
from FreeTAKServer.core.configuration.MainConfig import MainConfig
from FreeTAKServer.core.parsers.JsonController import JsonController
from FreeTAKServer.core.RestMessageControllers.SendSimpleCoTController import SendSimpleCoTController
from FreeTAKServer.services.rest_api_service.controllers.rest_api_communication_controller import RestAPICommunicationController

config = MainConfig.instance()
page = Blueprint('geoobject', __name__)

def create_geoobject_json(type, how, uid, lat, lon, timeout=0, name=None, remarks=None, link_uid=None):
    json_geoobj = {
            "event": {
                "@how": how,
                "@type": type,
                "@uid": uid,
                "@time": get_current_dtg(),
                "@start": get_current_dtg(),
                "@stale": get_current_dtg(timeout),
                "point": {
                    "@lat": lat,
                    "@lon": lon,
                    "@hae": "9999999",
                    "@ce": "9999999",
                    "@le": "9999999"
                },
                "detail": {
                }
            }
        }
    if name:
        json_geoobj["event"]["detail"]["contact"] = {"@callsign": name}
    if link_uid:
        json_geoobj["event"]["detail"]["link"] = {"@uid": link_uid}
    if remarks:
        json_geoobj["event"]["detail"]["remarks"] = {"#text": remarks}
    return json_geoobj

@page.route("/ManageGeoObject/GetRepeatedMessages", methods=["GET"])
@auth.login_required
def get_repeated_messages():
    try:
        response = RestAPICommunicationController().make_request("GetRepeatedMessages", "", {}, None, synchronous=True)
        message_nodes = response.get_value("message")

        # request to serialize repeated messages to CoT
        # TODO: parameterize message protocol
        response = RestAPICommunicationController().make_request("serialize", "", {"message": message_nodes, "protocol": "XML"}, None, synchronous=True)

        # convert response to json
        # TODO: this conversion should be automated 
        output = {"messages": {}}
        message = response.get_value("message")
        for i in range(len(message)):
            output["messages"][str(message_nodes[i].uid)] = message[i].decode()
        
        return json.dumps(output)

    except Exception as e:
        return {"message":str(e)}, 500

@page.route("/ManageGeoObject/DeleteRepeatedMessage", methods=["DELETE"])
@auth.login_required
def delete_repeated_messages():
    try:
        # get and blowup id list
        ids: List[str] = request.args.get("ids").split(",")
        response = RestAPICommunicationController().make_request("DeleteRepeatedMessage", "", {"ids": ids}, None, synchronous=True)
        if response.get_value("success"):
            for id in ids:
                # TODO move strings out to constants
                json_result = create_geoobject_json("t-x-d-d", "m-g", id, 0, 0, link_uid=id)
                RestAPICommunicationController().make_request("DeleteGeoObject", "XMLCoT", {"dictionary": json_result}, None, synchronous = False)
            return {"message":'operation successful'}, 200
        else:
            return {"message":'operation failed'}, 500
    except Exception as e:
        return str(e), 500

@page.route("/ManageGeoObject/putGeoObject", methods=["PUT"])
@auth.login_required
def put_geoobject():
    # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
    jsondata = request.get_json(force=True)
    if "-.-" in RestEnumerations.geoObject[jsondata["geoObject"]]:
        obj_type = RestEnumerations.geoObject[jsondata["geoObject"]].replace("-.-", RestEnumerations.attitude[jsondata['attitude']])
    else:
        obj_type = RestEnumerations.geoObject[jsondata["geoObject"]]
    
    if jsondata.get("address", None):
        locator = Nominatim(user_agent=str(uuid.uuid4()))
        location = locator.geocode(jsondata["address"])
        lon = location.longitude
        lat = location.latitude
    else:
        lon = jsondata["longitude"]
        lat = jsondata["latitude"]

    # check if the message it expected to be repeated
    if jsondata.get("distance", None):
        start_point = Point(lat, lon)
        d = distance.distance(meters=jsondata["distance"])
        if "bearing" in jsondata:
            end_point = d.destination(point=start_point, bearing=jsondata["bearing"])
        else:
            end_point = d.destination(point=start_point, bearing=360)
        lat = end_point.latitude
        lon = end_point.longitude

    json_result = create_geoobject_json(obj_type, RestEnumerations.how[jsondata["how"]], jsondata["uid"], lat, lon, jsondata["timeout"], jsondata.get("name", None), jsondata.get("remarks", None), jsondata.get("link_uid", None))
    
    RestAPICommunicationController().make_request("CreateGeoObject", "XMLCoT", {"dictionary": json_result, "repeated": jsondata.get("repeat", False)}, None, synchronous = False)

    return {"message":json_result["event"]["@uid"]}, 200

@page.route("/ManageGeoObject/postGeoObject", methods=["POST"])
@auth.login_required
def post_geoobject():
    """this method is responsible for creating publishing and saving a geoobject to the repeater
    Returns:
        str: the uid of the generated object
    """
    try:
        print("received request")
        # jsondata = {'longitude': '12.345678', 'latitude': '34.5677889', 'attitude': 'friend', 'geoObject': 'Ground', 'how': 'nonCoT', 'name': 'testing123'}
        jsondata = request.get_json(force=True)
        if "-.-" in RestEnumerations.geoObject[jsondata["geoObject"]]:
            obj_type = RestEnumerations.geoObject[jsondata["geoObject"]].replace("-.-", RestEnumerations.attitude[jsondata['attitude']])
        else:
            obj_type = RestEnumerations.geoObject[jsondata["geoObject"]]
        
        if jsondata.get("address", None):
            locator = Nominatim(user_agent=str(uuid.uuid4()))
            location = locator.geocode(jsondata["address"])
            lon = location.longitude
            lat = location.latitude
        else:
            lon = jsondata["longitude"]
            lat = jsondata["latitude"]

        # check if the message it expected to be repeated
        if jsondata.get("distance", None):
            start_point = Point(lat, lon)
            d = distance.distance(meters=jsondata["distance"])
            if "bearing" in jsondata:
                end_point = d.destination(point=start_point, bearing=jsondata["bearing"])
            else:
                end_point = d.destination(point=start_point, bearing=360)
            lat = end_point.latitude
            lon = end_point.longitude

        json_result = create_geoobject_json(obj_type, RestEnumerations.how[jsondata["how"]], jsondata["uid"], lat, lon, jsondata["timeout"], jsondata.get("name", None), jsondata.get("remarks", None), jsondata.get("link_uid", None))

        RestAPICommunicationController().make_request("CreateGeoObject", "XMLCoT", {"dictionary": json_result, "repeated": jsondata.get("repeat", False)}, None, synchronous = False)

        # make request to persist the model object to be re-sent
        #response = RestAPICommunicationController().make_request("CreateRepeatedMessage", "XMLCoT", {"message": [model_object]}, None, synchronous=False)

        print("putting in queue")
        #APIPipe.put(simpleCoTObject)
        #print(simpleCoTObject.xmlString)
        print('put in queue')
        return {"message":json_result["event"]["@uid"]}, 200
    except Exception as e:
        logger.error(str(e))
        return {"message":"An error occurred adding geo object."}, 500
    
@page.route("/ManageGeoObject/getGeoObject", methods=["GET"])
@auth.login_required
def get_geoobject():
    from ..controllers.persistency import dbController
    try:
        from math import sqrt, degrees, cos, sin, radians, atan2
        from sqlalchemy import or_, and_
        # jsondata = request.get_json(force=True)
        radius = request.args.get("radius", default=100, type=int)
        lat = request.args.get("latitude", default=0, type=float)
        lon = request.args.get("longitude", default=0, type=float)
        expectedAttitude = request.args.get("attitude", default="*", type=str)
        lat_abs = lat
        lon_abs = lon
        import geopy
        from geopy.distance import distance
        from FreeTAKServer.model.SQLAlchemy.CoTTables.Point import Point
        from FreeTAKServer.model.SQLAlchemy.Event import Event
        from FreeTAKServer.model.RestMessages.RestEnumerations import RestEnumerations
        import re
        radius_in_deg = (geopy.units.degrees(arcseconds=geopy.units.nautical(meters=radius))) / 2
        if lat_abs >= 0 and lon_abs >= 0:
            results = dbController.query_CoT(query=Event.point.has(and_(
                Point.lon >= 0,
                Point.lat >= 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) >= 0),
                    and_((
                        ((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lon_abs - Point.lat) * 110574.61)) >= 0)))))
        elif lon_abs < 0 and lat_abs < 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                Point.lon < 0,
                Point.lat < 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10),
                    and_(
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10)
                )
            ))])

        elif lon_abs < 0 and lat_abs > 0:
            results = dbController.query_CoT(query=Event.point.has(and_(
                Point.lon < 0,
                Point.lat >= 0,
                or_(
                    and_(
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0),
                    and_(
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0)
                ))))

        elif lon_abs > 0 and lat_abs < 0:
            results = dbController.query_CoT(query=[Event.point.has(and_(
                Point.lon >= 0,
                Point.lat < 0,
                or_(

                    and_(

                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) <= radius + 10,
                        (((lon_abs - Point.lon) * 111302.62) + ((lat_abs - Point.lat) * 110574.61)) > 0),
                    and_(

                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) <= radius + 10,
                        (((Point.lon - lon_abs) * 111302.62) + ((Point.lat - lat_abs) * 110574.61)) > 0))

            ))])

        else:
            return {"message":"unsupported coordinates"}, 500

        print(results)
        output = []
        for result in results:
            try:
                print(result.uid)
                dLon = (result.point.lon - lon)
                x = cos(radians(result.point.lat)) * sin(radians(dLon))
                y = cos(radians(lat)) * sin(radians(result.point.lat)) - sin(radians(lat)) * cos(
                    radians(result.point.lat)) * cos(radians(dLon))
                brng = atan2(x, y)
                brng = degrees(brng)
                type_pattern = [type for type in list(RestEnumerations.supportedTypeEnumerations.values()) if
                                re.fullmatch(type, result.type)]
                print(type_pattern)
                type_pattern = type_pattern[0]
                index_number = list(RestEnumerations.supportedTypeEnumerations.values()).index(type_pattern)
                print(index_number)
                type = list(RestEnumerations.supportedTypeEnumerations.keys())[index_number]
                print(type)
                part1 = result.type.split(type_pattern.split('.')[0])
                part2 = '-' + part1[1].split(type_pattern.split('.')[1])[0] + '-'
                attitude = list(RestEnumerations.attitude.keys())[list(RestEnumerations.attitude.values()).index(part2)]
                if attitude == expectedAttitude or expectedAttitude == "*":
                    pass
                else:
                    continue
                print(attitude)
                # attitude = RestEnumerations.attitude['-'+type.split(type_pattern.split('.')[0])[1].split(type_pattern.split('.')[1])+'-']

                output.append({"latitude": result.point.lat,
                               "longitude": result.point.lon,
                               "distance": distance((result.point.lon, result.point.lat), (lon, lat)).m,
                               "direction": brng,
                               "type": type,
                               "attitude": attitude
                               })
            except Exception as e:
                logger.error(str(e))
        return json.dumps(output)

    except Exception as e:
        logger.error(str(e))
        return {"message":"An error occurred retrieving geo object."}, 500