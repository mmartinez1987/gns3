from open_terminals import portscan
import telnetlib

global localhost
localhost = '127.0.0.1'

#get hostname of device by creating telenet session, running show config and then slicing the hostname and appending to hostnames array. Return hostnames array
def get_hostnames(ports = []):
	hostnames = []
	for x in range(0, len(ports)):
		session = telnetlib.Telnet(localhost, ports[x])
		print("Session Open")
		session.write("no")
		session.write("\r\n")
		session.write("en \r\n".encode('ascii'))
		session.write("\r\n".encode('ascii'))
		session.write("end \r\n".encode('ascii'))
		session.write("show run \r\n".encode('ascii'))
		session.write("\r\n".encode('ascii'))
		counter = 1 
		while (counter < 2):
			line = session.read_until('\n')
			if 'hostname' in line:
				print(line)
				counter += 1
				hostname = line[9:]
				print('Found Hostname %s' % hostname)
				hostnames.append(hostname)
	return hostnames

#iterate over hostnames array and print values
def print_hostnames(hostnames):
	print(len(hostnames))
	for x in range(0,len(hostnames)):
		print("Hostname is %s" % hostnames[x])

def main():
	ports = portscan()
	hostnames = get_hostnames(ports)
	#print_hostnames(hostnames)



if __name__ == '__main__':
	main()
