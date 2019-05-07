import struct
import socket
import select

from ICMPPacket import ICMPPacket
from constants import *

class Ping:
    def __init__(self):
        self.statusReport = {}

    def ping(self, format, remoteHosts):
        if(format == 's'):
            try:
                self.checkHostIsAlive(remoteHosts)
            except Exception as e:
                print(e)
                print("Input not in correct format for option s")

        elif(format == 'l'):
            try:
                remoteHostIPList = remoteHosts.split(',')
                for ip in remoteHostIPList:
                    self.checkHostIsAlive(ip)
            except Exception as e:
                print(e)
                print("Input not in correct format for option l")

        elif(format == 'r'):
            try:
                print(remoteHosts)
                remoteHosts = remoteHosts.split(':')
                ipStringSplit = remoteHosts[0].split('.')
                partA = ipStringSplit[0] + "." + ipStringSplit[1] + "." + ipStringSplit[2]
                firstNumber = int(ipStringSplit[3])
                lastNumber = int(remoteHosts[1])

            except Exception as e:
                print("Input not in correct format for option r")
                print(e)
                return

            remoteHostIPList = []
            for i in range(firstNumber, lastNumber + 1):
                ipString = partA + "." + str(i)
                remoteHostIPList.append(ipString)

            for ip in remoteHostIPList:
                self.checkHostIsAlive(ip)

        else:
            print("Not a valid option")
        return

    def checkHostIsAlive(self, remoteHostIP):
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
        icmpEchoRequest = ICMPPacket()
        icmpEchoRequest.initializePacket()
        sock.sendto(icmpEchoRequest.compactPacket, (remoteHostIP, 0))
        while True:
            rlist = [sock]
            wlist = []
            xlist = []
            retSubset = select.select(rlist, wlist, xlist, TIMEOUT)
            if(retSubset[0] == []):
                print(remoteHostIP, "is not Alive")
                sock.close()
                break
            echoReply, ipAddr = sock.recvfrom(SOCK_BUFFER_SIZE)
            compactPacket = echoReply[ICMP_START_INDEX:ICMP_END_INDEX]
            icmpEchoReply = ICMPPacket(compactPacket)
            if(icmpEchoReply.pktID == icmpEchoRequest.pktID):
                self.statusReport[remoteHostIP] = "Alive"
                print(remoteHostIP," is Alive")
                sock.close()
                break
        return
