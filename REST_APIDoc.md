# FreeTAKServer REST API Documentation
the FreeTAKServer REST API is a human readeble approach to the TAK world. The API allows you to easily connect third parties to the TAK family, without the need to understand the complexity of the COT structure or what a TCP connection is.  FTS also supports an [Internal API](REST_API_InternalDoc.md).
WARNING: the current document contains experimental, not yet released functions (listed)

## List of supported API
In the current release (1.7), FTS supports following API:
  * help
  * ManageGeoObject/postGeoObject
  * ManageGeoObject/putGeoObject
  * ManageGeoObject/getGeoObject
  * ManageGeoObject/getGeoObjectByZone
  * ManageEmergency/postEmergency
  * ManageEmergency/getEmergency
  * ManageEmergency/deleteEmergency 
  * ManageChat/postChatToAll
  * ManageRoute/postRoute
  * ManagePresence/postPresence
  * ManagePresence/putPresence 

  
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
  
  #### putGeoObject
  
  * verb: PUT
  * endpoint /ManageGeoObject/postGeoObject
  * returns: UID
  
  #### Parameters
  * uid
  * how
  * geoObject
  * longitude
  * latitude
  * address
  * name
  * timeout
  
   ##### Response
   * 200 Success: uid. you have create the geoObject
   * [MISSING PARAMETERNAME]: you have odmitted a parameter that is required
   * server error 500: you have probably missspelled the list of parameters (e.g geoObjects/ supported attitude). the names are case sensitive (!)
  *  server error 400: you have probably an error in the format of your JSON query
   * server error 404: you have an error in the end point definition
 
  
  #### postGeoObject

 * verb: POST
 * endPoint: /ManageGeoObject/postGeoObject
 * returns: UID
### manageGeoObject 
a GeoObject is an element place on a map. It has a name, characteristics and an attitude. 

#### postGeoObject

* verb: POST
* endPoint: /ManageGeoObject/postGeoObject
* returns: UID
 
#### Parameters
* GeoObject: It's the information that will determine which type will be placed on the tak maps including his icon. Please see API documentation for a list of valid entries. Since 1.7 you can also use nicknames for the geo objects.
*  longitude: OPTIONAL the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: OPTIONAL the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
* How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
* attitude: OPTIONAL the kind of expected behavior of the GeoObject (e.g friendly, hostile, unknown). Please see API documentation for a list of valid entries.
* name: a string to ID the GeoObject on a map.
* bearing: OPTIONALsince 1.7, the direction expressed in degrees (1-360.  default: 0)   
* distance": OPTIONAL since 1.7, the distance in meters from the Lat/long  or address
* timeout: OPTIONAL the length, expressed in seconds  until the point will stale out. Default is 300 seconds or 5 minutes.
*  uid: optional input parameter, need to be an Unique Id for this element, if not present will be  server generated, if sent ATAK will try to update an existing geoObject. Use ``putGeoObject`` instead
* address: OPTIONAL address of destination. If sent will try to solve the exact geolocation of the destination. Possible valid examples are  
     - Big Arkansas River Park, Wichita, KS, USA 
     - Wichita, KS, USA 
     - Big Arkansas River Park, Wichita
     - and so on


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

##### Example body alternate
```json
{
"address": "123 Sesame St imaginary land",
"attitude": "hostile",
"geoObject": "Gnd Combat Infantry Sniper",
"how": "nonCoT",
"name": "Putin",
"timeout": 600  
}
```

##### other Example body alternate
```json
{
"longitude": -77.0104,
"latitude": 38.889,
"distance": 500,
"bearing": 92,
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
Extensions since 1.7, not available in 1.5 

##### Example body
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
* bearing: since 1.7, the direction expressed in degrees (1-360)   
* distance": since 1.7, the distance in meters from the Lat/long 
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

#### getGeoObject
retrieve all geoObjects in a given radius
* verb: GET
* endPoint: /ManageGeoObject/getGeoObject

#### Parameters
NOTE: these should be provided in the form of url encoded variables
 * radius: radius in meters where geoobjects, default(100)
 * longitude: longitude from which radius is calculated, default(0)
 * latitude: latitude from which radius is calculated, default(0)
 * attitude: the attitude which will be filtered, default(*)

## ManageChat
### SendGeoChatObject
* verb: POST
* endPoint: /ManageChat/postChatToAll

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

##### Example body
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
  *  uid: server generated Unique Id of this element
  * address: OPTIONAL address of emergency

#### List of supported Emergency Types
* "911 Alert"
* "Ring The Bell"
* "Geo-fence Breached" 
* "In Contact" 

##### Example body
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

##### Example  response
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

##### Example body
```json
{
"uid": "459b5874-1ebf-11eb-9e70-4e58de281c19",
  "status": "off"
}
```
## ManagePresence
Manage a team member position

### postPresence
* verb: POST
* endPoint: /ManagePresence/postPresence
* returns: UID

#### Parameters
* longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
* How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
* role: the given role within the team . Please see API documentation for a list of valid entries.
* name: a string to ID the GeoObject on a map.
* team: the color of the team 
* uid: optional Unique Id of this element. if present will update an existing element. use the put insted *V. 1.7 only If you send the UID an existing CLI will be updated#

##### Example body
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
Updates the location of a team member
* verb: PUT
* endPoint: /ManagePresence/putPresence
* returns: UID
  #### Parameters
* uid: server generated Unique Id of this emergency
  
 ## getZoneCoT
 * description: retrieve all CoTs within a specified radius
 * verb: GET
 * endpoint: /getZoneCoT
 * returns: json shortened version of CoT elements
#### parameters
 * radius: the radius of the serach in meters
 * latitude: 
 * longitude: 

##### Example body
```json
{
"latitude": 43.85276,
"longitude": -66.10809,
"radius": 500
}
```

##### Example output
```json
[{"latitude": -0.0036174779081532614, "longitude": 0.0, "distance": 402.6957986915376, "direction": 180.0, "type":"Sniper", "attitude": "hostile"}, 
{"latitude": -0.004521847385157638, "longitude": 0.0, "distance": 503.36974836064377,"direction": 180.0, "type": "Sniper", "attitude": "hostile"}, 
{"latitude": 0.0, "longitude": 0.0, "distance": 0.0,"direction": 0.0, "type": "Rifleman", "attitude": "friend"}]
```
## ManageRoute
manage routes on the map

#### postRoute
 * verb: POST
 * endpoint: /ManageRoute/postRoute
 * returns: uid
 
#### parameters
 * timeout: OPTIONAL the length, expressed in seconds  until the point will stale out. Default is 300 seconds or 5 minutes.
 * address: OPTIONAL address of destination. If sent will try to solve the exact geolocation of the destination. Possible valid examples are  
     - Big Arkansas River Park, Wichita, KS, USA 
     - Wichita, KS, USA 
     - Big Arkansas River Park, Wichita
     - and so on
 * method: OPTIONAL the method we plan to use for the route (Driving, walking). currently not used
 * longitudeDest: OPTIONAL if address is not sent
 * latitudeDest: OPTIONAL if address is not sent
 * uid: OPTIONAL server generated Unique Id of this element. it will  update the existing element.  
 * routeName
 * endName
 * startName
 * uid: server generated Unique Id of this element. it will  update the existing element.  
* longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
 

##### Example body
```json
{
    "uid": "bf2035ce-8f40-11eb-895a-4e58de281c19",
   
  "longitude": -77.02385,
  "latitude": 40.999
}
```

##### Example body 2
```json
{
 "longitude": -77.01385,
 "latitude": 38.889,
"name": "trip to wichita",
"timeout": 40000,
"address": "Wichita, KS, USA"
}
```

##### Example body, alternate
```json
{
  "longitude": -77.02385,
  "latitude": 38.999,
"name": "end location",
"timeout": 40000,
"latitudeDest": -97,
"longitudeDest": 37,
"method": "Driving"
}
```

### getHelp
  * verb: GET
  * endpoint: /manageAPI/getHelp
  * returns: json containing API version and supported endpoints
  
Example return data
```json
{"APIVersion": "1.7", 
"SupportedEndpoints": 
["/ManageEmergency/deleteEmergency", "/ManageGeoObject/postGeoObject",
"/ManageEmergency/postEmergency", "/ManageGeoObject/putGeoObject", "/ManageGeoObject/getGeoObject",
"/ManageEmergency/getEmergency", "/ManagePresence/postPresence", "/ManagePresence/putPresence",
"/ManageRoute/postRoute", "/ManageChat/postChatToAll", "/DataPackageTable", "/ManageGeoObject", "/ManageEmergency",
"/FederationTable", "/ManagePresence", "/MissionTable", "/ExCheckTable", "/SendGeoChat", "/ManageRoute", "/checkStatus",
"/getZoneCoT", "/ManageChat", "/RecentCoT", "/APIUser", "/Clients", "/Alive", "/help", "/URL"]}
```
