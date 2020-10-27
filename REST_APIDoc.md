# FreeTAKServer REST API Documentation
the FreeTAKServer REST API is a human readeble approach to the TAK world. the API  allows you to connect easily third parties to the TAK family, without the need to understand the complexity of the COT structure or what a TCP connection is.  

In the current release FTS supports following API:
  * SendGeoEvent
  * SendGeoChatToAll
  * Send Emergency
  
## General Configuration
> REST APIs are easy to use, however they require a minimum ammount of knowledge, we DO NOT provide support to explain WHAT an API is. please refer to an online tutorial such as [this](http://www.steves-internet-guide.com/using-http-apis-for-iot-beginners-guide/).

### end Point
the APi uses the following format

VERB [Protocol]://IP:PORT/APIName

for example
```
http://104.58.20.216:9999/sendGeoObject
```

### Authorization
the authorization is placed in the header of the message.
Authorization: [YOUR_API_KEY]

you need to request the key to the FTS admin. the following is a non working example
```
{“Authorization”: “K0rv0 meg@secre7apip@guesmeIfyouCan”}
```

### Message
the message is placed in the body of the request as JSON formatted

## API List
  ### SendGeoObject
  
 a GeoObject is an element place on a map. It has a name, characteristics and an attitude. 
 verb: POST
 endPoint: GeoObject

  * GeoObject: It's the information that will determine which type will be placed on the tak maps including his icon. Please see API documentation for a list of valid entries.
  *  longitude: the angular distance of the geoobject from the meridian of the greenwich, UK expressed in positive or negative float. (e.g -76.107.7998).  remember to set the display of your TAK in decimal cohordinates, where *West 77.08* is equal to '-77.08' in the API
  * latitude: the angular distance of the geoobject from the earths equator expressed in positive or negative float. (e.g 43.855682)
  * How: the way in which this geo information has been acquired. Please see API documentation for a list of valid entries.
  * attitude: the kind of expected behavior of the GeoObject (e.g friendly, hostile, unknown). Please see API documentation for a list of valid entries.
  * name: a string to ID the GeoObject on a map.

  
  #### Example body
```
{
"longitude": -77.0104,
"latitude": 38.889,
"attitude": "hostile",
"geoObject": "Gnd Combat Infantry Sniper",
"how": "nonCoT",
"name": "Putin"
}
```
 #### Response
 Success: you have create the geoObject
 [MISSING PARAMETERNAME]: you have odmitted a parameter that is required
 server error 500: you have probably missspelled the list of geoObjects/ supported attitude. the names are case sensitive (!)
 server error 400: you have probably an error in the format of your JSON query
 server error 404: you have an error in the end point definition
 
 #### List of supported Geo Objects
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
  
   #### List of supported Attitude
  * "friend"
  * "friendly"
  * "hostile"
  *  "unknown"
  *  "pending" 
  * "assumed"
  *  "neutral" 
  *  "suspect" 
  
  ## SendGeoChatObject
   verb: POST
 endPoint: Chat
 to send a GeoChat to all, you need to connect to the rest API using a rest key (we are going to explain later how that works).
After you connect you simply send the text of the message and the sender
  * message: the text of the GeoChat message
  * Sender: the name of the chat's sender, changing this will also change the chat room for the client.

```
{
"message": "sending this over Rest API",
"sender": "Admin"
}
```

