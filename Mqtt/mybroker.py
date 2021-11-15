import socket
import struct
from packet import *
import time
import threading

class MyBroker:
    def __init__(self, port):
        print("create broker")
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('', port))
        s.listen(5)
        self.clientsocket, self.address = s.accept()

    def set_subscribe(self):
        clientsocket = self.clientsocket
        connect = clientsocket.recv(1024)
        connact = Connact()
        connact.send(clientsocket)
        subscribe = clientsocket.recv(1024)
        suback = Suback(subscribe)
        suback.send(clientsocket)
        print "subscribe from {},topic:{}".format(self.address,suback.topic)
        thread_checkping = threading.Thread(target=self.pingcheck)
        thread_checkping.setDaemon(True)
        thread_checkping.start()

    def pingcheck(self):
        while True:
            ping = self.clientsocket.recv(1024)
            print("sending ping!")
            pingresp = Pingresp()
            pingresp.send(self.clientsocket)
            del ping

    def publish(self, topic, data):
        publish = Publish(topic, data)
        publish.send(self.clientsocket)

    def close(self):
        self.clientsocket.close()
        print("socket close")

if __name__ == '__main__':
    process = MyBroker(port=1883)
    process.set_subscribe()
    process.publish("/topic/qos0", "000")
