import time
import zmq

yinan_ip = "tcp://10.110.179.38:5555"
self_socket = "tcp://0.0.0.0:5555"

def receive_sentence():
    print("waiting for sentence")
    comm('record')
    print("trying to get sentence")
    TIMEOUT = 15000
    response = "not_okay"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(yinan_ip)
    socket.send_string("request")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    evt = dict(poller.poll(TIMEOUT))
    if evt:
        if evt.get(socket) == zmq.POLLIN:
            response = socket.recv(zmq.NOBLOCK)
            print(response)
    socket.setsockopt(zmq.LINGER, 0)
    socket.close()
    context.term()
    time.sleep(0.2)

    return response

def receive_ack():
    print("trying to get ack")
    TIMEOUT = 3000
    response = "not_okay"
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect(yinan_ip)
    socket.send_string("request")
    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)
    evt = dict(poller.poll(TIMEOUT))
    if evt:
        if evt.get(socket) == zmq.POLLIN:
            response = socket.recv(zmq.NOBLOCK)
            print(response)
    socket.setsockopt(zmq.LINGER, 0)
    socket.close()
    context.term()
    time.sleep(0.2)

    return response

def comm(message):
    print("communicating..")
    while True:
        try:
            print("trying to send")
            context = zmq.Context()
            # socket = context.socket(zmq.REQ)
            socket = context.socket(zmq.PUB)
            socket.bind(self_socket)
            for x in range(1,10):
                socket.send_string(message)
                print(message)
                time.sleep(0.2)
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
        except:
            print("cannot send")
            socket.setsockopt(zmq.LINGER, 0)
            socket.close()
        res = receive_ack()
        print("response = ", res)
        if(res == "okay"):
            break
        time.sleep(0.2)

comm("emotion@joy")

#333 615 078 
#gkwf4ghw 