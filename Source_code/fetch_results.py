import os
import csv
import copy
import matplotlib.pyplot as plt
import numpy as np
class Parsers(object):
	def __init__(self,folder,writer):
		self.dc_serv={}
		self.dc_plab={}
		self.plab_serv={}
		self.plab_plab={}
		self.mob_ls={}
		self.ind_ls={}
		self.results={}
		self.folder=folder
		self.fw=writer

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
		self.results[datafile.split('/')[0].split(',')[0]]=0

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
			self.results[datafile.split('/')[0].split(',')[0]]=str(000)

	def partition_parsed_results(self):
		self.dc_serv=self.parse_pair('./DC_list','./filtered_servers')
		self.dc_plab=self.parse_pair('./DC_list','./active_nodes')
		self.plab_serv=self.parse_pair('./active_nodes','./filtered_servers')
		self.plab_plab=self.parse_pair('./active_nodes','./active_nodes')

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
			print len(lat_stretch)
		f1.close()
		f2.close()
		return lat_stretch

	def IndirectionStretch(self,fl1,fl2,fldc):
		f1=open(fl1,'r')
		lat_stretch=[]
		for line1 in f1:
			f2=open(fl2,'r')
			[dc_path,dcnode]=self.get_min_dc(fldc,line1.split(',')[0])
			for line2 in f2:
				direct_path=self.plab_serv[line1.split(',')[0]+'_'+line2.strip('\n')]
				dc_serv= self.dc_serv[dcnode+'_'+line2.strip('\n')]
				try:
					lat=(float(dc_path)+float(dc_serv) ) / float(direct_path)
				except:
					pass
				else:
					lat_stretch.append(lat)
					if lat>40:
						self.fw.write('IndirectionDC,'+line1.split(',')[0]+','+line2.strip('\n')+','+str(direct_path)+ \
							','+str(dc_path)+','+str(dc_serv)+','+str(lat)+'\n')
		return lat_stretch

	def get_min_dc(self, filedc, node):
		f=open(filedc,'r')
		lats=[]
		nodes=[]
		for line in f:
			lats.append(self.dc_plab[line.split(',')[0]+'_'+node])
			nodes.append(line.split(',')[0])
		return min(lats),nodes[lats.index(min(lats))]

	def plot_cdf(self,data1,data2):
		print len(data1),len(data2)
		data_sorted1 = np.sort(data1)
		data_sorted2 = np.sort(data2)
		# calculate the proportional values of samples
		p = 1. * np.arange(len(data1)) / (len(data1) - 1)
		p = 1. * np.arange(len(data2)) / (len(data2) - 1)
		# plot the sorted data:
		plt.plot(data_sorted1,p,label='mobileIP')
		plt.plot(data_sorted2,p,label='IndirectionDC')
		plt.legend()
		plt.hold()
		plt.xlabel('latency stretch')
		plt.ylabel('cdf')
		plt.show()
