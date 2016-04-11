import sys
import socket
import os
from Ping_experiments import Pinger
from fetch_results import Parsers
''' from command line run:
	python 'main.py 1 X' to run experiment 'X'
	python 'main.py 0 X'   to copy files
'''

def run(direc,duration,expno,pinger,exptype):
	if exptype==1: #plab-mobilIP-indirectio
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'active_nodes')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'filtered_servers')
		pinger.run_pl_ping(direc,duration,expno,open('node_pairs','r'),'filtered_servers',exptype)
	elif exptype==2: #large scale
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'Any_v3_node_list') #dc to nodes from iplane dataset
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab') #fromdc, plab nodes are servers here 
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'Any_v3_node_list',exptype) 
	elif exptype==3: #plab-plab just Indirection
		# need just two runs for theis, DC to Plab or plab to dc, and plab to plabservers
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab')
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'servers_plab',exptype)
	elif exptype==4: #plab-servers just Indirection
		# need 3 runs for this, DC to servers, DC to Plab (can use prev ones), and plab to servers
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'filtered_servers')
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'filtered_servers',exptype)

def install_on_new():
	pinger=Pinger('~/.ssh/mraja01_key','tufts_comp150_b','raja')
	pinger.install_libs('servers_plab','screen') # not scalable right now, IMPROVE , 'use uname to find dist and then install'
#	pinger.install_libs('servers_plab',Pinger.dcs)

def get_results(direc):
	fw=open(direc+'/outliers.csv','w')
	fw.write('type,node,server,direct_path,node_to_dc,DC_to_server,stretch\n')
	parser=Parsers(direc,fw)
	results={}
	dirs= os.walk('./'+direc+'/').next()[1]
	for elem in dirs:
		parser.parse_file(elem+'/screenlog.0')
	parser.partition_parsed_results()
	parser.plab_plab['planetlab1.emich.edu_planetlab3.eecs.umich.edu']=1.47
	ls1=parser.mobilIPstretch('./node_pairs','./filtered_servers')
	ls2=parser.IndirectionStretch('./active_nodes','./filtered_servers','./DC_list')
	# add processing 
	print max(ls1)
	print max(ls2)
	parser.plot_cdf(ls1,ls2)


def main(runexp,exptype):
	pinger=Pinger('~/.ssh/mraja01_key','tufts_comp150_b','raja')
	direc='~/Mamoon' #directory at remote host, saved as Mamoon+expno
	if runexp==0: #get results
		expno=29
		os.system('mkdir Results'+str(expno))
		if exptype==1:
			pinger.get_files(direc,expno,'Results'+str(expno),'DC_list','active_nodes') # 23 was last legit fo pl nodes
		else:
			pinger.get_files(direc,expno,'Results'+str(expno),'DC_list','servers_plab') # 23 was last legit fo pl nodes
	elif runexp==1: # run
		#   pinger.install_libs()
		run(direc,3600,30,pinger,exptype)
	elif runexp==2: #fetch_results
		get_results('Results'+str(23))
#23 1st
#26 2nd
#30 3rd type
#29 4th
#install_on_new()
main(int(sys.argv[1]),int(sys.argv[2]))