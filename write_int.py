import socket
import telnetlib

class writeint():

    def main(self):
        localhost = '127.0.0.1'
        counter = 0
        print('running createrouters()') 
        while (counter < 100):
            try:
                for port in range(5000, 5100):
                    counter += 1
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    result = sock.connect_ex((localhost, port))
                    if result == 0:
                        print('hostfound adding port')
                        ports.append(port)
                    sock.close()

            except ValueError:
              print('Failure')

      
        nhosts = len(ports)  # set nhosts to size of list to be used in for loop 
        index = len(ports)  # set index to size of list to be used to call port numbers in ports
        s = 60
    # run for loop to open telnet socket and write configuration
        for x in range(0, nhosts):
            session = telnetlib.Telnet(localhost, ports[index - 1])
            print('Telent Session open')
            for y in range(0, 20):
                session.write('en \r\n')
                session.write('conf term \r\n')
                session.write('int loopback % 10.10.%s.1\r\n' % s)
                s += 1        
                print('configuration saved!')
                index -= 1

if __name__ == '__main__':
    main()
