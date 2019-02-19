import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
host = '127.0.0.1'
port = 5000
serverSocket.bind((host, port))

serverSocket.listen(4)
client, addr = serverSocket.accept()
print('Connected with', addr)

while(True):
    msg = client.recv(1024)
    print(msg)




