from TCPFINScan import TCPFINScan
import threading
from scapy.all import sniff
import os
import time


fs = TCPFINScan()
fs.scan('172.24.22.11', '172.24.21.38', 's', 5000)
#fs.scan('172.24.22.11', '45.33.32.156', 's', 9929)
#fs.scan('172.24.22.11', '45.33.32.156', 'l', '9900,9901')
#fs.scan('172.24.22.11', '172.24.21.38', 'l', '4000,5000,6000,7000,8000')
#fs.scan('172.24.22.11', '172.24.21.38', 'r', '4900:6000')
