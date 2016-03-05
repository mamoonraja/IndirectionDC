import socket
import sys
import struct
from struct import *
import time
import os

def receiver(UDP_ip,UDP_port,output_file):
	head,tail= os.path.split(output_file)
	os.system("mkdir "+output_file)
	sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # UDP
	sock.bind((UDP_IP, UDP_PORT))
	print "rcvng...."
	while True:
		data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
		time_rcvd=int(round(time.time() * 1000))
		time_sent,hour_num,seq_num,re_rt=struct.unpack('!QHHI',data)
		lat=time_rcvd-time_sent
		out_file=head+"/"+tail+"/"+str(hour_num)+"_"+tail
		fi=open(out_file,'a')
		fi.write(str(hour_num)+" "+str(re_rt)+" "+str(seq_num)+" "+str(lat)+" "+str(time_sent)+" "+str(time_rcvd)+"\n")
		fi.close()



receiver('',int(sys.argv[1]),sys.argv[2])
