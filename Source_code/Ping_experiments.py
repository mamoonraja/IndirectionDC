import sys
import os
import glob
from helpers import Helpers
class Pinger(object): # Helper
	def __init__(self,Key,Username_PL,Username_DC):
		self.key=Key
		self.uname_pl=Username_PL
		self.uname_dc=Username_DC
		self.plab=Helpers(self.key,self.uname_pl) #call helpers for plab
		self.dcs=Helpers(self.key,self.uname_dc) #call helpers for dc

	def install_libs(self):
		self.plab.installer(open('active_nodes','r'))

	def get_files(self,direc,expnum,copyto):
		self.dcs.copy_from(direc,expnum,open('DC_list','r'),copyto)
		self.plab.copy_from(direc,expnum,open('active_nodes','r'),copyto)


	def run_dc_ping(self,direc,duration,expnum,f_dc,f_servers): #ping servers and plabs from DC
		for node in f_dc:
			self.ping_servers(direc,duration,expnum,str(node),open(f_servers,'r'))

	def ping_servers(self,direc,duration,expnum,node,f_s): #ping servers
			for server in f_s:
				self.dcs.do_ssh(node.split(',')[0],'mkdir '+direc+str(expnum))
				new_dir=direc+str(expnum)+'/'+node.split(',')[1]+'_'+server.strip('\n')
				self.dcs.do_ssh(node.split(',')[0],'mkdir '+new_dir)
				self.dcs.run_ping(new_dir,duration,server.split(',')[0].strip('\n'),node.split(',')[0],node.split(',')[1],expnum,'tcpping') 

	def run_pl_ping(self,direc,duration,expnum,f_pl,f_servers):  #ping DC and servers from pl pair, and ping between pl nodes
		for node in f_pl:
			self.plab.do_ssh(node.split(',')[0],'mkdir '+direc+str(expnum))
			self.plab.do_ssh(node.split(',')[2],'mkdir '+direc+str(expnum))
			self.pl_pinger(direc+str(expnum),duration,expnum,node.split(',')[0],node.split(',')[2],open(f_servers,'r'),expnum,'ping')
			self.plab.do_ssh(node.split(',')[0],'mkdir '+direc+str(expnum))
			new_dir=direc+str(expnum)+'/'+node.split(',')[0]+'_'+node.split(',')[2]
			self.plab.do_ssh(node.split(',')[0],'mkdir '+new_dir)
			self.plab.run_ping(new_dir,duration,node.split(',')[2],node.split(',')[0],node.split(',')[0],expnum,'ping')#ping other pl node 

	def pl_pinger(self,direc,duration,expnum,pl1,pl2,f_servers,exp_type,pingtype):
		for server in f_servers:
			new_dir=direc+'/'+pl1+'_'+server.strip('\n')
			self.plab.do_ssh(pl1,'mkdir '+new_dir)
			self.plab.run_ping(new_dir,duration,server.strip('\n'),pl1,pl1,expnum,pingtype)#2a 
			print server,pl2
			new_dir=direc+'/'+pl2+'_'+server.strip('\n')
			self.plab.do_ssh(pl2,'mkdir '+new_dir)
			self.plab.run_ping(new_dir,duration,server.strip('\n'),pl2,pl2,expnum,pingtype)#2b

