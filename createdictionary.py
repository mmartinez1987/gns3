from open_terminals import portscan
from gethostnames import get_hostnames

#create dictionary file for each router
def create_dictionary():
	ports = portscan()
	hostnames = get_hostnames(ports)
	for x in range(0, len(ports)):
		hostname = str(hostnames[x])
		port = str(ports[x])
		list = {"hostname":"%s" % hostname, "port":"%s" % port}
		f = open('routers_dict.txt', 'a')
		f.write(str(list))
		print('Dictionary for %s created' % hostnames[x])
		f.close()
		

def main():
	create_dictionary()

if __name__ == '__main__':
	main()
