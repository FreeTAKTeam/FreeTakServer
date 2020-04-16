import sys
import os
os.chdir('..')
path = os.path.dirname(__file__)
path = str(path)+'server.py'
os.system('sudo nohup python3 '+path+' &')