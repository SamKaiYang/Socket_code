"""
file: client.py
socket client
"""

import socket
import sys
import numpy as np


def socket_client():
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect(('192.168.0.1', 6666))
	except socket.error as msg:
		print (msg)
		sys.exit(1)
	print (s.recv(1024))
	while 1:
		#Od = np.array([float(x) for x in input().split()])
		data = input('please input work: '.encode('utf-8'))
		#data= np.array([float for x in input('please input work: ').split()])
		print (data.encode('utf-8'))
		s.send(data.encode('utf-8'))
		print (s.recv(1024))
		if data == 'exit':
			break
	s.close()


if __name__ == '__main__':
	socket_client()

