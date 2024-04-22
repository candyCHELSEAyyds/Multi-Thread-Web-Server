import socket
from threading import Thread
import os
import datetime
 
class WebServer(object):
 
    # Initialize web server settings
    def __init__(self):
        
        # Create a socket
        self.static = "html_docs"

        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
        # # Set address reuse, SOL_SOCKET refers to the current socket, SO_REUSEADDR sets address reuse
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
 
        # Bind port
        self.tcp_server_socket.bind(("", 8080))
 
        # Set listening, switch the socket from active to passive mode
        self.tcp_server_socket.listen(128)
 
    def writeToLogSafely(self, inIP, inTime, inFileName, inResponseType):
        # Write access and error logs to a file in a thread-safe manner
        with open('log.txt', 'a') as file:
            file.write('[IP]:'+str(inIP)+' [Time]:'+str(inTime)+' [File]:'+inFileName+' [Response]:'+str(inResponseType)+'\n')
        
    def getFileType(self, path):
        # Determine the content type of the file based on its extension
        _, ext = os.path.splitext(path)
        if ext in ['.html', '.htm']:
            return 'text/html'
        elif ext == '.png':
            return 'image/png'
        elif ext == '.jpg' or ext == '.jpeg':
            return 'image/jpeg'
        elif ext == '.mp3':
            return 'audio/mpeg'
        elif ext == '.mp4':
            return 'video/mp4'
        elif ext == '.txt':
            return 'text/plain'
        else:
            return 'application/octet-stream'  # Default for binary data

    def getIfModifiedSince(self, headers):
        # Extract the 'If-Modified-Since' header from request headers
        for h in headers:
            if 'if-modified-since' in h:
                header = h
        return header[19:48]

    def start(self):
        """ Start the Web Server """
        print('#'*89)
        print('#','\t\t\tWelcome to the Multi-thread Web Server!\t\t\t\t#')
        print('# > press <Control+C> to shutdown\t#' )
        print('#please open the browser and visit http://127.0.0.1:8080/index.html')
        print('# > The log file is log.txt\t\t\t\t\t\t\t\t#')
        print('# > Received requests and corresponding responses will be displayed below:\t\t#')
        while True:
            
            new_client_socket, ip_port = self.tcp_server_socket.accept() # Accept new connection
            print("New Client %s connected!" % str(ip_port))
                
            t1 = Thread(target=self.request_handler, args=(new_client_socket, ip_port))# Handle each client in a new thread
            t1.start()
 
    def request_handler(self, new_client_socket, ip_port):
        """receive requests and make response"""
        # Set a default timestamp indicating no modification since the Unix epoch start
        modified_since = datetime.datetime.strptime("1970-01-01 00:00:00", '%Y-%m-%d %H:%M:%S')
        # Log the current time for this request
        nowTime = datetime.datetime.now()
        
        request_data = new_client_socket.recv(1024)  # # Receive data from the client
        # print(request_data)
        # # If no data is received, log that the client has closed the connection
        if not request_data:
            print("%s client has closed the connection" % str(ip_port))
            new_client_socket.close()
        else:
            # 状态码
            code = 200

            # Start constructing the HTTP response
            response_line = "HTTP/1.1 200 OK\r\n"
            response_header = "Server:Python20WS/2.1\r\n"
            response_blank = "\r\n"

            # Decode the request data to string
            request_text = request_data.decode()

            # Find the location of the first carriage return and line feed to isolate the request line
            loc = request_text.find("\r\n") 
            # Extract the request line from the full request text
            request_line = request_text[:loc]
            # Split the request line into components
            request_line_list = request_line.split(" ")
 
            # Get the requested file path from the request line
            file_path = request_line_list[1]

            print("%s is requesting: %s" % (str(ip_port), file_path))

       
            # Determine the HTTP method used (GET, POST, etc.)
            requestCommand = request_line_list[0]

            # Check if the request header includes 'If-Modified-Since'
            if 'if-modified-since' in request_text:
                # Extract the time string from the headers
                timeStr = self.getIfModifiedSince(request_text.split("\r\n"))
                # Parse the date-time string to a datetime object
                modified_since = datetime.datetime.strptime(timeStr, '%a, %d %b %Y %H:%M:%S %Z')

            # Handle unsupported HTTP methods by responding with a 400 Bad Request
            if (requestCommand == 'POST' or requestCommand == 'DELETE' or requestCommand == 'PUT'):
                code = 400
                try:
                # Attempt to open a custom 400 error page if there is a 400 bad request
                    with open(self.static + '/400.html', 'r', encoding='utf-8') as file:
                    
                        response_body = file.read()
                except FileNotFoundError:
                # Fallback error message if the custom error page is not found
                    response_body = "<html><head><title>404 Not Found</title></head><body><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p></body></html>"

                response_line = 'HTTP/1.1 400 Bad Request\r\n'
                response_line+='Content-Length:' + str(len(response_body)) + '\r\n'
                response_line+='Content-Type: text/plain\r\n\r\n'
                response_body = response_body.encode()
                
            else:
                

                try:
                    # Check if the requested file path should be ignored
                    if "nohost-sw.js" not in file_path:
                        last_modified = datetime.datetime.fromtimestamp(os.path.getmtime(self.static + file_path))
                    # if requestCommand == 'HEAD'
                    print(self.static + file_path)

                    # Open and read the content of the requested file
                    with open(self.static + file_path, "rb") as file:
                        response_body = file.read()

                    fileType = self.getFileType(file_path)

                    # Handle conditional GET (If-Modified-Since)
                    if requestCommand == 'HEAD' or modified_since >= last_modified:
                        code = 304
                        response_line = 'HTTP/1.1 304 Not Modified\r\n'
                        response_line += 'Last-Modified: ' + str(last_modified) + '\r\n'
                    else:
                        response_line += 'Last-Modified: ' + str(datetime.datetime.fromtimestamp(os.path.getmtime(self.static + file_path))) + '\r\n'
                    
                    # Complete the HTTP headers
                    response_line += 'Content-Length: ' + str(len(response_body)) + '\r\n'
                    response_line += 'Content-Type: ' + fileType + '\r\n'

                except Exception as e:
                    # Handle exceptions such as file not found
                    print("Error",e)
                    code = 404
                    # Try to open 404.html if file not found.
                    response_line = "HTTP/1.1 404 Not Found\r\n"
                    response_body = "Error! %s " % str(e)
                    response_body = response_body.encode()
 
            # # Combine parts of the HTTP response and send to the client
            response_data = (response_line + response_header + response_blank).encode() + response_body
 
            # send the HTTP response
            new_client_socket.send((response_data))
 
            # close the connection
            new_client_socket.close()
            if "nohost-sw.js" not in file_path:
                self.writeToLogSafely(ip_port, nowTime, file_path, code)
 
if __name__ == '__main__':
    WS = WebServer()
    WS.start()