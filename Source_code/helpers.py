import sys
import os
import glob

class Helpers(object): # Helper
	def __init__(self,Key,Username):
		self.key=Key
		self.uname=Username

	def do_ssh(self,node,cmnd):
		op=os.system('''echo Y | ssh -o "StrictHostKeyChecking no" -l '''+self.uname+''' -i '''+self.key+''' '''+str(node)+''' ' '''+str(cmnd)+''' ' ''')

	def do_scp(self,node,src,dest):
		os.system('scp -i '+self.key+' '+src+' '+self.uname+'@'+node+':'+dest)

	def get_scp(self,node,src,dest):
		os.system('scp -r -i '+self.key+' '+self.uname+'@'+node+':'+src+' '+dest)

	def make_exp_dir(self,to_,from_,direc,output_file):  # make experiment directory at remote host (_to here)
		os.system('''ssh -o "StrictHostKeyChecking no" -l '''+self.uname+''' -i '''+self.key+''' '''+to_+''' 'screen -S mrecv'''+str(2)+''' -d -m nohup mkdir '''+direc+'''_'''+from_+'''_'''+to_+''' ' ''')

	def copy_files(self,hostname,pathto,pathfrom):  # copy source files to experiment directory at remote host
		os.system('''scp -i '''+self.key+''' '''+pathfrom+''' '''+self.uname+'''@'''+hostname+''':'''+pathto+'''/''')

	def run_code(self,hostname,sendto,direc,port,source_file,exp_num,duration): # run source code at remote host
		os.system('''ssh  -o "StrictHostKeyChecking no" -l '''+self.uname+''' -i '''+self.key+ ''' '''+hostname+''' 'screen -S experiment'''+str(exp_num)+''' -d -m nohup sudo python '''+direc+'''/'''+source_file+''' '''+str(port)+''' '''+sendto+''' '''+str(duration)+''' '''+direc+'''/'''+sendto+'''_'''+hostname+'''_'''+str(exp_num)+''' ' ''')

	def run_simple(self,port,expnum,direc,pl_node_file): # run receiver _ sender pair here, dc nodes are already running
		f = open(active_nodes, 'r')# get these old results by using PL_LINK_INFO_OLD file
		ind=0
		for line in f:
			line=line.strip("\n")
			for line2 in f:
				line2=line2.strip("\n")
				if line!=line2:
					self.make_exp_dir(line2,line1,direc)
					self.copy_files(line2,'udp_rec.py',direc)
					self.run_code(line2,'NA',direc,port,'udp_rec.py',expnum)
					self.make_exp_dir(line,direc)
					self.copy_files(line,'~/interDC/udp_exp/working/udp_send_nr.py',direc)	
					self.run_code(line,line2,direc,port,'udp_send.py',expnum)
				port=port+1
				print port

	def run_dc(self,port,direc,expnum):
		f=open('DC_list','r')
		for node in f:
			self.copy_files(node.split(',')[0],direc,'udp_dc.py')
			self.run_code(node.split(',')[0],direc+expnum,direc,port,'udp_dc.py',0,0) 

	def run_ping(self,direc,duration,server,hostname,hostlocation,expnum,pingtype):
		if pingtype is 'tcpping':
			os.system('''ssh  -o "StrictHostKeyChecking no" -l '''+self.uname+''' -i '''+self.key+''' '''+hostname+''' '(cd  '''+direc+''' ; screen -S '''+server+hostname+''' -d -m -L sudo timeout '''+str(duration)+'''s '''+pingtype+''' '''+server+''' )' ''')
		elif pingtype is 'ping':
			os.system('''ssh  -o "StrictHostKeyChecking no" -l '''+self.uname+''' -i '''+self.key+''' '''+hostname+''' '(cd '''+direc+''' ; screen -S '''+server+hostname+''' -d -m -L sudo '''+pingtype+''' -c 1000 '''+server+''' )' ''')
		
	def installer(self,node_file):
		for node in node_file:
			print node
			node=node.split(',')[0].strip('\n\r')
			self.do_ssh(node,'mkdir Mamoon')
			self.do_scp(node,'install_libraries','~/Mamoon/')
			self.do_ssh(node,'chmod 755 ~/Mamoon/install_libraries')
			self.do_ssh(node,'~/Mamoon/install_libraries')

	def copy_from(self,direc,expnum,f_disc,copyto):
		for node in f_disc:
			self.get_scp(node.split(',')[0].strip('\n\r'),direc+str(expnum)+'/*',copyto)
