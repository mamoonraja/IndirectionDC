import socket

#takes hostname and run ping tests on it
def check_ping(hostname):
    response = os.system("ping -c 5 " + hostname)
    print response
    if response == 0:
        print "true"
        return True
    else:
        return False

#takes ip and check if IP is legal
def check_legal(ip1):
  try:
      socket.inet_aton(ip1)
  except socket.error:
      return False
  return True

#filter dpip-city dataset for specified cities 
def filter_node_list(fname):
  cities=['New York','Los Angeles']
  for city in cities:
    fr=open(fname,'r')
    fw=open('./Nodes/'+city+'_nodes','w')
    for line in fr:
      if city in line.strip('\n') and check_legal(line.split(',')[0].strip('"')):
          fw.write(line)

def get_city_list():
  filter_node_list('dbip-city.csv')

get_city_list()
