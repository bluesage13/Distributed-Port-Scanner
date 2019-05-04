import socket

class TCPFullConnect:
    def scan(self, format, remoteHost, ports):
        if(format == 's'):
            try:
                self.portScan(remoteHost, ports)
            except:
                print("Input not in correct format for option s")

        elif(format == 'l'):
            try:
                portList = ports.split(',')

            except:
                print("Input not in correct format for option l")
            for port in portList:
                self.portScan(remoteHost, int(port))

        elif(format == 'r'):
            try:
                ports = ports.split(':')
                firstNumber = int(ports[0])
                lastNumber = int(ports[1])

            except:
                print("Input not in correct format for option r")
                return

            for port in range(firstNumber, lastNumber + 1):
                self.portScan(remoteHost, port)

        else:
            print("Not a valid option")
        return

    def portScan(self, remoteHost, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        returnCode = sock.connect_ex((remoteHost, port))

        try:
            if returnCode == 0:
                print("Port : ", port, " at IP : ", remoteHost, " is Open")
            else:
                print("Port : ", port, " at IP : ", remoteHost, " is Closed")
            sock.close()
        except:
            print("Conenction issue")
        return
