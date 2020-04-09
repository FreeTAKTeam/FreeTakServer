#######################################################
# 
# FreeTACServer.py
# Prototype Python implementation of a TAK server
# this is Alfa Code, not use it if you dont know what you are doing
# Created on:      11-Feb-2020 
# Original author: Corvo
# 
#######################################################

import sys
import socket
import select
import base64
import xmlsplitter
import _thread



HOST = '192.168.0.104' 
SOCKET_LIST = []
Threads = []
RECV_BUFFER = 4096 
PORT = 8087
CLIENT_PORT= 4242
# xml header
xmlheader = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?>"
pingEvent='<event version="2.0" uid="TACSERVER-ping" type="t-x-c-t" time="2020-02-17T12:59:03.000Z" start="2020-02-17T12:59:03.000Z" stale="2020-02-17T12:59:13.000Z" how="m-g">'
# xml point
xmlPoint ='<point lat=""0.00000000 lon=""0.00000000" hae="0.00000000" ce="9999999" le="9999999" />"'

xmlmessage = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><event version="2.0" uid="Linux-ABC.server-ping" type="b-t-f" time="2020-02-14T20:32:31.444Z" start="2020-02-14T20:32:31.444Z" stale="2020-02-15T20:32:31.444Z" how="h-g-i-g-o"><point lat="43.967087" lon="-66.126393" hae="29.30101602610336" ce="367.1" le="9999999.0" /><detail><__chat senderCallsign="freeTAKServer" chatroom="freeTAKServer" groupOwner="false" id="aa0b0312-b5cd-4c2c-bbbc-9c4c70216261" parent="RootContactGroup"><chatgrp uid0="ANDROID-R52JB0CDC4E" uid1="aa0b0312-b5cd-4c2c-bbbc-9c4c70216261" id="aa0b0312-b5cd-4c2c-bbbc-9c4c70216261"/></__chat><link relation="p-p" type="a-f-G-U-C" uid="ANDROID-R52JB0CDC4E"/><remarks time="2020-02-10T20:32:31.444Z" to="aa0b0312-b5cd-4c2c-bbbc-9c4c70216261" source="BAO.F.ATAK.ANDROID-R52JB0CDC4E">'
xmlmessage2 = '</remarks><__serverdestination destinations="192.168.0.103:4242:tcp:ANDROID-R52JB0CDC4E"/></detail></event>'
text = 'dont go away!'
ping=  xmlheader + pingEvent + xmlPoint
ping= bytes(ping, 'utf-8')



class FreeTac_server():
    
    def FreeTac_server(self):
        self.Threads = Threads
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)
     
        # add server socket object to the list of readable connections
        SOCKET_LIST.append(server_socket)     
        print("FreeTAK server started on port " + str(PORT))
     
        while 1:
    
            # get the list sockets which are ready to be read through select
            # 4th arg, time_out  = 0 : poll and never block
            ready_to_read,ready_to_write,in_error = select.select(SOCKET_LIST,[],[],0)
          
            for sock in ready_to_read:
                # a new connection request recieved
                if sock == server_socket: 
                    sockfd, addr = server_socket.accept()
                    SOCKET_LIST.append(sockfd)
                    print("Client (%s, %s) connected" % addr)
                   
                   #send ping back
                    pushTCP(addr[0], CLIENT_PORT,ping)
                   #sendPing(server_socket, sock, ping)
                    #message =   bytes( xmlmessage + "[%s:%s] entered our chatting room\n" + xmlmessage2, 'utf8')
                   # message= CursorOnTarget.atoms().encode()
                   # message=b'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n<event version="2.0" uid="GeoChat.ANDROID-7C:91:22:E8:6E:4D.All Chat Rooms.1d1f79ba-dcae-4043-8f08-2f8a8877d2ce" type="b-t-f" time="2020-02-15T03:22:01.229Z" start="2020-02-15T03:22:01.229Z" stale="2020-02-16T03:22:01.229Z" how="h-g-i-g-o"><point lat="43.855711" lon="-66.108124" hae="20.59563294031743" ce="3.0" le="9999999.0"/><detail><__chat senderCallsign="ghosty" chatroom="All Chat Rooms" groupOwner="false" id="All Chat Rooms" parent="RootContactGroup"><chatgrp uid0="ANDROID-7C:91:22:E8:6E:4D" uid1="All Chat Rooms" id="All Chat Rooms"/></__chat><link relation="p-p" type="a-f-G-U-C" uid="ANDROID-7C:91:22:E8:6E:4D"/><remarks time="2020-02-15T03:22:01.229Z" to="All Chat Rooms" source="BAO.F.ATAK.ANDROID-7C:91:22:E8:6E:4D">\xc3\xa0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa</remarks><__serverdestination destinations="192.168.0.25:4242:tcp:ANDROID-7C:91:22:E8:6E:4D"/></detail></event>'
                    #broadcast(server_socket, sockfd, message )
                 
                # a message from a client, not a new connection
                else:
                    # process data recieved from client, 
                    try:
                        # receiving data from the socket.
                        data = sock.recv(RECV_BUFFER)
                        print('received' + data.decode('utf-8'))
    
                        if data:
                            # there is something in the socket
                            broadcast(server_socket, sock, data)  
                        else:
                            # remove the socket that's broken    
                            if sock in SOCKET_LIST:
                                SOCKET_LIST.remove(sock)
    
                            # at this stage, no data means probably the connection has been broken
                            print ("Client (%s, %s) is offline\n" % addr) 
    
                    # exception 
                    except Exception as s:
                        print('something is wrong here: '  + str(s))
                        print ("Client (%s, %s) is offline\n" % addr) 
                        continue
    
        server_socket.close()
        
    
    # broadcast chat messages to all connected clients
    def broadcast (server_socket, sock, message):
        for socket in SOCKET_LIST:
            # send the message only to peer
            if socket != server_socket and socket != sock :
                try :
                    print("sending broadcast XML:")
                    print(message)
                    # try to push directly
                    address = socket.getsockname()
                    pushTCP(address[0], CLIENT_PORT, message)
                    #also broadcast
                    socket.send(message)
                    #socket.send(str.encode(message))
                    #socket.send(bytes(message, "utf8"))
                    #encoded = base64.b64encode(bytes(message,'utf-8'))
    
                    #socket.send( encoded)
                    #time.sleep(4)
                    resp = socket.recv(4096).decode('utf-8')
                    try:
                        print("response is:") 
                        print(str(resp))
                    except Exception as m:
                    # broken socket connection
                        print('broadcast response is borken. exception is: '  + str(m))
    
                except Exception as e:
                    # broken socket connection
                    print('exception by broadcasting! '  + str(e))
                    socket.close()
                    # broken socket, remove it
                    if socket in SOCKET_LIST:
                        SOCKET_LIST.remove(socket)
     
    #send a 'ping' back to keep the connection alive
    def sendPing(server_socket, sock, message):
        for socket in SOCKET_LIST:
            if socket== sock :
                try :
                    print("sending ping:")
                    print(message)
                    socket.send(message)
                except:
                    print('exception by ping! ')
    #push directly to the client using UDP 
    def pushUDP( ip_address, port, cot_xml):
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sent = sock.sendto(cot_xml, (ip_address, port))
                return sent
    #push directly to the client using TCP
    def pushTCP(ip_address, port, cot_xml):
                try:
                   sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                   conn = sock.connect((ip_address, port))
                   print("Pushing COT to " + ip_address)
                   print(cot_xml)
                   return sock.send( cot_xml)
                   #return sock.send(bytes(cot_xml,'utf-8'))
                except Exception as ty:
                    print('exception by pushing TCP! to IP:'+ ip_address+ "because: "  + str(ty))
    
    def getThreads(self):
            """Return the thread IDs used internally."""
            return self.Threads
    
    def __init__(self, host=None, port=0):
         sys.exit(FreeTac_server(self))   


    if __name__ == "__main__":
    
        sys.exit(FreeTac_server(self))     
    