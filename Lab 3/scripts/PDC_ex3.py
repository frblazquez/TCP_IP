import sys
import socket

SERVER      = sys.argv[1]
PORT        = int(sys.argv[2])
LAPSE_TIME  = 1

#creates ipv4 and ipv6 UDP sockets
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

#connects sockets to the UDP server
sock6.connect((SERVER,PORT))
sock.connect((SERVER,PORT))

message = "RESET:20"
data = ''
data6 = ''

lost = 0
i=0
length = 1024

while i<30:
	i=i+1

	try:
		data = data6 = ''
		#encoding of the message
		sock.sendall(message.encode())
		sock6.sendall(message.encode())

		#timeout redirect to 'except' if expired
		sock.settimeout(LAPSE_TIME)
		sock6.settimeout(LAPSE_TIME)
		#receiving of the packets
		data = sock.recv(length)
		data6 = sock6.recv(length)

		#test which IP address has sent a message back
		if (data):
			print('data4:',data.decode())
			sock.close()
			break

		if (data6):
			print('data6:',data6.decode())
			sock6.close()
			break	
	#keep count of lost packets
	except socket.timeout:
		lost = lost + 1

print('lost = ', lost)	

