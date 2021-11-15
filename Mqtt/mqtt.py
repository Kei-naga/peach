import socket
import sys
import time

from mybroker import MyBroker
from Peach.publisher import Publisher

class Broker(Publisher):
    def __init__(self, topic, port):
        Publisher.__init__(self)
        self.topic = topic
        self._port = int(port)

    def initialize(self):
        self.process = MyBroker(self._port)
        self.process.set_subscribe()
        time.sleep(3)

    def send(self, data):
        self.process.publish("/topic/qos0",data)
        time.sleep(1)

    def finalize(self):
        self.process.close()

    def connect(self):
        pass

    def close(self):
        pass
