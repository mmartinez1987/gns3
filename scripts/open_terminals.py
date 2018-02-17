import socket
import telnetlib


def portscan(host): # Method to scan check for open ports on localhost
  ports = []
  for port in range(2100,2200): # TCP Port scan port range 2100-200	    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Instantiate sock as object as IPv4 socket
    result = sock.connect_ex((host, port)) #bind destination host IPv4 address to port
    if result == 0: #if connection is successful then
      print('Adding port' + str(port)) #lets me know that this if statement is being executed
      ports.append(port) #append variable port to ports array
      print(len(ports))
      if port == 2200:
        return ports
    sock.close()


def get_hostnames(host, ports = []):
  for x in range(ports[0] + 1):
    counter = 0
    session = telnetlib.Telnet(host, ports[x-1])
    print('Session Open')
    session.write("show run \r\n".encode('ascii'))
    while (True):
      line = session.read_until('\n')
      #print(line)
      if '#' in line:
        counter += 1
        routers = []
 	hostname = line[:-1]
        routers.append(hostname)
        if counter >= len(ports) + 1:
          print('Breaking out of gethostnames..')
          break


#def open_sessions():


def main():
  localhost = '127.0.0.1'
  ports = portscan(localhost) # create array of open ports by portscanning localhos
  print(ports[0])
 

if __name__ == '__main__':
  main()
