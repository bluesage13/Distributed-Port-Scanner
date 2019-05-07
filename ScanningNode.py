import socket
import sys
from PingClass import Ping
from TCPFullConnect import TCPFullConnect
from TCPFINScan import TCPFINScan
from TCPSYNScan import TCPSYNScan
from constants import *
import time

def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8890

    try:
        soc.connect((host, port))
    except:
        print("Connection error")
        sys.exit()

    while True:
        #print("Waiting for input from master")
        try:
            task = soc.recv(5120)
            print(task)
            taskObject=parseTask(task.decode("utf8"))
            printTaskDetails(taskObject)
            returnText = ""
            if(taskObject['Mode'] == "isAlive"):
                p = Ping()
                p.ping(taskObject['Format'], taskObject['DestIP'])
                returnText = "ISALIVE:"
                for ip in list(p.statusReport.keys()):
                    returnText = returnText + ip + ","
                returnText = returnText.strip(',')
            elif(taskObject['Mode'] == "TCPFULL"):
                tcp = TCPFullConnect()
                tcp.scan(taskObject['Format'], taskObject['DestIP'],taskObject['PortList'])
                #print(tcp.portStatus)
                returnText = "PORTSCANNING:"
                openPorts = []
                numberOfClosedPorts = 0
                for k in tcp.portStatus.keys():
                    if(tcp.portStatus[k] == "Open"):
                        openPorts.append(k)
                    else:
                        numberOfClosedPorts += 1
                for port in openPorts:
                    returnText = returnText + str(port) + ","
                returnText = returnText.strip(',')
                returnText = returnText + ":" + str(numberOfClosedPorts)

            elif(taskObject['Mode'] == "TCPSYN"):
                ss = TCPSYNScan()
                ss.scan(SOURCE_IP_ADDR, taskObject['DestIP'], taskObject['Format'], taskObject['PortList'])
                print("=======",ss.portStatus)
                returnText = "PORTSCANNING:"
                openPorts = []
                numberOfClosedPorts = 0
                for k in ss.portStatus.keys():
                    if(ss.portStatus[k] == "Open"):
                        openPorts.append(k)
                    else:
                        numberOfClosedPorts += 1
                for port in openPorts:
                    returnText = returnText + str(port) + ","
                returnText = returnText.strip(',')
                returnText = returnText + ":" + str(numberOfClosedPorts)
            elif(taskObject['Mode'] == "TCPFIN"):
                fs = TCPFINScan()
                fs.scan(SOURCE_IP_ADDR, taskObject['DestIP'], taskObject['Format'], taskObject['PortList'])
                returnText = "PORTSCANNING:"
                openPorts = []
                numberOfClosedPorts = 0
                for k in fs.portStatus.keys():
                    if(fs.portStatus[k] == "Open|Filtered"):
                        openPorts.append(k)
                    else:
                        numberOfClosedPorts += 1
                for port in openPorts:
                    returnText = returnText + str(port) + ","
                returnText = returnText.strip(',')
                returnText = returnText + ":" + str(numberOfClosedPorts)
            time.sleep(2)
            soc.sendall(returnText.encode("utf8"))
            print("Message: ", returnText)
        except Exception as e:
            soc.sendall("Error".encode("utf8"))
            print(e)

    soc.close()

def printTaskDetails(taskObject):
    print('============================================')
    print('Mode: ', taskObject['Mode'])
    print('Destination IP: ', taskObject['DestIP'])
    print('Format: ', taskObject['Format'])
    if(len(taskObject) == 4):
        print('Port List: ', taskObject['PortList'])
    print('============================================')
    return

def parseTask(task):
    jobSplit = task.split(':')
    taskObject = {}
    if(jobSplit[0] == "isAlive"):
        taskObject['Mode'] = jobSplit[0]
        taskObject['Format'] = jobSplit[1]
        taskObject['DestIP'] = jobSplit[2]
        if(len(jobSplit) == 4):
            taskObject['DestIP'] = jobSplit[2] + ":" +jobSplit[3]
    else:
        taskObject['Mode'] = jobSplit[0]
        taskObject['Format'] = jobSplit[1]
        taskObject['DestIP'] = jobSplit[2]
        taskObject['PortList'] = jobSplit[3]
        if(len(jobSplit) == 5):
            taskObject['PortList'] = jobSplit[3] + ":" + jobSplit[4]
    return taskObject

if __name__ == "__main__":
    main()
