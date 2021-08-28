# pip install pyzmq opencv-python
import time
import zmq


def send_messege(message):
    context = zmq.Context()
    # socket = context.socket(zmq.REP)
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://0.0.0.0:5555")

    # while True:
    #     #  Wait for next request from client
    #     print("waiting for request")
    #     ack = socket.recv()
    #     print("Received request: %s" % ack)

    #     #  Do some 'work'.
    #     #  Try reducing sleep time to 0.01 to see how blazingly fast it communicates
    #     #  In the real world usage, you just need to replace time.sleep() with
    #     #  whatever work you want python to do, maybe a machine learning task?
    #     time.sleep(1)

    #     #  Send reply back to client
    #     #  In the real world usage, after you finish your work, send your output here
    #     socket.send(message)  #joy, hate, love, curious, idle
    #     print('sent')

    #     if(ack == b"okay"):
    #         print("^^^^^^^^^^okay^^^^^^^^^^^")
    #         break

    while True:
        # message = str(random.uniform(-1.0, 1.0)) + " " + str(random.uniform(-1.0, 1.0)) + " " + str(random.uniform(-1.0, 1.0))
        socket.send_string(message)
        print(message)
        time.sleep(0.5)
        socket.close()
        receive_ack()
        time.sleep(0.5)

def receive_ack():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://10.110.179.38:12346")
    count = 0 
    TIMEOUT = 1000
    response = ''

    while True:
        socket.send_string("request")
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)
        evt = dict(poller.poll(TIMEOUT))
        if evt:
            if evt.get(socket) == zmq.POLLIN:
                response = socket.recv(zmq.NOBLOCK)
                print(response)
                break
        time.sleep(0.2)
        socket.close()
        count += 1
        if(count > 50):
            break
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://10.110.179.38:12346")
    time.sleep(0.1)
    socket.close()
    return response

def send(message):
    context = zmq.Context()
    # socket = context.socket(zmq.REP)
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://0.0.0.0:5555")
    while True:
        socket.send_string(message)
        print(message)
        # time.sleep(0.5)
        # socket.close()
        # receive_ack()
        time.sleep(0.5)

def comm(message):
    while True:
        context = zmq.Context()
        # socket = context.socket(zmq.REP)
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://0.0.0.0:5555")
        for x in range(1,10):
            socket.send_string(message)
            print(message)
            time.sleep(0.2)
        socket.close()
        res = receive_ack()
        if(res == b"okay"):
            break
        time.sleep(0.5)
        


# comm("happy")
# time.sleep(1)

# 