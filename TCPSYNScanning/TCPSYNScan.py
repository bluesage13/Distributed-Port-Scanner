import socket
import struct
import select
from IPHeader import IPHeader
from TCPHeader import TCPHeader
from constants import *

class TCPSYNScan:
    def scan(self, sourceIP, destIP, format, portsList):
        if(format == 's'):
            #try:
            self.scanPort(sourceIP, destIP, portsList)
            #except:
            #    print("Input not in correct format for option s")

        elif(format == 'l'):
            try:
                portsList = portsList.split(',')
                for port in portsList:
                    self.scanPort(sourceIP, destIP, port)
            except:
                print("Input not in correct format for option l")

        elif(format == 'r'):
            try:
                portsList = portsList.split(':')
                firstPort = int(portsList[0])
                lastPort = int(portsList[1])

            except:
                print("Input not in correct format for option r")
                return

            for port in range(firstPort, lastPort + 1):
                self.scanPort(sourceIP, destIP, port)

        else:
            print("Not a valid option")
        return

    def scanPort(self, sourceIP, destIP, destPort):

        TCP = TCPHeader(sourceIP, destIP)
        TCP.fillTCPPacket(TCP_SOURCE_PORT, destPort)

        spoofedSYNPacket = TCP.compactHeader
        print(struct.unpack("!HHLLBBHHH",TCP.compactHeader))
        print(TCP.compactHeader)
        print('Sendign to ', destIP)

        maxTries = MAX_TRIES
        while (maxTries > 0):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                sock.sendto(spoofedSYNPacket, (destIP, 0))
            except:
                print("Error")
            rlist = [sock]
            wlist = []
            xlist = []
            # retSubset = select.select(rlist, wlist, xlist, TIMEOUT)
            # if(retSubset[0] == []):
            #     maxTries -= 1
            #     continue
            replyPacket, ipAddr = sock.recvfrom(SOCK_BUFFER_SIZE)
            #compactPacket = replyPacket[ICMP_START_INDEX:ICMP_END_INDEX]
            # icmpEchoReply = ICMPPacket(compactPacket)
            # if(icmpEchoReply.pktID == icmpEchoRequest.pktID):
            #     print(remoteHostIP," is Alive")
            #     sock.close()
            #     break
            print(replyPacket)
            sock.close()
        return
