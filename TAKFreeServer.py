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
import sys
import constant
import time
import datetime
const = constant.vars()
''' Server class '''
class ThreadedServer(object):
	def __init__(self, host, port):
		print('listening on port '+str(port))
		self.host = host
		self.port = port
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.sock.bind((self.host, self.port))
		self.valid = 0
		self.data1 = []
		self.data_important = []
		self.chat = {}
		self.IDs = []
		self.connected_xml = []
		self.client_id = 0
		self.client_dict = {}
		self.killSwitch = 0
	def logall(self):
		#kill all processes
		while True:
			try:
				time.sleep(60)
				const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + 'client dict is as follows '+'\n'+self.client_dict+'\n')
			except:
				const.LOGFILE.write('log all error')
	def listen(self):
		'''
		listen for client connections and begin thread if found
		'''
		try:
			self.sock.listen(1000)
			while True:
				if self.killSwitch == 1:
					sys.exit()
				client, address = self.sock.accept()
				localtime=time.asctime(time.localtime(time.time()))
				logging.basicConfig(filename='tcp_server.log',level=logging.INFO)
				log=address[0]+" got connected on "+localtime
				logging.info(log)
				threading.Thread(target = self.listenToClient,args = (client,address), daemon=True).start()
		except:
			const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()) + ' kill function error'+'\n')
	def check_xml(self, xml_string, current_id, client, address):
		'''
		check xml type or class
		'''
		try:
			data_value = ''
			if xml_string == const.EMPTY_BYTE:
				print('client disconnected now setting as disconnected')
				self.client_dict[current_id]['alive'] = 0
				const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) + 'client '+ self.client_dict[current_id]['id_data']+' has disconnected'+'\n')
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
		except:
			const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'xml check function error checking xml type recieved from '+str(client)+ ' at '+str(address)+ ' data is ' + str(xml_string)+'\n')
		#adds data to all connected client data list except sending client
			for x in self.client_dict:
				try:
					if x == current_id:
						True
					elif x != current_id and data_value != const.GEOCHAT:
						self.client_dict[x]['main_data'].insert(0, xml_string)
					elif x!=current_id:
						self.client_dict[x]['main_data'].append(xml_string)
				except:
					const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'xml check function error sharing xml with client id '+str(x)+'\n')
					const.LOGFILE.write(self.client_dict+'\n')
			self.data1.append(xml_string)
			return data_value

	def connectionSetup(self, client, address):
		try:
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
			const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'successfuly setup connection to '+str(id_data) + ' at '+str(address)+'\n')
			return str(first_run)+' δ '+str(total_clients_connected)+' δ '+str(id_data)+' δ '+str(current_id)
		except:
			const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'error in connectioon setup function while trying to setup connection to '+str(client)+ ' at '+str(address)+'\n')
	def listenToClient(self, client, address):
		''' 
		Function to receive data from the client. this must be long as everything
		'''
		try:
			defaults = self.connectionSetup(client, address)
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
		except:
			const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'error in listen to client function while trying to parse data from connection setup with client '+str(client)+ ' at '+str(address)+'\n')
		#main connection loop

		while True:
			#recieve data
			try:
				if first_run == 0:
					data = client.recv(4096)
					const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} '.format(datetime.datetime.now()) +'client ' + str(client)+ ' at '+str(address) + ' recieved '+ str(data)+'\n')
				elif first_run == 1:
					for x in self.client_dict[current_id]['main_data']:
						client.send(x)
				#just some debug stuff
				working = self.check_xml(data, current_id, client, address)
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
						const.LOGFILE.write('time is {:%Y-%m-%d %H:%M:%S} ' +'sent '+ str(x)+' to '+ str(address))
						self.client_dict[current_id]['main_data'].remove(x)
				else:
					for x in self.client_dict[current_id]['main_data']:
						client.send(x)
				first_run = 0
			except:
				True					   
if __name__ == "__main__":
	''' Taking port number from the command line.
	Run the code as name.py -p PortNumber '''
	parser=argparse.ArgumentParser()
	parser.add_argument("-p", type=int)

	args=parser.parse_args()
	port_num = args.p
	if args.p == '':
		ThreadedServer('',const.PORT).listen()
	else:
		ThreadedServer('',args.p).listen()
