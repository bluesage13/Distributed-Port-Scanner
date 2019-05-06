from TCPSYNScan import TCPSYNScan
import threading
from scapy.all import sniff
import os
import time


ss = TCPSYNScan()
#ss.scan('172.24.22.11', '45.33.32.156', 's', 9929)
ss.scan('172.24.22.11', '172.24.21.38', 's', 65535)
