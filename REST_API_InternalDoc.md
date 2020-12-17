## List of supported API
In the current release (1.3 internal), FTS supports following API:
  * authenticate
  * users
  * logs
  * serviceInfo
  * serverHealth
  * systemStatus
  * DataPackageTable
  * MissionTable
  
### Authorization
 to use the API you need to have  a rest key .
the authorization is placed in the header of the message.
Authorization: Bearer [YOUR_API_KEY]

> you need to use the string 'Bearer' before your API KEY

### Authorization Websocket
  to use websocket events you need to trigger
the event authenticate after connection and pass
as the body of the message ```{"Authorization": [YOUR WEBSOCKET KEY]}```

## authenticate
  ### description
   event used to authenticate new clients in the websocket
    
  ### returns
   will call the event authentication on client with message body
  ```{'successful': 'True'/'False'}``` dependant on whether or not
  the authentication was accepted.
  ### parameters
  a json body in the following format
  ```json
{"Authorization": [YOUR WEBSOCKET KEY]}
```
## users
  ### description
   event used to access list of connected client aswell as data
  relating to each client.
  
  ### returns
   a json message containing connected clients
   ```
   {
	"Users":[
		"user:"{"ip": "24.114.74.13", "callsign": "CorvoMobile", "team": "Yellow"},
		"user:"{â€‹"ip": "24.144.79.13", "callsign": "Ghost", "team": "Blue"}â€‹
	]
  }
  ```
  ### parameters
   None
   
 ## logs
 ### description
  event used to retrieve recent error log entries
  from the server
### returns
recent error logs in JSON to the client event `logUpdate` with data in the following format
```json
{
  "log_data": [
    {"time": "2020-12-16 21:15:14,618", "type": "ERROR", "file":"TCPCoTServiceController.py:31", "message": "there has been an exception in Data Package service startup maximum recursion depth exceeded while calling a Python object"}
  ]
}
```
 ### parameters
 the timestamp on the most recent log entry in format `%Y-%m-%d %H:%M:%S,%f`
 
 ## serviceInfo
 ### description
  event used to retrieve information about all services including
  their current status and port
 
 ### returns
 status and port of each service aswell as the server starttime to the client event `serviceInfoUpdate`
 with body data in the following format
 ```json
{
    "services": {
        "SSL_CoT_service": {
                      "status": "on",
                      "port": 11111
                  },
        "TCP_CoT_service": {
                      "status": "off",
                      "port": 55555
                  },
        "SSL_DataPackage_service": {
                      "status": "on",
                      "port": 52345
                  },
        "TCP_DataPackage_service": {
                      "status": "on",
                      "port": 55235
                  }
    },
    "starttime": "2020-12-16 19:51:13,278"
}
```
 ### parameters
 None
 
 ## serverHealth
 ### description
  event used to retrieve information regarding
  the status of the server hardware including
  cpu, disk and memory usage.
### returns
 current hardware usage to the client event `systemStatusUpdate` with body,
 ```json
{
    "CPU": 56,
    "memory": 39,
    "disk": 94
}
```

### parameters
None
 
 ## systemStatus
 ### description
  event used to execute test of all currently active
  services and return their respective status.
### returns
 current and expected status of all services on the server in JSON format 
 to the event `systemStatusUpdate` on the client with the body of the message 
 in the following format

 ```json
{
    "services": {
        "SSL_CoT_service": {
            "status_expected": "on",
            "status_actual": "off"
        },
        "TCP_CoT_service": {
            "status_expected": "on",
            "satus_actual": "on"
        },
        "SSL_DataPackage_service": {
            "status_expected": "on",
            "status_actual": "on"
        },
        "TCP_DataPackage_service": {
            "status_expected": "on",
            "status_actual": "on"
        },
        "SSL_Federation_service": {
            "status_expected": "off",
            "status_actual": "off"
        },
        "TCP_API_service": {
            "status_expected": "on",
            "status_actual": "on"
        }
    }
}
```

### parameters
None
 
 ## DataPackageTable
 ### description
  Endpoint used to access data regarding DataPackages
 
 #### methods
   * POST
   * GET
   * DELETE   
 
 ### GET
  returns json data containing information regarding all DataPackages currently on server
  ```json
{
"DataPackages":[
        {"Keywords": "88.104.44.76", "name": "WWIII Locations","privacy":"public", "size":"345KB", "submitted":"2020-02-10" },
        {"Keywords": "112.144.567.257", "name": "WWIII Locations","privacy":"public", "size":"345KB", "submitted":"2020-02-10" }
    ]
}
```

### POST
  accepts the zipped form of the file in the body of the message and the following arguments in the url
  * hash: 16 bit hash of the file
  * filename: the name of the zipped file
  * creator uid: the uid of the user associated with the DataPackage defaults to ```server``` if none is provided
  
### DELETE
 accepts the following json data
 ```json
{
"DataPackages":[
	{"hash": "194728885783f87ws84888943fjew"},
	{"hash": "19472mw45783f7ws848758943fjegr"}
]
}
```
the hash values are the hashes of DataPackages to be deleted
 
 ## MissionTable
 ### description 
 Endpoint used to access data regarding mission packages
 
 ### methods
 * GET
 * POST
 * DELETE
 
 ### GET
  return JSON data containing information about all current Missions
  with the following format
  ```json
{
    "version": "3",
    "type": "Mission",
    "data": [{
            "name": "save the world",
            "description": "Protect the world from Aliens",
            "chatRoom": "",
            "tool": "public",
            "keywords": ["War"],
            "creatorUid": "Anonymous",
            "createTime": "2020-12-09T15:53:42.873Z",
            "groups": ["__ANON__"],
            "externalData": [],
            "uids": [{
                    "data": "32e9089c-6ae0-4c7e-b4cd-cb16d3f46933",
                    "timestamp": "2020-12-09T15:58:10.635Z",
                    "creatorUid": "aa0b0312-b5cd-4c2c-bbbc-9c4c70216261",
                    "details": {
                        "type": "a-h-G",
                        "callsign": "R.9.155734",
                        "iconsetPath": "COT_MAPPING_2525B/a-h/a-h-G"
                    }
                }
            ],
            "contents": [{
                    "data": {
                        "filename": "Sout",
                        "keywords": [],
                        "mimeType": "application/octet-stream",
                        "name": "SWN Threat",
                        "submissionTime": "2020-12-09T15:55:21.468Z",
                        "submitter": "anonymous",
                        "uid": "3ec22850-d6de-44a5-b79c-3af16695af60",
                        "hash": "8a99e610d223426caaf267f12c3100513bbb62a66d07c5feb624d4cf5b90b69b",
                        "size": 18360
                    },
                    "timestamp": "2020-12-09T15:55:21.559Z",
                    "creatorUid": "Anonymous"
                }
            ],
            "passwordProtected": false
        }
    ],
    "nodeId": "6ff99444fa124679a3943ee90308a44c9d794c02-e5a5-42b5-b4c8-625203ea1287"
}
```
### POST
not yet implemented

### DELETE
not yet implemented

## ExCheck table
not yet implemented.