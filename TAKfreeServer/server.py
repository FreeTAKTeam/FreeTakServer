#######################################################
#
# TAKFreeServer.py
# Original author: naman108
# This code is Open Source, made available under the EPL 2.0 license.
# https://www.eclipse.org/legal/eplfaq.php
# credit to Harshini73 for base code
#
#######################################################
import argparse
import datetime
import logging
import os
import socket
import sqlite3
import sys
import threading
import time
import traceback
import uuid
import xml.etree.ElementTree as ET
from logging.handlers import RotatingFileHandler

import constants
import SQLcommands
from Controllers.RequestCOTController import RequestCOTController
from Controllers.serializer import Serializer

const = constants.vars()
sql = SQLcommands.sql()


def newHandler(filename, log_level, log_format):
    handler = RotatingFileHandler(
        filename,
        maxBytes=const.MAXFILESIZE,
        backupCount=const.BACKUPCOUNT
    )
    handler.setFormatter(log_format)
    handler.setLevel(log_level)
    return handler


log_format = logging.Formatter(const.LOGFORMAT)
logger = logging.getLogger(const.LOGNAME)
logger.setLevel(logging.DEBUG)
logger.addHandler(newHandler(const.DEBUGLOG, logging.DEBUG, log_format))
logger.addHandler(newHandler(const.WARNINGLOG, logging.WARNING, log_format))
logger.addHandler(newHandler(const.INFOLOG, logging.INFO, log_format))
console = logging.StreamHandler(sys.stdout)
console.setFormatter(log_format)
console.setLevel(logging.DEBUG)
logger.addHandler(console)


''' Server class '''
class ThreadedServer(object):
    def __init__(self, host=const.IP, port=const.PORT):
        # change from string
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.client_dict = {}
        logger.info(f"Server IP: {host}, server port: {port}")
        self.emergencyDict = {}
        # configure sql database
        with sqlite3.connect(const.DATABASE) as db:
            cursor = db.cursor()
            cursor.execute(sql.CREATEUSERSTABLE)
            cursor.close()
            db.commit()
        self.bandaidUID = ''

    def listen(self):
        '''
        listen for client connections and begin thread if found
        '''
        threading.Thread(target=self.bandaid, args=(), daemon=True).start()
        self.sock.listen(1000)
        while True:
            try:
                client, address = self.sock.accept()
                threading.Thread(target=self.listenToClient, args=(client, address), daemon=True).start()
            except:
                logger.error(traceback.format_exc())
                logger.error('Error in listen()')

    def bandaid(self):
        while True:
            try:
                start = datetime.datetime.now()
                end = start + datetime.timedelta(minutes=const.RENEWTIME)
                while datetime.datetime.now() < end:
                    time.sleep(10)
                self.bandaidUID = uuid.uuid1()
                mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                mysock.connect(('127.0.0.1', const.PORT))
                mysock.send(Serializer().serializerRoot(RequestCOTController().ping(eventuid=self.bandaidUID)).encode())
                mysock.recv(2048)
                mysock.shutdown(socket.SHUT_RDWR)
                mysock.close()
                logger.info('finished bandaid keepalive')
                logger.debug(f"Currently running {len(threading.enumerate())} threads")
            except ConnectionRefusedError:
                logger.warning("Bandaid listening socket was closed")
            except:
                logger.error(traceback.format_exc())
                logger.error("Error in bandaid()")

    def check_xml(self, xml_string, current_id):
        '''
        check xml type or class
        '''
        data_value = ''
        try:
            if xml_string == const.EMPTY_BYTE:
                logger.info('client disconnected via empty byte response')
                self.client_dict[current_id]['alive'] = 0
                logger.info(str(self.client_dict[current_id]['uid'])+' disconnected')
                return const.FAIL
            elif xml_string == None:
                logger.info('client disconnected via none response')
                self.client_dict[current_id]['alive'] = 0
                logger.info(str(self.client_dict[current_id]['uid'])+' disconnected')
                return const.FAIL

            tree = ET.fromstring(xml_string)
            uid = tree.get('uid')
            logger.debug('parsing data uid is ' + str(uid))
            cot_type = tree.get('type')
            if cot_type == "a-f-G-U-C":
                self.client_dict[current_id]['id_data'] = xml_string
            elif cot_type == 'b-f-t-a':
                destination = tree.find('detail').find('marti').find('dest').attrib['callsign']
                connData = self.client_dict[current_id]["id_data"]
                for x in self.client_dict:
                    if self.client_dict[x]["callsign"] == destination:
                        self.client_dict[x]["main_data"].append(connData)
                        logger.info('adding conn data to '+str(x))
                        logger.info(f"Now adding the following connection data: {str(connData)}")
            if uid.endswith("9-1-1"):
                for x in tree.iter('emergency'):
                    if x.get('cancel') != 'true':
                        self.emergencyDict[uid] = xml_string
                    else:
                        del self.emergencyDict[uid]
            elif uid.endswith(const.PING):
                data_value = const.PING
                logger.debug(f"Received a ping: {xml_string}")
            elif uid.startswith(const.GEOCHAT):
                data_value = const.GEOCHAT
                logger.debug(f"Received a GeoChat: {xml_string}")
            else:
                logger.debug(f"Received CoT: {xml_string}")

            # adds data to all connected client data list except sending client
            for detail in tree.findall('detail'):
                marti = detail.find('marti')
                if marti != None:
                    dest = marti.find('dest')
                    callsign = dest.attrib['callsign']
                    for client_id in self.client_dict:
                        if self.client_dict[client_id]['callsign'] == callsign:
                            self.client_dict[client_id]['main_data'].append(xml_string)
                else:
                    for client_id in self.client_dict:
                        if client_id != current_id:
                            self.client_dict[client_id]['main_data'].append(xml_string)
            return data_value

        except:
            logger.error(traceback.format_exc())
            logger.error(f"Error in check_xml for: {xml_string}")

    def connectionSetup(self, client, address):
        db = sqlite3.connect(const.DATABASE)
        try:
            cursor = db.cursor()
            first_run = 1
            # Create client dictionary within main dictionary containing arrays for data and chat also other stuff for client initial connection
            total_clients_connected = 0
            total_clients_connected += 1
            id_data = client.recv(const.STARTBUFFER)
            logger.debug(f"id_data = {id_data}")
            tree = ET.fromstring(id_data)
            uid = tree.get('uid')
            if uid == self.bandaidUID:
                return 'Bandaid'
            callsign = tree.find('detail').find('contact').attrib['callsign']
            current_id = uuid.uuid1().int

            # add identifying information
            self.client_dict[current_id] = {
                'id_data': id_data,
                'main_data': [],
                'alive': 1,
                'uid': uid,
                'client': client,
                'callsign': callsign
            }
            cursor.execute(sql.INSERTNEWUSER, (str(current_id), str(uid), str(callsign)))
            cursor.close()
            db.commit()
            logger.info(f"Client connected, initial information for current_id={current_id}: {self.client_dict[current_id]}")
            return str(first_run)+' ? '+str(total_clients_connected)+' ? '+str(id_data)+' ? '+str(current_id)
        except:
            logger.error(traceback.format_exc())
            logger.error('Error in connection setup')
            return "error"
        finally:
            db.close()

    def recieveAll(self, client):
        try:
            total_data = []
            while True:
                data = client.recv(const.BUFFER)
                logger.debug(f"Received {sys.getsizeof(data)} bytes from {client}")
                if sys.getsizeof(data) == const.BUFFER+33:
                    total_data.append(data)
                elif sys.getsizeof(data) < const.BUFFER+33:
                    total_data.append(data)
                    break
            total_data = b''.join(total_data)
            return total_data
        except:
            logger.error(traceback.format_exc())
            logger.error(f"Error in recieveAll() from {client}")
            return None

    def listenToClient(self, client, address):
        ''' 
        Function to receive data from the client. this must be long as everything
        '''
        try:
            defaults = self.connectionSetup(client, address)
            if defaults == 'error':
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                return
            elif defaults == 'Bandaid':
                self.sock.shutdown(socket.SHUT_RDWR)
                client.close()
                return
            else:
                defaults = defaults.split(' ? ')
                logger.debug(defaults)
                first_run = int(defaults[0])
                id_data = bytes(defaults[2], 'utf-8')
                current_id = int(defaults[3])
                # main connection loop
                while True:
                    # Receive data
                    try:
                        if first_run == 0:
                            data = self.recieveAll(client)
                            logger.debug(f"Received data from client: {str(data)}")
                            working = self.check_xml(data, current_id)
                            # checking if check_xml detected client disconnect
                            if working == const.FAIL:
                                timeoutInfo = Serializer().serializerRoot(RequestCOTController().timeout(
                                    eventhow='h-g-i-g-o',
                                    eventuid=uuid.uuid1(),
                                    linkuid=self.client_dict[current_id]['uid']
                                ))
                                logger.debug(f"Sending timeout: {timeoutInfo.encode()}")
                                for client_id in self.client_dict:
                                    if client_id != current_id:
                                        self.client_dict[client_id]['client'].send(timeoutInfo.encode())
                                uid = self.client_dict[current_id]['uid']
                                del self.client_dict[current_id]
                                with sqlite3.connect(const.DATABASE) as db:
                                    cursor = db.cursor()
                                    cursor.execute(sql.DELETEBYUID, (uid,))
                                    cursor.close()
                                    db.commit()
                                    client.shutdown(socket.SHUT_RDWR)
                                    client.close()
                                return
                            elif working == const.PING:
                                logger.debug('Received ping')

                        elif first_run == 1:
                            for client_id in self.client_dict:
                                client = self.client_dict[client_id]['client']
                                if client != self.client_dict[current_id]['client']:
                                    logger.info('Sending '+str(id_data))
                                    client.send(self.client_dict[current_id]['id_data'])
                            for client_id in self.client_dict:
                                data = self.client_dict[client_id]['id_data']
                                logger.debug('Sending conn data to '+str(client))
                                client.send(data)
                            threading.Thread(
                                target=self.sendClientData,
                                args=(client, address, current_id),
                                daemon=True).start()

                        # just some debug stuff
                        first_run = 0
                    except:
                        logger.error(traceback.format_exc())
                        logger.error('Error in listenToClient() main loop')
                        client.close()
                        return
        except Exception as e:
            logger.error(traceback.format_exc())
            logging.error("Unknown error in listenToClient")
            client.close()

    def sendClientData(self, client, address, current_id):
        try:
            while True:
                time.sleep(const.DELAY)
                for uid in self.emergencyDict:
                    client.send(self.emergencyDict[uid])
                    logger.info(f"Emergency activated: {uid}")

                if len(self.client_dict[current_id]['main_data']) > 0:
                    for x in self.client_dict[current_id]['main_data']:
                        logger.debug(self.client_dict[current_id]['main_data'])
                        client.send(x)
                        logger.info('Sent ' + str(x) + ' to ' + str(address))
                        self.client_dict[current_id]['main_data'].remove(x)
                else:
                    client.send(Serializer().serializerRoot(RequestCOTController().ping(eventuid=uuid.uuid1())).encode())
        except:
            logger.error(traceback.format_exc())
            logger.warning('Error in sendClientData')
        finally:
            client.close()


def startup():
    logger.info('starting windows service')
    ThreadedServer(host=const.IP, port=const.PORT).listen()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("-p", type=int)
        args = parser.parse_args()
        port = args.p
    except:
        ThreadedServer(host='', port=const.PORT).listen()
        logger.error(f"Failed to read port number from command arguments, defaulting to {const.PORT}")
        port = const.PORT
    ThreadedServer(host=const.IP, port=port).listen()
