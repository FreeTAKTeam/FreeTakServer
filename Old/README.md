# TAKlib
TAKlib is a Python3 library made to emulate a TAK Server for use with TAK devices, it is cross-platform and is only dependant on python stdlib libraries. 

## Documentation
under docs, you can find various documents including a UMl model of the model classes involved in a COT event.

## Requirements
- Python 3

## Installing and using TAKLib
TAKLib requires Python 3.0 or later to run. Once you’ve installed Python 3, install TAKLib using git:
```bash
git clone https://github.com/Tapawingo/TAKlib.git
cd TAKLib
```
Once TAKLib is installed you can use it by importing it to your project:
```python
from TAKlib import TAK
```
This will import the TAK class from TAKLib into your project. This means that you can now make a new server instance with:
```python
TAKServer = TAK(hostAddress, port)
```

## Example Server
The following is a simple example on how you can create a new server instance:
```python
# Imported modules
from TAKlib import TAK

# TAK connection defaults
HostAddress = "10.0.0.115"
HostPort = 8087

# Create server
TAKSock = TAK(HostAddress, HostPort)

# Create a server console
While True:

    # Grab user input
    Inp = input("Command: ")
    
    # If user enters "show clients", output connected clients
    if Inp == "show clients":
        print(str(TAKSock.getClients()))

    # If user enters "stop", stop the server
    if Inp == "stop":
        prompt = input("Are you sure(y/n)? ")
        if prompt == "y":
            TAKSock.close()
            break
```
For more information on how to use TAKlib reference the [Documentation](https://github.com/Tapawingo/TAKlib/wiki "Documentation")

The repository contains an example server with a simple console which is the same server i use for testing:
[Example Server with simple console](https://github.com/Tapawingo/TAKlib/blob/master/ServerExample.py "Example Server with simple console")
