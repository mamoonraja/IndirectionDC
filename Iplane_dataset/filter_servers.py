from test_pings import Test_pings
from ip_to_city import IP_to_Loc
import socket
ic=IP_to_Loc()

def top_n_servers(n):
	f=open('../misc/top-1m.csv','r')
	fw=open('filtered_servers','w')
	tp=Test_pings()
	counter=0
	for line in f:
		print counter
		s=line.split(',')[1].strip('\n')
		if counter>=n:
			break
		if tp.check_ping(s) and tp.check_tcpping(s) and ic.in_US(s):
			counter+=1
			fw.write(s+'\n')

top_n_servers(100)
