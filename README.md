# cse509
## Distributed Network and TCP Port Scanner with Web UI
### Controlling Node:
1.	Will host the webUI to present the task options and viewing the report for scanning.
2.	Tasks available:
a.	List the available scanning nodes in the pool
b.	Port scanning : Take as input : IP address/es, mode of scanning, ports to scan (can be a range, list, common ports)
c.	Display the report after submitting the job.
3.	Connect to the database to store the report of previous jobs.
4.	Enable viewing of the history of jobs (all or specific IP) with timestamp
### Scanning Node:
1.	Creating a scanning node:
a.	Each node can be created, say manually, for the purpose of this project.
b.	On creation the node will send a message to the controlling server that it is online.
c.	The main server will add it to the pool of available nodes.
2.	Accept command from server and start execution. After execution return the partial report to the controlling node.


## Tasks:
1.	Single node port scanning: isAlive mode
2.	Single node port scanning: Full TCP connect
3.	Single node port scanning: TCP SYN (using raw sockets)
4.	Single node port scanning: TCP FIN (using raw sockets)
5.	Setting up the distributed system one controller and variable scanners
6.	Developing webUI and database
7.	Setting up a small array of clients to enable safe port scanning
