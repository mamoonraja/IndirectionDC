import socket
import sys
import time 
import struct
from struct import *
import os

def ip2long(ip):
	packedIP = socket.inet_aton(ip)
	return struct.unpack("!L", packedIP)[0]

def long2ip(longip):
	return socket.inet_ntoa(struct.pack('!L', longip))

def rcv_socket(UDP_PORT,UDP_IP):
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	return sock

def Relay(UPORT,UIP,output_file,hours_passed):
	head,tail= os.path.split(output_file) # to seperate path into recent directory
	sock=rcv_socket(UPORT,UIP)
	sock.bind((UIP, UPORT))
	sock1 = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
	os.system("mkdir "+output_file) #directory to keep record of data here
	out_file=head+"/"+tail+"/"+str(hours_passed)+"_"+tail
	fi=open(out_file,'a')
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		time_sent,hours_passed,seq_num,re_route,dest_IP,sento_port=struct.unpack('!QHHILH',data)
		lat=int(round(time.time() * 1000))-time_sent
		fi.write(str(hours_passed)+" "+str(re_route)+" "+str(seq_num)+" "+str(lat)+" "+str(time_sent)+" "+str(time_rcvd)+"\n")
		if re_route==1:
			packet = struct.pack('!QHHI', time_sent,hours_passed,seq_num,re_route) 
			sock1.sendto(packet, (long2ip(dest_IP), sendto_port))
	fi.close()

Relay(int(sys.argv[1]),'',sys.argv[2],0)
