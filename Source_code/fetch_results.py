import os
import csv
import copy
import matplotlib.pyplot as plt
import numpy as np

'''
   Parse the results here using following method:
   		initialize  Initialize the experiments by walking through directory and parsing files one by one by calling parse_file
   		parse_file  Open log file and parse it
   		parse_ping  Parse simple pings
   		parse_tcpping Parse for TCP ping
   		partition_parsed_results  Partition all the results into more specific names
   		parse_pair   Parse pairs, for mobilIP comparison experiments
   		mobileIPstretch  Find sretch for mobileIP 
   		diff_in_keys     Check difference between node names, to filter out anything between same node names
   		IndirectionStretch  Finds IndirectionDC latency stretch
   		get_latency_stretch  helper function to get latency stretch
   		get_best_DC      returns the optimal datacenter to be used for source,destination pairs
   		get_min_DC       returns the nearest datacenter to source

'''
class Parsers(object):
	def __init__(self,folder,filelist):
		self.dc_serv={}  # store dc to server latencies in form on key value where key is of form 'DCnode_SERVERnode'
		self.dc_plab={}  # DC to Planet lab nodes latencies
		self.plab_serv={} 
		self.plab_plab={}
		self.mob_ls={} # to store mobilIP latency stretch
		self.ind_ls={} # to store IndirectionDC latency stretch
		self.results={} # store all latencies
		self.folder=folder # folder to fetch results from
		self.fw=open(folder+'/outliers.csv','w')
		self.fw.write('type,node,server,direct_path,node_to_dc,DC_to_server,stretch\n')
		self.fwi=open(folder+'/improved.csv','w')
		self.fwi.write('type,node,server,direct_path,node_to_dc,DC_to_server,stretch\n')		
		self.filelist=filelist 
		self.all=[]
		self.outliers=[]
		self.outliers_lat=[]
		self.improved=[]
		self.double_lat=[]

	def initialize(self,direc):
		dirs= os.walk('./'+direc+'/').next()[1]
		for elem in dirs:
			self.parse_file(elem+'/screenlog.0')


	def parse_file(self,datafile):
		try:
			f=open(self.folder+'/'+datafile,'r')
		except:
			print "EXCEPTION" , datafile.split('/')[0]
			self.results[datafile.split('/')[0]]=0
		else:
			for line in f:
				if "PING" in line:
					self.parse_ping(datafile)
					break
				else:
					self.parse_tcpping(datafile)
					break

	def parse_ping(self,datafile):
		f=open(self.folder+'/'+datafile,'r')
		for line in f:
			if "rtt" in line:
				self.results[datafile.split('/')[0].split(',')[0]]=line.split('/')[4]
				return 0

	def parse_tcpping(self,datafile):
		f=open(self.folder+'/'+datafile,'r')
		rtt=[]
		for line in f:
			if "timeout" in line:
				pass
			else :
				try:
					rtt.append(float(line.split(' ')[8]))
				except:
					try:
						rtt.append(float(line.split(' ')[7]))
					except:
							try:
	 							rtt.append(float(line.split(' ')[9]))
	 						except:
	 							pass
		try:
			self.results[datafile.split('/')[0].split(',')[0]]=str(float(sum(rtt)/len(rtt)))
		except:
			pass

	def partition_parsed_results(self):
		self.dc_serv=self.parse_pair(self.filelist[2],self.filelist[1])
		self.dc_plab=self.parse_pair(self.filelist[2],self.filelist[0])
		self.plab_serv=self.parse_pair(self.filelist[0],self.filelist[1])
		self.plab_plab=self.parse_pair(self.filelist[0],self.filelist[0])

	def parse_pair(self,first_file,second_file):
		out={}
		f1=open(first_file,'r')
		for line1 in f1:
			f2=open(second_file,'r')
			for line2 in f2:
				try:
					out[line1.split(',')[0].strip('\n')+'_'+line2.split(',')[0].strip('\n')]= \
					self.results[line1.split(',')[0].strip('\n')+'_'+line2.split(',')[0].strip('\n')]
				except:
					pass
		return out

	def mobilIPstretch(self,fl1,fl2):
		f1=open(fl1,'r')
		lat_stretch=[]
		for line1 in f1:
			f2=open(fl2,'r')
			try:
				pair_path=self.plab_plab[line1.split(',')[0]+'_'+line1.split(',')[2]]
			except:
				pair_path=self.plab_plab[line1.split(',')[2]+'_'+line1.split(',')[0]]			
			for line2 in f2:
				direct_path_1=self.plab_serv[line1.split(',')[0]+'_'+line2.strip('\n')]
				direct_path_2=self.plab_serv[line1.split(',')[2]+'_'+line2.strip('\n')]
				try:
					lat=(float(direct_path_1)+float(pair_path)) / float(direct_path_2)
				except:
					pass
				else:
					lat_stretch.append(lat)
				try:
					lat=(float(direct_path_2)+float(pair_path)) / float(direct_path_1)
				except:
					pass
				else:
					lat_stretch.append( lat )
#			print len(lat_stretch)
		f1.close()
		f2.close()
		return lat_stretch

	def diff_in_keys(self,k1,k2):
		import difflib
		S_r=difflib.SequenceMatcher(None,k1,k2).ratio()
		df=float((len(k1)-1))/float(len(k1))
		if S_r == df or S_r == df:
			return False
		return True

	def IndirectionStretch(self,fl1,fl2,fldc):
		f1=open(fl1,'r')
		lat_stretch_best=[]
		lat_stretch_nearest=[]
		for node1 in f1:
			f2=open(fl2,'r')
			try:
				[dc_path_from_src,dcnode1]=self.get_min_dc(fldc,node1.split(',')[0],self.dc_plab) # nearest DC from source
			except:
				pass
			else:
				for node2 in f2:
					n1=node1.split(',')[0].strip('\n\r')
					n2=node2.strip('\n\r')
					try:
						[dc_path_from_dst,dcnode2]=self.get_min_dc(fldc,node2.split(',')[0],self.dc_serv) # nearest DC from dest	
					except:
						pass
					else:
						l2=self.get_latency_stretch(n1,n2,dc_path_from_src,dcnode1,False) # nearest to source
						if l2!="NA":
							lat_stretch_nearest.append(l2)
					try:
						[dc_path,dcnode]=self.get_best_dc(dc_path_from_dst,dc_path_from_src,dcnode1,dcnode2)	
					except:
						pass
					else:
						l1=self.get_latency_stretch(n1,n2,dc_path,dcnode,True) # best dc
						if l1!="NA":
							lat_stretch_best.append(l1)
#		print "lens ",len(lat_stretch_best),len(lat_stretch_nearest)
		return [lat_stretch_best,lat_stretch_nearest]

	def get_latency_stretch(self,n1,n2,dc_path,dcnode,record_anom):
		lat_stretch=[]
		if n1 != n2 and self.diff_in_keys(n1,n2):
			try:
				direct_path=self.plab_serv[n1+'_'+n2]
			except:
				return "NA"
			try:
				dc_serv= self.dc_serv[dcnode+'_'+n2]
			except:
				return "NA"
			try:
				lat=(float(dc_path)+float(dc_serv) ) / float(direct_path)
			except:
				pass
			else:
#				lat_stretch.append(lat)
				if record_anom:
					self.all.append(float(direct_path))
					if lat>5: #storing outliers
						self.outliers.append(float(direct_path))
						self.outliers_lat.append(float(float(dc_path)+float(dc_serv)))
						self.fw.write('IndirectionDC,'+n1+','+n2+','+str(direct_path)+ \
							','+str(dc_path)+','+str(dc_serv)+','+str(lat)+'\n')
					if lat>2: #when stretch>2
						self.double_lat.append(float(float(dc_path)+float(dc_serv)))
					if lat<=1:
						self.improved.append(float(direct_path))
						self.fwi.write('IndirectionDC,'+n1+','+n2+','+str(direct_path)+ \
							','+str(dc_path)+','+str(dc_serv)+','+str(lat)+'\n')
				return lat

	def get_best_dc(self,p1,p2,n1,n2):
		if p1<p2:
			return p1,n1
		else:
			return p2,n2

	def get_min_dc(self, filedc, node,src_dest):
		f=open(filedc,'r')
		lats=[]
		nodes=[]
		for line in f:
			try:
				lats.append(src_dest[line.split(',')[0]+'_'+node.strip('\n\r')])
				nodes.append(line.split(',')[0])
			except:
				pass
		return min(lats),nodes[lats.index(min(lats))]

	def filterlist(self,lst,latency):
			return [s for s in lst if s < latency]

	def compare_outliers(self):
		colors = ['red', 'tan', 'lime']
		a = [self.filterlist(self.outliers,200),self.filterlist(self.improved,200),self.filterlist(self.all,200)]
		self.plot_hist(a,['Outliers','Latency stretch less than 1','All'],'Latency (ms)' \
			,colors,'Direct route latencies for different scenarios')
		self.plot_hist(self.double_lat,'Latency stretch greater than 2','Latency (ms)'\
			,'red','InDirect route latencies Outliers')

	def plot_cdf(self,datas,labels,xl):
		linestyles = ['-', '--', '-.', ':']
		ind=0
		for data in datas:
			data_sorted = np.sort(data)
			p = 1. * np.arange(len(data)) / (len(data) - 1)
			plt.plot(data_sorted,p,label=labels[ind],linestyle=linestyles[ind],linewidth=3)
			plt.xscale("log", nonposx='clip')
			ind+=1
			plt.hold(True)
			plt.grid(True)
		plt.legend(loc=4)
		plt.title('Latency stretch using Indirection', fontsize=14)
		plt.xlabel(xl,fontsize=14)
		plt.ylabel('CDF',fontsize=14)
		plt.show()

	def plot_hist(self,datas,labels,xl,colors,figtitle):
		n_bins = 20
		plt.hist(datas, n_bins,normed=1,histtype='bar', color=colors, label=labels)
		plt.legend(prop={'size': 10})
		plt.title(figtitle,fontsize=14)
		plt.xlabel(xl,fontsize =14)
		plt.ylabel('Normalized Frequency',fontsize=14)
		plt.show()