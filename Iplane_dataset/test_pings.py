import os
import time
import paramiko
class Test_pings(object):
	def check_output_tcpping(self,ftcp):
		f2=open(ftcp,'r')
		for line in f2:
			if 'timeout' in line:
				return False
			else:
				return True

	def check_tcpping(self,node):
		os.system('tcpping -x 1 -w 1 ' + node + ' > result_tcpping') 
		return self.check_output_tcpping('result_tcpping')

	def check_ping(self,hostname):
	    response = os.system("ping -c 1 -W 1 " + hostname)
	    print response
	    if response == 0:
	        return True
	    else:
	        return False

	def check_ssh(self,hostname,user,key_file):
		print hostname
		import socket
		ip = socket.gethostbyname(hostname)
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			s.connect((ip, 22))
			s.close()
			print "yes"
			return True
		except socket.error as e:
			print "error"
			s.close()
			return False
