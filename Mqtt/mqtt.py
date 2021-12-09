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

    # only data part
#    def send(self, data):
#        try:
#            self.process.publish("/topic/qos0",data)
#            time.sleep(1)
#
#        except Exception as e:
#            raise

    # data part and topic
    def sendWithNode(self, data, dataNode):
        params = dict()
        params_l = ["topic", "message"]
        for child in dataNode.getAllChildDataElements():
            if child.get_Value() is None:
                params[child.name] = ""
            else:
                params[child.name] = child.get_Value()
        print(params["topic"], params["message"])
        try:
            self.process.publish(params["topic"], "0")#params["message"])
        except Exception as e:
            logging.warning("miss sending")
            raise

    def finalize(self):
        print("finalize")
        self.process.close()

    def connect(self):
        pass

    def close(self):
        pass
