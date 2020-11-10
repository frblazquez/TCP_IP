import sys
import socket
import struct

GROUP =     sys.argv[1]
PORT  = int(sys.argv[2])
RECV_SIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sock.connect((GROUP,PORT))

# https://stackoverflow.com/questions/603852/how-do-you-udp-multicast-in-python
sock.bind((GROUP, PORT))
mreq = struct.pack("4sl", socket.inet_aton(GROUP), socket.INADDR_ANY)
sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

data = sock.recv(RECV_SIZE).decode()
#data = data[7:] #First six bytes are header
while data:
	# It's important to add flush flag for it to work!
	print(data, flush=True)
	data = sock.recv(RECV_SIZE).decode()

sock.close()