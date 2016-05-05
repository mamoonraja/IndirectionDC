import sys
import socket
import os
from Ping_experiments import Pinger
from fetch_results import Parsers

''' From command line run:
	'python main.py X Y Z' to do task X for experiment type Y
	X : 0-2
		0, get results from remote hosts
		1, run experiments
		2, parse the results and plot results
	Y:  1-4
		1, From PlabNodes(pairs) to DCs to Servers , both mobilIP & indirection
		2, large scale experiments, From IplaneNodes to DCs to PlabNodes(As Servers) , both MobilIP & Indirection
		3, From PlabNodes to DCs to PlabNodes(asServers)  , just Indirection
		4, From PlabNodes to DCs to ServerList,             Just Indirection
	Z:  Experiment Number

    *** Current experiments info:
    Experiment Number      Experiment Type
		35					1st
		33 					2nd
		31 					3rd type
		32 					4th Local

	*** For new experiment assign new experiemnt number and store it in table above for future reference
	*** Currently I have results for type 1,3 and type 4, stll need to figure some details about type 2

	NOTE : For future experiment, I will change naming methods, use experiment name instead of exp number
	       After that there will be no need of providing both number and type 

'''

def run(direc,duration,expno,pinger,exptype):
	if exptype==1: #plab-mobilIP-indirectio
		pinger.run_dc_ping(direc,duration,expno,open('DC_list_new','r'),'active_nodes')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list_new','r'),'filtered_servers')
		pinger.run_pl_ping(direc,duration,expno,open('node_pairs','r'),'filtered_servers',exptype)
	elif exptype==2: #large scale
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'Any_v3_node_list') #dc to nodes from iplane dataset
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab') #fromdc, plab nodes are servers here 
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'Any_v3_node_list',exptype) 
	elif exptype==3: #plab-plab just Indirection
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab')
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'servers_plab',exptype)
	elif exptype==4: #plab-servers just Indirection
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'servers_plab')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'filtered_servers_global')
		pinger.run_pl_ping(direc,duration,expno,open('servers_plab','r'),'filtered_servers_global',exptype)

def install_on_new():
	pinger=Pinger('~/.ssh/mraja01_key','tufts_comp150_b','raja')
	pinger.install_libs('servers_plab','screen') # not scalable right now, IMPROVE , 'use uname to find dist and then install'

def GET_logs(expno,exptype,direc,fdc,fs,fnodes,pinger):
	os.system('mkdir Results'+str(expno))
	if exptype==1:
		pinger.get_files(direc,expno,'Results'+str(expno),fdc,fnodes) 
	else:
		pinger.get_files(direc,expno,'Results'+str(expno),fdc,fs) 

def parse_results(exptype,direc,f1,f2,f3,f4):
	parser=Parsers(direc,[f1,f2,f3,f4])
	parser.initialize(direc)
	parser.partition_parsed_results()
	labels=[]
	ls=[]
	if exptype<3: # need mobilIP for exptype < 3
		ls.append(parser.mobilIPstretch(f4,f2))
		labels.append('mobileIP')
	[ls1,ls2]=parser.IndirectionStretch(f1,f2,f3)
	labels.append('IndirectionDC_best')
	labels.append('IndirectionDC_nearest')
	ls.append(ls1)
	ls.append(ls2)
	parser.plot_cdf(ls,labels,'Latency Stretch')
	parser.compare_outliers()


def main(runexp,exptype,expno):
	pinger=Pinger('~/.ssh/mraja01_key','tufts_comp150_b','raja')
	direc='~/Mamoon' #directory at remote host, saved as Mamoon+expno
	if runexp==0: #GET results
	    GET_logs(expno,exptype,direc,'DC_list_new','active_nodes','servers_plab',pinger)
	elif runexp==1: #run
		#   pinger.install_libs()
		run(direc,3600,expno,pinger,exptype)
	elif runexp==2: #parse_results
		expno=str(expno)
		if exptype==1:
			parse_results(exptype,'Results'+expno,'./active_nodes','./filtered_servers','./DC_list','./node_pairs')
		elif exptype==2:
			parse_results(exptype,'Results'+expno,'./active_nodes','./filtered_servers','./DC_list','./node_pairs')
		elif exptype==3:
			parse_results(exptype,'Results'+expno,'servers_plab','./servers_plab','./DC_list','')
		elif exptype==4:
			parse_results(exptype,'Results'+expno,'servers_plab','./filtered_servers','./DC_list','')


main(int(sys.argv[1]),int(sys.argv[2]),int(sys.argv[3]))
#install_on_new()