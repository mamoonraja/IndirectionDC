import os
import csv
import copy
import matplotlib.pyplot as plt
import numpy as np

class Parsers(object):
	def __init__(self):
		self.dc_serv={}
		self.dc_plab={}
		self.plab_serv={}
		self.plab_plab={}

	def parse_file(self,datafile):
		try:
			f=open(datafile,'r')
		except:
			print "EXCEPTION" , datafile.split('/')[0]
			results[datafile.split('/')[0]]=0
		else:
			for line in f:
				if "PING" in line:
					self.parse_ping(datafile)
					break
				else:
					self.parse_tcpping(datafile)
					break

	def parse_ping(self,datafile):
		f=open(datafile,'r')
		for line in f:
			if "rtt" in line:
				results[datafile.split('/')[0].split(',')[0]]=line.split('/')[4]
				return 0
		results[datafile.split('/')[0].split(',')[0]]=0

	def parse_tcpping(self,datafile):
		f=open(datafile,'r')
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
			results[datafile.split('/')[0].split(',')[0]]=str(float(sum(rtt)/len(rtt)))
		except:
			results[datafile.split('/')[0].split(',')[0]]=str(000)

	def partition_parsed_results(self):
		print results
		self.dc_serv=self.parse_pair('./../DC_list_2','./../Servers')
		self.dc_plab=self.parse_pair('./../DC_list_2','./../active_nodes')
		self.plab_serv=self.parse_pair('./../active_nodes','./../Servers')
		self.plab_plab=self.parse_pair('./../active_nodes','./../active_nodes')

	def parse_pair(self,first_file,second_file):
		print first_file,second_file
		out={}
		f1=open(first_file,'r')
		for line1 in f1:
			f2=open(second_file,'r')
			for line2 in f2:
				print line1 , line2
				try:
					out[line1.split(',')[0].strip('\n')+'_'+line2.split(',')[0].strip('\n')]= \
					results[line1.split(',')[0].strip('\n')+'_'+line2.split(',')[0].strip('\n')]
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
					lat_stretch.append((float(direct_path_1)+float(pair_path)) / float(direct_path_2) )
				except:
					pass
				try:
					lat_stretch.append((float(direct_path_2)+float(pair_path)) / float(direct_path_1) )
				except:
					pass
			print len(lat_stretch)
		return lat_stretch

	def IndirectionStretch(self):
		pass

	def plot_cdf(self,data):
		print data
		data_sorted = np.sort(data)
		print "sorted",data
		# calculate the proportional values of samples
		p = 1. * np.arange(len(data)) / (len(data) - 1)
		# plot the sorted data:
		plt.plot(data_sorted,p,label='ls')
		plt.legend()
		plt.show()

parser=Parsers()
results={}
dirs= os.walk('./').next()[1]
for elem in dirs:
	parser.parse_file(elem+'/screenlog.0')
parser.partition_parsed_results()
parser.plab_plab['planetlab3.eecs.umich.edu_planetlab1.emich.edu']=1.47
parser.plab_serv['planetlab1.emich.edu_imgur.com']=6.47
ls=parser.mobilIPstretch('./../node_pairs','./../Servers')
parser.IndirectionStretch()
# add processing
print len(parser.plab_plab)
print parser.plab_plab
print len(parser.plab_serv)
print len(ls)
parser.plot_cdf(ls)