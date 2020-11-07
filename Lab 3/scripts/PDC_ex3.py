import sys
import socket

SERVER      = sys.argv[1]
PORT        = int(sys.argv[2])
LAPSE_TIME  = 1



sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.connect((SERVER,PORT))
#sock.setblocking(0)
#sock.settimeout(LAPSE_TIME)

message = "RESET:20"
sock.sendall(message.encode())

lost = 0
length = 1024	
while True:
	data = sock.recv(length)
	if data:
		break
	else:
		lost = lost + 1
		time.sleep(LAPSE_TIME)

print(data.decode())
print(lost)
sock.close()