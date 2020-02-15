import sys
import socket
import select
import base64
from CoT  import CursorOnTarget

HOST = '192.168.0.104' 
SOCKET_LIST = []
RECV_BUFFER = 4096 
PORT = 8087
xmlmessage = "<?xml version='1.0' encoding='UTF-8' standalone='yes'?><event version='2.0' uid='GeoChat.ANDROID-R52JB0CDC4E.Eliopoli HQ.7c9bb4f4-5061-40f4-b0b4-33a7eba4d3bd' type='b-t-f' time='2020-02-10T20:32:31.444Z' start='2020-02-10T20:32:31.444Z' stale='2020-02-11T20:32:31.444Z' how='h-g-i-g-o'><point lat='43.967087' lon='-66.126393' hae='29.30101602610336' ce='367.1' le='9999999.0' /><detail><__chat senderCallsign='corvTab' chatroom='Eliopoli HQ' groupOwner='false' id='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' parent='RootContactGroup'><chatgrp uid0='ANDROID-R52JB0CDC4E' uid1='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' id='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261'/></__chat><link relation='p-p' type='a-f-G-U-C' uid='ANDROID-R52JB0CDC4E'/><remarks time='2020-02-10T20:32:31.444Z' to='aa0b0312-b5cd-4c2c-bbbc-9c4c70216261' source='BAO.F.ATAK.ANDROID-R52JB0CDC4E'>"
xmlmessage2 = "</remarks><__serverdestination destinations='192.168.0.103:4242:tcp:ANDROID-R52JB0CDC4E'/></detail></event>"

def FreeTac_server():

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(10)
 
    # add server socket object to the list of readable connections
    SOCKET_LIST.append(server_socket)
 
    print("Chat server started on port " + str(PORT))
 
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
                #message =  xmlmessage + "[%s:%s] entered our chatting room\n" + xmlmessage2
                message= CursorOnTarget.atoms().encode()
                broadcast(server_socket, sockfd, message )
             
            # a message from a client, not a new connection
            else:
                # process data recieved from client, 
                try:
                    # receiving data from the socket.
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        # there is something in the socket
                        broadcast(server_socket, sock, "\r" + '[' + str(sock.getpeername()) + '] ' + data)  
                    else:
                        # remove the socket that's broken    
                        if sock in SOCKET_LIST:
                            SOCKET_LIST.remove(sock)

                        # at this stage, no data means probably the connection has been broken
                        broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr) 

                # exception 
                except:
                    broadcast(server_socket, sock, "Client (%s, %s) is offline\n" % addr)
                    continue

    server_socket.close()
    
# broadcast chat messages to all connected clients
def broadcast (server_socket, sock, message):
    for socket in SOCKET_LIST:
        # send the message only to peer
        if socket != server_socket and socket != sock :
            try :
                print("sending XML:")
                print(message)
                socket.send(bytes(message, "utf8"))
                #encoded = base64.b64encode(bytes(message,'utf-8'))

                #socket.send( encoded)
                time.sleep(2)
                resp = socket.recv(3000)
                print("response is:" + resp)
            except :
                # broken socket connection
                print('exception trown!')
                socket.close()
                # broken socket, remove it
                if socket in SOCKET_LIST:
                    SOCKET_LIST.remove(socket)
 
if __name__ == "__main__":

    sys.exit(FreeTac_server())     
