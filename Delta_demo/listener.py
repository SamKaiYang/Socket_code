from socket import *


serverName = "192.168.1.2" # one computer -> terminal -> hostname -i
# serverName = "192.168.43.135" # two computer -> terminal -> hostname -I
serverPort = 200
BUFSIZ = 1024
ADDR = (serverName, serverPort)
clientSocket = socket(AF_INET, SOCK_STREAM)
print("waiting for connection")
clientSocket.connect(ADDR)
print("connection is successful")


while True:
    data = int(clientSocket.recv(BUFSIZ))
    print(str(data) + "\n")
    returnData = str(data)
    clientSocket.send(returnData.encode('utf-8'))

clientSocket.close()

