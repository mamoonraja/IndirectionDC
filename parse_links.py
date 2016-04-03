import geoip2.database
class iplane_extract(object):
	def __init__(self):
		AS_IP_MAP={}

	def check_ping(self,hostname):
	    response = os.system("ping -c 1" + hostname)
	    print response
	    if response == 0:
	        print "true"
	        return True
	    else:
	        return False

	def get_ip_to_city(self,ip):
		reader = geoip2.database.Reader('GeoLite2-City.mmdb')
		try:
			response = reader.city(ip)
		except:
			reader.close()
			return None
		reader.close()
		if response.country.name == 'United States':
			return response.city.name
		else:
			return None

	def test_get_city(self,testfile):
		f=open(testfile,'r')
		for line in f:
			print self.get_ip_to_city(line.split(',')[1].strip('\n'))

	def ip_to_pop_map(self,city):
		f=open('ip_to_pop_mapping.txt','r')
		counter=0
		for line in f:
			self.AS_IP_map[line.split(' ')[1].strip('\n')]=[line.split(' ')[0]]
		print "mapping_done",len(self.AS_IP_map.keys())

	def inter_pop_to_city(self,city,ip_map):
		f=open('inter_pop_links.txt','r')
		writer=open(city+'_pairs.txt','w')
		for line in f:
			as1=line.split(' ')[1]
			as2=line.split(' ')[3]
			pop1=line.split(' ')[0]
			pop2=line.split(' ')[2]
			try:
				ip1=ip_map[pop1]
				ip2=ip_map[pop2]
			except:
				pass
			else:
				if as1 != as2:
					if self.get_ip_to_city(ip1[0]) == self.get_ip_to_city(ip2[0]) and self.get_ip_to_city(ip2[0]) is not None:
						city=self.get_ip_to_city(ip1[0]).encode('utf-8')
						if int(line.split(' ')[4]) > 0:
							writer.write(ip1[0]+' '+as1+' '+pop1+' '+ip2[0]+' '+as2+' '+pop2+' '+city+' '+line.split(' ')[4])

extract=iplane_extract()
#parser.test_get_city('test_cities')
extract.ip_to_pop_map('Any')
extract.inter_pop_to_city('Any')