#######################################################
# 
# TAKFreeServer.py
# Original author: naman108
# This code is Open Source, made available under the EPL 2.0 license.
# https://www.eclipse.org/legal/eplfaq.php
# credit to Harshini73 for base code
#
#######################################################
import sys
import os
PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import socket
import threading
import argparse
import time
import xml.etree.ElementTree as ET
import constants
import logging
from Controllers.RequestCOTController import RequestCOTController
from Controllers.serializer import Serializer
import multiprocessing as multi
const = constants.vars()
from logging.handlers import RotatingFileHandler
import uuid
import datetime
import sqlite3
from SQLcommands import sql
sql = sql()
'''
configure logging
'''
format = logging.Formatter(const.LOGTIMEFORMAT)
logger = logging.getLogger(const.LOGNAME)
logger.setLevel(logging.DEBUG)
debug = RotatingFileHandler(const.DEBUGLOG, maxBytes=const.MAXFILESIZE,backupCount=const.BACKUPCOUNT)
debug.setLevel(logging.DEBUG)
warning = RotatingFileHandler(const.WARNINGLOG, maxBytes=const.MAXFILESIZE,backupCount=const.BACKUPCOUNT)
warning.setLevel(logging.WARNING)
info = RotatingFileHandler(const.INFOLOG, maxBytes=const.MAXFILESIZE,backupCount=const.BACKUPCOUNT)
info.setLevel(logging.INFO)
debug.setFormatter(format)
warning.setFormatter(format)
info.setFormatter(format)
logger.addHandler(warning)
logger.addHandler(debug)
logger.addHandler(info)

logger.debug('called or imported')
hostname = socket.gethostname()
''' Server class '''
class ThreadedServer(object):
	def __init__(self, host = const.IP, port=const.DEFAULTPORT):
		#change from string
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.client_dict = {}
		logger.info('startup ip is '+self.host+' startup port is '+str(self.port))
		self.emergencyDict = {}
		#configure sql database
		sqliteServer = sqlite3.connect(const.DATABASE)
		cursor = sqliteServer.cursor()
		cursor.execute(sql.CREATEUSERSTABLE)
		sqliteServer.commit()
		cursor.close()
		sqliteServer.close()
		self.bandaidUID = ''
	def listen(self):
		'''
		listen for client connections and begin thread if found
		'''
		threading.Thread(target = self.bandaid, args = (), daemon=True).start()
		self.sock.listen(1000)
		while True:
			try:
				client, address = self.sock.accept()
				threading.Thread(target = self.listenToClient,args = (client,address), daemon=True).start()
				
			except Exception as e:
				logger.warning('error in main listen function '+str(e))
	#issue in following func
	def bandaid(self):
		while True:
			start = datetime.datetime.now()
			end = start + datetime.timedelta(minutes = const.RENEWTIME)
			while datetime.datetime.now() < end:
				time.sleep(10)
			self.bandaidUID=uuid.uuid1()
			mysock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			mysock.connect(('127.0.0.1', const.DEFAULTPORT))
			mysock.send(Serializer().serializerRoot(RequestCOTController().ping(eventuid = self.bandaidUID)).encode())
			mysock.recv(2048)
			mysock.shutdown(socket.SHUT_RDWR)
			mysock.close()
			logger.info('finished bandaid keepalive')
			logger.info('nuber of threads is ')
			logger.info(threading.enumerate())
	def check_xml(self, xml_string, current_id):
		'''
		check xml type or class
		'''
		data_value = ''
		try:
			if xml_string == const.EMPTY_BYTE:
				print('client disconnected via empty byte response')
				self.client_dict[current_id]['alive'] = 0
				logger.info(str(self.client_dict[current_id]['uid'])+' disconnected')
				return const.FAIL
			elif xml_string == None:
				print('client disconnected via none response')
				self.client_dict[current_id]['alive'] = 0
				logger.info(str(self.client_dict[current_id]['uid'])+' disconnected')
				return const.FAIL

			tree = ET.fromstring(xml_string)
			uid = tree.get('uid')
			logger.debug('parsing data uid is ' +str(uid))
			type = tree.get('type')
			if type == "a-f-G-U-C":
				self.client_dict[current_id]['id_data'] = xml_string
			elif type == 'b-f-t-a':
				detail = tree.find('detail')
				marti = detail.find('marti')
				dest = marti.find('dest')
				destination = dest.attrib['callsign']
				connData = self.client_dict[current_id]["id_data"]
				for x in self.client_dict:
					if self.client_dict[x]["callsign"] == destination:
						self.client_dict[x]["main_data"].append(connData)
						print('adding conn data to '+str(x))
						logger.info('now adding connection data as follows')
						logger.info(str(connData))
					else:
						pass

			try:
				uid_by_dot = uid.split('.')
				uid_by_dash = uid.split('-')
			except:
				uid_by_dash = uid.split('-')
			logger.debug(uid_by_dash)
			if str(uid_by_dash[-1]) == '1' and str(uid_by_dash[-2]) == '1' and str(uid_by_dash[-3] == '9'):
				for x in tree.iter('emergency'):
					if x.get('cancel') != 'true':
						self.emergencyDict[uid] = xml_string
					else:
						del self.emergencyDict[uid]
			elif uid_by_dash[-1] == const.PING:
				data_value = const.PING
			elif len(uid_by_dot)>0:
				if uid_by_dot[0] == const.GEOCHAT:
					data_value = const.GEOCHAT
					logger.info('recieved the following GeoChat '+str(xml_string))
				else:
					True
			else:
				logger.info('recieved the following CoT '+str(xml_string))
				pass
			
			#adds data to all connected client data list except sending client
			for detail in tree.findall('detail'):
				marti = detail.find('marti')
				if marti != None:
					sqliteServer = sqlite3.connect(const.DATABASE)
					dest = marti.find('dest')
					callsign = dest.attrib['callsign']
					if type == 'b-f-t-a':
						for x in self.client_dict:
							id = x
							if self.client_dict[id]['callsign'] == callsign:
								self.client_dict[id]['main_data'].insert(-1 ,xml_string)
							else:
								pass
					else:
						for x in self.client_dict:
							id = x
							if self.client_dict[id]['callsign'] == callsign:
								self.client_dict[id]['main_data'].append(xml_string)
							else:
								pass
				else:
					for x in self.client_dict:
						if x == current_id:
							pass
						elif x!=current_id:
							self.client_dict[x]['main_data'].append(xml_string)
		
				return data_value

		except Exception as e:
			logger.warning('error in message parsing '+str(e))
			logger.warning(xml_string)


	def connectionSetup(self, client, address):
		try:

			sqliteServer = sqlite3.connect(const.DATABASE)
			cursor = sqliteServer.cursor()

			first_run = 1
			#create client dictionary within main dictionary containing arrays for data and chat also other stuff for client enitial connection
			current_id = 0
			total_clients_connected = 0
			total_clients_connected += 1
			id_data = client.recv(const.STARTBUFFER)
			print(id_data)
			print('\n'+str(id_data))
			print('\n \n')
			tree = ET.fromstring(id_data)
			uid = tree.get('uid')
			if uid == self.bandaidUID:
				return 'Bandaid'
			callsign = tree[1][1].attrib['callsign']
			current_id = uuid.uuid1().int

			#add identifying information
			self.client_dict[current_id] = {'id_data': '', 'main_data': [], 'alive': 1, 'uid': '', 'client':client, 'callsign':callsign}
			self.client_dict[current_id]['id_data'] = id_data
			self.client_dict[current_id]['uid'] = uid
			cursor.execute(sql.INSERTNEWUSER,(str(current_id), str(uid), str(callsign)))
			sqliteServer.commit()
			cursor.close()
			sqliteServer.close()
			#print(self.client_dict)
			logger.info('client connected, information is as follows initial'+ '\n'+ 'connection data:'+str(id_data)+'\n'+'current id:'+ str(current_id))
			return str(first_run)+' ? '+str(total_clients_connected)+' ? '+str(id_data)+' ? '+str(current_id)
		except Exception as e:
			logger.warning('error in connection setup: ' + str(e))
			logger.warning(id_data)
			return "error"

	def recieveAll(self, client):
				try:
					total_data = []
					count = 0
					dead = 0
					final = []
					#227:260
					#360:393
					while True:
						data = client.recv(const.BUFFER)
						print(sys.getsizeof(data))
						if sys.getsizeof(data)==const.BUFFER+33:
							total_data.append(data)
						elif sys.getsizeof(data) < const.BUFFER+33:
							total_data.append(data)
							break
					total_data=b''.join(total_data)
					return total_data
				except Exception as e:
					logger.warning('error in recieve all')
					logger.warning(e)
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
				return 1
			elif defaults == 'Bandaid':
				self.sock.shutdown(socket.SHUT_RDWR)
				client.close()
				return 1
			else:
				defaults = defaults.split(' ? ')
				print(defaults)
				first_run=defaults[0]
				id_data=defaults[2]
				current_id = defaults[3]
				first_run = int(first_run)
				id_data = bytes(id_data, 'utf-8')
				current_id = int(current_id)
				#main connection loop
				killSwitch = 0
				while killSwitch == 0:
					#recieve data

					try:
						if first_run == 0:
							data = self.recieveAll(client)
							logger.debug(data)
							working = self.check_xml(data, current_id)
							#checking if check_xml detected client disconnect
							if working == const.FAIL:
								timeoutInfo = Serializer().serializerRoot(RequestCOTController().timeout(eventhow = 'h-g-i-g-o', eventuid = uuid.uuid1(), linkuid = self.client_dict[current_id]['uid']))
								print(timeoutInfo.encode())
								logger.debug('sending timeout information')
								if len(self.client_dict)>0:

									for x in self.client_dict:
						
										if x != current_id:
											self.client_dict[x]['client'].send(timeoutInfo.encode())

										else:
											pass
								else:
									pass
								uid = self.client_dict[current_id]['uid']
								del self.client_dict[current_id]
								sqliteServer = sqlite3.connect(const.DATABASE)
								cursor = sqliteServer.cursor()
								cursor.execute(sql.DELETEBYUID,(uid,))
								sqliteServer.commit()
								cursor.close()
								sqliteServer.close()
								client.shutdown(socket.SHUT_RDWR)
								client.close()
								break
							elif working == const.PING:
								logger.debug('recieved ping')

							else:
								pass
				
						elif first_run == 1:
							print('something \n')
							for x in self.client_dict:
								client = self.client_dict[x]['client']
								if client != self.client_dict[current_id]['client']:
									print('sending'+str(id_data))
									print(id_data)
									client.send(self.client_dict[current_id]['id_data'])
								else:
									pass
							for x in self.client_dict:
								data = self.client_dict[x]['id_data']
								logger.debug('sending conn data '+str(self.client_dict[x]['id_data'])+'to '+str(client)+'\n')
								client.send(data)
							threading.Thread(target = self.sendClientData, args = (client, address, current_id), daemon=True).start()

						#just some debug stuff
						first_run = 0
					except Exception as e:
						logger.warning('error in main loop')
						logger.warning(str(e))
						client.close()
						killSwitch =1
						return 1
		except Exception as e:
			client.close()
			return 1
			
	def sendClientData(self, client, address, current_id):
		killSwitch = 0
		try:
			while killSwitch == 0:
				time.sleep(const.DELAY)
				if killSwitch == 1:
					break
				if len(self.emergencyDict)>0:
						for x in self.emergencyDict:
							client.send(self.emergencyDict[x])
						logger.debug('emergency activated')
				else:
					pass

				if len(self.client_dict[current_id]['main_data'])>0:

					for x in self.client_dict[current_id]['main_data']:
						logger.debug(self.client_dict[current_id]['main_data'])
						client.send(x)
						print('\n'+'sent '+ str(x)+' to '+ str(address) + '\n')
						self.client_dict[current_id]['main_data'].remove(x)

				else:
					client.send(Serializer().serializerRoot(RequestCOTController().ping(eventuid = uuid.uuid1())).encode())
			client.shutdown(socket.SHUT_RDWR)
			client.close()
		except Exception as e:
			logger.warning('error in send info '+str(e))
			client.close()
			return 1

	def queryCallSign(self, uid):
		for x in self.client_dict:
			if self.client_dict[x]['uid']==uid:
				return self.client_dict[x]['callsign']
			else:
				pass
def startup():
	logger.info('starting windows service')
	ThreadedServer(host = '',port = const.DEFAULTPORT).listen()
if __name__ == "__main__":
	try:
		parser=argparse.ArgumentParser()
		parser.add_argument("-p", type=int)
		args=parser.parse_args()
		port_num = args.p
		ThreadedServer('',port_num).listen()
	except:
		ThreadedServer(host = '',port = const.DEFAULTPORT).listen()
