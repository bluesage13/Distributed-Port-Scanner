# cse509
## Distributed Network and TCP Port Scanner with Web UI
Instructions to run the code:
Open a new terminal to run each of the below commands and run them in the given order:
* python3 User.py
* python3 app2.py
* python3 ControllingNode.py
* sudo python3 ScanningNode.py (Can run this n number of times on n terminals to spawn new scanning nodes)
* Open 2.html file in browser to provide commands.

Potential jobs are:

1) isAlive:172.24.22.11:s:X

For the above job give the below inputs into the web UI, do so similarly for the remaining jobs which covers all the tests cases.

    IP address - 172.24.22.11
    Port number - X
    Mode - Single ( dropdown )
    job - isAlive ( dropdown )
    
2) isAlive:172.24.22.11,172.24.22.11,172.24.22.11,172.24.22.11,172.24.22.11,172.24.22.11:l:X
3) isAlive:1,2,3,4,5,6,7:l:X
4) isAlive:172.24.22.1/244:r:X
5) isAlive:172.24.22.1/1:r:X


6) TCPFULL:172.24.21.38:s:5000
7) TCPFULL:172.24.21.38:l:1234,12432,2314,3123,51,5010,145,5000
8) TCPFULL:172.24.21.38:r:5000/5025


9) TCPSYN:172.24.21.38:s:1234
10) TCPSYN:172.24.21.38:l:1234,12432,2314,3123,51,45,145,5000
11) TCPSYN:172.24.21.38:r:5000/5025

12) TCPFIN:172.24.21.38:s:5000
13) TCPFIN:172.24.21.38:l:1234,12432,2314,5010,51,45,145,5000
14) TCPFIN:172.24.21.38:r:5000/5010

Report will be loaded into the web UI upon reloading 2.html


Files
-----------------------------------------------------
app2.py has the flask code which is used to connect to the HTML page, a connection will be established to HTML page. All the jobs can be assigned one after the other using the web UI 

2.html contains the Web UI where in the user enters IP address, port number/port range along with the type of value -> single, list, range and the job to be done - to check if port is alive (or) to perform scanning (  Normal port scanning, TCP SYN Scanning, TCP FIN scanning ), 


References:

https://pentest-tools.com/network-vulnerability-scanning/tcp-port-scanner-online-nmap
https://linuxhint.com/python-for-hacking-port-scanner/
https://www.python-course.eu/python_network_scanner.php
https://scholarworks.sjsu.edu/cgi/viewcontent.cgi?article=1141&context=etd_projects
https://github.com/secdev/scapy
https://pastebin.com/YCR3vp9B
https://www.cyberciti.biz/faq/linux-unix-open-ports/
https://gist.github.com/pklaus/856268
https://www.geeksforgeeks.org/ping-in-c/
https://www.binarytides.com/raw-socket-programming-in-python-linux/
https://www.binarytides.com/category/programming/sockets/
https://github.com/mayurkadampro/TCP-Port-Scanner/blob/master/tcp_port_scanner.py
https://github.com/realpython/materials/tree/master/python-sockets-tutorial
https://github.com/securecurebt5/checksum/blob/master/checksum.py
http://www.bitforestinfo.com/2018/01/code-icmp-raw-packet-in-python.html
https://github.com/surajsinghbisht054/py-pinger
https://eli.thegreenplace.net/2011/12/27/python-threads-communication-and-stopping
https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/
https://stackoverflow.com/questions/19071512/socket-error-errno-48-address-already-in-use
