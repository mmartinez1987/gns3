import socket
import subprocess

def portscan():
	ports = []
	localhost='127.0.0.1'
	counter = 0
	while (counter < 100):
		for port in range(2000,3000):
			counter += 1
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			result = sock.connect_ex((localhost,port))
			if result == 0:
				print('Host found adding port %s to ports array' % port)
				ports.append(port)
			sock.close()
	return ports

def open_terminals(ports = []):
	for x in range(0,len(ports)):
		print('Opening terminal to router on port %s' % ports[x])
		subprocess.Popen(["xterm", "-e", "telnet localhost %s" % ports[x]])

def main():
	ports = portscan()
	open_terminals(ports)

if __name__ == '__main__':
	main()
