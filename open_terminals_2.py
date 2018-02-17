import subprocess
import socket
import telnetlib
import time

def portscan(network): # Method to scan check for open ports on localhost
	ports = []
	for port in range(2100,2200): # TCP Port scan port range 2100-200	    
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instantiate sock as object as IPv4 socket
		result = sock.connect_ex((network, port)) #bind destination host IPv4 address to port
		if result == 0: #if connection is successful then
			print('Adding port') #lets me know that this if statement is being executed
			ports.append(port) #append variable port to ports 
		sock.close()
	return ports
	

def get_hostnames(network, ports = []): #method to get host name of device over telnet
	hostnames = []
	for x in range(0,len(ports)):
		session = telnetlib.Telnet(network, ports[x-1])
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
				hostnames.append(hostname)
	return hostnames

#Create Dictionary for router info
def create_dictionary(hostnames, ports = []):
	routers_list = []
	for x in range(0, len(ports)):
		AS_NUM = 7777
		id_num = 0
		router = str(hostnames[x])
		print(router) 
		router = {"host_name": hostnames[x],"port": ports[x],"as_num": AS_NUM,"id": id_num}
		routers_list.append(router)
		print('%s dictionary created' % routers_list[x])
		id_num += 1
	return routers_list

#Method to open a console session to every router listening on TCP port 2100-2200
def open_terminals(routers_list = []):
	for x in range(0,len(routers_list)):
		router = routers_list[x]
		print(router)
                print('Connecting to %s on port %s' % (router['host_name'], router['port']))
		subprocess.Popen(["xterm", "-e", "telnet localhost %s" % router['port']])

#Method to configure SSH
def configure_ssh(network, routers_list = []):
	for x in range(0,len(routers_list)):
		router = routers_list[x]
		session = telnetlib.Telnet(network, router['port'])
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


#Method to configure snp
def configure_snmp(hostnames, ports = []):
	return	

#Method to configure interfaces
def configure_interfaces(network, routers_list = []):
	print(len(routers_list))
	for x in range(0, len(routers_list)):
		print('running interfaces for loop')
		interfaces = ['fa 0/0', 'fa 0/1']
		router = routers_list[x]
		session = telnetlib.Telnet(network ,router['port'])
		session.write("\r\n")
		session.write("conf term \r\n")
		for y in range(0, len(interfaces)):
			print router['id']
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
		


#Method to 'show ip bgp sum'
def check_bgp_status(hostnames, ports = []):
	return

#Method to 'show ip bgp neigh'
def check_bgp_neighbors(hostnames, ports = []):
	return

#Method to 'save running config'
def save_running_config(hostnames, ports = []):
	return


#Run script
def main():
  network = '127.0.0.1'
  ports = portscan(network) #create array of open ports on localhost TCP port 2100-2200
  print('Ports Created')
  hostnames = get_hostnames(network, ports) #create array of hostname at cooresponding port
  print('Hostnames created')
  routers_list = create_dictionary(hostnames, ports) #create array of dictionaries for each router
  print(len(routers_list))
  print('%s Dictionary Created' % str(routers_list))
  open_terminals(routers_list)
  #print('Console Sessions to routers open..')
  configure_ssh(network, routers_list)
  #print('SSH config created...')
  #print(len(routers_list))
  configure_interfaces(network, routers_list)
  #print('Interfaces configured..')
  #configure_bgp(network, routers_list)
  print('BGP peering configured..')
  
  

if __name__ == '__main__':
  main()
