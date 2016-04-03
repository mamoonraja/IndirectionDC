import sys
import socket
import os
from Ping_experiments import Pinger

def run(direc,duration,expno,pinger,exptype):
	if exptype==1: #plab
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'active_nodes')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'Servers')
		pinger.run_pl_ping(direc,duration,expno,open('node_pairs','r'),'Servers')
	elif exptype==2: #large scale
		pinger.run_dc_ping(direc,duration,expno,open('DC_list_large_scale','r'),'active_nodes_2')
		pinger.run_dc_ping(direc,duration,expno,open('DC_list_large_scale','r'),'Servers_2') #plab nodes are servers here 
		pinger.run_dc_ping(direc,duration,expno,open('Servers_2','r'),'active_nodes_2') #using dc ping because we already have info for pairs

def main():
  pinger=Pinger('~/.ssh/mraja01_key','tufts_comp150_b','raja')
  direc='~/Mamoon'
  if int(sys.argv[1])==0: #get results
    pinger.get_files(direc,14,'Results')
  elif int(sys.argv[1])==1: # run
#   pinger.install_libs()
   run(direc,3600,15,pinger,int(sys.argv[2]))


main()
