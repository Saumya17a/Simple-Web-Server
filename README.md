# Simple-Web-Server
Uses the STREAM socket (i.e., supported by TCP) in Python to create a Simple Web Server (SWS) supporting both persistent and non-persistent HTTP connections

Only supports “GET /filename HTTP/1.0” command, and “Connection: keep-alive” and “Connection: close” request and response header when supporting persistent HTTP connection. 
The request header is terminated by an empty line. If unsupported commands received or in unrecognized format, SWS will respond “HTTP/1.0 400 Bad Request”. 
If the file indicated by filename is inaccessible, SWS will return “HTTP/1.0 404 Not Found”. For successful requests, SWS will respond “HTTP/1.0 200 OK”, 
followed by response header if any, an empty line indicating the end of the response header, and the content of the file.

Run on Terminal 1 “python3 sws.py ip_address port_number”, where ip_address and port_number indicate where SWS binds its socket for incoming requests.
On Terminal 2 (acts as a client), “telnet sws_ip_address sws_port_number” to connect to SWS, and type “GET /sws.py HTTP/1.0” followed by “Connection: keep-alive” and an empty line 
to request the file sws.py from SWS (in this case, SWS shall keep the connection alive after sending back sws.py following an empty line after 
“Connection: keep-alive”, and wait for the next request from the same client through the same TCP connection, until the connection times out, i.e., 
“Connection: close”). If the client does not include “Connection: keep-alive” or does include “Connection: close” in its request, 
SWS will close the connection after serving the request. For each served request, even if unsuccessfully, SWS will output a log line 
“time: client_ip:client_port request; response”, e.g., “Wed Sep 16 21:44:35 PDT 2020: 192.168.1.100:54321 GET /sws.py HTTP/1.0; HTTP/1.0 200 OK”.
Please note that SWS will keep waiting to serve more clients and can serve multiple concurrent clients, until interrupted by Ctrl-C.
