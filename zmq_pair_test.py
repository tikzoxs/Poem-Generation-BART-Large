import zmq
import random
import sys
import time


yinan_ip = "tcp://10.110.179.38:5555"
self_socket = "tcp://0.0.0.0:5555"

port = "5555"
context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.bind(self_socket)

def receive_sentence():
	socket.send_string("record@data")
	msg = socket.recv()
	print("Ack = ", msg)
	socket.setsockopt( zmq.LINGER, 0 )
	sentence = socket.recv()
	socket.setsockopt( zmq.LINGER, 0 )
	return sentence.decode("utf-8")

def comm(message):
	socket.send_string(message)
	msg = socket.recv()
	print("Ack = ", msg)
	socket.setsockopt( zmq.LINGER, 0 )
	return msg.decode("utf-8")


# while True:
# 	socket.send_string("exit")
# 	msg = socket.recv()
# 	print(msg)
# 	socket.setsockopt( zmq.LINGER, 0 )
# 	time.sleep(1)