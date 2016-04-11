from test_pings import Test_pings
from ip_to_city import IP_to_Loc
import socket
ic=IP_to_Loc()

def top_n_servers(n):
	f=open('../misc/top-1m.csv','r')
	fw=open('filtered_servers','w')
	tp=Test_pings()
	counter=0
	google=0
	for line in f:
		googleflag=True
		print counter
		s=line.split(',')[1].strip('\n')
		if 'google' in s and google>1:
			googleflag=False
		if counter>=n:
			break
		if tp.check_ping(s) and tp.check_tcpping(s) and ic.in_US(s) and googleflag:
			if 'google' in s:
				google+=1
			counter+=1
			fw.write(s+'\n')

def top_n_plab(n):
	f=open('pl_nodes','r')
	fw=open('servers_plab','w')
	tp=Test_pings()
	counter=0
	for line in f:
		print counter
		s=line.split()[0]
		print s
		if counter>=n:
			break
		if  ic.in_US(s) and tp.check_ping(s) \
				and tp.check_ssh(s,'tufts_comp150_b','~/.ssh/mraja01_key'):
			counter+=1
			fw.write(s+'\n')

#top_n_servers(100)
top_n_plab(50)
