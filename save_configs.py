from open_terminals import portscan
from gethostnames import get_hostnames
import telnetlib
global localhost
localhost = '127.0.0.1'

def save_running_config(ports):
	for x in range(0,len(ports)):
		session = telnetlib.Telnet(localhost, ports[x])
		session.write("\r\n")
		session.write("end")
		print("Saving configuration on %s" % hostnames[x])
		session.write("copy running-config startup-confg")
		session.write("\r\n")
		print("Configuration saved on device %s" % hostnames[x])

def main():
	ports = portscan()
	print('Ports created')
	hostnames = get_hostnames()
	print('hostnames created')
	save_running_config(ports)

if __name__ == '__main__':
	main()	
