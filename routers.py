import socket
import telnetlib
import mysql.connector

global add_router
add_router = ("INSERT INTO router "
              "(host , port) "
              "VALUES (%s, %s)")    

# create router object
class router:
    global nhost
    nohost = 0
    
    def __init__(self, hostname, port):
        self.hostname = hostname
        self.port = port

    def gethostname(self):
        return self.hostname
    
    def getport(self):
        return self.port
    
# connect to database
class dbconnect:


    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
            
        
    def write(self, hostname, port):
        try:
            conn = mysql.connector.connect(host=self.host, database=self.database, user=self.user, password=self.password)
            # if conn.is_connected():
            print('Connected to database')
            cursor = conn.cursor()
            # print('cursor created')
            # print(hostname)
            router_data = (hostname, port)
            # print(router_data[0], router_data[1])
            cursor.execute(add_router, router_data)
            conn.commit()
            print('Writing to database')
            cursor.close()
            conn.close()
        except:
            print('Error connecting to database')
            

            
# get hostname over telnet        
class gethost:
    
    def __init__(self, host, port):
        self.host = host
        self.port = port
        
    def connect(self):

        session = telnetlib.Telnet(self.host, self.port)    
        session.write("\r\n")
        print('Session created')
        while(True):
            line = session.read_until('\n')
            if '#' in line:
                line = line[:-1]
                print(line)
                #new = line.strip()
                v = router(line, self.port)
                db = dbconnect('127.0.0.1', 'routers', 'root', 'password')
                host = v.gethostname()
                host.rstrip().format()
                port = v.getport()
                db.write(host,port)
                break
             
class portscan:
    
    def __init__(self, host):
        self.host = host
        
    def scan(self):
        counter = 0
        print('Running PortScan')
        while (counter < 100):
            for port in range(5000, 5100):
                counter += 1
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((self.host, port))
                if result == 0:
                    print('Getting hostname')
                    connect = gethost(self.host, port)
                    print('Objected Created')
                    connect.connect()
                    print('Session open')
                sock.close()  
                    
                    
                    
def main():
    localhost = '127.0.0.1'
    print('Creating Scan Object')
    scan = portscan(localhost)
    print('Running scan')
    scan.scan()
    print('Completed!!')
    
if __name__ == '__main__':
    main()
                    
                    
