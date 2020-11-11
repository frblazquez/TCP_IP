import socket
import struct
import sys


GROUP 	= sys.argv[1]
PORT 	= int(sys.argv[2])

gsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
gsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

gsock.bind((GROUP, PORT))

mreq = struct.pack("4sl", socket.inet_aton(GROUP), socket.INADDR_ANY)
gsock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

while True:
  print (gsock.recv(10505))