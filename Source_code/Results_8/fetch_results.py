import os
import csv
import copy
class Parsers(object):
	def __init__(self):
		pass

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
				results[datafile.split('/')[0]]=line.split('/')[4]
				return 0
		results[datafile.split('/')[0]]=0

	def parse_tcpping(self,datafile): #fw is file object
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
							rtt.append(float(line.split(' ')[9]))
		try:
			results[datafile.split('/')[0]]=str(float(sum(rtt)/len(rtt)))
		except:
			results[datafile.split('/')[0]]=str(000)

	def parse_result_file(self,results):
		csvw=open('All_results.csv','wb')
		csvw.write('\n'+'DC_list_Servers'+'\n')
		self.parse_pair('./../DC_list_2','./../Servers','single',True,csvw,results)
		csvw.write('\n'+'Plab_Servers'+'\n')
		self.parse_pair('./../active_nodes','./../Servers','single',True,csvw,results)
		csvw.write('\n'+'DC_PL'+'\n')
		self.parse_pair('./../DC_list_2','./../active_nodes','single',False,csvw,results)
		csvw.write('\n'+'PL_pairs'+'\n')
		self.parse_pair('./../DC_list_2','./../node_pairs','pairs',True,csvw,results)

	def parse_pair(self,first_file,second_file,kind,splt,cw,results):
	# cw is csv writer,split defines whether we need to split node name
	# needed that for dc_plnode
		if kind is "single":
			top_row=self.get_list(open(second_file,'r'),0)
			cw.write(top_row+'\n')
			self.put_in_file(first_file,second_file,cw,splt)
		
		if kind is "pairs":
			trow=self.get_list(open(second_file,'r'),2)
			cols=self.get_list(open(second_file,'r'),0)
			cw.write(trow+'\n')
			self.put_in_file(cols.split(','),trow.split(','),cw,splt)

	def get_list(self,fobj,position):
		trow=' , '
		for elem in fobj:
				trow=trow+','+elem.split(',')[position].strip('\n')
		return trow

	def put_in_file(self,f1,f2,cw,splt):
			s=''
			try:
				f1obj=open(f1,'r')
			except:
				f1obj=f1
			for elem1 in f1obj:
				self.put_collumns(elem1,f2,cw,splt,s)
	
	def put_collumns(self,elem1,f2,cw,splt,s):
			try:
				f2obj=open(f2,'r')
			except:
				f2obj=f2
			for elem2 in f2obj:
				if splt:
					try:
						s=s+','+str(results[elem1.split(',')[0].strip('\n')+'_'+elem2.split(',')[0].strip('\n')])
					except:
						pass
				else:
					try:	
						#print elem1.split(',')[0].strip('\n')+'_'+elem2.strip('\n') 	
						s=s+','+str(results[elem1.split(',')[0].strip('\n')+'_'+elem2.strip('\n')])
					except:
						pass
			cw.write(elem1.split(',')[0]+','+s+'\n')

parser=Parsers()
results={}
dirs= os.walk('./').next()[1]
for elem in dirs:
	parser.parse_file(elem+'/screenlog.0')
parser.parse_result_file(results)
