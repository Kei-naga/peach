import socket
from struct import *

class Packet(object):
    def __init__(self):
        self.len = 0
        self.out = b''

    def __str__(self):
        return self.__class__.__name__

    def getFixedHeader(self):
        name = str(self)
        if name == "Connact":
            return b'\x20'
        elif name == "Suback":
            return b'\x90'
        elif name == "Publish":
            return b'\x30'
        elif name == "Pingresp":
            return b'\xd0'

    def send(self, s):
        s.sendall(self.out)

class Connact(Packet):
    def __init__(self):
        super(Connact, self).__init__()
        self.getConnact()

    def getConnact(self):
        self.out += self.getFixedHeader()
        self.out += b'\x02'
        self.out += b'\x00'
        self.out += b'\x00'

class Suback(Packet):
    def __init__(self, subsc):
        super(Suback, self).__init__()
        self.msg = subsc
        self.msgId = 0
        self.topic = b''
        self.getTopic()
        self.getSuback()

    def getTopic(self):
        self.msgId = self.msg[2:4]
        topiclen = unpack('!H', self.msg[4:6])[0]
        self.topic += self.msg[6:6+topiclen]

    def getSuback(self):
        self.out += self.getFixedHeader()
        self.out += b'\x03'
        self.out += self.msgId
        self.out += b'\x00'

class Publish(Packet):
    def __init__(self, topic, data):
        super(Publish, self).__init__()
        self.topic = topic
        self.data = data
        self.create_pub()

    def getmsgLen(self):
        msglen = 2 + len(self.topic) + len(self.data)
        o = b''
        while msglen > 0:
            digit = msglen % 128
            msglen = msglen // 128
            if msglen > 0:
                digit = digit | 128
            o += pack('!B', digit)
        return o

    def create_pub(self):
        msg_len = self.getmsgLen()
        l=len(self.topic)
        if (l<65536):
            topic_len = pack('!H', l)
            self.out += self.getFixedHeader()
            self.out += msg_len
            self.out += topic_len
            for s in list(self.topic):
                self.out += pack('c',s)
            for s in list(self.data):
                self.out += pack('c',s)
        else:
            print("topic length is over max!!")

class Pingresp(Packet):
    def __init__(self):
        super(Pingresp, self).__init__()
        self.getPingresp()

    def getPingresp(self):
        self.out += self.getFixedHeader()
        self.out += b'\x00'
