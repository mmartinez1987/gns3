import socket
import sys
import os
import subprocess

class openterminals():

    global ports
    ports = []

    def portscan():
          localhost='127.0.0.1'
          counter = 0
          print('running createrouters()') 
        while (counter < 100):
            try:
              for port in range(5000,5100):
            counter += 1
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex((localhost, port))
            if result == 0:
              print('hostfound adding port')
                   ports.append(port)
        sock.close()

            except ValueError:
              print('Failure')

      
      nhosts = len(ports) #set nhosts to size of list to be used in for loop 
      index = len(ports)  #set index to size of list to be used to call port numbers in ports

    #run for loop and open new terminal for each router
      for x in range(0, nhosts):
            subprocess.Popen(["xterm", "-e", "telnet localhost %s" % ports[index - 1]])
          index -= 1


        portscan()
