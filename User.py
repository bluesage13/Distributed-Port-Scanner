import socket
import sys
import traceback
from threading import Thread
import time
import os


def main():
    startUser()


def startUser():
    host = "127.0.0.1"
    port = 8889

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("Socket created")

    try:
        soc.bind((host, port))
    except Exception as e:
        print(e)
        sys.exit()

    soc.listen(5)
    print("Socket now listening")

    while True:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print("Thread did not start.")
            traceback.print_exc()

    soc.close()

def dumpResult(jobDict, client_input):
    if(jobDict == None):
        dumpString = "Job Not Done\nPlease Check the Field Input and/or Connections"
    else:
        try:
            print(jobDict)
            dumpString = "\n" + ("==" *30)
            dumpString += "\nMode : "
            dumpString += jobDict['mode']
            dumpString += "\nRemote Host(s) Scanned : "
            dumpString += jobDict['ip']
            dumpString += "\nFormat : "
            dumpString += jobDict['format']
            dumpString += "\nPort(s) Scanned : "
            dumpString += jobDict['port']
            dumpString += "\n" + ("==" *30)
            dumpString += "\nRESULT"
            dumpString += "\n" + ("-" *25)
            if(jobDict['mode'] == 'isAlive'):
                csp = client_input.split(':')
                if(csp[1] == ""):
                    dumpString += "\n(All) Host(s) are Down"
                else:
                    hosts = csp[1].split(',')
                    for h in hosts[:-1]:
                        dumpString += "\n| "
                        dumpString += h
                        dumpString += " | Alive |"
            else:
                csp = client_input.split(':')
                if(csp[1] == ""):
                    dumpString += "\nAll ports are closed"
                else:
                    hosts = csp[1].split(',')
                    for h in hosts[:-1]:
                        dumpString += "\n| "
                        dumpString += h
                        if(jobDict['mode'] == 'TCPFIN'):
                            dumpString += " | Open | Filtered |"
                        else:
                            dumpString += "| Open |"
            dumpString += "\n" + ("-" *25)
            print(dumpString)
        except:
            dumpString = "Job Not Done\nPlease Check the Field Input and/or Connections"
    resultFile = open("results/result.txt", "w+")
    resultFile.write(dumpString)

def client_thread(connection, ip, port, max_buffer_size = 5120):
    is_active = True

    while is_active:
        try:
            jobFile = open('job.txt', 'r')
        except FileNotFoundError:
            time.sleep(1)
            continue
        try:
            jobDict = {
                'mode' : None,
                'ip'   : None,
                'port' : None,
                'format' : None
            }
            for line in jobFile.readlines():
                sp = line.split("_")
                jobDict[sp[0]] = sp[1].strip('\n')
                print(sp)
            if jobDict['port'] == '':
                jobDict['port'] = 'X'
            jobString = jobDict['mode']+":"+jobDict['ip']+":"+jobDict['format']+":"+jobDict['port']
            print("Sending Job:", jobString)
            connection.sendall(jobString.encode("utf8"))
            client_input = connection.recv(max_buffer_size)
            client_input = client_input.decode("utf8").rstrip()
            print(client_input)
            dumpResult(jobDict, client_input)
            os.remove('job.txt')
        except:
            dumpResult(None, None)
            continue

if __name__ == "__main__":
    main()
