import socket
import struct
import select
import threading
import os
import time
from multiprocessing import Process
import threading
from scapy.all import sniff
from IPHeader import IPHeader
from TCPHeader import TCPHeader
from constants import *

class TCPSYNScan:
    def __init__(self):
        self.sniffer = None
        self.threadList = []
        self.maxPortsPerThread = MAX_PORTS_PER_THREAD
        self.maxThreads = 0
        self.totalPorts = 0

    def startSniffer(self,sourceIP, capturePackets=1):
        self.sniffer = Process(target=self.listenOnPort, args=(sourceIP,capturePackets,))
        self.sniffer.start()
        time.sleep(2)

    def scan(self, sourceIP, destIP, format, portsList):
        if(type(portsList) == int):
            temp = [portsList]
            portsList = temp
        self.totalPorts = len(portsList)
        self.maxThreads = int(len(portsList) / MAX_PORTS_PER_THREAD) + 1
        if(self.maxThreads > MAX_THREADS):
            self.maxThreads = MAX_THREADS
            self.maxPortsPerThread = int(numPorts/MAX_THREADS)


        if(format == 's'):
            try:
                self.startSniffer(sourceIP)
                self.scanPort(sourceIP, destIP, 1234)
            except Exception as e:
                print(e)
                print("Input not in correct format for option s")

        elif(format == 'l'):
            try:
                portsList = portsList.split(',')
                portsList = [int(x) for x in portsList]

                self.totalPorts = len(portsList)
                self.maxThreads = int(len(portsList) / MAX_PORTS_PER_THREAD) + 1
                if(self.maxThreads > MAX_THREADS):
                    self.maxThreads = MAX_THREADS
                    self.maxPortsPerThread = int(numPorts/MAX_THREADS)
                self.startSniffer(sourceIP,self.totalPorts)
                self.initializeThreads(portsList, sourceIP, destIP)
                print("Starting Thread::")
                for thread in self.threadList:
                    thread.start()
            except Exception as e:
                print(e)

        elif(format == 'r'):
            try:
                portsList = portsList.split(':')
                firstPort = int(portsList[0])
                lastPort = int(portsList[1])
                portsList = [x for x in range(firstPort, lastPort+1)]

                self.totalPorts = len(portsList)
                self.maxThreads = int(len(portsList) / MAX_PORTS_PER_THREAD) + 1
                if(self.maxThreads > MAX_THREADS):
                    self.maxThreads = MAX_THREADS
                    self.maxPortsPerThread = int(numPorts/MAX_THREADS)
                self.startSniffer(sourceIP,self.totalPorts)

                self.initializeThreads(portsList, sourceIP, destIP)
                print("TOTAL PORTS ", self.totalPorts)
                print("Starting Threads::", len(self.threadList))
                for thread in self.threadList:
                    thread.start()
            except Exception as e:
               print(e)
               return

        else:
            print("Not a valid option")
        for thread in self.threadList:
            thread.join()
        self.sniffer.join()
        return

    def threadScan(self, sourceIP, destIP, portsList):
        for port in portsList:
            self.scanPort(sourceIP, destIP, port)

    def scanPort(self, sourceIP, destIP, destPort):
        TCP = TCPHeader(sourceIP, destIP)
        TCP.fillTCPPacket(TCP_SOURCE_PORT, destPort)

        spoofedSYNPacket = TCP.compactHeader

        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            sock.sendto(spoofedSYNPacket, (destIP, 0))
            sock.close()
        except:
            print("Error")
        return

    def listenOnPort(self, sourceIP, capturePackets):
        print("Listening::")
        filterStr = "tcp and host " + sourceIP + " and port " + str(TCP_SOURCE_PORT)
        packets=sniff(count=capturePackets * 2,filter=filterStr, timeout=10)
        print("Total packets captured :", len(packets))
        statusDict = {}
        for packet in packets:
            if(packet['TCP'].flags == 'SA'):
                statusDict[packet['TCP'].sport] = "Open"
            if(packet['TCP'].flags == 'RA'):
                statusDict[packet['TCP'].sport] = "Closed"
        print("Total Port Reports : " , len(statusDict))
        for k in statusDict:
            if(statusDict[k] == "Open"):
                print("Port ", k, "is Open")
        return

    def initializeThreads(self, portsList, sourceIP, destIP):
        numPorts = len(portsList)
        start = 0
        for i in range(0, self.maxThreads):
            ports = []
            if(start+self.maxPortsPerThread < numPorts):
                ports = portsList[start:start+self.maxPortsPerThread]
                start = start + self.maxPortsPerThread
            else:
                ports = portsList[start:numPorts]
            thread = threading.Thread(target=self.threadScan, args=(sourceIP, destIP, ports,))
            self.threadList.append(thread)
        print("Threads Initialized")
        return
