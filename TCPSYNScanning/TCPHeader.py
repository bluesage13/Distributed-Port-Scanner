import struct
import socket
from random import randint
from constants import *

# class TCPHeader2:
#     def __init__(self, sourceIP, destIP):
#         self.compactHeader = None
#         self.sourceIP = socket.inet_aton(sourceIP)
#         self.destIP = socket.inet_aton(destIP)
#
#     def fillTCPPacket(self, sourcePort, destPort):
#         offset_Reserved_Byte = (TCP_DATA_OFFSET << 4) + TCP_RESERVED
#
#         f_fin = TCP_FLAG_UNSET
#         f_syn = TCP_FLAG_SET << 1
#         f_rst = TCP_FLAG_UNSET << 2
#         f_psh = TCP_FLAG_UNSET << 3
#         f_ack = TCP_FLAG_UNSET << 4
#         f_urg = TCP_FLAG_UNSET << 5
#         f_ece = TCP_FLAG_UNSET << 6
#         f_cwr = TCP_FLAG_UNSET << 7
#
#         flags = f_fin + f_syn + f_rst + f_psh + f_ack + f_urg + f_ece + f_cwr
#
#         flags = 2
#
#         TCPHeader = struct.pack("!HHLLBBHHH", sourcePort, destPort, TCP_INIT_SEQ_NUM, TCP_ACKNOWLEDGE_NUM, offset_Reserved_Byte, flags, TCP_MAX_WINDOW_SIZE, TCP_INIT_CHECKSUM, TCP_URG_POINTER)
#
#         zeroes = 0
#         protocol = socket.IPPROTO_TCP
#         TCPLength = len(TCPHeader) + len(TCP_PAYLOAD)
#
#         pseudoHeader = struct.pack("!4s4sBBH", self.sourceIP, self.destIP, zeroes, protocol, TCPLength)
#
#         TCPChecksum = self.calculateChecksum(TCPHeader, pseudoHeader)
#
#         print(sourcePort, destPort)
#         TCPHeader = struct.pack("!HHLLBBH", sourcePort, destPort, TCP_INIT_SEQ_NUM, TCP_ACKNOWLEDGE_NUM, offset_Reserved_Byte, flags, TCP_MAX_WINDOW_SIZE) +  struct.pack("H", TCPChecksum) + struct.pack("!H", TCP_URG_POINTER)
#
#         self.compactHeader = TCPHeader
#
#
#     def calculateChecksum(self, TCPHeader, pseudoHeader):
#         compactData = TCPHeader + pseudoHeader + bytes(TCP_PAYLOAD, 'utf-8')
#         rawSum = 0
#         itr = len(compactData) % 2
#         end = len(compactData) - itr
#
#         for i in range(0, end, 2):
#             rawSum = rawSum + compactData[i] + (compactData[i+1] << 8)
#         if itr:
#             rawSum = rawSum + compactData[i+1]
#         while(rawSum >> 16):
#             rawSum = (rawSum & 0xFFFF) + (rawSum >> 16)
#         rawSum = ~rawSum & 0xFFFF
#         return rawSum

class TCPHeader:
    def __init__(self, sourceIP, destIP):
        self.compactHeader = None
        self.sourceIP = socket.inet_aton(sourceIP)
        self.destIP = socket.inet_aton(destIP)

    def fillTCPPacket(self, sourcePort, destPort):
        TCPSrc = sourcePort
        TCPDst = destPort
        TCPSeqNumber = 0
        TCPAckNumber = 0
        TCPHeaderLen = 80
        f_FIN = (0)
        f_SYN = (1 << 1)
        f_RST = (0 << 2)
        f_PSH = (0 << 3)
        f_ACK = (0 << 4)
        f_URG = (0 << 5)
        f_ECN = (0 << 6)
        f_CWR = (0 << 7)
        f_NOC = (0 << 8)
        f_RSV = (0 << 9)

        TCPFlags = f_RSV + f_NOC + f_CWR + f_ECN + f_URG + f_ACK + f_PSH + f_RST + f_SYN + f_FIN

        TCPWindowSize = socket.htons(TCP_MAX_WINDOW_SIZE)
        TCPChecksum = 0
        TCPURGPointer = 0

        self.compactHeader = struct.pack("!HHLLBBHHH", TCPSrc, TCPDst, TCPSeqNumber, TCPAckNumber, TCPHeaderLen, TCPFlags, TCPWindowSize, TCPChecksum, TCPURGPointer)

        TCPChecksum = self.calculateChecksum()

        self.compactHeader = struct.pack("!HHLLBBH", TCPSrc, TCPDst, TCPSeqNumber, TCPAckNumber, TCPHeaderLen, TCPFlags, TCPWindowSize) + struct.pack("H", TCPChecksum) + struct.pack("!H", TCPURGPointer)


    def calculateChecksum(self):
        srcIP = self.sourceIP
        dstIP = self.destIP
        zeroes = 0
        protocol = socket.IPPROTO_TCP
        # totalLen = len(self.compactHeader) + len(TCP_PAYLOAD)
        totalLen = len(self.compactHeader)

        pseudoHeader = struct.pack("!4s4sBBH", srcIP, dstIP, zeroes, protocol, totalLen)

        #pseudoHeader = pseudoHeader + self.compactHeader + bytes(TCP_PAYLOAD, 'utf-8')
        pseudoHeader = pseudoHeader + self.compactHeader
        
        rawSum = 0
        itr = len(pseudoHeader) % 2
        end = len(pseudoHeader) - itr

        for i in range(0, end, 2):
            rawSum = rawSum + pseudoHeader[i] + (pseudoHeader[i+1] << 8)

        rawSum = rawSum + (rawSum >> 16)
        rawSum = ~rawSum & 0xFFFF

        return rawSum
