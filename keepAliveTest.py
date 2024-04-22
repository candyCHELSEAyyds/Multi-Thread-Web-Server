#==========================================================================
# COMP2322 Computer Networking                                              
# Project: Multi-thread Web Server                                          
#                                                                           
# 2024-04-08                                                                
#                                                                           
# This program is used to test Connection header in request                 
#   Connection: Keep-Alive, and Connection: close will be tested            
#==========================================================================

import socket 
 
SERVER_HOST = '127.0.0.1' 
SERVER_PORT = 8080 
 
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client_socket.connect((SERVER_HOST, SERVER_PORT)) 
print("Client connected to server at %s:%d" % (SERVER_HOST, SERVER_PORT))
request = "HEAD /helloworld.html HTTP:/1.1\r\nConnection: Keep-Alive\r\n"
while True:
    try:
        client_socket.send(request.encode()) 
        print ('Client sent:\n'+request)
        response = client_socket.recv(1024) 
        print ('Server response:') 
        print (response.decode()) 
        print("1: Connection: Keep-Alive; 2: Connection: Close; 0: Quit")
        cmd = input("Please Enter command [0,1,2] to show your choice:")
        if cmd == '0':
            print('Thank you for using.')
            break
        elif cmd == '1':
            request = "HEAD /helloworld.html HTTP:/1.1\r\nConnection: Keep-Alive\r\n"
        elif cmd == '2':
            request = "HEAD /helloworld.html HTTP:/1.1\r\nConnection: Close\r\n"
        else:
            print("Invalid Input. Please input 0,1 or 2.")
            break
    except Exception as e:
        print("Error: %s" % e)
        break

client_socket.close()
print("Client closed")