import websocket
import sys

SERVER  = sys.argv[1]
PORT 	= sys.argv[2]
COMMAND = sys.argv[3]




ws = websocket.WebSocket()
ws.connect("ws://"+SERVER+":"+PORT)
ws.send(COMMAND)
results = ''
results = ws.recv()


while(results):
	print("received : ", results.decode())
	results = ws.recv()

ws.close()



