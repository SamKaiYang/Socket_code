from socket import *

if __name__ == '__main__':

    host = "192.168.1.2" # one computer -> terminal -> hostname -i
    # host = "192.168.43.135" # two computer -> terminal -> hosname -I
    port = 200
    ADDR = (host, port)
    BUFSIZ = 1024

    tcpSocket = socket(AF_INET, SOCK_STREAM)
    tcpSocket.bind(ADDR)
    # set the max number of tcp connection
    tcpSocket.listen(5)
    print('waiting for connection...')
    clientSocket, clientAddr = tcpSocket.accept()
    print('conneted form: %s', str(clientAddr))
    while True:
        data = input(">")
        if not data:
            print("No data!")
            break
        clientSocket.send(data.encode('utf-8'))
        returnData = clientSocket.recv(BUFSIZ)
        if not returnData:
            print("No returnData!")
            break
        print('Return time is:%s' % returnData.decode('utf-8'))

    clientSocket.close()


    # #data = str(action)
    # #clientSocket.send(data.encode('utf-8'))
    # #returnData = clientSocket.recv(BUFSIZ)
    # #if not returnData:
    # #    print("No returnData!")
    # #    break
    
    # Ctrl+K Ctrl+C	添加行注释 Add line comment
    # Ctrl+K Ctrl+U	删除行注释 Remove line comment