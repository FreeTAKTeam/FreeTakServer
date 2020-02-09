# Imported modules
from TAKlib import *
import time
import os
from CoT import CursorOnTarget

# TAK connection defaults
HostAddress = "142.93.239.220"
HostPort = 8087


# Define function to validate IP
def validateIP(s):
    if ":" in s:
        s = s.split(':')
        a = s[0].split('.')
        if len(a) != 4:
            return False
        for x in a:
            if not x.isdigit():
                return False
            i = int(x)
            if i < 0 or i > 255:
                return False
        return True
    else:
        return False

# Define function to clear screen
def clearScreen():
    os.system('cls' if os.name=='nt' else 'clear')

# Create isRunning variable
isRunning = False

# Main loop
print('To start server type "start"')
CursorOnTarget.atoms()
while True:
    # Grab user input and convert it to uppercase
    Inp = input("@TAKServer# ").upper()
    Inp = Inp.split(" ")

    # display help information
    if Inp[0] == "HELP":
        print('Available commands:')
        print('Start       -    starts the server')
        print('Show        -    shows specified information')
        print('Send        -    Send data to clients')
        print('Set         -    Sets specified variable')
        print('Shutdown    -    initiate shutdown')
        print('Stop        -    Cleanly stop server')
        print('Exit        -    Exit this Command Line Interface')

    elif Inp[0] == "START":
        if not isRunning:
            isRunning = True
            TAKSock = TAK(HostAddress, HostPort)
            print("Server starting...")
            time.sleep(2)
        else:
            print("Server already running")

    # Handle show command
    elif Inp[0] == "SHOW":
        if len(Inp) >= 2:

            # Show running threads
            if Inp[1] == "THREADS":
                print(str(TAKSock.getThreads()))

            # Show connected clients
            elif Inp[1] == "CLIENTS":
                print(str(TAKSock.getClients()))

            # Return errorlog
            elif Inp[1] == "ERRORLOG":
                print(TAKSock.getErrorLog())

            # Return log
            elif Inp[1] == "LOG":
                    print(TAKSock.getLog())

            # Return fileno of socket
            elif Inp[1] == "FILENO":
                if len(Inp) >= 3:
                    if Inp[2] == "TAK":
                        print(str(TAKSock.TAKFileno()))
                    elif Inp[2] == "HTTP":
                        print(str(TAKSock.httpFileno()))
                    else:
                        print("invalid parameter:", Inp[2])
                else:
                    print("show fileno requires more parameters:\nTAK     -    Shows Fileno for TAk socket\nHTTP    -    Shows Fileno for HTTP socket")
            else:
                print("invalid parameter:", Inp[1])
        else:
            print("Show requires more parameters:\nthreads    -    Shows currently running threads\nclients    -    Shows currently connected clients\nFileno     -    Shows fileno of specified socket\nErrorlog   -    Shows the errorlog\nLog        -    Shows the log")

    # Clear screen
    elif Inp[0] == "CLEAR":
        clearScreen()

    # Send data to clients
    elif Inp[0] == "SEND":
        if len(Inp) >= 2:

            # Send data to all clients
            if Inp[1] == "ALL":
                xmlData = input("XML String: ")
                Success, e = TAKSock.sendToAll(xmlData)
                if Success:
                    print("Sent Data")
                else:
                    print("failed to send data", e)

            # Send data to specific client
            elif validateIP(Inp[1]):
                Host = Inp[1].split(':')
                xmlData = input("XML String: ")
                Success, e = TAKSock.sendTo(xmlData, Host[0], int(Host[1]))
                if Success:
                    print("Sent Data")
                else:
                    print("failed to send data", e)
            else:
                print("invalid parameter:", Inp[1])
        else:
            print("Send requires more parameters:\nall             -    Sends data to all connected clients\n[IP Address]    -    Sends data to specified IP address")

    # Set variable
    elif Inp[0] == "SET":
        if len(Inp) >= 2:

            # Set debuglevel
            if Inp[1] == "DEBUGLEVEL":
                if len(Inp) >= 3:
                    TAKSock.setDebugLevel(int(Inp[2]))
                else:
                    print('not enough parameters')
            else:
                print('invalid parameter:', Inp[1])
        else:
            print("set requires more parameters:\ndebuglevel    -    Sets current debug level")

    # Cleanly stop server
    elif Inp[0] == "STOP":
        if isRunning:
            YN = input("Are you sure(y/n)? ")
            if YN.upper() == "Y":
                TAKSock.close()
                isRunning = False
                print("Server shutting Down...")
                time.sleep(2)
        else:
            print("Server is already stopped")

    # Cleanly shutdown server
    elif Inp[0] == "SHUTDOWN":
        if isRunning:
            YN = input("Are you sure(y/n)? ")
            if YN.upper() == "Y":
                TAKSock.close()
                isRunning = False
                print("Server shutting Down...")
                time.sleep(2)
                break
        else:
            break

    elif Inp[0] == "EXIT":
        if not isRunning:
            break
        else:
            print("Can't exit while the server is running")
    else:
        print('invalid input:', Inp[0])