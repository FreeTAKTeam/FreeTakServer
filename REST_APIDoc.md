# FreeTAKServer REST API Documentation
the FreeTAKServer REST API is a human readeble approach to the TAK world. The API allows you to easily connect third parties to the TAK family, without the need to understand the complexity of the COT structure or what a TCP connection is.  FTS also supports an [Internal API](REST_API_InternalDoc.md).
WARNING: the current document contains experimental, not yet released functions (listed)

## List of supported API
In the current release (1.5), FTS supports following API:
  * ManageGeoEvent
  * ManageChat
  * ManageEmergency
  * ManagePresence
  
## General Configuration
> To quickly test the API, you can use a browser extension (Chrome) like ARC Advanced rest client.REST APIs are easy to use, however they require a minimum ammount of knowledge, we DO NOT provide support to explain WHAT an API is. Please refer to an online tutorial such as [this](http://www.steves-internet-guide.com/using-http-apis-for-iot-beginners-guide/). 

### endpoint
the API uses the following format

VERB [Protocol]://IP:PORT/APIName/action

for example
```
POST http://104.58.20.216:9999/manageGeoObject/postGeoObject
```

### Authorization
to use the API you need to have a REST API key.
the authorization is placed in the header of the message.
Authorization: Bearer [YOUR_API_KEY]

> you need to use the string 'Bearer' before YOUR_API_KEY

a valid key is generated from FTS' [CLI](https://github.com/FreeTAKTeam/FreeTAKServer-User-Docs/blob/main/docs/docs/CLI.md) or, since 1.4 also from the Web UI, and stored into the DB. 
to add an API user in the CLI type  
```
add_api_user
```
see CLI help for details.
To create a REST API key using the Web UI, go to the User section.

to consume the API you will need to request a key to your FTS admin. 

the following is a non-working example of a key
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
* bearing: FUTURE DEVELOPMENT, the direction expressed in degrees (1-360)   
* distance": FUTURE DEVELOPMENT, the distance in meters from the Lat/long 
* timeout:the length, expressed in seconds  until the point will stale out. Default is 300 seconds or 5 minutes.
*  uid: optional input parameter, need to be an Unique Id for this element, if not present will be  server generated, if sent ATAK will try to update an existing geoObject. Use ``putGeoObject`` instead

##### Example body
```json
{
"longitude": -77.0104,
"latitude": 38.889,
"attitude": "hostile",
 "bearing": 132, 
 "distance": 1,
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
* "Gnd Combat Infantry Rifleman",  Nickname: "Rifleman"
* "Gnd Combat Infantry grenadier", Nickname: "Grenadier"
* "Gnd Combat Infantry Mortar" , Nickname: "Mortar" 
* "Gnd Combat Infantry MachineGunner (LMG)",  Nickname: "LMG" 
* "Gnd Combat Infantry Medic" ,  Nickname: "Medic"
* "Gnd Combat Infantry Sniper",  Nickname: "Sniper"
* "Gnd Combat Infantry Recon" ,  Nickname: "Recon"
* "Gnd Combat Infantry anti Tank" ,  Nickname: "anti Tank"
* "Gnd Combat Infantry air defense",  Nickname: "AA"
* "Gnd Combat Infantry Engineer",  Nickname: "Engineer"
* "Ground"
  
##### Extensions for EMS
planned extensions for 1.7, not yet implemented in 1.5 
```json
{
"longitude": -77.0104,
"latitude": 38.889,
"attitude": "hostile",
 "bearing": 132, 
 "distance": 1,
"geoObject": "Medevac",
"how": "nonCoT",
"name": "Medevac",
"timeout": 600  
}
```

* "Gnd Equip Vehic Civilian", Nickname: Vehicle (OK)
* "Gnd Equip Vehic Ambulance": "a-.-G-E-V-m" , Nickname: Ambulance (OK)
* "Gnd Structure IM Facilities Emergency Management": "a-.-G-I-i-e" Nickname: Emergency Station (empty shape)
* "Gnd Structure IM Facilities Law Enforcement": "a-.-G-I-i-l",  Nickname: Police Station (empty shape)
* "Gnd Structure petroleum gas oil": "a-.-G-I-R-P", Nickname: gas Station (empty shape)
* "Gnd Structure Utility Electric Power": "a-.-G-I-U-E", Nickname: Power Station (empty shape)
* Gnd Structure Utility Telecommunications": "a-.-G-I-U-T", Nickname: Telco Station (empty shape)
* "Gnd Structure Hospital": "a-.-G-I-X-H", Nickname: Hospital (empty shape)
* "Gnd IM Resources": "a-.-G-U-i" Nickname: Resources (empty shape)
* "FOOD DISTRIBUTION": "b-r-.-O-O-O", Nickname: Food (OK, only label, need to implement nick) 
* "Gnd Crowd Control Team": "a-.-G-U-i-l-cct" Nickname: Police (OK)
* "Gnd Generators ": "a-.-G-U-i-p-gen" Nickname: Generator (empty shape)
* "Other incident other": "a-.-X-i-o" Nickname: incident (OK, missing nich name?) 
* "Combat search &amp; rescue (CSAR)": "a-.-A-M-F-Q-H", Nickname: SAR (OK)
* "Medevac": "a-.-G-U-C-V-R-E",, Nickname: Medevac  (OK)
* "Alarm": "b-l",  Nickname: Alarm
* "Alarm/Security/Law Enforcement/Civil Disturbance or Disorder": "b-l-l-l-cd", Nickname: Disorder
* "REFUGEES": "b-r-.-O-I-R" Nickname: Refugees
* "VANDALISM/RAPE/LOOT/RANSACK/PLUNDER/SACK": "b-r-.-O-I-V" Nickname: Riot

##### List of supported Attitude
* "friend"
* "friendly"
* "hostile"
* "unknown"
* "pending" 
* "assumed"
* "neutral" 
* "suspect" 

#### putGeoObject
update an existing geoObject cohordinates (can also update other features)

* verb: PUT
* endPoint: /ManageGeoObject/putGeoObject
* returns: UID

 #### Parameters
 *  * REQUIRED*  uid: optional input parameter, need to be an Unique Id for this element, if not present will be  server generated, if sent ATAK will try to update an existing geoObject. Use ``putGeoObject`` instead
* REQUIRED* GeoObject: It's the information that will determine which type will be placed on the tak maps including his icon. Please see API documentation for a list of valid entries.
*REQUIRED*  longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* REQUIRED* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
* REQUIRED* attitude: the kind of expected behavior of the GeoObject (e.g friendly, hostile, unknown). Please see API documentation for a list of valid entries.
* How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
* name: a string to ID the GeoObject on a map.
* bearing: FUTURE DEVELOPMENT, the direction expressed in degrees (1-360)   
* distance": FUTURE DEVELOPMENT, the distance in meters from the Lat/long 
* timeout:the length, expressed in seconds  until the point will stale out. Default is 300 seconds or 5 minutes.
##### Example body
```
{
"uid": "44455566775623",
  "longitude": -66.12614,
  "latitude": 43.96552,
"attitude": "hostile",
"geoObject": "Sniper",
}
```
 #### Response
 * 200 with UID

## ManageChat
### SendGeoChatObject
* verb: POST
* endPoint: /ManageChat/postChatToAll

 #### Parameters
* message: the text of the GeoChat message
* Sender: the name of the chat's sender, changing this will also change the chat room for the client.

```json
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
```json
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
```json
{
  "json_list": [
    {
      "PrimaryKey": 1,
      "event_id": "459b5874-1ebf-11eb-9e70-4e58de281c19"
    }
  ]
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
```json
{
"uid": "459b5874-1ebf-11eb-9e70-4e58de281c19",
  "status": "off"
}
```

## ManagePresence
manage team member position
### postPresence
* verb: POST
* endPoint: /ManagePresence/postPresence
* returns: UID

* longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
* How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
* role: the given role within the team . Please see API documentation for a list of valid entries.
* name: a string to ID the GeoObject on a map.
* team: the color of the team 
* uid: optional Unique Id of this element. if present will update an existing element. use the put insted *V. 1.7 only If you send the UID an existing CLI will be updated#

Example
```json
{
    "uid": "999b5874-1ebf-11zz-9e70-4e58de281c19",
  "how": "nonCoT",
  "name": "POTUS",
  "longitude": -77.01385,
  "latitude": 38.889,
  "role": "Team Member",
  "team": "Yellow"
}
```

### putPresence
Updates the location of a team memeber
* verb: PUT
* endPoint: /ManagePresence/putPresence
* returns: UID
 
 * uid: server generated Unique Id of this element. it will  update the existing element.  
* longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
 
Example
```json
{
    "uid": "999b5874-1ebf-11zz-9e70-4e58de281c19",
  "longitude": -77.02385,
  "latitude": 38.999
}
```
