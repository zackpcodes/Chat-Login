import socket

newSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '127.0.0.1'
port = 5000

newSock.connect((host, port))


while(True):

    strOut = str(input())
    newSock.sendall(strOut.encode('UTF-8'))
    
newSock.close()
