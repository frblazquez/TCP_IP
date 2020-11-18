import sys
import socket

SERVER     =     sys.argv[1]
PORT       = int(sys.argv[2])
LAPSE_TIME = 1
RECV_SIZE  = 1024
COMMAND    = "RESET:20"


sock_v4 = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM)
sock_v6 = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)

sock_v4.connect((SERVER,PORT))
sock_v6.connect((SERVER,PORT))

sock_v4.settimeout(LAPSE_TIME)
sock_v6.settimeout(LAPSE_TIME)

losts = []
for _ in range(100):

	data_v4=''
	data_v6=''
	lost = 0	
	while True:
		#print("Sending data "+str(lost+1))
		sock_v4.send(COMMAND.encode())
		sock_v6.send(COMMAND.encode())

		try:
			data_v4 = sock_v4.recv(RECV_SIZE).decode()
		except:
			pass # Intentionally empty
		try:
			data_v6 = sock_v6.recv(RECV_SIZE).decode()
		except:
			pass # Intentionally empty

		if data_v4 or data_v6:
			break

		lost = lost+1

	#if data_v4:
	#	print(data_v4[7:])
	#if data_v6:
	#	print(data_v6[7:])
	#print(lost)
	losts.append(lost)


print(sum(losts)/len(losts))

sock_v4.close()
sock_v6.close()