import sys
import socket

SERVER      = sys.argv[1]
PORT        = int(sys.argv[2])
#LAPSE_TIME  = sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((SERVER,PORT))

#message = "CMD_short:"+LAPSE_TIME
message = "CMD_floodme"
sock.sendall(message.encode())

received = 0
length = 2048	
data = sock.recv(length)
while data:
	print (data.decode())
	data = sock.recv(length)
	received = received + 1

print()
print(received)

