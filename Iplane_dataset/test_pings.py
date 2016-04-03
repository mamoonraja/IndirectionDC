import os
import time

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
	        print "true"
	        return True
	    else:
	        return False