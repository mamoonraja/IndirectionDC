import geoip2.database
import socket

'''
   used to conevrt IP to location
'''
db_file='GeoLite_db_file/GeoLite2-City.mmdb'
class IP_to_Loc(object):
	def get_ip_to_city(self,ip): # for any ip returns city name if city is in US, None if not in US or can not resole ip to city
		reader = geoip2.database.Reader(db_file)
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

	def in_US(self,webadr,Flag): # takes hostname, converts to ip and return True if in US, if flag is false no need to check for US
		if Flag:
			try:
				addr = socket.gethostbyname(webadr)
			except:
				return False
			reader = geoip2.database.Reader(db_file)
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
		else:
			return True

	def test_get_city(self,testfile): # testing ip_to_city
		f=open(testfile,'r')
		for line in f:
			print self.get_ip_to_city(line.split(',')[1].strip('\n'))