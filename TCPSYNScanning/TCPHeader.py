import struct
import socket
from random import randint
from constants import *

class TCPHeader:
    def __init__(self, sourceIP, destIP):
        self.compactHeader = None
        self.sourceIP = socket.inet_aton(sourceIP)
        self.destIP = socket.inet_aton(destIP)

class TCPHeader:
    def __init__(self, sourceIP, destIP):
        self.compactHeader = None
        self.sourceIP = socket.inet_aton(sourceIP)
        self.destIP = socket.inet_aton(destIP)

    def fillTCPPacket(self, sourcePort, destPort):
        TCPSrc = sourcePort
        TCPDst = destPort
        TCPSeqNumber = TCP_INIT_SEQ_NUM
        TCPAckNumber = TCP_ACKNOWLEDGE_NUM
        TCPHeaderLen = TCP_HEADER_LEN
        f_FIN = (TCP_FLAG_UNSET)
        f_SYN = (TCP_FLAG_SET << 1)
        f_RST = (TCP_FLAG_UNSET << 2)
        f_PSH = (TCP_FLAG_UNSET << 3)
        f_ACK = (TCP_FLAG_UNSET << 4)
        f_URG = (TCP_FLAG_UNSET << 5)
        f_ECN = (TCP_FLAG_UNSET << 6)
        f_CWR = (TCP_FLAG_UNSET << 7)
        f_NOC = (TCP_FLAG_UNSET << 8)
        f_RSV = (TCP_FLAG_UNSET << 9)

        TCPFlags = f_RSV + f_NOC + f_CWR + f_ECN + f_URG + f_ACK + f_PSH + f_RST + f_SYN + f_FIN

        TCPWindowSize = TCP_MAX_WINDOW_SIZE
        TCPChecksum = TCP_INIT_CHECKSUM
        TCPURGPointer = TCP_URG_POINTER

        self.compactHeader = struct.pack("!HHLLBBHHH", TCPSrc, TCPDst, TCPSeqNumber, TCPAckNumber, TCPHeaderLen, TCPFlags, TCPWindowSize, TCPChecksum, TCPURGPointer)

        TCPChecksum = self.calculateChecksum()

        self.compactHeader = struct.pack("!HHLLBBH", TCPSrc, TCPDst, TCPSeqNumber, TCPAckNumber, TCPHeaderLen, TCPFlags, TCPWindowSize) + struct.pack("H", TCPChecksum) + struct.pack("!H", TCPURGPointer)


    def calculateChecksum(self):
        srcIP = self.sourceIP
        dstIP = self.destIP
        zeroes = 0
        protocol = socket.IPPROTO_TCP
        totalLen = len(self.compactHeader)

        pseudoHeader = struct.pack("!4s4sBBH", srcIP, dstIP, zeroes, protocol, totalLen)
        pseudoHeader = pseudoHeader + self.compactHeader

        rawSum = 0
        itr = len(pseudoHeader) % 2
        end = len(pseudoHeader) - itr

        for i in range(0, end, 2):
            rawSum = rawSum + pseudoHeader[i] + (pseudoHeader[i+1] << 8)
        if itr:
            rawSum = rawSum + pseudoHeader[i+1]
        while(rawSum >> 16):
            rawSum = (rawSum & 0xFFFF) + (rawSum >> 16)
        rawSum = ~rawSum & 0xFFFF
        return rawSum
