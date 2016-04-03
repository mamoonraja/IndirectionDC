import matplotlib.pyplot as plt
import numpy as np

def read_contents(fname):
	f=open(fname,'r')
	dat=[]
	for line in f:
		dat.append(line.strip('\n').split('\t'))
	return dat
#files=['MobileIP','Indirection using Central DC','Indirection using nearest DC']
files=['Home_MobileIP','Home_Indirection using DC']
for fname in files:
	data = read_contents(fname)
	data = [float(item) for sublist in data for item in sublist]
	data_sorted = np.sort(data)
	print "sorted",data
	# calculate the proportional values of samples
	p = 1. * np.arange(len(data)) / (len(data) - 1)

	# plot the sorted data:
	plt.plot(data_sorted,p,label=fname)
	plt.legend()
	plt.hold
plt.xlabel('latency stretch')
plt.ylabel('cdf')
plt.show()