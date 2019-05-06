import socket
import struct
import select
import threading
from multiprocessing import Process
import os
import time
from scapy.all import sniff
from TCPHeader import TCPHeader
from constants import *

class TCPFINScan:

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

    def listenOnPort(self, sourceIP):
        filterStr = "tcp and host " + sourceIP + " and port " + str(TCP_SOURCE_PORT)
        packets=sniff(count=2,filter=filterStr,timeout=3)
        for packet in packets:
            if(packet['TCP'].flags == 'RA'):
                print('Port is closed')
                return
        print("Port is open|filtered")
        return


    def scanPort(self, sourceIP, destIP, destPort):
        TCP = TCPHeader(sourceIP, destIP)
        TCP.fillTCPPacket(TCP_SOURCE_PORT, destPort)

        spoofedSYNPacket = TCP.compactHeader

        try:
            # childpid = os.fork()
            # if childpid == 0:
            #     self.listenOnPort(sourceIP)
            sniffer = Process(target=self.listenOnPort, args=(sourceIP,))
            sniffer.start()
            time.sleep(1)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.sendto(spoofedSYNPacket, (destIP, 0))
            sock.close()
        except:
            print("Error")
        #os.waitpid(childpid, 0)
        sniffer.join()
        return
