import socket
import struct
import select
import threading
import os
import time
from multiprocessing import Process
import threading
from scapy.all import sniff

MAX_PORTS_PER_THREAD = 25
MAX_THREADS = 100

class TCPFullConnect:
    def __init__(self):
        self.sniffer = None
        self.threadList = []
        self.maxPortsPerThread = MAX_PORTS_PER_THREAD
        self.maxThreads = 0
        self.totalPorts = 0
        self.portStatus = {}

    def scan(self, format, remoteHost, portsList):
        print("FORMAT ", format)
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
                self.scanPort(remoteHost, portsList[0])
            except Exception as e:
                print(e)

        elif(format == 'l'):
            try:
                portsList = portsList.split(',')
                portsList = [int(x) for x in portsList]

                self.totalPorts = len(portsList)
                self.maxThreads = int(len(portsList) / MAX_PORTS_PER_THREAD) + 1
                if(self.maxThreads > MAX_THREADS):
                    self.maxThreads = MAX_THREADS
                    self.maxPortsPerThread = int(numPorts/MAX_THREADS)
                self.initializeThreads(portsList, remoteHost)
                print("Starting Thread::",  len(self.threadList))
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
                self.initializeThreads(portsList, remoteHost)
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
        return

    def threadScan(self, remoteHost, portsList):
        for port in portsList:
            self.scanPort(remoteHost, port)

    def scanPort(self, remoteHost, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        returnCode = sock.connect_ex((remoteHost, port))

        try:
            if returnCode == 0:
                self.portStatus[port] = "Open"
                #print("Port : ", port, " at IP : ", remoteHost, " is Open")
            else:
                self.portStatus[port] = "Closed"
                #print("Port : ", port, " at IP : ", remoteHost, " is Closed")
            sock.close()
        except:
            print("Conenction issue")
        return

    def initializeThreads(self, portsList, remoteHost):
        numPorts = len(portsList)
        start = 0
        for i in range(0, self.maxThreads):
            ports = []
            if(start+self.maxPortsPerThread < numPorts):
                ports = portsList[start:start+self.maxPortsPerThread]
                start = start + self.maxPortsPerThread
            else:
                ports = portsList[start:numPorts]
            thread = threading.Thread(target=self.threadScan, args=(remoteHost, ports,))
            self.threadList.append(thread)
        print("Threads Initialized")
        return
