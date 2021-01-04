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

## connect
### description
event triggered on initial connection to server<br />
Event: `connect` (this is a special event as it is called automatically on connection)<br />
Subscription: `connectUpdate`

### returns
  ```json
{
"starttime": ""(time at which server was started),
"version": ""(version of FTS currently running)
}
```

## authenticate
  ### description
   event used to authenticate new clients in the websocket<br />
   Event: `authenticate` <br />
   Subscription: `authentication`
  ### returns
   will call the event authentication on client with message body
  ```{'successful': 'True'/'False'}``` dependant on whether or not
  the authentication was accepted.
  
  ### parameters
  a JSON body in the following format
  ```json
{"Authorization": [YOUR WEBSOCKET KEY]}
```
## users
  ### description
   event used to access list of connected client aswell as data
  relating to each client.<br />
   Event: `users` <br />
   Subscription: `userUpdate`
  
  ### returns
   a JSON message containing connected clients
   ```
   {
	"Users":[
		"user:"{"ip": "24.114.74.13", "callsign": "CorvoMobile", "team": "Yellow"},
		"user:"{"ip": "24.144.79.13", "callsign": "Ghost", "team": "Blue"}
	]
  }
  ```
  ### parameters
   None
   
 ## systemUser
 retrieve all system users and their associated information<br />
   Event: `systemUser` <br />
   Subscription: `systemUserUpdate`
 
 ### returns
 system user information
 ```json
{
	"systemUsers": [
		  {"Name": "Dan", "Group": "Yellow", "Token": "", "Password": "", "Certs": "a.zip", "Uid": ""},
		  {"Name": "Joe", "Group": "Yellow", "Token": "", "Password": "", "Certs": "b.zip", "Uid": ""},
		  {"Name": "Bill", "Group": "Yellow", "Token": "", "Password": "", "Certs": "c.zip", "Uid": ""}
	]
}
````
 ### parameters
 None
 
 ## addSystemUser
 ### description
 add one or many system users to the server<br />
   Event: `addSystemUser`
 ### returns
 None
 ### parameters
 ```json
 {
	"systemUsers": [
		  {"Name": "Dan", "Group": "Yellow", "Token": "", "Password": "", "Certs": "true"},
		  {"Name": "Joe", "Group": "Blue", "Token": "", "Password": "", "Certs": "true"},
		  {"Name": "Bill", "Group": "Red", "Token": "", "Password": "", "Certs": "true"}
	]
}
```
## removeSystemUser
### description
remove a system user from the server<br />
   Event: `removeSystemUser`
### returns
None
### parameters
```json
{
  "systemUsers": [
    {"uid": "[uid of system user to be deleted]"},
    {"uid": "[uid of system user to be deleted]"},
    {"uid": "[uid of system user to be deleted]"}
  ]
}
```
 ## logs
 ### description
  event used to retrieve recent error log entries
  from the server<br />
   Event: `logs` <br />
   Subscription: `logUpdate`
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
  their current status and port<br />
   Event: `serviceInfo` <br />
   Subscription: `serviceInfoUpdate`
 
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
                  },
        "Federation_server_service": {
                      "status": "on",
                      "port": 55235
                  },
        "Rest_API_service": {
                      "status": "on",
                      "port": 55235
                  }
    },
    "IP": "127.0.0.1"
}
```
 ### parameters
 None
 
 ## serverHealth
 ### description
  event used to retrieve information regarding
  the status of the server hardware including
  cpu, disk and memory usage.<br />
   Event: `serverHealth` <br />
   Subscription: `serverHealthUpdate`
### returns
 current hardware usage to the client event `serverHealthUpdate` with body,
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
  services and return their respective status.<br />
   Event: `systemStatus` <br />
   Subscription: `systemStatusUpdate`
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
 
 ## changeServiceInfo
 ### description
 Event used to change the status of each service running on the server<br />
   Event: `changeServiceInfo` <br />
   Subscription: `systemStatusUpdate`
 
### returns
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
    "ip": "127.0.0.1"
  }
 ```

 ### parameters
 accepts JSON data containing information regarding the desired status of each service in the following format
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
    "ip": "127.0.0.1"
}
```

`ip`: ip on which the server should be listening eg: `0.0.0.0`<br/>
`status`: whether the service is to be started or stopped eg: `on`, `off` <br />
`port`(optional): the port on which the service should be listening eg: `8089` <br />
not all services need to be in every message only those you would like to change
 
 ## systemUsers
  Event used to retrieve all system users<br />
   Event: `systemUsers` <br />
   Subscription: `systemUsersUpdate`
 ### returns
 the metadata of each user
 ```json{
	"systemUsers":[
		{"Name": "Dan", "Group": "Yellow", "Token": "Token1", "Password": "psw1", , "Certs": "a.zip"},
		{"Name": "Joe", "Group": "Yellow", "Token": "Token1", "Password": "psw1", , "Certs": "a.zip"},
		{"Name": "Bill", "Group": "Yellow", "Token": "Token1", "Password": "psw1", , "Certs": "a.zip"}
	]
}
```
##parameters
None

## addSystemUsers
used to create a new system user on the server<br />
   Event: `addSystemUsers` <br />
### returns
None
### parameters
```json
{
  "systemUsers":
	[
	    {"Name":"dan", "Group":"Yellow", "Token":"token", "Password": "psw1", "Certs":"true" }
	]
}
```
 * Name: name of user
 * Group: group of user
 * Token: api token of user(optional)
 * Password: password for user(optional)
 * Certs: whether the user should have certs generated(should be true in ui)
 ## removeSystemUsers
used to remove a system user and their associated files from the server<br />
   Event: `removeSystemUsers` <br />
 ###returns
 None
 ### parameters
 ```json
{ "systemUsers": 
  [ 
    { "uid": "46b3de87-85f5-400d-a098-536f2e1421ce" } 
  ] 
}
```
 * uid: uid of user to remove
 ## DataPackageTable
 ### description
  Endpoint used to access data regarding DataPackages
 
 #### methods
   * POST
   * GET
   * DELETE   
 
 ### GET
  returns JSON data containing information regarding all DataPackages currently on server
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
  * filename: the name of the zipped file
  * creatorUid(optional): the uid of the user associated with the DataPackage defaults to ```server``` if none is provided
  
### DELETE
 accepts the following JSON data
 ```json
{
"DataPackages":[
	{"hash": "194728885783f87ws84888943fjew"},
	{"hash": "19472mw45783f7ws848758943fjegr"}
]
}
```
the hash values are the hashes of DataPackages to be deleted

### PUT
 accepts the following JSON data
 ```json
{
  "DataPackages": [
    {"PrimaryKey": "1", "Name": "new_name", "Keywords": "new keywords", "Privacy": "0"}
  ]
}
```
 * PrimaryKey: primary key of DataPackage to be modified
 * Name: optional new name of DataPackage if not set name will not be changed
 * Keywords: optional new keywords of DataPackage if not set keywords will not be changed
 * Privacy: optional new privacy of DataPackage if not set privacy will not be changed must be 1(Private) or 0(Public)

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
Endpoint used to access data regarding ExCheck items such as checklists and templates

### POST
  creates a template on the server from a supplied xml file accepting the following URL encoded values:
  * clientUid: the uid of the client to be recognized as the creator of the template

### DELETE
accepts the following data
  ```json
{
    "ExCheck": 
    {
      "Templates": [{"uid": "TemplateUID1"}, {"uid": "TemplateUID2"}],
      "Checklists": [{"uid": "ChecklistUID1"}, {"uid": "ChecklistUID2"}]  
    }
}
```
`uid`: the uid of those Checklists and Templates to be deleted

### GET
return JSON data containing the following information about Checklists and Templates present on the server
```json
{
  "ExCheck": {
    "Templates": [
      {
        "filename": "cdd39d06-b43e-42f4-839d-32362febe9a1.xml", (name of file containing template xml)
        "name": "test from atak", (name associated with template)
        "submissionTime": "2020-12-22T22:07:31.749284Z", (time template was submitted to server)
        "submitter": "[('NOVA',)]", (callsign of submitter)
        "uid": "cdd39d06-b43e-42f4-839d-32362febe9a1", (uid of template)
        "hash": "bfb97ed985f789b0c97cf3a93a4354e36eadadd0b6d156c4e4a5ad25330a8c45", (hash of template)
        "size": 1735, (size of template in bytes)
        "description": "test from atak desc" (description of template)
      }
    ],
    "Checklists": [
      {
        "filename": "c5322e53-5b95-4def-953d-6be9e42e79fd.xml", (name of file containing checklist xml)
        "name": "test from atak", (name associated with template)
        "startTime": "2020-12-22T22:07:32.841000Z", (time checklist was created)
        "submitter": "NOVA", (callsign of user to submit checklist)
        "uid": "c5322e53-5b95-4def-953d-6be9e42e79fd", (uid of checklist)
        "description": "test from atak desc", (description of checklist)
        "template":"cdd39d06-b43e-42f4-839d-32362febe9a1" (uid of template of which the checklist is an instance)
      }
    ]
  }
}
```
## FederationTable
endpoint used to access federation objects

### GET
return JSON data containing the following information regarding current checklists and templates present on the server
```json
{
"outgoingFederations":
	[{
		"Name": "federation 1",
		"Address": "127.0.0.1",
		"Port": "11111",
		"FallBack": "federation 2",
		"Status": "Disabled",
		"ReconnectInterval": "32",
		"MaxRetries": "15",
		"LastError": "Timeout"
	}]
}
```

### POST
create a new outgoing federation
```json
{
"outgoingFederations":[{
		"Name": "federation 1",
		"Address": "127.0.0.1",
		"Port": "11111",
		"FallBack": "federation 2",
		"Status": "Disabled",
		"ReconnectInterval": "32",
		"MaxRetries": "15",
	}]
}
```

### DELETE
Not yet implemented
