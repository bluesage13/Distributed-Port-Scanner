import socket
import struct
import select
import threading
import os
import time
from multiprocessing import Process
import threading
from scapy.all import sniff
from TCPHeader import TCPHeader
from constants import *

class TCPFINScan:
    def __init__(self):
        self.sniffer = None
        self.threadList = []
        self.maxPortsPerThread = MAX_PORTS_PER_THREAD
        self.maxThreads = 0
        self.totalPorts = 0

    def startSniffer(self,sourceIP, portList,capturePackets=1):
        self.sniffer = Process(target=self.listenOnPort, args=(sourceIP,capturePackets,portList,))
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
                self.startSniffer(sourceIP, portsList)
                self.scanPort(sourceIP, destIP, portsList[0])
            except Exception as e:
               print(e)
               return

        elif(format == 'l'):
            try:
                print(portsList)
                portsList = portsList.split(',')
                portsList = [int(x) for x in portsList]

                self.totalPorts = len(portsList)
                self.maxThreads = int(len(portsList) / MAX_PORTS_PER_THREAD) + 1
                if(self.maxThreads > MAX_THREADS):
                    self.maxThreads = MAX_THREADS
                    self.maxPortsPerThread = int(numPorts/MAX_THREADS)
                self.startSniffer(sourceIP, portsList, self.totalPorts)
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
                self.startSniffer(sourceIP, portsList, self.totalPorts)

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

    def listenOnPort(self, sourceIP, capturePackets, portsList):
        print("Listening::")
        filterStr = "tcp and host " + sourceIP + " and port " + str(TCP_SOURCE_PORT)
        packets=sniff(count=capturePackets * 2,filter=filterStr, timeout=10)
        print("Total packets captured :", len(packets))
        allPorts = {}
        for p in portsList:
            allPorts[p] = "Open|Filtered"
        for packet in packets:
            if(packet['TCP'].flags == 'RA'):
                allPorts[packet['TCP'].sport] = "Closed"

        print("Total Port Reports : " , len(allPorts))
        for k in allPorts:
            if(allPorts[k] != "Closed"):
                print("Port ", k, "is Open|Filtered")
        return

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
