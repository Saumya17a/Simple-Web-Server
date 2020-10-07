from socket import *
import sys
import _thread
import re
import datetime



def client_threads(conn,addr):
    try:
        while(True):
            date = datetime.datetime.now()
            date = date.strftime('%a %b %d %H:%M:%S PDT %Y')
            response = ''
            request = ""
            counter = 0
            data = []
            get = False
            flag = False
            while(counter < 3):
                message = conn.recv(1024)
                message = message.decode("utf-8")
                if((counter == 0) and (re.findall("GET /(.*) HTTP/1.0", message.strip()))):
                    get = True
                    data += [message]
                    counter += 1
                elif((counter == 0) and (message.strip() == "") ):
                    continue
                elif((counter == 0) and len(re.findall("GET /(.*) HTTP/1.0", message.strip())) == 0):
                    if("GET" in message.lower()):
                        request = message
                    else:
                        request = ""
                    response = "HTTP/1.0 400 Bad Request\r\n"
                    print(date+":"+addr[0]+":"+str(addr[1])+" "+request+"; "+response)
                    conn.send(response.encode())
                    conn.close
                    flag = True
                    break
                elif((get == True) and (message.strip() == "")):
                    break
                else:
                    data += [message]
                    counter += 1


            if(flag == True):
                break
        
            filename = re.findall("GET /(.*) HTTP/1.0", data[0].strip())[0]
            f = open(filename)
            outputdata = f.read()
            response = 'HTTP/1.0 200 OK\n'
            request = "GET "+"/"+filename+ " HTTP/1.0"
            print(date+":"+addr[0]+":"+str(addr[1])+" "+request+"; "+response)
            conn.send((response + 'Content-Type: text/html\n' + '\r\n').encode())
            for i in range(0, len(outputdata)):
                conn.send(outputdata[i].encode())
            conn.send("\r\n".encode())
            if(len(data) == 2):
                data[1] = data[1].strip().lower()
                if(data[1] != "connection:keep-alive"):
                    conn.close()
                    break
                elif(data[1] == "connection:keep-alive"):
                    data = []
                    counter = 0
            else:
                conn.close()
                break
        conn.close()
    except IOError:
        response = 'HTTP/1.0 404 Not Found\r\n'
        request = "GET "+"/"+filename+" HTTP/1.0"
        print(date+":"+addr[0]+":"+str(addr[1])+" "+request+"; "+response)
        conn.send(response.encode())
        conn.send(('<html>\n'+'<head><title> 404 Not Found</title></head>\n'+'<body>\n'+'<center><h1>404 Not Found</h1></center>\n'+'</body>\n'+'</html>\r\n').encode())
        conn.close()
host = str(sys.argv[1])
port = int(sys.argv[2])
sock = socket(AF_INET, SOCK_STREAM)
sock.bind((host, port))
sock.listen(10)
while True:
    print("Ready to serve...")
    conn, addr = sock.accept()
    _thread.start_new_thread(client_threads, (conn,addr))

sock.close()
sys.exit()