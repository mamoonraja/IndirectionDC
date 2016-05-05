from test_pings import Test_pings
from ip_to_city import IP_to_Loc
import socket
ic=IP_to_Loc()
'''
used to filter servers
'''
def top_n_servers(n,inUS_flag):
	'''
	   from alexa server list, generates 'filtered_servers' file with top n servers
	'''
	f=open('../misc/top-1m.csv','r')
	if inUS_flag: # check for US servers
		fw=open('filtered_servers','w')
	else:
		fw=open('filtered_servers_global','w')
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
		if tp.check_ping(s) and tp.check_tcpping(s) and ic.in_US(s,inUS_flag) and googleflag:
			if 'google' in s:
				google+=1
			counter+=1
			fw.write(s+'\n') # writing to file, if all conditions are satisfid

def top_n_plab(n):
	'''
	    from all_pl_nodes file, filter top n nodes and store them to 'servers_plab'
	'''
	f=open('all_pl_nodes','r')
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

#top_n_plab(60)
top_n_servers(100,False)