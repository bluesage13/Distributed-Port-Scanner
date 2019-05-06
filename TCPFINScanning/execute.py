from TCPFINScan import TCPFINScan
import threading
from scapy.all import sniff
import os
import time


fs = TCPFINScan()
fs.scan('172.24.22.11', '172.24.21.38', 's', 65535)
