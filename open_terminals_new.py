import subprocess
import socket
import telnetlib
import time

class host(object):

	def __init__(self, host):
		self.host = host
		self.ports = []
		self.hostnames = []
		self.routers_list = []

	def portscan(self): # Method to scan check for open ports on localhost
		self.ports = []
		for port in range(2100,2200): # TCP Port scan port range 2100-200	    
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instantiate sock as object as IPv4 socket
			result = sock.connect_ex((self.host, port)) #bind destination host IPv4 address to port
			if result == 0: #if connection is successful then
				print('Adding port') #lets me know that this if statement is being executed
				self.ports.append(port) #append variable port to ports 
			sock.close()
		return self.ports
		

	def get_hostnames(self): #method to get host name of device over telnet
		self.hostnames = []
		for x in range(0,len(self.ports)):
			session = telnetlib.Telnet(self.host , self.ports[x-1])
			print('Session Open')
			session.write("\r\n".encode('ascii'))
			session.write("end \r\n".encode('ascii'))
			session.write("show run \r\n".encode('ascii'))
			session.write("\r\n".encode('ascii'))
			counter = 1
			while (counter < 2):
				line = session.read_until('\n')
				if 'hostname' in line:
					counter += 1
					hostname = line[9:]
					print('Hostname is ' + hostname)
					self.hostnames.append(hostname)
		return self.hostnames

	def print_hostnames(self):
		for x in self.hostnames:
			print(self.hostnames[x])

	def get_ports(self):
		for x in range(0, len(self.ports)):
			print(self.ports[x])

	#Create Dictionary for router info
	def create_dictionary(self):
		for x in range(0, len(self.ports)):
			AS_NUM = 7777
			id_num = 0
			router = str(self.hostnames[x])
			print(router) 
			router = {"host_name": self.hostnames[x],"port": self.ports[x],"as_num": AS_NUM,"id": id_num}
			self.routers_list.append(router)
			print('%s dictionary created' % self.routers_list[x])
			id_num += 1
		return self.routers_list

	#Method to open a console session to every router listening on TCP port 2100-2200
	def open_terminals(self):
		for x in range(0,len(self.routers_list)):
			router = self.routers_list[x]
			print(router)
			print('Connecting to %s on port %s' % (router['host_name'], router['port']))
			subprocess.Popen(["xterm", "-e", "telnet localhost %s" % router['port']])

	#Method to configure SSH
	def configure_ssh(self):
		for x in range(0,len(self.routers_list)):
			router = self.routers_list[x]
			ans = raw_input('Do you want to configure SSH on %s? (y/n)' % router['host_name'])
			if ans != 'y': continue
			session = telnetlib.Telnet(self.host, router['port'])
			print('Session to %s connected' % (router['host_name']))
			session.write("\r\n".encode('ascii'))
			session.write("en \r\n".encode('ascii'))
			session.write("conf term \r\n".encode('ascii'))
			session.write("ip domain-name %s \r\n".encode('ascii') % (router['host_name']))
			session.write("crypto key generate rsa \r\n".encode('ascii'))
			while (True):
				line = session.read_until('\n')
				print(str(line))
				if 'You already have RSA keys defined' in line:
					#RSA Keys have already been generated.
					regenerate = raw_input('RSA Keys have already been generated. Do you want to replace them(y/n)?')
					print(str(regenerate))
					if regenerate == 'n':
						session.write('no \r')
						print('Skipping the rest of the SSH Configuration for %s' % router['host_name'])
						break
					else:
						session.write('yes \r\n')
						session.write("1024 \r\n")
						print('Generating 1024 bit RSA key please wait...')
						time.sleep(5)
						session.write('line vty 0 4 \n')
						session.write('login local \r\n')
						session.write('transport input ssh \r\n')
						session.write(' \r\n')
						print('SSH on Device %s configured!' % (router['host_name']))
						break


	def configure_interfaces(self):
		for x in range(0, len(self.routers_list)):
			router = self.routers_list[x]
			ans = raw_input("Do you want to configure interfaces on %s? (y/n)" % router)
			if ans != 'y': continue
			print('running interfaces for loop')
			interfaces = ['fa 0/0', 'fa 0/1']
			router = self.routers_list[x]
			session = telnetlib.Telnet(self.host ,router['port'])
			session.write("\r\n")
			session.write("conf term \r\n")
			for y in range(0, len(interfaces)):
				print(router['id'])
				session.write("int + %s" % interfaces[y])
				session.write("ip address ")
				print('IP address IP_ADRESS has been written to %s on host %s' % (interfaces[y], router['host_name']))

	#Method to configure BGP
	def configure_bgp(network, routers_list = []):
		for x in range(0, len(routers_list)):
			router = routers_list[x]
			session = telnetlib.Telnet(network,router['port'])
			session.write("\r\n")
			session.write("conf term \r\n")
			session.write("router bgp %s \r\n" % router['as_num'])
			


#Run script
def main():
	network = host('127.0.0.1')
	print('Scanning routers for open TCP ports')
	network.portscan()
	network.get_ports()
	print('Getting hostnames')
	network.get_hostnames()
	print('Creating dictionary')
	network.create_dictionary()
	print('Dictionary Created')
	network.open_terminals()
	print('Console to virtual routers opened')
	network.configure_ssh()
	network.configure_interfaces()
	network.configure_bgp()

	 

if __name__ == '__main__':
  main()
