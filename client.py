from socket import *
HOST = 'localhost'
PORT = 50001BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpCliSock= socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)
print ("client side")
while (1):
    data = raw_input(">")
    if not data: break
    tcpCliSock.send(data)
    data = tcpCliSock.recv(BUFSIZ)
    if not data: break
    print data
tcpCliSock.close()
