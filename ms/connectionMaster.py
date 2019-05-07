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
        job = userConn.recv(5120)
        job = job.decode('utf-8')
        print("Job received is: ", job)
        jobSplit = job.split(':')
        start = int(jobSplit[0])
        end = int(jobSplit[1])
        print("Starting Job : ", jobNumber)
        jobQueue.put(1)
        work_count = 0
        for i in range(start, end+1):
            task_q.put(i)
            work_count += 1
        print("jobs assigned")
        print("work_count ", work_count)
        print("Waiting for job to get done...")
        time.sleep(3)
        while(res_q.qsize() < work_count):
            continue
        report = ""
        while(work_count > 0):
            result = res_q.get()
            report += (result + "\n")
            work_count -= 1
        temp = jobQueue.get()
        print("Job is done!")
        userConn.sendall(report.encode("utf8"))

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



# def client_thread(connection, ip, port, max_buffer_size = 5120):
#     is_active = True
#
#     while is_active:
#         client_input = receive_input(connection, max_buffer_size)
#
#         if "--QUIT--" in client_input:
#             print("Client is requesting to quit")
#             connection.close()
#             print("Connection " + ip + ":" + port + " closed")
#             is_active = False
#         else:
#             print("Processed result: {}".format(client_input))
#             connection.sendall("-".encode("utf8"))
#
#
# def receive_input(connection, max_buffer_size):
#     client_input = connection.recv(max_buffer_size)
#     client_input_size = sys.getsizeof(client_input)
#
#     if client_input_size > max_buffer_size:
#         print("The input size is greater than expected {}".format(client_input_size))
#
#     decoded_input = client_input.decode("utf8").rstrip()  # decode and strip end of line
#     result = process_input(decoded_input)
#
#     return result
#
#
# def process_input(input_str):
#     print("Processing the input received from client")
#
#     return "Hello " + str(input_str).upper()
