import os
import socket
import sys
import time 
import struct
from struct import *

def ip2long(ip):
	print ip
	packedIP = socket.inet_aton(str(ip))
	print packedIP
	return struct.unpack("!L", packedIP)[0]

def get_DC(Data_center_list):
	global_rtt=10000
	nearest_node=''
	for item in Data_center_list:
		nodes_rtt=get_RTT(item.split(',')[0])
		if  nodes_rtt < global_rtt:
			global_rtt=nodes_rtt
			nearest_node=item.split(',')[0]
	return nearest_node

def get_RTT(node):
	os.system('timeout 10s tcpping '+node.strip('\n')+' > ping_status')
	return ping_parser(open('ping_status','r'),1)

def ping_parser(ping_file,info_to_get):#
	result=[]
	if info_to_get==1:
		for line in ping_file:
				if "timeout" not in line:
					result.append(float(line.split(' ')[8]))
	return 	float(max(result))/float(len(result))			


def sender(UDP_IP,UDP_PORT,seq_num,hours_passed,exp_duration,DC_PORT):
	print UDP_IP,UDP_PORT,exp_duration
	DC_IP=get_DC(open('DC_list','r')) #fetching ip of nearest DC
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
	while hours_passed < int(exp_duration):	
		if seq_num==3600:
			seq_num=0
			hours_passed+=1
		while seq_num < 3600:
			packet_direct = struct.pack('!QHHI', int(round(time.time() * 1000)),hours_passed,seq_num,0) #direct packet   
			packet_dc = struct.pack('!QHHILH', int(round(time.time() * 1000)),hours_passed,seq_num,1,ip2long(UDP_IP),UDP_PORT) #for dc to forward    
			sock.sendto(packet_direct, (UDP_IP, UDP_PORT))
			sock.sendto(packet_dc, (DC_IP, DC_PORT))
			time.sleep(1)
			seq_num+=1

sender(str(sys.argv[2]),int(sys.argv[1]),0,0,sys.argv[3],5000)

