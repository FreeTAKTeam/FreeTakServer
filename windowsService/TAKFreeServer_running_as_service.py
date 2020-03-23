#######################################################
# 
# TAKFreeServer.py
# Original author: naman108
# This code is Open Source, made available under the EPL 2.0 license.
# https://www.eclipse.org/legal/eplfaq.php
# credit to Harshini73 for base code
#
#######################################################
import socket
import threading
import argparse
import logging
import time
import xml.etree.ElementTree as ET
import constant
const = constant.vars()
''' Server class '''
class ThreadedServer(object):
	def __init__(self, host, port):
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.valid = 0
		self.data1 = []
		self.data = ''
		self.data_important = []
		self.chat = {}
		self.IDs = []
		self.connected_xml = []
		self.client_id = 0
		self.client_dict = {}

	def listen(self):
		'''
		listen for client connections and begin thread if found
		'''
		self.sock.listen(1000)
		while True:
			client, address = self.sock.accept()
			localtime=time.asctime(time.localtime(time.time()))
			logging.basicConfig(filename='tcp_server.log',level=logging.INFO)
			log=address[0]+" got connected on "+localtime
			logging.info(log)
			threading.Thread(target = self.listenToClient,args = (client,address), daemon=True).start()
	def check_xml(self, xml_string, current_id):
		'''
		check xml type or class
		'''
		data_value = ''
		if xml_string == const.EMPTY_BYTE:
			print('client disconnected now setting as disconnected')
			self.client_dict[current_id]['alive'] = 0
			return const.FAIL

		tree = ET.fromstring(xml_string)
		print(tree)
		uid = tree.get('uid')

		print('\n'+'uid is '+ uid +'\n')
		try:
			uid_by_dot = uid.split('.')
			uid_by_dash = uid.split('-')
		except:
			uid_by_dash = uid.split('-')

		if uid_by_dash[-1] == const.PING:
			print('is ping')
			data_value = const.PING
			self.data_important.append(xml_string)
		elif len(uid_by_dot)>0:
			if uid_by_dot[0] == const.GEOCHAT:
				print('is geochat')
				data_value = const.GEOCHAT
				self.data_important.append(xml_string)
			else:
				True
		else:
			new = 1
			count = 0
			while count < self.connected_xml:
				if self.connected_xml[count] == xml_string:
					new = 0
					break
				else:
					count += 1
					True
			if new == 1:
				self.connected_xml.append(xml_string)
				self.IDs.append(uid)
			else:
				True
		
			self.data_important.append(xml_string)
		#adds data to all connected client data list except sending client
		for x in self.client_dict:
			if x == current_id:
				True
			elif x != current_id and data_value != const.GEOCHAT:
				self.client_dict[x]['main_data'].insert(0, xml_string)
			elif x!=current_id:
				self.client_dict[x]['main_data'].append(xml_string)
		self.data1.append(xml_string)
		
		return data_value
	def connectionSetup(self, client):
		first_run = 1
		#create client dictionary within main dictionary containing arrays for data and chat also other stuff for client enitial connection
		current_id = 0
		total_clients_connected = 0
		total_clients_connected += 1
		id_data = client.recv(4096)
		self.data = id_data
		print('enitial data is '+str(id_data))
		tree = ET.fromstring(id_data)
		uid = tree.get('uid')
		if self.client_id == 0:
			print('creating new a')
			current_id = self.client_id
			self.client_id += 1
			#add identifying information
			self.client_dict[current_id] = {'id_data': '', 'main_data': [], 'alive': 1, 'uid': ''}
			self.client_dict[current_id]['id_data'] = id_data
			self.client_dict[current_id]['uid'] = uid
		print(self.client_dict)
		for x in self.client_dict:
			print(self.client_dict[x]['uid'])
			if self.client_dict[x]['uid'] == uid:
				current_id = x
				print('already there ')
			else:
				True
		if current_id == 0:
			print('creating new b')
			current_id = self.client_id
			self.client_id += 1
			#add identifying information
			self.client_dict[current_id] = {'id_data': '', 'main_data': [], 'alive': 1, 'uid': ''}
			self.client_dict[current_id]['id_data'] = id_data
			self.client_dict[current_id]['uid'] = uid
		return str(first_run)+' δ '+str(total_clients_connected)+' δ '+str(id_data)+' δ '+str(current_id)
	def listenToClient(self, client, address):
		''' 
		Function to receive data from the client. this must be long as everything
		'''
		defaults = self.connectionSetup(client)
		defaults = defaults.split(' δ ')
		print(defaults)
		first_run=defaults[0]
		total_clients_connected=defaults[1]
		id_data=defaults[2]
		current_id = defaults[3]
		first_run = int(first_run)
		total_clients_connected = int(total_clients_connected)
		id_data = bytes(id_data, 'utf-8')
		current_id = int(current_id)
		#main connection loop
		while True:
			#recieve data
			if first_run == 0:
				self.data = client.recv(4096)
			elif first_run == 1:
				for x in self.client_dict[current_id]['main_data']:
					client.send(x)
			#just some debug stuff

			print(self.data)

			working = self.check_xml(self.data, current_id)
			#checking if check_xml detected client disconnect
			if working == const.FAIL:
				client.close()
				break
			#check if all connected clients are detected
			if len(self.client_dict) != total_clients_connected:
				for x in self.client_dict:
					client.send(self.client_dict[x]['id_data'])
				total_clients_connected += 1
			#send recieved data
			if len(self.client_dict[current_id]['main_data'])>1:
				for x in self.client_dict[current_id]['main_data']:
					client.send(x)
					print('\n'+'sent '+ str(x)+' to '+ str(address) + '\n')
					self.client_dict[current_id]['main_data'].remove(x)
			else:
				for x in self.client_dict[current_id]['main_data']:
					client.send(x)
			first_run = 0
				
				
					   
if __name__ == "__main__":
	''' Taking port number from the command line.
	Run the code as name.py -p PortNumber '''
	try:
		parser=argparse.ArgumentParser()
		parser.add_argument("-p", type=int)
		args=parser.parse_args()
		port_num = args.p
		ThreadedServer('',port_num).listen()
	except:
		ThreadedServer('',const.DEFAULTPORT).listen()
