import geoip2.database
import socket

class IP_to_Loc(object):
	def get_ip_to_city(self,ip): # for eery ip returns city name if city is in US, None if not in US or can not resole ip to city
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

	def in_US(self,webadr): # takes hostname, converts to ip and return True if in US
		addr = socket.gethostbyname(webadr)
		reader = geoip2.database.Reader('GeoLite2-City.mmdb')
		try:
			response = reader.city(addr)
		except:
			reader.close()
			return False
		reader.close()
		print response.country.name		
		if response.country.name == 'United States':
			return True
		else:
			return False

	def test_get_city(self,testfile): # testing ip_to_city
		f=open(testfile,'r')
		for line in f:
			print self.get_ip_to_city(line.split(',')[1].strip('\n'))