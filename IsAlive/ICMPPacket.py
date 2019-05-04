import struct
import socket
from random import randint
from constants import *

class ICMPPacket:

    def __init__(self, packet = None):
        self.compactPacket = None
        if( packet == None):
            self.pktType = 0
            self.code = 0
            self.chksum = 0
            self.pktID = 0
            self.sequenceNo = 0
        else:
            icmpPacket = struct.unpack(ICMP_PACKET_FORMAT, packet)
            self.pktType = icmpPacket[0]
            self.code = icmpPacket[1]
            self.chksum = icmpPacket[2]
            self.pktID = icmpPacket[3]
            self.sequenceNo = icmpPacket[4]

    def initializePacket(self):
        self.pktType = ICMP_ECHO_REQUEST
        self.pktID = randint(0, 0xFFFF) #id is 16 bits
        self.sequenceNo = 1
        self.compactPacket = struct.pack(ICMP_PACKET_FORMAT, self.pktType, self.code, self.chksum, self.pktID, self.sequenceNo)
        self.chksum = self.calculateCheckSum(self.compactPacket)
        self.compactPacket = struct.pack(ICMP_PACKET_FORMAT, self.pktType, self.code, socket.htons(self.chksum), self.pktID, self.sequenceNo)

    def calculateCheckSum(self, compactPacket):
        rawSum = 0
        itr = len(compactPacket) % 2
        end = len(compactPacket) - itr

        for i in range(0, end, 2):
            rawSum = rawSum + compactPacket[i] + (compactPacket[i+1] << 8)
        if itr:
            rawSum = rawSum + compactPacket[i+1]
        while(rawSum >> 16):
            rawSum = (rawSum & 0xFFFF) + (rawSum >> 16)
        rawSum = ~rawSum & 0xFFFF
        return rawSum
