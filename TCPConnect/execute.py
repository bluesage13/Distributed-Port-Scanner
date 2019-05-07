from TCPFullConnect import TCPFullConnect
import threading
from scapy.all import sniff
import os
import time


#fs = TCPFullConnect()
#fs.scan('172.24.21.38', 's', 5000)
#fs.scan('172.24.22.11', '45.33.32.156', 's', 9929)
#fs.scan('172.24.22.11', '45.33.32.156', 'l', '9900,9901')
#fs.scan('172.24.22.11', '172.24.21.38', 'l', '4000,5000,6000,7000,8000')
#fs.scan('172.24.22.11', '172.24.21.38', 'r', '4900:6000')

tcp = TCPFullConnect()
#tcp.scan("l", "172.24.21.38", '4000,5000,6000,7000,8000')
tcp.scan('r','172.24.21.38', '1:10')
#TCPFULL:172.24.22.38:r:1/10
