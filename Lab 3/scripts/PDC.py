import sys
import socket

SERVER  =     sys.argv[1]
PORT    = int(sys.argv[2])
COMMAND =     sys.argv[3]
LENGTH  = 1024
MSG_LEN = 18 # len('This is PMU data k')

# Connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER,PORT))

# Send command
sock.sendall(COMMAND.encode())
	
if COMMAND=='CMD_floodme':
	data = sock.recv(LENGTH).decode()
	while data:
		print(data, end = '')	
		data = sock.recv(LENGTH).decode()
else:
	count       = 0
	threshold   = 10

	data = sock.recv(LENGTH).decode()
	while data:
		while len(data)>=MSG_LEN:
			str_n = data[:MSG_LEN]
			data  = data[MSG_LEN:]
			print (str_n)

			count = count + 1
			if count==threshold:
				count = 0
				threshold = threshold*10
				MSG_LEN = MSG_LEN + 1

		data = data + sock.recv(LENGTH).decode()

	
