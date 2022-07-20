import socket
import sys
from time import *
import threading
import os

from mybroker import MyBroker
from Peach.publisher import Publisher

class Broker(Publisher):
    def __init__(self, topic, port):
        Publisher.__init__(self)
        self.withNode = True
        self.topic = topic
        self._port = int(port)
        self.tempfile_t = "tempfile_t.dat"
        self.tempfile_m = "tempfile_m.dat"
        self.crashfile = "Logs/MQTT/mqtt_target.DefaultRun_" + strftime("%Y-%j_%H-%M-%S", localtime())
        os.mkdir(self.crashfile)
        self.crashcount = 0
        #thread = threading.Thread(name="thread", target=self.crash_check)

    def initialize(self):
        try:
            self.process = MyBroker(self._port)
            self.process.set_subscribe()
            sleep(3)
        except Exception as e:
            raise e
    """
    # only data part
    def send(self, data):
        try:
            print(data)
            self.process.publish(data)
            with open(self.tempFile, "wb") as f:
                f.write(data)
            sleep(2)
        except Exception as e:
            f = open(self.tempFile, "rb")
            data = f.read()
            f.close()
            with open("crash.dat", "wb") as f:
                f.write(data)
            logging.warning("miss sending")
            raise e

    # data part and topic
    """
    def sendWithNode(self, data, dataNode):
        try:
            params = dict()
            params_l = ["topic", "message"]
            for child in dataNode.getAllChildDataElements():
                if child.get_Value() is None:
                    params[child.name] = ""
                else:
                    params[child.name] = child.get_Value()
            print(params["topic"], params["message"])
            self.process.publish(params["topic"], params["message"])
            with open(self.tempfile_t, "wb") as f:
                f.write( params["topic"])
            with open(self.tempfile_m, "wb") as f:
                f.write( params["message"])
            sleep(1)
            if not self.myping("192.168.0.141"):
                with open(self.tempfile_t, "rb") as f:
                    topic = f.read()
                with open(self.tempfile_m, "rb") as f:
                    message = f.read()
                with open(self.crashfile+"/crash_topic.dat", "wb") as f:
                    f.write(topic)
                with open(self.crashfile+"/crash_message.dat", "wb") as f:
                    f.write(message)
                raise PeachException
            sleep(4)
        except Exception as e:
            raise

    def finalize(self):
        os.remove(self.tempfile_t)
        os.remove(self.tempfile_m)
        print("finalize")
        self.process.close()



    def connect(self):
        pass

    def close(self):
        pass

    def myping(self,host):
        try:
            response = os.system("ping -c 1 -w 2 " + host)
            if response == 0:
                return True
            else:
                return False

        except KeyboardInterrupt as e:
            raise e
