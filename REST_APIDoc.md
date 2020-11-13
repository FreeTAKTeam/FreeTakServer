# FreeTAKServer REST API Documentation
the FreeTAKServer REST API is a human readeble approach to the TAK world. the API  allows you to connect easily third parties to the TAK family, without the need to understand the complexity of the COT structure or what a TCP connection is.  

## List of supported API
In the current release (1.2), FTS supports following API:
  * ManageGeoEvent
  * ManageChat
  * ManageEmergency
  * ManagePresence
  
## General Configuration
> To quickly test the APi you can use a browser extension (Chrome) like ARC Advanced rest client.REST APIs are easy to use, however they require a minimum ammount of knowledge, we DO NOT provide support to explain WHAT an API is. Please refer to an online tutorial such as [this](http://www.steves-internet-guide.com/using-http-apis-for-iot-beginners-guide/). 

### end Point
the APi uses the following format

VERB [Protocol]://IP:PORT/APIName/action

for example
```
POST http://104.58.20.216:9999/manageGeoObject/postGeoObject
```

### Authorization
 to use the API you need to have  a rest key .
the authorization is placed in the header of the message.
Authorization: Bearer [YOUR_API_KEY]

> you need to use the string 'Bearer' before your API KEY

a valid key is generated from FTS' [CLI](https://github.com/FreeTAKTeam/FreeTAKServer-User-Docs/blob/main/docs/docs/CLI.md) and stored into the DB. 
to add an API user in the CLI type  
```
add_api_user
```
see CLI help for details
to consume the API you need to request a key to your FTS admin. 

the following is a key non working example
```
{“Authorization”: “Bearer meg@secre7apip@guesmeIfyouCan”}
```

### Message
the message is placed in the body of the request as JSON formatted. See below for detailed examples.

## API Details
  ### manageGeoObject 
   a GeoObject is an element place on a map. It has a name, characteristics and an attitude. 
  #### postGeoObject
  
 * verb: POST
 * endPoint: /ManageGeoObject/postGeoObject
 * returns: UID
 
 #### Parameters
  * GeoObject: It's the information that will determine which type will be placed on the tak maps including his icon. Please see API documentation for a list of valid entries.
  *  longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
  * latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
  * How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
  * attitude: the kind of expected behavior of the GeoObject (e.g friendly, hostile, unknown). Please see API documentation for a list of valid entries.
  * name: a string to ID the GeoObject on a map.
  * timeout:the length, expressed in seconds  until the point will stale out. Default is 300 seconds or 5 minutes.
  *  UID: server generated Unique Id of this element

  ##### Example body
```
{
"longitude": -77.0104,
"latitude": 38.889,
"attitude": "hostile",
"geoObject": "Gnd Combat Infantry Sniper",
"how": "nonCoT",
"name": "Putin",
"timeout": 600  
}
```

 ##### Response
   * 200 Success: uid. you have create the geoObject
   * [MISSING PARAMETERNAME]: you have odmitted a parameter that is required
   * server error 500: you have probably missspelled the list of parameters (e.g geoObjects/ supported attitude). the names are case sensitive (!)
  *  server error 400: you have probably an error in the format of your JSON query
   * server error 404: you have an error in the end point definition
 
 ##### List of supported Geo Objects
  * "Gnd Combat Infantry Rifleman"
  * "Gnd Combat Infantry grenadier" 
  * "Gnd Combat Infantry Mortar" 
  * "Gnd Combat Infantry MachineGunner (LMG)" 
  * "Gnd Combat Infantry Medic" 
  * "Gnd Combat Infantry Sniper"
  * "Gnd Combat Infantry Recon" 
  * "Gnd Combat Infantry anti Tank" 
  * "Gnd Combat Infantry air defense"
  * "Gnd Combat Infantry Engineer"
  * "Ground"
  
   ##### List of supported Attitude
  * "friend"
  * "friendly"
  * "hostile"
  * "unknown"
  * "pending" 
  * "assumed"
  * "neutral" 
  * "suspect" 
  
  ## ManageChat
  ### SendGeoChatObject
   * verb: POST
   * endPoint: /ManageChat/postChatToAll

 #### Parameters
  * message: the text of the GeoChat message
  * Sender: the name of the chat's sender, changing this will also change the chat room for the client.

```
{
"message": "sending this over Rest API",
"sender": "Admin"
}
```
## ManageEmergency
### postEmergency
create a emergency into the server

  * verb: POST
  *  endPoint: /ManageEmergency/postEmergency
 
 #### Parameters
  * Name: the name of the person that has an emergency.
  * EmergencyType: the type of emergency to be displayed
  *  longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
  * latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
  *  UID: server generated Unique Id of this element


   #### List of supported Emergency Types
* "911 Alert"
* "Ring The Bell"
* "Geo-fence Breached" 
* "In Contact" 

Example
```

{
  "name": "Corvo",
  "emergencyType": "In Contact",
 "longitude": -77.01395,
"latitude": 38.889
}

```
### getEmergency
get a list of current active emergencies 

  * verb: GET
  * endPoint: /ManageEmergency/getEmergency

no parameter required

Example response
```
{
"json_list": [
  {
"PrimaryKey": 1,
"event_id": "459b5874-1ebf-11eb-9e70-4e58de281c19"
}
],
}
```

### deleteEmergency
delete an active emergency.
(TODO: delete of emergencies can be only done by the originator of it.)

  *  verb: DELETE
   * endPoint: /ManageEmergency/deleteEmergency

 #### Parameters
  * uid: server generated Unique Id of this emergency
  * status: if the emergency is currently active or not (on/off)


Example
```
{
"uid": "459b5874-1ebf-11eb-9e70-4e58de281c19",
  "status": "off"
}
```

## ManagePresence
manage team member position
### postPresence
  * verb: POST
  *  endPoint: /ManagePresence/postPresence
  *  returns: UID

  *  longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
  * latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
  * How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
  * role: the given role within the team . Please see API documentation for a list of valid entries.
  * name: a string to ID the GeoObject on a map.
  * team: the color of the team 
  * UID: server generated Unique Id of this element

Example
```
{
    "how": "nonCoT",
    "name": "POTUS",
"longitude": -77.01385,
"latitude": 38.889,
    "role": "Team Member",
    "team": "Yellow"
}
```
 
