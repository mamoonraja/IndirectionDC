import sys
import socket
import os
from Ping_experiments import Pinger
def run(direc,duration,expno):
	pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'active_nodes')
	pinger.run_dc_ping(direc,duration,expno,open('DC_list','r'),'Servers')
	pinger.run_pl_ping(direc,duration,expno,open('node_pairs','r'),'Servers')

def main():
  pinger=Pinger('~/.ssh/mraja01_key','tufts_dogar','raja')
  direc='~/Mamoon'
  pinger.install_libs()
  if int(argv[1])==0:
    pinger.get_files(direc,10,'Results')
  else:
    run('~/Mamoon',3600,11)


main()
