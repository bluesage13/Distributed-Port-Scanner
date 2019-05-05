from TCPSYNScan import TCPSYNScan

ss = TCPSYNScan()
#ss.scan('172.24.22.11', '45.33.32.156', 's', 22)
ss.scan('172.24.22.11', '172.24.21.38', 's', 5000)
