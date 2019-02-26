"""
file: service.py
socket service
"""


import socket
import threading
import time
import sys
import numpy as np


def socket_service():
	#錯誤處理
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		# 防止socket server重启后端口被占用（socket.error: [Errno 98] Address already in use）
		s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		s.bind(('192.168.1.195', 8080))
		s.listen(10)
	except socket.error as msg:
		print (msg)
		sys.exit(1)
	print ('Waiting connection...')

	while 1:
		conn, addr = s.accept()
		t = threading.Thread(target=deal_data, args=(conn, addr))
		t.start()

def deal_data(conn, addr):
	print ('Accept new connection from {0}'.format(addr))
	#conn.send('Hi, Welcome to the server!'.encode('utf-8'))#.encode('utf-8')
	conn.send('1'.encode('utf-8'))#.encode('utf-8')
	while 1:
		data = conn.recv(1024)
		print ('{0} client send data is {1}'.format(addr, data.decode('utf-8')))
		data_list = np.array([float(x) for x in str(data.decode('utf-8')).split()])	
		print(data.decode('utf-8'))#5 5 5
		print(data_list)#<class 'float'>
		#time.sleep(1)
		if data == 'exit' or not data:
			print ('{0} connection close'.format(addr))#.encode('utf-8')
			conn.send('Connection closed!'.encode('utf-8'))
			break
		#conn.send('Hello, {0}'.format(data).encode('utf-8'))#.encode('utf-8')
		conn.send('2, {0}'.format(data).encode('utf-8'))#.encode('utf-8')
	conn.close()


if __name__ == '__main__':
	socket_service()
    		
