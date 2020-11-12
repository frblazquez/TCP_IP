import sys
import socket
import ssl

HOST = 'localhost'           
PORT = 5003

CERTIFICATE = sys.argv[1]
KEY         = sys.argv[2]

context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(CERTIFICATE,KEY)




while True:
	try:

		print('try')

		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		sock.bind((HOST, PORT))
		sock.listen(1)
		context.wrap_socket(sock, server_side=True)
		connection, addr = sock.accept()

		data = connection.recvfrom(1024).decode()
		print("received:", data)
		connection.sendall('This is PMU data 0'.encode())
	except:
		print('except')


	
connection.close()
sock.close()