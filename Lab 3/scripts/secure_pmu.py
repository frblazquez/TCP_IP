import socket
import ssl
import sys

CERT = sys.argv[1]
KEY = sys.argv[2]

#https://docs.python.org/3/library/ssl.html
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(CERT, KEY)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
sock.bind(('127.0.0.1', 5003))
sock.listen(5)

ssock = context.wrap_socket(sock, server_side=True)   

while True: 
	conn, addr = ssock.accept()

	data = conn.read(1024).decode()
	conn.send('This is PMU data 0'.encode())

	conn.close()

ssock.close()
sock.close()