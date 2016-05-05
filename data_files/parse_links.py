import os
from test_pings import Test_pings
from ip_to_city import IP_to_Loc
'''
   Parser for Iplane dataset files
   generates:
             Any_vX_pairs  => list of node pairs
   and       Any_vX_nodelits => only node list
   where X is for version number
'''
class iplane_extract(object):
	def __init__(self):
		self.AS_IP_map={}
		self.direc='Iplane_files'

	def ip_to_pop_map(self,city): # crate hash table mapping 'as' pair to 'ip'
		f=open(self.direc+'inter_ip_links.txt','r')
		for line in f:
			lsplit=line.split()
			self.AS_IP_map[lsplit[1]+'_'+lsplit[3].strip('\n')]=lsplit[0]+'_'+lsplit[2]
		print "mapping_done",len(self.AS_IP_map.keys())

	def inter_pop_to_city(self,city):
		i=0
		f=open(self.direc+'inter_pop_links.txt','r')
		writer=open(city+'_pairs.txt','w')
		writer2=open(city+'_node_list','w')
		for line in f:
			lsplit=line.split() # got list in form of pop1,as1,pop,as2
			try:
				ip1=self.AS_IP_map[lsplit[1]+'_'+lsplit[3]].split('_')[0]
				ip2=self.AS_IP_map[lsplit[1]+'_'+lsplit[3]].split('_')[1]
			except:
				pass
			else:
				if i>=50:
					break;
				if lsplit[1] != lsplit[3]:  # checking if as1!=as2
					if ic.get_ip_to_city(ip1) == ic.get_ip_to_city(ip2) and ic.get_ip_to_city(ip2) is not None \
					   and tp.check_ping(ip1) and tp.check_ping(ip2) and tp.check_tcpping(ip1) \
					   and tp.check_tcpping(ip2) :
							city=ic.get_ip_to_city(ip1).encode('utf-8')
							if int(line.split(' ')[4]) > 1:
								i+=1
								writer.write(ip1+','+lsplit[1]+','+ip2+','+lsplit[3]+','+lsplit[0]+','+lsplit[2]+','+city+','+line.split()[4]+'\n')
								writer2.write(ip1+'\n'+ip2+'\n')
tp=Test_pings()
ic=IP_to_Loc()
extract=iplane_extract()
extract.ip_to_pop_map('Any_v4')
extract.inter_pop_to_city('Any_v4')