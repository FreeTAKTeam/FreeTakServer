import argparse
import sys
import os
if __name__ == '__main__':
	parser=argparse.ArgumentParser()
	parser.add_argument("-p", type=int)
	parser.add_argument("-ip", type=str)
	args=parser.parse_args()
	port_num = args.p
	ip_addr = args.ip
	if ip_addr != None and port_num != None:
		os.chdir('..')
		path = os.path.dirname(__file__)
		serverpath = str(path)+'server.py'
		os.system('sudo nohup python3 '+serverpath+' &')
		httpserverpath = str(path)+'httpServer.py'
		os.system('sudo nohup python3 '+httpserverpath+' &')
	else:
		os.chdir('..')
		path = os.path.dirname(__file__)
		serverpath = str(path)+'server.py'
		os.system('sudo nohup python3 '+serverpath+' &')
		httpserverpath = str(path)+'httpServer.py'
		os.system('sudo nohup python3 '+httpserverpath+' &')