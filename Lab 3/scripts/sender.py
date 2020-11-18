import sys
import socket

GROUP =     sys.argv[1]
PORT  = int(sys.argv[2])
CAMIPRO_ID= sys.argv[3]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

message  = CAMIPRO_ID
message += input()

sock.sendto(message.encode(), (GROUP, PORT))

sock.close()