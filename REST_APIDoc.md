# FreeTAKServer REST API Documentation
the FreeTAKServer REST API is a human readeble approach to the TAK world. The API allows you to easily connect third parties to the TAK family, without the need to understand the complexity of the COT structure or what a TCP connection is.  FTS also supports an [Internal API](REST_API_InternalDoc.md).

## How FTS manages the information
FTS will send the  information coming trough the API to all the connected clients, addtionally it will save it to the persistency, to be query in future. 

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
> To quickly test the API, you can use a browser extension like ARC Advanced rest client (Chrome). REST APIs are easy to use, however they require a minimum ammount of knowledge, we DO NOT provide support to explain WHAT an API is. Please refer to an online tutorial such as [this](http://www.steves-internet-guide.com/using-http-apis-for-iot-beginners-guide/). 

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
In most end points, the message is placed in the body of the request as JSON formatted. See below for detailed examples.
In the API using the *Get* verbs it's a variable.

## API Details
### manageAPI
set of commands relative to API management

#### getHelp
retrieve API version and supported endpoints
  * verb: GET
  * endpoint: /manageAPI/getHelp
  * returns: json containing API version and supported endpoints
  

##### Example  return data (1.7)
```json
{"APIVersion": "1.1", 
"SupportedEndpoints": 
["/ManageEmergency/deleteEmergency", "/ManageGeoObject/postGeoObject",
"/ManageEmergency/postEmergency", "/ManageGeoObject/putGeoObject", "/ManageGeoObject/getGeoObject",
"/ManageEmergency/getEmergency", "/ManagePresence/postPresence", "/ManagePresence/putPresence",
"/ManageRoute/postRoute", "/ManageChat/postChatToAll", "/DataPackageTable", "/ManageGeoObject", "/ManageEmergency",
"/FederationTable", "/ManagePresence", "/MissionTable", "/ExCheckTable", "/SendGeoChat", "/ManageRoute", "/checkStatus",
"/getZoneCoT", "/ManageChat", "/RecentCoT", "/APIUser", "/Clients", "/Alive", "/help", "/URL"]}
```

  ### manageGeoObject 
  A GeoObject is an element place on a map. It has a name, characteristics and an attitude. 
  
  #### putGeoObject
  
  * verb: PUT
  * endpoint /ManageGeoObject/postGeoObject
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
*  uid: REQUIRED input parameter, need to be an existing Id for this element,
* address: OPTIONAL address of destination if you are not sending lat/long. If sent will try to solve the exact geolocation of the destination. Possible valid examples are  
     - Big Arkansas River Park, Wichita, KS, USA 
     - Wichita, KS, USA 
     - Big Arkansas River Park, Wichita
     - and so on

   ##### Response
   * 200 Success: uid. you have create the geoObject
   * [MISSING PARAMETERNAME]: you have odmitted a parameter that is required
   * server error 500: you have probably missspelled the list of parameters (e.g geoObjects/ supported attitude). the names are case sensitive (!)
  *  server error 400: you have probably an error in the format of your JSON query
   * server error 404: you have an error in the end point definition
 

### postGeoObject

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
"address": "Washington, DC, USA",
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

##### Example 1.7 body
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

##### Response
* 200 Success: uid. you have create the geoObject
* [MISSING PARAMETERNAME]: you have odmitted a parameter that is required
* server error 500: you have probably missspelled the list of parameters (e.g geoObjects/ supported attitude). the names are case sensitive (!)
*  server error 400: you have probably an error in the format of your JSON query
* server error 404: you have an error in the end point definition
 
##### Basic GeoObjects
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
  
#####  GeoObjects Extensions for EMS
Extensions since 1.7, not available in 1.5 

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
* "Other incident other": "a-.-X-i-o" Nickname: incident (OK, missing nick name?) 
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
 * radius: radius in meters where geoObjects, default(100)
 * longitude: longitude from which radius is calculated, default(0)
 * latitude: latitude from which radius is calculated, default(0)
 * attitude: the attitude which will be filtered, default(any). see list of supported attitude above

``` JSON Variables
  "longitude": -77.02385,
  "latitude": 38.999,
  "radius"
 ```
 
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
 * method: OPTIONAL the method we plan to use for the route (Driving, Flying, Walking, Swimming, Watercraft). currently not used and set to Driving in the client
 * longitudeDest: OPTIONAL if address is not sent
 * latitudeDest: OPTIONAL if address is not sent
 * uid: OPTIONAL server generated Unique Id of this element. it will  update the existing element.  
 * routeName:OPTIONAL the name of the route
 * endName: OPTIONAL the name of the destination (end point on the route)
 * startName: OPTIONAL the  name of the start (start point of the route)
 * uid: OPTIONALserver generated Unique Id of this element. it will  update an existing route.  
* longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
* latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
 

##### Example body
```json
{
  "longitude": -77.02385,
  "latitude": 38.999,
  "routeName": "trip to Phil",
  "startName": "Washington",
  "endName": "Philadelphia",
  "timeout": 40000,
  "latitudeDest": 39.940,
  "longitudeDest": -75.01385
}
```

##### Example body 2
```json
{
 "longitude": -77.01385,
 "latitude": 38.889,
"routeName": "trip to wichita",
"timeout": 40000,
"address": "Wichita, KS, USA"
}
```

##### Example body 3
```json
{
  "longitude": -77.02385,
  "latitude": 38.999,
  "routeName": "trip to halifax",
  "latitudeDest": 44.69,
  "longitudeDest": -63.57,
  "method": "Flying"
}
```
