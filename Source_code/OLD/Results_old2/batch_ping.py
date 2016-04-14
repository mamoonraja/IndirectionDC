import os
import sys
def batch_ping (node,servers_list,expnum,direc,duration,pingtype):
	f=open(direc+'/'+servers_list,'r')
	for server in f:
		serv=server.strip('\n')
		new_dir=direc+'/'+node+'_'+serv
		os.system('mkdir '+new_dir)
		if pingtype == 'tcpping':
			os.system('(cd '+new_dir+' ; screen -S '+serv+node+' -d -m -L sudo timeout '+str(duration)+'s '+pingtype+' '+serv+' )')
		elif pingtype == 'ping':
			os.system('(cd '+new_dir+' ; screen -S '+serv+node+' -d -m -L sudo '+pingtype+' -c '+ str(duration) +' '+serv+' )')

batch_ping(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5],sys.argv[6])