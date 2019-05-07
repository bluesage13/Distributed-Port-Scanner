import socket
import sys
import traceback
#from threading import Thread
import threading
import queue as q
import time


def main(numList):
    startMaster(numList)

def connectToUser():
    ##Connect to the user who will be sending the jobs, this will connect to the server hosting the webui
    userSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = "127.0.0.1"
    port = 8889
    try:
        userSock.connect((host, port))
    except:
        print("Connection error")
        sys.exit()
    return userSock


def startMaster(numList):
    userConn = connectToUser()
    #userConn = None
    task_q = q.Queue()
    res_q = q.Queue()
    shouldExit = q.Queue()
    connectionList = q.Queue()
    jobQueue = q.Queue()
    stopConnections = 0
    host = "127.0.0.1"
    port = 8890

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

    connPool = []
    connThreadPool = []
    JobThread =  threading.Thread(target=jobLoop, args=(userConn,numList,task_q,res_q,stopConnections,shouldExit,connectionList,jobQueue,))
    JobThread.start()

    while True:
        connection, address = soc.accept()
        connPool.append(connection)
        ip, port = str(address[0]), str(address[1])
        print("Connected with " + ip + ":" + port)
        try:
            #Thread(target=client_thread, args=(connection, ip, port)).start()
            th = WorkerThread(connection = connection, ip=ip, port=port, task_q=task_q, res_q=res_q,jobQueue=jobQueue, max_buffer_size =5120)
            th.start()
            connThreadPool.append(th)
            connectionList.put(connection)
        except:
            print("Thread did not start.")
            traceback.print_exc()

        ##For this job all connections have been accepted
        if(shouldExit.qsize() == 1):
            break

    print("Ending all connections")

    for th in connThreadPool:
        th.join()
    soc.close()

def jobLoop(userConn, numList, task_q, res_q, stopConnections, shouldExit, connectionList, jobQueue):
    jobNumber = 1
    while True:
        while True:
            try:
                job = userConn.recv(5120)
                taskObject = parseJob(job.decode('utf-8'))
                while(connectionList.qsize() == 0):
                    continue
                jobQueue.put(1)
                buildTaskQueue(taskObject, task_q, connectionList.qsize())
                work_count = task_q.qsize()
                print(work_count)
                time.sleep(3)
                while(res_q.qsize() < work_count):
                    continue

                openPortDict = {}
                mode = ""
                while(res_q.empty() != True):
                    reply = res_q.get().split(':')
                    mode = reply[0]
                    openPortsList = reply[1]
                    if(len(openPortsList) != 0):
                        openPorts = openPortsList.split(',')
                        for port in openPorts:
                            openPortDict[port] = "True"
                combinedReport = "" + mode + ":"
                for p in list(openPortDict):
                    combinedReport = combinedReport + p + ","
                combinedReport.strip(',')

                userConn.sendall(combinedReport.encode("utf8"))
                temp = jobQueue.get()
            except:
                userConn.sendall("Job Not Done".encode("utf8"))

        return
        # while True:
        #     job = userConn.recv(5120)
        #     job = job.decode('utf-8')
        #     print("Job received is: ", job)
        #     jobSplit = job.split(':')
        #     start = int(jobSplit[0])
        #     end = int(jobSplit[1])
        #     print("Starting Job : ", jobNumber)
        #     jobQueue.put(1)
        #     work_count = 0
        #     for i in range(start, end+1):
        #         task_q.put(i)
        #         work_count += 1
        #     print("jobs assigned")
        #     print("work_count ", work_count)
        #     print("Waiting for job to get done...")
        #     time.sleep(3)
        #     while(res_q.qsize() < work_count):
        #         continue
        #     report = ""
        #     while(work_count > 0):
        #         result = res_q.get()
        #         report += (result + "\n")
        #         work_count -= 1
        #     temp = jobQueue.get()
        #     print("Job is done!")
        #     userConn.sendall(report.encode("utf8"))

def buildTaskQueue(taskObject, task_q, numConn):
    if(taskObject['Mode'] == 'isAlive'):
        print("Here")
        if(taskObject['Format'] == 's'):
            taskString = "isAlive:"+taskObject['Format']+":"+taskObject['DestIP']
             #print(taskString)
            task_q.put(taskString)
        elif(taskObject['Format'] == 'l'):
            ipList = taskObject['DestIP'].split(',')
            perConn = int(len(ipList)/numConn)
            for i in range(0, len(ipList), perConn):
                destIPString = ""
                for j in range(i, min(perConn+i, len(ipList))):
                    destIPString = destIPString + ipList[j] + ","
                destIPString = destIPString[:-1]
                taskString = "isAlive:"+taskObject['Format']+":"+destIPString
                 #print(taskString)
                task_q.put(taskString)
        elif(taskObject['Format'] == 'r'):
            ipSplit = taskObject['DestIP'].split('/')
            ipStringSplit = ipSplit[0].split('.')
            partA = ipStringSplit[0] + "." + ipStringSplit[1] + "." + ipStringSplit[2] + "."
            first = int(ipStringSplit[3])
            end = int(ipSplit[1])
            perConn = int((end - first + 1)/numConn) + 1
            for i in range(first, end+1, perConn):
                destIPString = partA + str(i) + ":" + str(min(i+perConn, end))
                taskString = "isAlive:"+taskObject['Format']+":"+destIPString
                 #print(taskString)
                task_q.put(taskString)

    else:
        if(taskObject['Format'] == 's'):
            taskString = taskObject['Mode']+":"+taskObject['Format']+":"+taskObject['DestIP']+":"+taskObject['PortList']
             #print(taskString)
            task_q.put(taskString)
        elif(taskObject['Format'] == 'l'):
            ipList = taskObject['PortList'].split(',')
            perConn = int(len(ipList)/numConn)+1
            for i in range(0, len(ipList), perConn):
                portString = ""
                for j in range(i, min(perConn+i, len(ipList))):
                    portString = portString + ipList[j] + ","
                portString = portString[:-1]
                taskString = taskObject['Mode']+":"+taskObject['Format']+":"+taskObject['DestIP']+":"+portString
                 #print(taskString)
                task_q.put(taskString)
        elif(taskObject['Format'] == 'r'):
            ipSplit = taskObject['PortList'].split('/')
            first = int(ipSplit[0])
            end = int(ipSplit[1])
            perConn = int((end - first + 1)/numConn) + 1
            for i in range(first, end+1, perConn):
                portString = str(i) + ":" + str(min(i+perConn, end))
                taskString = taskObject['Mode']+":"+taskObject['Format']+":"+taskObject['DestIP']+":"+portString
                 #print(taskString)
                task_q.put(taskString)


def printTaskDetails(taskObject):
    print('============================================')
    print('Mode: ', taskObject['Mode'])
    print('Destination IP: ', taskObject['DestIP'])
    print('Format: ', taskObject['Format'])
    print('Port List: ', taskObject['PortList'])
    print('============================================')
    return

def parseJob(job):
    jobSplit = job.split(':')
    taskObject = {}
    taskObject['Mode'] = jobSplit[0]
    taskObject['DestIP'] = jobSplit[1]
    taskObject['Format'] = jobSplit[2]
    taskObject['PortList'] = jobSplit[3]
    return taskObject

class WorkerThread(threading.Thread):

    def __init__(self, connection, ip, port, task_q, res_q, jobQueue, max_buffer_size = 5120):
        super(WorkerThread, self).__init__()
        self.connection = connection
        self.ip = ip
        self.port = port
        self.max_buffer_size = max_buffer_size
        self.task_q = task_q
        self.res_q = res_q
        self.stoprequest = threading.Event()
        self.jobQueue = jobQueue
        #self.prevJobID = 0

    def run(self):
        while(True):
            if(self.jobQueue.empty() != True):
                while not self.stoprequest.isSet():
                    try:
                        if(self.task_q.qsize() != 0):
                            num = self.task_q.get(True, 0.5)
                            self.connection.sendall(str(num).encode("utf8"))
                            client_input = self.connection.recv(self.max_buffer_size)
                            print("INPUT FROM CLIENT ==>", client_input.decode("utf8").rstrip())
                            decoded_input = client_input.decode("utf8").rstrip()
                            self.res_q.put(decoded_input)
                    except Exception as e:
                        print(e)
                        continue
            else:
                continue

    def join(self, timeout=None):
        self.stoprequest.set()
        super(WorkerThread, self).join(timeout)

if __name__ == '__main__':
    num_list = []
    for n in sys.argv[1:]:
        num_list.append(int(n))
    main(num_list)
