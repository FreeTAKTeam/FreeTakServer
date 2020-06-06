class SendDataController:

    def __init__(self):
        pass
    def sendDataInQueue(self, sender, processedCoT, clientInformationQueue):
        try:
            if processedCoT.modelObject.m_detail.m_marti.m_dest.callsign:
                for client in clientInformationQueue:
                    if client.modelObject.m_detail.m_contact.callsign == processedCoT.modelObject.m_detail.m_marti.m_dest.callsign:
                        sock = client.socket
                        try:
                            sock.send(processedCoT.xmlString)
                        except:
                            pass                    
                    else:
                        pass
            
            elif sender == processedCoT:
                for client in clientInformationQueue:
                    try:
                        sock = client.socket
                        sock.send(processedCoT.idData.encode())
                        sender.socket.send(client.idData.encode())
                    except:
                        pass

            else:
                for client in clientInformationQueue:

                    if client != sender:
                        sock = client.socket
                        try:
                            sock.send(processedCoT.xmlString)
                        except:
                            pass
                    else:
                        pass
        except Exception as e:
            print('data reception error')
            print(e)