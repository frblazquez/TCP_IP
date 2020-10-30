import socket

HOST = "localhost"
PORT = 5002   

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST,PORT))

message = "Oh Romeo, Romeo! wherefore art thou Romeo?"
print("sending:", message)
sock.sendall(message.encode())
	
received = 0
expected = len(message)
	
while received < expected:
	data = sock.recv(8).decode()
	received += len(data)
	print ('received:', data)

while True:
	pass
