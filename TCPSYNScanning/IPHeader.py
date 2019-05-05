import struct
import socket
from random import randint
from constants import *

class IPHeader:
    def __init__(self, sourceIP, destIP):
        self.sourceIP = socket.inet_aton(sourceIP)
        self.destIP = socket.inet_aton(destIP)
        self.compactHeader = None

    # def fillIPHeader(self):
    #     version_IHL = (IP_VERSION << 4) + IP_INTERNET_HEADER_LENGTH
    #     #pktID = randint(0, 0xFFFF)
    #     pktID = 1
    #     protocol = socket.IPPROTO_TCP
    #
    #     self.compactHeader = struct.pack("!BBHHHBBH4s4s", version_IHL, IP_TYPE_OF_SERVICE, IP_INIT_LENGTH, pktID, IP_FLAG_FRAG_OFFSET, IP_TIME_TO_LIVE, protocol, IP_INIT_CHECKSUM, self.sourceIP, self.destIP)
    def fillIPHeader(self):
        ip_ihl = 5
        ip_ver = 4
        ip_tos = 0
        ip_tot_len = 0
        ip_id = 54321
        ip_frag_off = 0
        ip_ttl = 255
        ip_proto = socket.IPPROTO_TCP
        ip_check = 0
        ip_saddr = self.sourceIP
        ip_daddr = self.destIP
        ip_ihl_ver = (ip_ver << 4) + ip_ihl

        self.compactHeader = struct.pack('!BBHHHBBH4s4s' , ip_ihl_ver, ip_tos, ip_tot_len, ip_id, ip_frag_off, ip_ttl, ip_proto, ip_check, ip_saddr, ip_daddr)
