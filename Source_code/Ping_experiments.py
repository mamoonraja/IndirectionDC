import sys
import os
import glob
from helpers import Helpers

'''
    Class Pinger to Ping from hosts to servers for latency experiments, using following methods
	    install_libs
	    get_files
	    run_dc_ping
	    ping_servers
	    run_pl_ping    

'''
class Pinger(object): 
	def __init__(self,Key,Username_PL,Username_DC):
		self.key=Key
		self.uname_pl=Username_PL #planet lab username
		self.uname_dc=Username_DC #datacenter username
		self.plab=Helpers(self.key,self.uname_pl) #call helpers for plab
		self.dcs=Helpers(self.key,self.uname_dc) #call helpers for dc

	def install_libs(self,fname,toinstall):
		f=open(fname,'r')
		for node in f:
			print node
#			self.plab.do_ssh(node.split(',')[0].strip('\n\r'),'sudo apt-get install '+toinstall) #automate this, decide ase on os			
			self.plab.do_ssh(node.split(',')[0].strip('\n\r'),'sudo yum update ; sudo yum  -y -t --nogpgcheck install '+toinstall)

	def get_files(self,direc,expnum,copyto,f1,f2):
		self.dcs.copy_from(direc,expnum,open(f1,'r'),copyto)
		self.plab.copy_from(direc,expnum,open(f2,'r'),copyto)

	def run_dc_ping(self,direc,duration,expnum,f_dc,f_servers): #ping servers and plabs from DC
		for node in f_dc:
			self.ping_servers(direc,duration,expnum,node.split(',')[0].strip('\r\n'),f_servers,'tcpping',self.dcs)

	def ping_servers(self,direc,duration,expnum,node,f_s,pingtype,node_obj): #ping servers
			print node,direc,expnum,f_s
			direc=direc+str(expnum)
			node_obj.do_ssh(node,'mkdir '+direc) # making dir at host
			node_obj.do_scp(node,f_s,direc) # copying files to host
			node_obj.do_scp(node,'batch_ping.py',direc)
			node_obj.do_ssh(node,'python '+direc+'/batch_ping.py '+ \
				node+' '+f_s+' '+str(expnum)+' '+direc+' '+str(duration)+' '+pingtype)

	def run_pl_ping(self,direc,duration,expnum,f_pl,f_servers,exptype):  #ping DC and servers from pl pair, and ping between pl nodes
		for node in f_pl:
			print node
			self.ping_servers(direc,duration,expnum,node.split(',')[0].strip('\r\n'),f_servers,'ping',self.plab)
			if exptype ==1:
				self.ping_servers(direc,duration,expnum,node.split(',')[2],f_servers,'ping',self.plab)
				new_dir=direc+str(expnum)+'/'+node.split(',')[0]+'_'+node.split(',')[2]
				self.plab.do_ssh(node.split(',')[0],'mkdir '+new_dir)
				self.plab.run_ping(new_dir,duration,node.split(',')[2],node.split(',')[0], \
				  node.split(',')[0],expnum,'ping')#ping other pl node 